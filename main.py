import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionopencv-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognitionopencv.appspot.com"
})



cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print('Loading Encoded File ...')

file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print('Encode File Loaded ...')


modeType = 0
counter = 0
id = -1



while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)


    img = cv2.resize(img, (640, 480))
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]







    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print("matches", matches)
        # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)

        # print("Match Index", matchIndex)

        if matches[matchIndex]:
            print("Known Face Detected")
            print(studentIds[matchIndex])
            top, right, bottom, left = faceLoc  # Correctly unpack the faceLoc tuple
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4  # Scale coordinates
            cv2.rectangle(imgBackground, (left + 55, top + 162), (right + 55, bottom + 162), (255, 0, 255), 2)
            id = studentIds[matchIndex]

            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:
        if counter == 1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
        

            counter +=1


    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
