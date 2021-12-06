import cv2#OpenCV
#VideoCapture() is made into an object
video = cv2.VideoCapture(0)
#endless while loop
while True:
    #looks to see if frame is active 
    check,frame = video.read()
    #shows image added for testing
    cv2.imshow("Video",frame)
    #adds key press to variable and waits 
    key = cv2.waitKey(1)
    #breaks loop if r is pressed
    if(key == ord('r')):
        break
#turns of webcam
video.release()
#closes all windows
cv2.destroyAllWindows()
