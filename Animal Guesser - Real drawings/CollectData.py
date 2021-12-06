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
import glob
import numpy as np
import imutils
from datetime import datetime
from PIL import Image, ImageOps

def edge_filter(image):
    edged = cv2.Canny(image, 200, 200)
    edged_blurred = cv2.GaussianBlur(edged,(5,5),0)
    
    kernel = np.ones((8, 8), np.uint8)
    edged_blurred = cv2.morphologyEx(edged_blurred, cv2.MORPH_CLOSE, kernel)#merge

    return(edged,edged_blurred)

if __name__ == '__main__':

    local_path = (os.path.dirname(os.path.realpath('__file__')))
    drawings_path = os.path.join(local_path,"drawings")
    dirlist = next(os.walk(drawings_path))[1]

    print(dirlist)
    
    for item_name in dirlist:
        images_path = os.path.join(drawings_path,item_name)
        #print(images_path)

        png_files = os.listdir(images_path)
        png_files = [os.path.join(images_path,x) for x in png_files]

        print(png_files)

        for file_name in png_files:
            og_image = cv2.imread(file_name)
            image = og_image
            edged,edged_blurred = edge_filter(image)
            contours, hierarchy = cv2.findContours(edged_blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                for i in range(len(contours)):
                    
                    contour = contours[i]
                    if hierarchy[0,i,3] != -1:#if contour in contour
                        continue
                    x, y, w, h = cv2.boundingRect(contour)
                    if h < 10:
                        continue

                    cropped_image = edged[y:y+h, x:x+w]
                    cropped_image = cv2.bitwise_not(cropped_image)#invert colours
                    
                    crop_name = (str(datetime.now())).replace(':',',') + "(" + str(i)+ ").png"
                    destination = os.path.join(images_path,'cropped')
                    if not os.path.exists(destination):
                        os.makedirs(destination)
                    destination = os.path.join(destination,crop_name)
                    
                    print("saving >>> "+destination)
                    cv2.imwrite(destination, cropped_image) 

                
        #cv2.imshow('image',edged)
        


