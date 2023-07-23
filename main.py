
import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
detector = HandDetector(detectionCon=0.8)

class MCQ():
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self,cursor,bboxs):
        for x,bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if(x1<cursor[0]<x2 and y1<cursor[1]<y2):
                self.userAns = x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)

pathcsv = 'mcq.csv'
with open(pathcsv,newline = '\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]
print(dataAll)

mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))


qNo = 0
qTotal = len(dataAll)
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    hands,img = detector.findHands(img,flipType=False)

    if qNo<qTotal:
        mcq = mcqList[qNo]
        img, bbox = cvzone.putTextRect(img, mcq.question, [20, 40], 1, 2, offset=10, border=2)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [40, 100], 1, 1, offset=10, border=2)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [200, 100], 1, 1, offset=10, border=2)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [40, 200], 1, 1, offset=10, border=2)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [200, 200], 1, 1, offset=10, border=2)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, info = detector.findDistance(lmList[8][:2], lmList[12][:2])
            if length < 60:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    qNo += 1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score/qTotal)*100)
        img, _ = cvzone.putTextRect(img, 'Quiz Completed', [190, 200], 2, 2, offset=10, border=2)
        img, _ = cvzone.putTextRect(img, f'Score : {score}%', [220, 300], 2, 2, offset=10, border=2)

    barValue = 40 + (510//qTotal)*qNo
    cv2.rectangle(img, (40, 400), (550, 400), (255, 0, 255), 10)
    cv2.rectangle(img, (40, 400), (barValue, 400), (0, 255, 0), 8)
    img, _ = cvzone.putTextRect(img, f'{round((qNo/qTotal)*100)}%', [barValue, 440], 1, 1, offset=10, border=2)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
