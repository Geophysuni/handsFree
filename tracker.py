# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 18:50:50 2023

@author: Sergey Zhuravlev
"""

import cv2
import time
import numpy as np
# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam (0 is usually the default camera)
# cap = cv2.VideoCapture(0)

def track(frame, kb, crdList, gl):
    # print(time.time())
    try:
        
        frame = cv2.flip(frame, 1)
        
        keyboard = np.copy(kb)
        keyboard = cv2.resize(keyboard, (1500,500), interpolation = cv2.INTER_AREA)
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
        # Draw rectangles around the detected faces
        for (fx, fy, fw, fh) in faces:
            cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), (0, 255, 0), 2)
            try:
                face = frame[fy:fy+fh, fx:fx+fw]
            except:
                bonk = 1
                
        
        gray_frame = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (7,7), 0)
        _, threshold_frame = cv2.threshold(gray_frame, gl ,255, cv2.THRESH_BINARY)
        
        contours, _  = cv2.findContours(threshold_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse = True)
        
        try:
            for cnt in contours:
                (x,y,w,h) = cv2.boundingRect(cnt)
                cv2.rectangle(face, (x,y), (x+w, y+h), (255, 0, 0), 2)
                kx, ky = 5, 5
                # print(str(fx+x)+'/'+str(fy+y))
                
                xs, ys = crdList[0][0], crdList[0][1]
                if len(crdList)==1:
                    crdList.append((fx+x,fy+y))
                else:
                    dx, dy = int(kx*(fx+x-crdList[1][0])), int(ky*(fy+y-crdList[1][1]))
        
                    smX = int(xs+dx)
                    smY = int(ys+dy)
            
                    cv2.circle(keyboard, (smX, smY), 10, (0, 255, 0), -1)
                    if len(crdList)==2:
                        crdList.append((smX, smY))
                    if len(crdList)==3:
                        crdList[2]=(smX, smY)

                break
        except:
            bonk =1 
        
        return frame, keyboard, crdList
    except:
        # bonk = 1
        return frame, keyboard, crdList

