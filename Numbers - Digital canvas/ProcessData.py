import math, random, sys
import random
import os
import time
import cv2
import numpy as np
import xlsxwriter
import csv

def collect_data(path):
     all_image_data = []
     for filename in os.listdir(path):
          image_path = (os.path.join(path,filename))
          #print (image_path)
          image = cv2.imread(image_path)

          height, width, channels = image.shape
          #print ([width, height])

          rows = 7
          columns = 5
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
          #cv2.imshow(folder_name,image)

     return (all_image_data)
          
if __name__ == '__main__':
    # code to be executed only on direct execution, but not on import
     folder_name = input("folder name: ")
     path = os.path.join(os.path.dirname(__file__),folder_name)

     all_image_data = collect_data(path)


     titles = ['number']
     for i in range(len(all_image_data[0])):#length of first image of data in all data
         titles.append("unit"+str(i))
     with open(folder_name+".csv", "a", newline='') as fp:
         wr = csv.writer(fp, dialect='excel')
         wr.writerow(titles)
         
             
     for data in all_image_data:
         writedata = [str(folder_name)]
         writedata.extend(data)
         print (writedata)
         with open(folder_name+".csv", "a", newline='') as fp:
             wr = csv.writer(fp, dialect='excel')
             wr.writerow(writedata)
     print("finished")

			
