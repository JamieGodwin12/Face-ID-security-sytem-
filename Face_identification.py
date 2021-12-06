import cv2
video = cv2.VideoCapture(0)
# load "haarcascade_frontalface_default.xml" and make object
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
while True:
    check,frame = video.read()
    #convert video into a gray scale image which is only single colour lowwers amount of computation reqired
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detectMultiScale used to detect faces from video. returns x,y,w,h
    face = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 6)
    #loop through x,y,w,h
    for x,y,w,h in face:
        #draws a rectangle around face
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 3)       
    cv2.imshow("Video",frame)
    key = cv2.waitKey(1)
    if(key == ord('r')):
        break
video.release()
cv2.destroyAllWindows()

