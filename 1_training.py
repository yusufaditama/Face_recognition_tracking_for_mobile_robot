import cv2
import numpy as np
from PIL import Image
import os
import time
# Path for face image database
start = time.time()
path = 'dataset'
mulai = time.time()
recognizer = cv2.face.FisherFaceRecognizer_create()
detector = cv2.CascadeClassifier('haar/haarcascade_eye.xml');
# function to get the images and label data
def getImagesAndLabels(path):
    width_d, height_d = 70, 70
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(cv2.resize(img_numpy[y:y+h,x:x+w], (width_d, height_d)))
            ids.append(id)
    return faceSamples,ids
selesai = time.time() - mulai
print ("proses ekstraksi: ",str(selesai)+"s")
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
s = time.time()
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer.yml
recognizer.save('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
e = time.time() - s
print ("proses training: ",str(e)+"s")
end = time.time() - start
print ("overall time: ",str(end)+"s")
