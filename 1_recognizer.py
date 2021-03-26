from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import os
import time
import sys
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)
print("Connected to Arduino...")

recognizer = cv2.face.FisherFaceRecognizer_create()
database = "trainer/trainer.yml"
data = recognizer.read(database)
cascadePath = "haar/haarcascade_frontalface_default.xml"
eyePath = "haar/haarcascade_eye.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
eyeCascade = cv2.CascadeClassifier(eyePath);
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0

names = ['None', 'Yusuf', 'Retno']

camera = PiCamera()
camera.resolution = (230, 230)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(230, 230))

time.sleep(0.1)

width_d, height_d = 70, 70


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    #s = time.time()
    #k = time.time()
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray,1.3,5)

    if len(faces) == 0:
        print ("Tak ada wajah")
        ser.write (b'6')
    elif len(faces) == 1:
        for(x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
            #ew = time.time() - s
            #print ("deteksi wajah: ", str(ew)+" s")
            
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]

            Xpos = x +(w/2)
            Ypos = y +(h/2)
            
            cv2.putText(image, str(Xpos), (10, 20), font, 0.5, (255,255,255), 1)
            cv2.putText(image, str(Ypos), (10, 40), font, 0.5, (255,255,255), 1)

            #m = time.time()
            
            eyes = eyeCascade.detectMultiScale(roi_gray,1.3,5)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)
            
            #deteksi = time.time() - s
            #print ("deteksi : ", str(deteksi)+" s")
            
            start = time.time()
            id, confidence = recognizer.predict(cv2.resize(roi_gray[ey:ey+eh,ex:ex+ew], (width_d, height_d)))

            #print(confidence)
            
            if (confidence < 21):
                id = names[id]
                print ("dikenali atas nama: ", str(id), ", dengan distance: ", str(confidence))
                #print('posisi x: ' , Xpos)
                
                
                if Xpos <= 90:
                    ser.write(b'1')
                    cv2.putText(image, "Kanan", (10, 200), font, 0.5, (255,255,255), 1)
                    #print("BELOK KIRI")
                elif Xpos >= 145:
                    ser.write(b'2')
                    cv2.putText(image, "Kiri", (10, 200), font, 0.5, (255,255,255), 1)
                    #print("BELOK KANAN")
                elif (Xpos > 90) & (Xpos < 145):
                    ser.write(b'0')
                    cv2.putText(image, "Tengah", (10, 200), font, 0.5, (255,255,255), 1)
                    #print("MAJU")

                if Ypos <= 100:
                    ser.write(b'3')
                    cv2.putText(image, "Kanan", (10, 220), font, 0.5, (255,255,255), 1)
                elif Ypos >= 160:
                    ser.write(b'4')
                    cv2.putText(image, "Kiri", (10, 220), font, 0.5, (255,255,255), 1)
                elif (Ypos > 100) & (Ypos < 160):
                    ser.write(b'5')
                    cv2.putText(image, "Tengah", (10, 220), font, 0.5, (255,255,255), 1)             
                #recog = time.time() - start
                #print ("dikenali: ", str(recog)+" s")

                
                #ser.write(b"1")
                
            else:
                ser.write(b"6")
                id = "unknown"
                print (str(id), "dengan distance: ", str(confidence))
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
                #unk = time.time() - start
                #print ("unknown: ", str(unk)+" s")
                
                
            #end = time.time() - start
            #se = time.time() - s
            #print ("pengenalan: ", str(end)+" s")
            #print ("waktu proses: ", str(se)+" s")
            
            cv2.putText(image, str(id), (x+5,y-5), font, 0.5, (255,255,0), 1)
            cv2.putText(image, str(confidence), (x+5,y+h-5), font, 0.5, (255,255,0), 1)
    
    cv2.imshow("Frame", image)
    cv2.imshow("Gray", gray)
    
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
        

    
