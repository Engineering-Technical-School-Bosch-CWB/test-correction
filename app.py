from flask import Flask, render_template, Response, request, jsonify
import numpy as np
import utils
import cv2

app = Flask(__name__)
answersList = []
searching = True

@app.route('/')
def index():
    return render_template('index.html', answers=answersList)

@app.route('/update_variable')
def update_variable():
    global answersList
    nova_variavel = ''.join(str(c) for c in answersList)
    return jsonify(nova_variavel)

def gen():
    # Test settings
    questions = 19
    options = 5
    considerQuestion = 0
    questionsToIgnore = 3
    correctAnswers = ((6, 'C'), # 2 
                    (6, 'E'), # 3
                    (4, 'A'), # 4
                    (4, 'B'), # 5
                    (0, 'X'), # 6
                    (6, 'D'), # 7
                    (0, 'X'), # 8
                    (4, 'E'), # 9
                    (4, 'C'), # 10
                    (4, 'A'), # 11
                    (4, 'B'), # 12
                    (4, 'D'), # 13
                    (6, 'C'), # 14
                    (0, 'X'), # 15
                    (4, 'A'), # 16
                    (8, 'E'), # 17
                    (4, 'D'), # 18
                    (8, 'B'), # 19
                    (8, 'B')) # 20


    # Camera settings
    HIGH_VALUE = 10000
    WIDTH = HIGH_VALUE
    HEIGHT = HIGH_VALUE
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    _, frame = cap.read()
    imgWidth = frame.shape[1]
    imgHeight = frame.shape[0]

    # Hough settings
    minDist = 10
    param1 = 20
    param2 = 28
    minRadius = 8
    maxRadius = 17

    # Upper left , upper right, bottom right, bottom left
    dictPoints = [326, 683, 779, 856]
    dict_aruco = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL )
    myArucoDict = { dictPoints[0]: (0, 0), dictPoints[1]: (0, 0), dictPoints[2]: (0, 0), dictPoints[3]: (0, 0) }
    parameters = cv2.aruco.DetectorParameters_create()

    while True:
        global searching
        if searching == "false":
            try:
                fixedFrame = cv2.imread('currentImage.jpg')
                fixedFrame = cv2.resize(fixedFrame, (340, 620))
                cv2.imwrite('video.jpg', fixedFrame)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + open('video.jpg', 'rb').read() + b'\r\n')
            except:
                searching = "true"
        else:
            _, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

            imgWarped = frame.copy()
            imgTresh = frame.copy()
            imgFinal = frame.copy()

            pos = []
            posY = []
            posX = []
            grade = 0
            questionsW = 0
            questionsY = 0
            questionValues = np.zeros((questions, options))

            try:
                for i in range(len(ids)):
                    myArucoDict[ids[i][0]] = corners[i][0][0]
                imgWarped = utils.warp(myArucoDict, imgWarped, imgWidth, imgHeight, False)
                imgCircles = cv2.cvtColor(imgWarped, cv2.COLOR_BGR2GRAY)
            except:
                imgCircles = cv2.cvtColor(imgWarped, cv2.COLOR_BGR2GRAY)
                
            imgCircles = cv2.resize(imgCircles, (900, 893))
            imgQuestions = imgCircles.copy()
            imgCircles = cv2.GaussianBlur(imgCircles, (5,5) , 1)
            circles = cv2.HoughCircles(imgCircles, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
            imgCircles = cv2.cvtColor(imgCircles, cv2.COLOR_GRAY2BGR)


            if circles is not None:
                try:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0,:]:
                        cv2.circle(imgCircles, (i[0], i[1]), i[2], (0, 255, 0), 2)
                        pos.append(i[0] + i[1])
                        posY.append(i[1])
                        posX.append(i[0])
                        
                    posMax = max(pos)
                    posMin = min(pos)
                    posMaxIndex = pos.index(posMax)
                    posMinIndex = pos.index(posMin)
                    circleMaxSize = circles[0][posMaxIndex][2] 
                    circleMinSize = circles[0][posMinIndex][2] 
                    
                    tempNewX = int(max(posX) + circleMaxSize * 1.5)
                    tempX = int(min(posX) - circleMinSize * 1.5)
                    tempNewY = int(max(posY) + circleMaxSize)
                    tempY = int(min(posY) - circleMinSize)

                    clone = cv2.resize(imgWarped, (900, 893))
                    clone = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)
                    imgCircles = cv2.rectangle(imgCircles, (tempNewX, tempNewY), (tempX, tempY), (0, 255, 0), 3)
                    imgQuestions = clone[tempY:tempNewY, tempX:tempNewX]
                    questionsW = imgQuestions.shape[1]
                    questionsY = imgQuestions.shape[0]
                    _, imgTresh = cv2.threshold(imgQuestions, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
                    imgQuestions = cv2.resize(imgQuestions, (imgWidth, imgHeight))    
                    
                    imgTresh = cv2.resize(imgTresh, (900, 893))
                    boxes = utils.splitBoxes(imgTresh, questions, options)

                    considerQuestion += cv2.countNonZero(imgTresh)
                    considerQuestion = int(considerQuestion/(len(boxes) - (questionsToIgnore * options)))

                    countColumn = 0
                    countRow = 0

                    for image in boxes:
                        marked = 0
                        totalPixels = cv2.countNonZero(image)
                        if totalPixels > considerQuestion: marked = 1

                        questionValues[countRow][countColumn] = marked
                        countColumn += 1
                        if (countColumn == options): countRow += 1; countColumn = 0

                    questionValues, grade, newAnswersList = utils.giveGrades(questionValues, correctAnswers)
                    global answersList
                    answersList = newAnswersList
                    imgResult = np.zeros_like(clone)
                    imgResult = cv2.cvtColor(imgResult, cv2.COLOR_GRAY2BGR)
                    imgResult = utils.showAnswers(imgResult, questionValues, questions, options, correctAnswers)
                    imgResultScaled = cv2.resize(imgResult, (questionsW, questionsY))
                    tempImage = cv2.resize(imgWarped, (900, 893))
                    imgResultFinal = np.zeros_like(tempImage)
                    imgResultFinal[tempY:tempNewY, tempX:tempNewX] = imgResultScaled
                    imgResultFinal = cv2.resize(imgResultFinal, (imgFinal.shape[1], imgFinal.shape[0]))
                    imgFinal = imgWarped.copy()
                    imgFinal = cv2.addWeighted(imgFinal, 1, imgResultFinal, 1, 0)
                    # imgFinal = cv2.putText(imgFinal, str(grade), (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 255, 0), 20, cv2.LINE_AA)

                except:
                    pass
            
            try:
                frame = imgFinal
            except:
                pass

            frame = cv2.resize(frame, (340, 620))

            cv2.imwrite('video.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('video.jpg', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
    app.debug = True
