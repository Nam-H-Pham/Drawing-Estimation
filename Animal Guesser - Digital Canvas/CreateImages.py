import math, random, sys
import pygame
import random
import os
import time
from pygame.locals import *
import cv2

			
W, H = 500, 400
AREA = W * H


pygame.init()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Draw")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)


dots = []
DS.fill(WHITE)

left = 500
right = 0
top = 400
bottom = 0

name_of_drawing = input("Drawing Name: ")
number_of_saves = 0
empty_canvas = True
path = os.path.join(os.path.dirname(__file__),name_of_drawing)

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
                        print ("x:"+str(left)+"-"+str(right)+",y:"+str(top)+"-"+str(bottom))
                        name = str(name_of_drawing)+str(number_of_saves)+".jpeg"
                        name = os.path.join(path,name)
                        pygame.image.save(DS, name)
                        DS.fill(WHITE)
                        image = cv2.imread(name)
                        image = image[top:bottom, left:right]
                        image = cv2.resize(image, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_NEAREST)
                        cv2.imwrite(name, image)

                        number_of_saves += 1
                        left = 500
                        right = 0
                        top = 400
                        bottom = 0
                        DS.fill(WHITE)
                        empty_canvas = True 
                        time.sleep(0.1)
        #DS.fill(WHITE)
