import cv2
import utils
import excel
import os
import sys
import webview
import numpy as np
from flask import Flask, render_template, Response, request, jsonify, json

args = sys.argv

file = "ProcessoSeletivo.xlsx"

base_dir = ''
app = Flask(__name__,
            static_folder=os.path.join(base_dir, 'static'),
            template_folder=os.path.join(base_dir, 'templates')
            )
window = webview.create_window("Scanner Ets", app)

if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

_availableCams = utils.listAvailableCams()
print(_availableCams)
# _selectedCam = _availableCams[len(_availableCams) - 1]
_selectedCam = 1

# Camera settings
vid_capture = cv2.VideoCapture(_selectedCam, cv2.CAP_DSHOW)
vid_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vid_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
vid_capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
vid_capture.set(cv2.CAP_PROP_FOURCC,
                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# Test settings & variables
answersCorners = [(590, 520), (915, 1885)]
questions = 20
options = 5
questionsOverlapMargin = 5
considerQuestion = 0
correctAnswers, _ = excel.readExcelGabarito(file)
answersList = []
answersListWithOptions = []
candidate = excel.readExcelNome(file)

# Aruco settings
arUcoPoints = [326, 683, 779, 856]
arUcosCornerPositions = {arUcoPoints[0]: (0, 0), arUcoPoints[1]: (
    0, 0), arUcoPoints[2]: (0, 0), arUcoPoints[3]: (0, 0)}
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
parameters = cv2.aruco.DetectorParameters_create()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/candidates')
def candidates():
    return candidate

# @app.route("/getCams")
# def getCams():
#     return (_availableCams, _selectedCam)

@app.route('/register', methods=['POST'])
def register():
    candidate = request.form.get('candidate')
    race = request.form.get('race')
    grade = request.form.get('grade')
    answers = request.form.get('answers')
    return excel.registerCandidate(candidate, race, answers, grade, answersListWithOptions, file)


@app.route('/candidate', methods=['GET'])
def getCandidate():
    candidate = request.args.get('candidate')
    exists, _ = excel.findCandidate(candidate, file)

    if exists:
        return 'Candidate exists', 200

    return 'Candidate not found', 403


@app.route('/questionsValues')
def questionsValues():
    _, values = excel.readExcelGabarito(file)
    return values


@app.route('/getGabarito')
def getGabarito():
    gabarito, _ = excel.readExcelGabarito(file)
    return gabarito


@app.route('/update_variable')
def update_variable():
    global answersList
    nova_variavel = ''.join(str(c) for c in answersList)
    return jsonify(nova_variavel)


def gen():

    while (vid_capture.isOpened()):

        ret, frame = vid_capture.read()

        if ret == True:
            questionValues = np.zeros((questions, options))

            imgWidth = frame.shape[0]
            imgHeight = frame.shape[1]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            (corners, ids, rejected) = cv2.aruco.detectMarkers(
                gray, aruco_dict, parameters=parameters)

            if len(corners) > 0:
                for i in range(0, len(ids)):
                    arUcosCornerPositions[ids[i][0]] = corners[i][0][0]
                    cv2.aruco.drawDetectedMarkers(gray, corners, ids)

            imgWarped = utils.warp(arUcosCornerPositions,
                                   frame, imgWidth, imgHeight, False)
            
            imgWarpedWithCoordinates = cv2.circle(imgWarped, 
                                                  (answersCorners[0][0], answersCorners[0][1]),
                                                  10, (0,255,0), -1)
            
            imgWarpedWithCoordinates = cv2.circle(imgWarped, 
                                                  (answersCorners[1][0], answersCorners[1][1]),
                                                  10, (0,0,255), -1)

            upLeftCirclesRecX = answersCorners[0][0]
            upLeftCirclesRecY = answersCorners[0][1]
            downRightCirclesRecX = answersCorners[1][0]
            downRightCirclesRecY = answersCorners[1][1]

            imgQuestions = imgWarped[upLeftCirclesRecY:downRightCirclesRecY,
                                     upLeftCirclesRecX:downRightCirclesRecX]
            imgQuestions = cv2.cvtColor(imgQuestions, cv2.COLOR_BGR2GRAY)
            imgQuestionsW = imgQuestions.shape[1]
            imgQuestionsH = imgQuestions.shape[0]
            
            #aplicando filtro gaussian
            blurred = cv2.GaussianBlur(imgQuestions, (9,9), 0)
            normalizated = cv2.normalize(blurred, None, 0, 255, cv2.NORM_MINMAX)
            _, imgTresh = cv2.threshold(normalizated, 215, 255, cv2.THRESH_BINARY)
            kernel = np.ones((30,30), np.uint8)
            imgTresh = cv2.morphologyEx(imgTresh, cv2.MORPH_CLOSE, kernel)

            imgTresh = cv2.resize(imgTresh, (640, 480))
            boxes, considerQuestion = utils.splitBoxes(
                imgTresh, questions, options, questionsOverlapMargin)

            countColumn = 0
            countRow = 0

            for image in boxes:
                marked = 0
                totalPixels = cv2.countNonZero(image)

                if totalPixels < considerQuestion:
                    marked = 1

                questionValues[countRow][countColumn] = marked
                countColumn += 1

                if (countColumn == options):
                    countRow += 1
                    countColumn = 0

            questionValues2, grade, answers = utils.giveGrades(
                questionValues, correctAnswers)
            global answersList, answersListWithOptions
            answersListWithOptions = questionValues2
            answersList = answers
            blankImage = cv2.resize(cv2.cvtColor(np.zeros_like(
                imgQuestions), cv2.COLOR_GRAY2BGR), (640, 640))
            blankImageWithFeedback = utils.showAnswers(
                blankImage, questionValues2, questions, options)
            blankImageWithFeedback = cv2.resize(
                blankImageWithFeedback, (imgQuestionsW, imgQuestionsH))

            resizedImageWithFeedback = np.zeros_like(imgWarped)
            resizedImageWithFeedback[upLeftCirclesRecY:downRightCirclesRecY,
                                     upLeftCirclesRecX:downRightCirclesRecX] = blankImageWithFeedback
            imgFinal = cv2.addWeighted(
                imgWarped, 1, resizedImageWithFeedback, 1, 0)

            #print(np.sum(imgFinal == 0))
            if (np.sum(imgFinal == 0) > 5000 or np.max(imgFinal) - np.min(imgFinal) < 200):
                print(f"{np.max(imgFinal)} - {np.min(imgFinal)}")
                imgFinal = frame

            imgFinal = cv2.resize(imgFinal, (340, 620))

            if '--debug' in args:
                utils.showDebug(
                    [
                        frame,
                        imgWarpedWithCoordinates,
                        # imgQuestions,
                        imgTresh,
                        blurred,
                        resizedImageWithFeedback,
                        normalizated,
                        blankImageWithFeedback,
                        imgFinal
                    ])

            cv2.imwrite('video.jpg', imgFinal)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('video.jpg', 'rb').read() + b'\r\n')

        key = cv2.waitKey(20)

        if key == 27:
            vid_capture.release()
            break


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    webview.start()
    print('closed')
