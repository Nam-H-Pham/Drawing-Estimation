import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import xlrd
import pygame
import cv2
import time
import shutil

import ProcessData
import CollectData

########Initialise random forest

local_path = (os.path.dirname(os.path.realpath('__file__')))

file_name = ('Data.xlsx')#file of total data
data_path = os.path.join(local_path,file_name)
print (data_path)
df = pd.read_excel (r''+data_path) 

print (df)

rows, columns = ProcessData.total_units_in_data()
units_in_data = rows*columns #no. of units in data

titles = []
for i in range(units_in_data):
    titles.append("unit"+str(i))
X = df[titles]
y = df['drawing']


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.5,random_state=2)

clf = RandomForestClassifier(n_estimators=30)#random forest
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print('Accuracy: ',metrics.accuracy_score(y_test, y_pred))

#########Begin predictions with drawings

predict_filename = input("File for analyzing: ")

predict_file = os.path.join(local_path,predict_filename)

print("analyzing >> "+predict_file)
og_image = cv2.imread(predict_file)
image = og_image
edged,edged_blurred = CollectData.edge_filter(image)
contours, hierarchy = cv2.findContours(edged_blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) > 0:
    for i in range(len(contours)):
        contour = contours[i]

        #sys.stdout.write("\033[F") #back to previous line
        #sys.stdout.write("\033[K") #clear line
        print(str(i+1)+"/"+str(len(contours)), end="\r")
        
        if hierarchy[0,i,3] != -1:#if contour in contour
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if h < 10:
            continue

        cropped_image = edged[y:y+h, x:x+w]
        cropped_image = cv2.bitwise_not(cropped_image)#invert colours

        crop_folder = os.path.join(local_path,'crop_for_prediction')
        if not os.path.exists(crop_folder):
            os.makedirs(crop_folder)
        else:
            shutil.rmtree(crop_folder)
            os.makedirs(crop_folder)

        cv2.imwrite(os.path.join(crop_folder,'crop.png'), cropped_image) 
        
        image_data = ProcessData.translate_to_data(crop_folder)[0]
        test_recordings = image_data
        
        #print (test_recordings)
        prediction = clf.predict([test_recordings])#input 
        #print ('Predicted Result: ', prediction)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(og_image, str(prediction), (x,y), font, 1.25, (255, 0, 0), 1, cv2.LINE_AA)

og_image = cv2.resize(og_image, (0,0), fx=0.4, fy=0.4) 

cv2.imwrite(('final_predictions.png'), og_image)

predictions_image = cv2.imread('final_predictions.png')
cv2.imshow('image',predictions_image)
cv2.waitKey(0)



