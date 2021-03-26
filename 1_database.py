# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import math

faceCascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
#eyeCascade = cv2.CascadeClassifier('haar/haarcascade_eye.xml')


face_id = input('\n enter user id end press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
count = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (230, 230)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(230, 230))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    centers=[]
    
    faces = faceCascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        #eyes = eyeCascade.detectMultiScale(roi_gray)
        #for (ex, ey, ew, eh) in eyes:
            #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)

        count += 1
            
    # show the frame
    cv2.imshow("Frame", image)
    cv2.imshow("Gray", gray)

    cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + '.' + ".jpg", gray[y:y+h,x:x+w])    

    # clear the stream in preparation for the next frame
    k = cv2.waitKey(100) & 0xff
    rawCapture.truncate(0)
    if k == 27: # press 'ESC' to quit
        break
    elif count >= 100: # Take 100 face sample and stop video
        print ("Done! Exiting program...")
        break

cv2.destroyAllWindows
