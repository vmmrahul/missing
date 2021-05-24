import cv2
import base64
import numpy as np
import face_recognition
import os
from pymysql import *
import datetime


def makeConnections():
    return connect(host='127.0.0.1', user='root', password='', database='missingPerson',
                   cursorclass=cursors.DictCursor)



def get_cropped_img_if_2_eye(image_path):
    face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')
    img = image_path
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return True
        else:
            return False





class MakeEncodeAndCFindCriminal:
    def __init__(self):
        self.path = "./static/media/missingPerson"
        self.images = []
        self.classNames = []
        self.myList = os.listdir(self.path)

        for cl in self.myList:
            curImage = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImage)
            self.classNames.append(os.path.splitext(cl)[0])

        self.encodeListKnown = self.findEncodings(self.images)

    def search(self,image):
        # imgS = cv2.imread(image)
        imgS = image
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            print(matches)
            if True in matches:
                faceDistance = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                print(faceDistance)
                matchIndex = np.argmin(faceDistance)
                name = self.getPersionName(self.classNames[matchIndex].upper())
                return name


    def findEncodings(self,images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def getPersionName(self,id):
        query = "SELECT * FROM `profile` where id={} ".format(id)
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        result = cr.fetchone()
        return result



def get_cv2_image_from_base64_string(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


# file = open('../bash64Images/mes.txt','r')
# d  = get_cv2_image_from_base64_string(file.read())
#
# obj =MakeEncodeAndCFindCriminal()
# print(obj.search(d))

# obj = MakeEncodeAndCFindCriminal()
# print(obj.search('/home/rahul/Desktop/Programming/Pycharm_project/celebrity/Moedl/images_dataset/cropped/roger_federer/roger_federer1.png'))
