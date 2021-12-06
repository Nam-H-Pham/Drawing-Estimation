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
import imutils
from datetime import datetime
import csv

def total_units_in_data():
     rows = 7
     columns = 6
     return(rows,columns)

def translate_to_data(path):
     all_image_data = []
     for filename in os.listdir(path):
          image_path = (os.path.join(path,filename))
          #print (image_path)
          image = cv2.imread(image_path)

          height, width, channels = image.shape
          #print ([width, height])

          rows, columns = total_units_in_data()
          x_unit = width/columns
          y_unit = height/rows

          image_data = []#list of squares and if black or white (1 = black, 0 = white)       
          for col in range(columns):
              x = col*x_unit
              for row in range(rows):
                  y = row*y_unit

                  cv2.rectangle(image,(int(x), int(y)),(int(x+x_unit), int(y+y_unit)),(0, 255, 0), 0)#green squares = white
                  image_unit = image[int(y):int(y+y_unit), int(x):int(x+x_unit)]

                  square_contains_black = False
                  image_unit_width, image_unit_height, channels = image_unit.shape #search each block for black
                  for px in range(image_unit_width):
                      for py in range(image_unit_height):
                          r, g, b = image_unit[px, py]
                          if [0, 0, 0] == [r, g, b]:
                              square_contains_black = True

                  if square_contains_black == True:
                     cv2.rectangle(image,(int(x), int(y)),(int(x+x_unit), int(y+y_unit)),(0, 0, 255), 1)#red squares = blacked
                     image_data.append(1)
                  else:
                     image_data.append(0)
                     
          all_image_data.append(image_data)

     return (all_image_data)

if __name__ == '__main__':
     local_path = (os.path.dirname(os.path.realpath('__file__')))
     drawings_path = os.path.join(local_path,"drawings")
     dirlist = next(os.walk(drawings_path))[1]

     titles = ['drawing']
     rows, columns = total_units_in_data()
     for i in range(rows*columns):#length of first image of data in all data
         titles.append("unit"+str(i))
     with open("CSV_Data.csv", "a", newline='') as fp:  #creating titles
         wr = csv.writer(fp, dialect='excel')
         wr.writerow(titles)

     for item_name in dirlist:
          images_path = os.path.join(drawings_path,item_name)
          data_path = os.path.join(images_path,"cropped")
          print(data_path)

          all_image_data = translate_to_data(data_path)
          #print (all_image_data)

              
                  
          for data in all_image_data: #filling in rows
              writedata = [str(item_name)]
              writedata.extend(data)
              print (writedata)
              with open("CSV_Data.csv", "a", newline='') as fp:
                  wr = csv.writer(fp, dialect='excel')
                  wr.writerow(writedata)
     Finished = input("Finished.")


    


