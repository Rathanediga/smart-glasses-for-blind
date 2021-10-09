import numpy as np
import cv2
import speech_recognition as sri
import os
from playsound import playsound
global it

def speech():
    print('ASK THE BOT FOR SEARCHING  \n')
    playsound('asking.mp3')
    try:
        with sri.Microphone() as source:
            global x
            r = sri.Recognizer()
            audio = r.listen(source)
            it = r.recognize_google(audio)
            print("You have asked to search " + it)
            return(it)
    except sri.UnknownValueError:
        print("No clue what you said, listening again... \n")
        speech()


#Loading YOLO algo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layerNames = net.getLayerNames()
outputLayer = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
cnt=0
while True: 
    check, frame = webcam.read()
#    print(check)
    if(cnt==0):
        it=speech()
        cnt=5
    print("searching for ",it)        
    image = cv2.resize((frame), None, fx=0.8, fy=0.8)
    width, height, channels = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0,), True, crop=False)     #RGB extraction
    net.setInput(blob)
    outputs = net.forward(outputLayer)
    boxes = []
    confidences = []
    classIDs = []
    flag = 0
    for out in outputs:
        for detect in out:
            score = detect[5:]
            classID = np.argmax(score)
            confidence = score[classID]

            if confidence > 0.5:
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                print(center_x, center_y, w, h, width, height)
                
                if w < width/3:
                    flag = 0
                elif w > width/2:
                    flag = 3
                else:
                    if center_x < width/2:
                        flag = 1
                    elif center_x > width/2:
                        flag = 2
                
                
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                classIDs.append(classID)
    n = len(boxes)
    cnt=cnt-1
    la=0
    for i in range(n):
        x,y,w,h = boxes[i]
        label = str(classes[classIDs[i]])
        print(label)
        if(str(it)==str(label)):
            la=1
            di=flag
        cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(image, label, (x, y+30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        
    playsound('searching.mp3')    
    if(la==1):
        print(flag)
        if (flag == 0 and flag==di):
            cv2.putText(image, "   ", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            playsound('under.mp3')
        elif (flag == 1 and flag==di):
            cv2.putText(image, "   ", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            playsound('object_left.mp3')
        elif (flag == 2 and flag==di):
            cv2.putText(image, "  ", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            playsound('object_right.mp3')
        else:
            cv2.putText(image, "  ", (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            playsound('object_front.mp3')
        cv2.imshow('Image',image)
    key = cv2.waitKey(500)
        

