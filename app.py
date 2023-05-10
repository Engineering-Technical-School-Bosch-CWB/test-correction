from flask import Flask, render_template, Response, request, jsonify, json
import numpy as np
import utils
import cv2

app = Flask(__name__)
answersList = []

candidate = ["Maria Aparecida Silva","João Pedro Santos","Ana Luiza Oliveira","Lucas dos Santos Souza","Carla Fernanda Pereira","Rodrigo Almeida Costa","Larissa Lima Santos","Guilherme Castro Alves","Juliana de Souza Ferreira","Rafaela Nunes Cardoso","Pedro Henrique Rodrigues","Camila Vieira Gomes","Matheus Oliveira Martins","Isabela Silva Sousa","Thiago Ferreira Carvalho","Gabriela Costa Ribeiro","Fernando Alves Pereira","Bianca Santos Silva","Arthur Oliveira Lima","Amanda Castro Santos","Leonardo Carvalho Rodrigues","Giovanna Fernandes Souza","Ricardo Cardoso Nunes","Lívia Lima Almeida","Vinicius Pereira Gonçalves","Maria Clara Rodrigues Castro","Tiago Ferreira Almeida","Mariana Oliveira Costa","Diego Souza Ramos","Helena Martins Gomes","Luiz Henrique Silva Santos","Lara Nunes Oliveira","Renato Almeida Castro","Natália Costa Ferreira","Enzo Cardoso Sousa","Luana Ribeiro Carvalho","Daniel Pereira Alves","Gabrielle Santos Lima","Alexandre Rodrigues Castro","Leticia Ferreira Lima","Luciano Oliveira Santos","Sofia Sousa Almeida","Thales Gomes Pereira","Lorena Martins Silva","Júlio César Nunes Costa","Ana Beatriz Alves Rodrigues","Victor Hugo Souza Santos","Mariana Ferreira Oliveira","Lucas Cardoso Lima","Raquel Sousa Castro","Henrique Ribeiro Costa","Gabriela Almeida Carvalho","Felipe Santos Pereira","Carolina Lima Gomes","Pedro Castro Silva","Julia Rodrigues Oliveira","André Luiz Ferreira Santos","Isadora Costa Almeida","Matheus Nunes Sousa","Larissa Oliveira Ribeiro","Rafael Silva Martins","Beatriz Castro Lima","Rodrigo Souza Santos","Alice Carvalho Pereira","Leonardo Gomes Alves","Maria Eduarda Nunes Castro","Thiago Rodrigues Lima","Gabriela Costa Silva","Lucas Almeida Santos","Bianca Pereira Oliveira","Guilherme Lima Ferreira","Amanda Ribeiro Gomes","Luiz Felipe Martins Sousa","Vitória Santos Almeida","Rafaela Carvalho Costa","Gustavo Silva Rodrigues","Camila Castro Lima","Pedro Henrique Oliveira Santos","Mariana Ferreira Alves","Carlos Eduardo Lima Souza","Isabela Santos Costa","Ricardo Nunes Pereira","Lívia Almeida Rodrigues","Vinicius Castro Gomes"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/candidates')
def candidates():
    return candidate

@app.route('/questionsValues')
def questionsValues():
    _, values = utils.readExcelGabarito()
    return values

@app.route('/getGabarito')
def getGabarito():
    gabarito, _ = utils.readExcelGabarito()
    return gabarito

@app.route('/update_variable')
def update_variable():
    global answersList
    nova_variavel = ''.join(str(c) for c in answersList)
    return jsonify(nova_variavel)

def gen():
    # Test settings
    questions = 20
    options = 5
    considerQuestion = 0

    correctAnswers, _= utils.readExcelGabarito()

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

    # Upper left , upper right, bottom right, bottom left
    dictPoints = [326, 683, 779, 856]
    dict_aruco = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL )
    myArucoDict = { dictPoints[0]: (0, 0), dictPoints[1]: (0, 0), dictPoints[2]: (0, 0), dictPoints[3]: (0, 0) }
    parameters = cv2.aruco.DetectorParameters_create()

    while True:
        
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, __ = cv2.aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        imgWarped = frame.copy()
        imgTresh = frame.copy()
        imgFinal = frame.copy()

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
            
        imgCircles = cv2.resize(imgCircles, (900, 900))
        imgQuestions = imgCircles.copy()

        try:

            tempNewX = 757
            tempX = 501
            tempNewY = 887
            tempY = 271

            clone = cv2.resize(imgWarped, (900, 900))
            clone = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)
            imgCircles = cv2.rectangle(imgCircles, (tempNewX, tempNewY), (tempX, tempY), (0, 255, 0), 3)
            imgQuestions = clone[tempY:tempNewY, tempX:tempNewX]
            questionsW = imgQuestions.shape[1]
            questionsY = imgQuestions.shape[0]
            _, imgTresh = cv2.threshold(imgQuestions, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            imgQuestions = cv2.resize(imgQuestions, (imgWidth, imgHeight))    
            
            imgTresh = cv2.resize(imgTresh, (900, 900))
            boxes = utils.splitBoxes(imgTresh, questions, options)

            considerQuestion += cv2.countNonZero(imgTresh)
            considerQuestion = int(considerQuestion/len(boxes))

            countColumn = 0
            countRow = 0

            for image in boxes:
                marked = 0
                totalPixels = cv2.countNonZero(image)
                if totalPixels > considerQuestion: marked = 1

                questionValues[countRow][countColumn] = marked
                countColumn += 1
                if (countColumn == options): countRow += 1; countColumn = 0

            questionValues, ___, newAnswersList = utils.giveGrades(questionValues, correctAnswers)
            global answersList
            answersList = newAnswersList
            imgResult = np.zeros_like(clone)
            imgResult = cv2.cvtColor(imgResult, cv2.COLOR_GRAY2BGR)
            imgResult = utils.showAnswers(imgResult, questionValues, questions, options, correctAnswers)
            imgResultScaled = cv2.resize(imgResult, (questionsW, questionsY))
            tempImage = cv2.resize(imgWarped, (900, 900))
            imgResultFinal = np.zeros_like(tempImage)
            imgResultFinal[tempY:tempNewY, tempX:tempNewX] = imgResultScaled
            imgResultFinal = cv2.resize(imgResultFinal, (imgFinal.shape[1], imgFinal.shape[0]))
            imgFinal = imgWarped.copy()
            imgFinal = cv2.addWeighted(imgFinal, 1, imgResultFinal, 1, 0)
        
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
