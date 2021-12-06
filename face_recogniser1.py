import cv2
import pickle
import serial
import time
import os
import readchar
import datetime
#Setting serial port to COM3  at bard rate of 9600
port = serial.Serial('COM3',9600)
now = datetime.datetime.now()
loop=True
print('Press A to enter password. Press B for facial recognition')
#loop to pick how to open door
while loop == True:
    ch = readchar.readkey()
    ch=ch.upper()
    print (ch)
    if ch == 'A':
        loop = False
    elif ch == 'B':
        loop = False
    else:
        print('please enter a or b')
#added password which when entered correctly will send a 1 to the port which will work with the code uploaded to the arduino
if ch == 'A':
    count =0
    while True:
        Password =input('Enter password\n')
        if Password == '7859':
            print('correct password')
            print("Current date and time: ")
            print(str(now))
            #sends 1 to arduino
            port.write(str.encode('1'))
            break
        else:
            print('Inccorect password')
            print("Current date and time: ")
            print(str(now)) 
            print(ch)
            count = count +1 #added a count if password is wrong 5 times program ends
            if count >=5:
                ch='B'
                break
if ch == 'B':           
    #creates video as object 
    video = cv2.VideoCapture(0)
    #loads haarcascade using a CascadeClassifier
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #loads face recogniser and reads the trained data
    recognise = cv2.face.LBPHFaceRecognizer_create()
    recognise.read("trainner.yml")
    #Opens labels.pickle file and creating a dictionary containing the label id
    labels = {}
    with open("labels.pickle", 'rb') as f:
        og_label = pickle.load(f)
        labels = {v:k for k,v in og_label.items()}
        print(labels)

    while True:
        check,frame = video.read()
        #convert video into a gray scale image which is only single colour lowwers amount of computation reqired
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #detectMultiScale used to detect faces from video. returns x,y,w,h
        face = cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5)
        #loop through x,y,w,h
        for x,y,w,h in face:
            face_save = gray[y:y+h, x:x+w]
            #predicts the face being identified 
            ID, conf = recognise.predict(face_save)
            if conf >= 20 and conf <= 115:
                print(ID)
                print(labels[ID])
                #used to draw a text string on any image
                cv2.putText(frame,labels[ID],(x-10,y-10),cv2.FONT_HERSHEY_COMPLEX ,1, (18,5,255), 2, cv2.LINE_AA )

                #Checking the ID if 1 unlocks if 0 stays locked
                if(ID == 1):
                    #sends 1 to arduino
                    port.write(str.encode('1'))
                    print("Unlocking door")
                    print("Current date and time: ")
                    print(str(now))
                    time.sleep(10)

                elif(ID == 0):
                    #sends 0 to arduino
                    port.write(str.encode('0'))
                    print("Not recognized")
                    print("Current date and time: ")
                    print(str(now))
                    time.sleep(10)
            #draws a rectangle
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,255),4)
        #r will end program
        cv2.imshow("Video",frame)
        key = cv2.waitKey(1)
        if(key == ord('r')):
            break
    #turns off webcam
    video.release()
    #closes any windows which are open from the program
    cv2.destroyAllWindows()
