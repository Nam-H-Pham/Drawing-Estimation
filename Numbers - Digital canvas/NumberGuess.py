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

from ProcessData import collect_data
########Initialise random forest

local_path = (os.path.dirname(os.path.realpath('__file__')))

file_name = ('Numbers.xlsx')#file of total data
data_path = os.path.join(local_path,file_name)
#print (data_path)
df = pd.read_excel (r''+data_path) 

print (df)

units_in_data = 35 #no. of units in data
titles = []
for i in range(units_in_data):
    titles.append("unit"+str(i))
X = df[titles]
y = df['number']


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.4,random_state=0)

clf = RandomForestClassifier(n_estimators=100)#random forest
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print('Accuracy: ',metrics.accuracy_score(y_test, y_pred))
clear = lambda: os.system('cls')
clear()

#########Begin predictions with drawings

W, H = 300, 400
AREA = W * H
pygame.init()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Draw")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

dots = []
DS.fill(WHITE)

left = 300
right = 0
top = 400
bottom = 0

empty_canvas = True
path = os.path.join(os.path.dirname(__file__),'prediction_images')

if not os.path.exists(path):
    os.makedirs(path)

while True:
        penwidth = 8
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if pygame.mouse.get_pressed()[0]:
                      mx, my = pygame.mouse.get_pos()
                      dots.append([mx, my])
                      if len(dots) > 2:
                              dots.pop(0)
                      if mx < left:
                              left = mx-penwidth
                      if mx > right:
                              right = mx+penwidth
                              
                      if my < top:
                              top = my-penwidth
                      if my > bottom:
                              bottom = my+penwidth
                      empty_canvas = False  
                else:dots = []


        for a in dots:
          for b in dots: 
              pygame.draw.line(DS, BLACK, (a), (b), penwidth)
        
        pygame.display.update()


        if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                   if empty_canvas == False:
                        #print ("x:"+str(left)+"-"+str(right)+",y:"+str(top)+"-"+str(bottom))
                        name = "predict.jpeg"
                        name = os.path.join(path,name)
                        try:os.remove(name)
                        except:pass
                        pygame.image.save(DS, name)
                        image = cv2.imread(name)
                        image = image[top:bottom, left:right]
                        image = cv2.resize(image, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_NEAREST)
                        cv2.imwrite(name, image)

                        left = 300
                        right = 0
                        top = 400
                        bottom = 0
                        DS.fill(WHITE)
                        empty_canvas = True 
                        time.sleep(0.1)

                        test_recordings = collect_data(path)[0]
                        
                        #print (test_recordings)
                        prediction = clf.predict([test_recordings])#input 
                        print ('Predicted Result: ', prediction)

