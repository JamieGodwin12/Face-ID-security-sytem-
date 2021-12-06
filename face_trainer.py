# import the required libraries
import cv2
import os
import numpy as np
from PIL import Image
import pickle
#loads haarcascade using a CascadeClassifier
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognise = cv2.face.LBPHFaceRecognizer_create()
#gets images function
def getdata():
    current_id = 0
    label_id = {} 
    face_train = [] 
    face_label = [] 
    #finding the path of the base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #looks for image_data folder 
    my_face_dir = os.path.join(BASE_DIR,'image_data')
    #gets all folders inside of the image_data folder. the users faces 
    for root, dirs, files in os.walk(my_face_dir):
        for file in files:
            #sees if file is png or jpg 
            if file.endswith("png") or file.endswith("jpg"):
                #Adds path of the file with the base path
                path = os.path.join(root, file)
                #gets the name of the folder and uses it as a label to mark who is who 
                label = os.path.basename(root).lower()
                #gives lable id as 1 or 2+ for diffrent users. 
                if not label in label_id:
                    label_id[label] = current_id
                    current_id += 1
                ID = label_id[label]
                #converts image into gray scale
                pil_image = Image.open(path).convert("L")
                #converts image data into numpy array
                image_array = np.array(pil_image, "uint8")    
                #identifies faces
                face = cascade.detectMultiScale(image_array)
                #finds location  and appends the data 
                for x,y,w,h in face:
                    img = image_array[y:y+h, x:x+w]
                    cv2.imshow("Test",img)
                    cv2.waitKey(1)
                    face_train.append(img)
                    face_label.append(ID)
    #puts lables into a file
    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_id, f) 
    return face_train,face_label
#creates the yml files to be used by other program 
face,ids = getdata()
recognise.train(face, np.array(ids))
recognise.save("trainner.yml")
