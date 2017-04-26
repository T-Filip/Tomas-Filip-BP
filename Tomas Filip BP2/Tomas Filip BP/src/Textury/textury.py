'''
Created on 4. 3. 2017

@author: T.Filip
'''
from Textury import textury
from Textury import enumTextura
import pygame
import logging


uvodNastaveniaOkno = 0 
TUN1center = 0
TUN1left = 0
TUN1leftOznacene = 0
TUN2 = 0
TUN2Oznacene = 0
TUN3 = 0
TUN3Krizik = 0
TUN2Oznacene2 = 0
TUN1right = 0
TUN1rightOznacene = 0

'''
predvytvorene fonty aby sa za kazdym nemuseli vytvarat
pristupuje sa k nim pomocou metody a ako parameter velkost fontu
'''
FONTY = [0 for i in range (100)]

TEXTURY_SCALE = {}

def dajTexturu(id,rozmerX,rozmerY):
    try:
        return textury.TEXTURY_SCALE[(id,rozmerX,rozmerY)]
    except:
        povodna = textury.TEXTURY_SCALE[(id,0,0)]
        textury.TEXTURY_SCALE[(id,rozmerX,rozmerY)] = pygame.transform.scale(povodna,(rozmerX,rozmerY))
        return textury.dajTexturu(id, rozmerX, rozmerY)


#iba pri inicializacii textury
def vlozTexturuScaleBezId (textura,id):
    textury.TEXTURY_SCALE[(id,textura.get_width(),textura.get_height())] = textura
    textury.TEXTURY_SCALE[(id,0,0)] = textura


def init():
    textury.uvodNastaveniaOkno = pygame.image.load('img/uvodneNastavenia/uvodNastaveniaOkno.png').convert_alpha()    
    textury.TUN1center = pygame.image.load('img/uvodneNastavenia/TUN1center.png').convert_alpha()
    textury.TUN1left = pygame.image.load('img/uvodneNastavenia/TUN1left.png').convert_alpha()
    textury.TUN1leftOznacene = pygame.image.load('img/uvodneNastavenia/TUN1leftOznacene.png').convert_alpha()
    textury.TUN2 = pygame.image.load('img/uvodneNastavenia/TUN2.png').convert_alpha()
    textury.TUN2Oznacene = pygame.image.load('img/uvodneNastavenia/TUN2Oznacene.png').convert_alpha()
    textury.TUN3 = pygame.image.load('img/uvodneNastavenia/TUN3.png').convert_alpha()
    textury.TUN3Krizik = pygame.image.load('img/uvodneNastavenia/TUN3Krizik.png').convert_alpha()
    textury.TUN2Oznacene2 = pygame.image.load('img/uvodneNastavenia/TUN2Oznacene2.png').convert_alpha()
    textury.TUN1right = pygame.transform.flip(textury.TUN1left,True,False)
    textury.TUN1rightOznacene = pygame.transform.flip(textury.TUN1leftOznacene,True,False)
    
    textury.POSTAVY = pygame.image.load('img/Postavy/postavyNew.png').convert_alpha()  
    textury.TVARE = pygame.image.load('img/Postavy/tvareNew.png').convert_alpha() 
    textury.FRAME = pygame.image.load('img/Postavy/frame.png').convert_alpha()
    textury.KRVAVE_SKVRNY = pygame.image.load('img/Postavy/krvaveSkvrny.png').convert_alpha()
    
    
    textury.PREDMETY = pygame.image.load('img/Predmety/predmety.png').convert_alpha()
    textury.MENU_TLACIDLO = pygame.image.load('img/uvodneNastavenia/TlacidloMenu.png').convert_alpha()
    textury.MENU_TLACIDLO_OZNACENE = pygame.image.load('img/uvodneNastavenia/TlacidloMenuOznacene.png').convert_alpha()
    textury.MENU_TLACIDLO_LOCKNUTE = pygame.image.load('img/uvodneNastavenia/TlacidloMenuLocknute.png').convert_alpha()
    
    
    
    miestoPredmet = pygame.Surface((64,64),pygame.SRCALPHA)
    miestoPredmet.blit(textury.PREDMETY,(0,0),(64,0,64,64))
    vlozTexturuScaleBezId(miestoPredmet, enumTextura.EnumTextura.MIESTO_PREDMET )
    
    miestoPredmetOznacene = pygame.Surface((64,64),pygame.SRCALPHA)
    miestoPredmetOznacene.blit(textury.PREDMETY,(0,0),(128,0,64,64))
    vlozTexturuScaleBezId(miestoPredmetOznacene, enumTextura.EnumTextura.MIESTO_PREDMET_OZNACENY )
    
    #HPBAR
    hp = pygame.image.load('img/uvodneNastavenia/HealthBar.png').convert_alpha()
    hpBar = pygame.Surface((600,20),pygame.SRCALPHA)
    hpBar.blit(hp,(0,0),(0,0,600,20))
    vlozTexturuScaleBezId(hpBar, enumTextura.EnumTextura.HEALTH_BAR)
    
    
    
    
    textury.PREDMET_BEZ_TEXTURY =  pygame.Surface((64,64),pygame.SRCALPHA)
    textury.PREDMET_BEZ_TEXTURY.blit(textury.PREDMETY,(0,0),(0,0,64,64))
    
    textury.CRAFT_ITEM = pygame.image.load('img/Menu/CraftItem.png').convert_alpha()
    textury.CRAFT_ITEM_OZN = pygame.image.load('img/Menu/CraftItemOzn.png').convert_alpha()
    textury.CRAFT_ITEM_LOCK = pygame.image.load('img/Menu/CraftItemLock.png').convert_alpha()
    
    textury.TPlus = pygame.image.load('img/Menu/TPlus.png').convert_alpha()
    textury.TPlusOznacene = pygame.image.load('img/Menu/TPlusOznacene.png').convert_alpha()
    textury.TPlusLock = pygame.image.load('img/Menu/TPlusLock.png').convert_alpha()
    
    textury.MENU_OKNO = pygame.image.load('img/Menu/MenuOkno.png').convert()
    
    #pom = pygame.image.load('img/Menu/inventar2.png').convert_alpha()
    #textury.INVENTAR_RAMEC = pygame.Surface(pom.get_size(),pygame.SRCALPHA)#.convert_alpha()

    #textury.INVENTAR_RAMEC.blit(pom,(0,0))

    fon = textury.FONTY
    for i in range(100):
        fon[i] = pygame.font.Font("font/armalite.ttf",i)
    
def dajFont(velkost):
    if velkost > 100:
        logging.warning("textury.dajFont -> taka velkost fontu nie je nacitana")
        return textury.FONTY[99]
    elif velkost < 2:
        logging.warning("textury.dajFont -> prilis mala velkost fontu")
        return textury.FONTY[2]
    else:
        return textury.FONTY[velkost]

