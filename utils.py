import math
import numpy as np
import cv2

def warp(dict, img, imgWidth, imgHeight, inverse):
    if inverse:
        pts2 = np.float32([[dict[326][0], dict[326][1]], [dict[683][0], dict[683][1]],[dict[779][0], dict[779][1]], [dict[856][0], dict[856][1]]])
        pts1 = np.float32([[0, 0],[imgWidth, 0],[imgWidth, imgHeight], [0, imgHeight]])
    else:
        pts1 = np.float32([[dict[326][0], dict[326][1]], [dict[683][0], dict[683][1]],[dict[779][0], dict[779][1]], [dict[856][0], dict[856][1]]])
        pts2 = np.float32([[0, 0],[imgWidth, 0],[imgWidth, imgHeight], [0, imgHeight]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img, M, (imgWidth, imgHeight))
    return dst

# 

def splitBoxes(img, questions, options, questionsOverlapMargin):
    """
        A method to verify if user marked an option by question\n
        options = option of question (A,B,C,D,E...)\n
        question = question of test (1 ~ 20)

    """
    total = 0
    
    rows = np.vsplit(img, questions)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, options)
        for box in cols:
            total += np.count_nonzero(box[questionsOverlapMargin:box.shape[0]-questionsOverlapMargin, questionsOverlapMargin:box.shape[1]-questionsOverlapMargin])
            boxes.append(box[questionsOverlapMargin:box.shape[0]-questionsOverlapMargin, questionsOverlapMargin:box.shape[1]-questionsOverlapMargin])

    return boxes, int(total/(questions*options))

def giveGrades(answers, rigthAnswers):
    grade = 0
    
    answersList = []
    for a in range(len(answers)):
        if sum(answers[a]) != 1 or (ord(rigthAnswers[a][1]) - 65) != np.argmax(answers[a]):
            answersList.append(0)
        else:
            answersList.append(1)
            grade += rigthAnswers[a][0]
            answers[a][np.argmax(answers[a])] = -1

    return answers, grade, answersList

def showAnswers(img, answers, questions, choices):
    optionH = int(img.shape[1]/questions)
    optionW = int(img.shape[0]/choices)

    for currentRow in range(questions):
        if sum(answers[currentRow]) == -1:
            answer = np.argmin(answers[currentRow])
            cX = int((answer*optionW) + optionW / 2)
            cY = int((currentRow * optionH) + optionH / 2)
            cv2.ellipse(img, (cX,cY), (50, 15), 0, 0, 360, (0, 255, 0), -1)
        elif (sum(answers[currentRow]) == 1):
            answer = np.argmax(answers[currentRow])
            cX = int((answer*optionW) + optionW / 2)
            cY = int((currentRow * optionH) + optionH / 2)
            cv2.ellipse(img, (cX,cY), (50, 15), 0, 0, 360, (0, 0, 255), -1)

    return img

#! ================== making debug image to view data ============================

def showDebug(images, width = 1080, height = 720, title= "debug"):
    background = np.zeros((height, width, 3), dtype=np.uint8)
    img_height = int(height / 2)
    img_width = int(width / 4)
    for i in range(len(images)):
        if len(images[i].shape) == 2:
            images[i] = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGR)
        images[i] = cv2.resize(images[i], (img_width, img_height))
        line = math.floor(i / 4)
        column = i % 4
        background[
            line * img_height : (line + 1) * img_height,
            column * img_width: img_width * (column + 1)
            ] = images[i]
        cv2.imshow(title, background)


def listAvailableCams(max_cameras = 10):
    cameras_disponiveis = []
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # No Windows, use CAP_DSHOW
        if cap is not None and cap.isOpened():
            cameras_disponiveis.append(index)
            cap.release()
    return cameras_disponiveis