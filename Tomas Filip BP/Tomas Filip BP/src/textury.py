'''
Created on 4. 3. 2017

@author: T.Filip
'''

import pygame
import logging
import textury

textury.uvodNastaveniaOkno = 0 
textury.TUN1center = 0
textury.TUN1left = 0
textury.TUN1leftOznacene = 0
textury.TUN2 = 0
textury.TUN2Oznacene = 0
textury.TUN3 = 0
textury.TUN3Krizik = 0
textury.TUN2Oznacene2 = 0
textury.TUN1right = 0
textury.TUN1rightOznacene = 0

textury.FONTY = [0 for i in range (20)]

def init():
    textury.uvodNastaveniaOkno = pygame.image.load('img\\uvodneNastavenia\\uvodNastaveniaOkno.png').convert_alpha()    
    textury.TUN1center = pygame.image.load('img\\uvodneNastavenia\\TUN1center.png').convert_alpha()
    textury.TUN1left = pygame.image.load('img\\uvodneNastavenia\\TUN1left.png').convert_alpha()
    textury.TUN1leftOznacene = pygame.image.load('img\\uvodneNastavenia\\TUN1leftOznacene.png').convert_alpha()
    textury.TUN2 = pygame.image.load('img\\uvodneNastavenia\\TUN2.png').convert_alpha()
    textury.TUN2Oznacene = pygame.image.load('img\\uvodneNastavenia\\TUN2Oznacene.png').convert_alpha()
    textury.TUN3 = pygame.image.load('img\\uvodneNastavenia\\TUN3.png').convert_alpha()
    textury.TUN3Krizik = pygame.image.load('img\\uvodneNastavenia\\TUN3Krizik.png').convert_alpha()
    textury.TUN2Oznacene2 = pygame.image.load('img\\uvodneNastavenia\\TUN2Oznacene2.png').convert_alpha()
    textury.TUN1right = pygame.transform.flip(textury.TUN1left,True,False)
    textury.TUN1rightOznacene = pygame.transform.flip(textury.TUN1leftOznacene,True,False)

    fon = textury.FONTY
    for i in range(20):
        fon[i] = pygame.font.Font("font\\armalite.ttf",i+10)
    
def dajFont(velkost):
    if velkost < 10 or velkost > 30:
        logging.warning("textury.dajFont -> taka velkost fontu nie je nacitana")
    else:
        return textury.FONTY[velkost-10]

