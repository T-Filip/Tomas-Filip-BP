'''
Created on 14. 2. 2017

@author: T.Filip
'''
import pygame


POLICKO_TRAVA = [pygame.Surface((64,64)) for i in range (0,6)]

def initTextury():
    trava = pygame.image.load('img/Policka/PolickaTrava.png').convert()
    for i in range (0,6):
        POLICKO_TRAVA[i].blit(trava,(0,0),(64*i,0,64,64))