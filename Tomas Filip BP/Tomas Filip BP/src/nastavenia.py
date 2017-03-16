# -*- coding: utf-8 -*-
#from win32api import GetSystemMetrics
import ctypes
import pygame
import math
import random
import time




BORDER = ["BorderLess", "Border"]
borderIndex = 1 # nacitat
WINDOW = ["Full screen","Windowed"]
windowIndex = 1 #nacitat

DEBUG = True

#VYPIS = True





MAP_SIZE_X = 18
MAP_SIZE_Y = 18

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

#3 typy pre kazdy postavu ine vlastnosti
#Zdravie Sila Rychlost vytrvalost
#mala postava fit a silna
VLASTNOSTI_POSTAVY = ["Zdravie", "Sila", "Rychlost", "Vytrvalost"]
VLASTNOSTI_POSTAVY_TYP_POSTAVY = [[3,3,5,5,],[4,4,4,4],[6,5,3,2]]
VLASTNOSTI_POSTAVY_POHLAVIE = [[0,1,0,0],[0,0,0,1]]


SEED = 123456


ROZLISENIA_X = [1280, 1600, 1920, 2560, 3200]
ROZLISENIA_Y = [720, 900, 1080, 1440, 1800]
vybrateRozlisenie = 0

UVODNE_NASTAVENIA_VYSKA = 400
UVODNE_NASTAVENIA_SIRKA = 400
UVODNE_NASTAVENIA_TITLE = "Bakalárska práca - nastavenia"

F2 = 0.5*(math.sqrt(3)-1)
G2 = (3-math.sqrt(3))/6

P_SUPPLY = (103, 30, 0, 120, 223, 131, 235, 238, 239, 92, 71, 183, 133, 247, 234, 162,
             48, 64, 242, 249, 96, 116, 45, 10, 154, 21, 146, 169, 230, 113, 148, 198,
              189, 205, 151, 127, 125, 248, 159, 233, 91, 177, 98, 123, 214, 216, 194,
               112, 165, 224, 207, 218, 57, 124, 6, 219, 102, 240, 68, 202, 178, 109,
                149, 143, 16, 38, 179, 147, 67, 161, 132, 121, 73, 81, 255, 47, 167, 29,
                 137, 75, 31, 129, 236, 168, 199, 90, 12, 32, 63, 24, 60, 8, 173, 188,
                  41, 196, 72, 142, 39, 141, 251, 106, 61, 158, 201, 53, 11, 84, 228,
                   211, 160, 200, 33, 172, 138, 227, 139, 58, 17, 104, 244, 197, 180,
                    246, 87, 222, 204, 65, 66, 231, 7, 20, 4, 86, 157, 13, 217, 171,
                     140, 18, 229, 105, 174, 50, 150, 187, 186, 210, 36, 253, 237, 136,
                      88, 9, 5, 15, 152, 28, 166, 145, 144, 128, 221, 181, 25, 23, 126,
                       62, 206, 208, 82, 245, 79, 241, 135, 35, 93, 52, 215, 37, 122, 110,
                        22, 95, 55, 182, 203, 175, 225, 111, 40, 115, 192, 94, 59, 85,
                         212, 107, 220, 77, 19, 153, 232, 195, 163, 44, 185, 2, 114, 89,
                          42, 250, 51, 243, 119, 155, 74, 190, 70, 43, 56, 100, 26, 97, 101,
                           164, 99, 14, 130, 49, 1, 191, 254, 134, 170, 69, 46, 108, 34, 176,
                            78, 54, 117, 193, 156, 83, 76, 226, 184, 3, 80, 27, 118, 252, 213, 209)







