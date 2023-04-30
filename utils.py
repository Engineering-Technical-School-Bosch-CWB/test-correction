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

def splitBoxes(img, questions, options):
    rows = np.vsplit(img, questions)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, options)
        for box in cols:
            boxes.append(box)

    return boxes

def giveGrades(answers, rigthAnswers):
    grade = 0

    for a in range(len(answers)):
        if sum(answers[a]) != 1 or (ord(rigthAnswers[a][1]) - 65) != np.argmax(answers[a]):
            pass
        else:
            grade += rigthAnswers[a][0]
            answers[a][np.argmax(answers[a])] = -1

    return answers, grade

def showAnswers(img, index, questions, choices, correctAnswers):
    secH = int(img.shape[1]/questions)
    secW = int(img.shape[0]/choices)

    for x in range(questions):
        if sum(index[x]) == -1:
            answer = np.argmin(index[x])
            cX = int((answer*secW) + secW / 2)
            cY = int((x * secH) + secH / 2)
            cv2.ellipse(img, (cX,cY), (50, 15), 0, 0, 360, (0, 255, 0), -1)
        elif (sum(index[x]) == 1):
            answer = np.argmax(index[x])
            cX = int((answer*secW) + secW / 2)
            cY = int((x * secH) + secH / 2)
            cv2.ellipse(img, (cX,cY), (50, 15), 0, 0, 360, (0, 0, 255), -1)
            cv2.circle(img, (int((ord(correctAnswers[x][1]) - 65) * secW + (secW / 2)), cY), 10, (0, 255, 0), -1)

    return img

def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver