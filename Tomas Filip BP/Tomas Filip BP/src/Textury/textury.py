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

textury.FONTY = [0 for i in range (100)]

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
    
    textury.POSTAVY = pygame.image.load('img\\Postavy\\postavyNew.png').convert_alpha()  
    textury.TVARE = pygame.image.load('img\\Postavy\\tvareNew.png').convert_alpha() 
    textury.FRAME = pygame.image.load('img\\Postavy\\frame.png').convert_alpha()
    
    textury.PREDMETY = pygame.image.load('img\\Predmety\\predmety.png').convert_alpha()
    textury.MIESTO_PREDMET = pygame.Surface((64,64),pygame.SRCALPHA)
    textury.MIESTO_PREDMET.blit(textury.PREDMETY,(0,0),(64,0,64,64))
    
    textury.PREDMET_BEZ_TEXTURY =  pygame.Surface((64,64),pygame.SRCALPHA)
    textury.PREDMET_BEZ_TEXTURY.blit(textury.PREDMETY,(0,0),(0,0,64,64))
    
    textury.CRAFT_ITEM = pygame.image.load('img\\Menu\\CraftItem.png').convert_alpha()
    textury.CRAFT_ITEM_OZN = pygame.image.load('img\\Menu\\CraftItemOzn.png').convert_alpha()
    textury.CRAFT_ITEM_LOCK = pygame.image.load('img\\Menu\\CraftItemLock.png').convert_alpha()
    
    textury.TPlus = pygame.image.load('img\\Menu\\TPlus.png').convert_alpha()
    textury.TPlusOznacene = pygame.image.load('img\\Menu\\TPlusOznacene.png').convert_alpha()
    textury.TPlusLock = pygame.image.load('img\\Menu\\TPlusLock.png').convert_alpha()
    
    textury.MENU_OKNO = pygame.image.load('img\\Menu\\MenuOkno.png').convert()
    
    #pom = pygame.image.load('img\\Menu\\inventar2.png').convert_alpha()
    #textury.INVENTAR_RAMEC = pygame.Surface(pom.get_size(),pygame.SRCALPHA)#.convert_alpha()

    #textury.INVENTAR_RAMEC.blit(pom,(0,0))

    fon = textury.FONTY
    for i in range(100):
        fon[i] = pygame.font.Font("font\\armalite.ttf",i)
    
def dajFont(velkost):
    if velkost > 100:
        logging.warning("textury.dajFont -> taka velkost fontu nie je nacitana")
    else:
        return textury.FONTY[velkost]

