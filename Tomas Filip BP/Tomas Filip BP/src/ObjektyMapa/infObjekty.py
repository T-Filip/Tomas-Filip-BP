'''
Created on 15. 2. 2017

@author: T.Filip
'''
from collections import namedtuple
import pygame
import collections
import mapa
from ObjektyMapa import scale
import copy

INF_OBJ_MAPA = {}
objMapaScalovanie = pygame.sprite.Group() # mnozina objektov na mape ktorym je nutne menit poziciu na obrazovke pri pohybe hraca (tak ako policka alebo aj samotnemu hracovi)
infObjScalovanie = {}# mnozina infObj ktore su momentalne pouzivane a pre zobrazenie potrebuju scalovat
nextID = 0


#InfObj = namTupDef("InfObj", "img rectObjOblastMapa rychlostPrechodu pocPouzivajucich", {'pocPouzivajucich':0})
class InfObj:
    def __init__(self,img, rectObjOblastMapa = None, rychlostPrechodu = 1):
        self.img = img
        if rectObjOblastMapa == None:
            self.rectObjOblastMapa = self.img.get_rect()
        else:
            self.rectObjOblastMapa = rectObjOblastMapa #relativna pozicia v img
        
        self.rychlostPrechodu = rychlostPrechodu



        
        
class InfObjScale(InfObj,scale.ObjScale):
    def __init__(self,img, rectObjOblastMapa, rychlostPrechodu):
        self.imgZaloha = img.copy()
        infObjScalovanie[self]=self
        self.sprites = pygame.sprite.Group()
        super().__init__(img, rectObjOblastMapa, rychlostPrechodu)
        
    def scale(self,nas):
        self.img = pygame.transform.scale(self.imgZaloha,(int(self.imgZaloha.get_width()*nas),int( self.imgZaloha.get_height()*nas)))
        print(str(int(self.imgZaloha.get_width()*nas)))
        for sp in self.sprites:
            sp.scale(nas)
            sp.newRefImg()

    #metoda sa vola pri vytvarani noveho objektu v mape s aktivnym prekreslovanim, kedze data objektov ktore nie su pouzivane sa nescaluju je potrebne tak urobit na zaciatku ich pouzivania
    def aktualizujData(self): 
        if len(self.sprites) <= 1:
            self.scale(mapa.SINGLETON_MAPA.dajNas())

    #def vymazSprite(self,sprite):
    #   self.sprites.remove(sprite) 




        
#informacie o celopolickovych objektoch - obsahuju niekolko InfObj a to o kazdom jeho kusku
class InfObjCelPol:
    def __init__(self,zoznam,texturaPolicka):
        self.infObjekty = zoznam
        self.texturaPolicka = texturaPolicka # Tato textura sa vyuzije ak su vsade naokolo policka objekty s tymto id
        
        
class InfObjCelPolPozadie(InfObjCelPol):
    def __init__(self,zoznam,texturaPolicka,pozadie,zozRectPoz = None):
        self.pozadie = pozadie
        self.rectPozadia = zozRectPoz
        super().__init__(zoznam,texturaPolicka)
        
        
    
        
#InfObjCeloPolickoveSpajanie = namTupDef("InfObjCeloPolickoveSpajanie", "img rychlostPrechodu pocPouzivajucich",{'pocPouzivajucich':0})




def vlozInf (obj):
    global nextID
    INF_OBJ_MAPA[nextID] = obj
    print(nextID)
    nextID +=1
    

  


            

def nacitajTexturyObjMapa():

    global nextID

#-------------------STOROMY----------------
    stromy = pygame.image.load('img\\objektyMapa\\Stromy.png').convert_alpha()
    texturaStromov = [pygame.Surface((48,64),pygame.SRCALPHA) for i in range (0,18)]

    #rectStromov = pygame.Rect(16,16,16,32)#relativna hodnota v texturovej oblasti, zatial docasne rovnake pre vsetky stromy .. docasne? 
    rectStromov = pygame.Rect(16,16,16,32)
    id = 0
    for x in range (0,6):
        for y in range (0,3):
            texturaStromov[id].blit(stromy,(0,0),(48*x,64*y,48,64))
            vlozInf(InfObjScale(texturaStromov[id],rectStromov,0.5))
            id+=1



#------------------------KVIETKY-------------------
    nextID = 50
    kvietky = pygame.image.load('img\\objektyMapa\\kvietky.png').convert_alpha()
    rect = pygame.Rect(4,10,8,6)
    texturaKvietkov = [pygame.Surface((16,16),pygame.SRCALPHA) for i in range (0,6)]
    for y in range (0,6):
        texturaKvietkov[y].blit(kvietky,(0,0),(0,16*y,16,16))
        vlozInf(InfObj(texturaKvietkov[y],rect,0.95))

    

#---------------------SUTRE---------------
    sutre = pygame.image.load('img\\objektyMapa\\Sutre.png').convert_alpha()
    
    
    #zacinaju sutre
     
    nextID = 100
    
    for druh in range(0,2):
    
        posun = 76*druh
        #velke
        rect = pygame.Rect(6,20,50,23)
        surf = pygame.Surface((63,45),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(0,30+posun,63,45))
        vlozInf(InfObjScale(surf,rect,0))
        
        rect = pygame.Rect(10,10,45,30)
        surf = pygame.Surface((60,43),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(67,26+posun,60,43))
        vlozInf(InfObjScale(surf,rect,0))
        
        rect = pygame.Rect(8,30,18,27)
        surf = pygame.Surface((29,49),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(128,26+posun,29,49))
        vlozInf(InfObjScale(surf,rect,0))
        
        #stredna1
        rect = pygame.Rect(3,13,25,10)
        surf = pygame.Surface((30,30),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(1,1+posun,30,30))
        vlozInf(InfObjScale(surf,rect,0.2))
        #stred 2
        
        rect = pygame.Rect(6,11,23,12)
        surf = pygame.Surface((33,24),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(32,0+posun,33,24))
        vlozInf(InfObjScale(surf,rect,0.35))
        
        #male
        rect = pygame.Rect(2,5,13,7)
        surf = pygame.Surface((17,13),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(64,0+posun,17,13))
        vlozInf(InfObj(surf,rect,0.65))
        
        rect = pygame.Rect(1,3,9,5)
        surf = pygame.Surface((13,8),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(64,13+posun,13,8))
        vlozInf(InfObj(surf,rect,0.75))
        
        rect = pygame.Rect(5,3,6,5)
        surf = pygame.Surface((12,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(80,0+posun,12,9))
        vlozInf(InfObj(surf,rect,0.75))
        
        rect = pygame.Rect(2,3,7,6)
        surf = pygame.Surface((11,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(80,8+posun,11,9))
        vlozInf(InfObj(surf,rect,0.7))
        
        rect = pygame.Rect(2,4,9,5)
        surf = pygame.Surface((13,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(91,0+posun,13,9))
        vlozInf(InfObj(surf,rect,0.65))
        
        rect = pygame.Rect(3,2,5,5)
        surf = pygame.Surface((10,7),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(90,8+posun,10,7))
        vlozInf(InfObj(surf,rect,0.9))
        
        rect = pygame.Rect(1,4,9,5)
        surf = pygame.Surface((13,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(76,16+posun,13,9))
        vlozInf(InfObj(surf,rect,0.8))
        
        rect = pygame.Rect(2,1,6,4)
        surf = pygame.Surface((8,6),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(89,15+posun,8,6))
        vlozInf(InfObj(surf,rect,1))
    
    

    
    
    
    #------------------------------------- VODA CELOPOLICKO-------------------------
    #zacinaju celopolicka

    nextID = 200
    pobrezia = pygame.image.load('img\\objektyMapa\\Pobrezia.png').convert_alpha()
    voda  = pygame.image.load('img\\objektyMapa\\voda.png').convert_alpha()
    hlbokaVoda = pygame.image.load('img\\objektyMapa\\hlbokaVoda.png').convert_alpha()
    

    #Zozanm[][]   [tvar][cislotextury]
    #pocet textur variabilny osetrene by malo byt vsade
    texturyCasti = [0 for x in range(3)]
    
    pocetTexturVType = [0 for i in range(3)]
    pocetTexturVType[0] = 3
    pocetTexturVType[1] = 1
    pocetTexturVType[2] = 1
    
    texturyCasti[0] = [0 for y in range(pocetTexturVType[0])]
    texturyCasti[1] = [0 for y in range(pocetTexturVType[1])]
    texturyCasti[2] = [0 for y in range(pocetTexturVType[2])]
    
    zoznamInf = [0 for y in range(12)] 
    for i in range (0,4):
        zoznamInf[i] = [0 for j in range(pocetTexturVType[0])]
    for i in range (4,8):
        zoznamInf[i] = [0 for j in range(pocetTexturVType[1])]
    for i in range (8,12):
        zoznamInf[i] = [0 for j in range(pocetTexturVType[2])]
    zozRect = copy.deepcopy(zoznamInf)
    
    
    for i in range (0,pocetTexturVType[0]):
        texturyCasti[0][i] = pygame.Surface((16,16),pygame.SRCALPHA)
        texturyCasti[0][i].blit(pobrezia,(0,0),(0,i*16,16,16))
                                
    for i in range (0,pocetTexturVType[1]):
        texturyCasti[1][i] = pygame.Surface((16,16),pygame.SRCALPHA)
        texturyCasti[1][i].blit(pobrezia,(0,0),(16,i*16,16,16))
        
    for i in range (0,pocetTexturVType[2]):
        texturyCasti[2][i] = pygame.Surface((16,16),pygame.SRCALPHA)
        texturyCasti[2][i].blit(pobrezia,(0,0),(32,i*16,16,16))

    
    #ROHVODA
    rect = pygame.Rect(10,10,6,6)
    for i in range (0,pocetTexturVType[0]):
        zoznamInf[0][i] = InfObj(texturyCasti[0][i],rect,0.75)
        zozRect[0][i] = [pygame.Rect(10,10,6,6)]
      
    rect = pygame.Rect(0,10,6,6)
    for i in range (0,pocetTexturVType[0]):
        text = pygame.transform.flip(texturyCasti[0][i],True,False)
        zoznamInf[1][i] = InfObj(text,rect,0.75)
        zozRect[1][i] = [pygame.Rect(0,10,6,6)]
      
    rect = pygame.Rect(10,0,6,6)  
    for i in range (0,pocetTexturVType[0]):
        text = pygame.transform.flip(texturyCasti[0][i],False,True)
        zoznamInf[2][i] = InfObj(text,rect,0.75)
        zozRect[2][i] = [pygame.Rect(10,0,6,6) ]
        
    rect = pygame.Rect(0,0,6,6)
    for i in range (0,pocetTexturVType[0]):
        text = pygame.transform.flip(texturyCasti[0][i],True,True)
        zoznamInf[3][i] = InfObj(text,rect,0.75)
        zozRect[3][i] = [pygame.Rect(0,0,6,6) ]
        
        
    #ROVNOVODA
    rect = pygame.Rect(0,10,16,6)
    for i in range (0,pocetTexturVType[1]):
        zoznamInf[4][i] = InfObj(texturyCasti[1][i],rect,0.6)
        zozRect[4][i] = [pygame.Rect(0,10,16,6) ]
        
    rect = pygame.Rect(10,0,6,16)
    for i in range (0,pocetTexturVType[1]):
        text = pygame.transform.rotate(texturyCasti[1][i],90)
        zoznamInf[5][i] = InfObj(text,rect,0.6)
        zozRect[5][i] = [pygame.Rect(10,0,6,16) ]
    
    rect = pygame.Rect(0,0,16,6)
    for i in range (0,pocetTexturVType[1]):
        text = pygame.transform.rotate(texturyCasti[1][i],270)
        zoznamInf[6][i] = InfObj(text,rect,0.6)
        zozRect[6][i] = [pygame.Rect(0,0,16,6) ]
    
    rect = pygame.Rect(0,0,6,16)
    for i in range (0,pocetTexturVType[1]):
        text = pygame.transform.rotate(texturyCasti[1][i],180)
        zoznamInf[7][i] = InfObj(text,rect,0.6)
        zozRect[7][i] = [pygame.Rect(0,0,6,16)]
        
       
    #ROHZEM 
    for i in range (0,pocetTexturVType[2]):
        zoznamInf[8][i] = InfObj(texturyCasti[2][i],None,0.6)
        zozRect[8][i] = [pygame.Rect(0,0,16,6),pygame.Rect(0,6,6,10),pygame.Rect(6,6,5,5) ]
        

    for i in range (0,pocetTexturVType[2]):
        text = pygame.transform.rotate(texturyCasti[2][i],90)
        zoznamInf[9][i] = InfObj(text,None,0.6)
        zozRect[9][i] = [pygame.Rect(0,10,16,6),pygame.Rect(10,0,6,10),pygame.Rect(5,6,5,5) ]
        #zozRect[9][i] = [pygame.Rect(0,0,16,6),pygame.Rect(10,6,6,10),pygame.Rect(5,6,5,5) ]
    

    for i in range (0,pocetTexturVType[2]):
        text = pygame.transform.rotate(texturyCasti[2][i],270)
        zoznamInf[10][i] = InfObj(text,None,0.6)
        #zozRect[10][i] = [pygame.Rect(0,10,16,6),pygame.Rect(10,0,6,10),pygame.Rect(5,6,5,5) ]
        zozRect[10][i] = [pygame.Rect(0,0,16,6),pygame.Rect(10,6,6,10),pygame.Rect(5,6,5,5) ]
    

    for i in range (0,pocetTexturVType[2]):
        text = pygame.transform.rotate(texturyCasti[2][i],180)
        zoznamInf[11][i] = InfObj(text,None,0.6)
        zozRect[11][i] = [pygame.Rect(0,10,16,6),pygame.Rect(10,0,6,10),pygame.Rect(5,5,5,5) ]
        
    
        
    
    
        
    
    celoPolVoda = InfObjCelPolPozadie(zoznamInf,hlbokaVoda,voda,zozRect)
    vlozInf(celoPolVoda)
    print("Nacitavanie inf done")

 # -----------------------------------
'''
Povinne:
rychlostPrechodu # nasobitel ak 0.5 tak sa pohybuje 50% rychlostou (este sa to ale potom priemeruje)
pocPouzivajucich # pocet objektov ktore prave vyuzivau tuto texturu (aby sa nemuseli scalovat vsetky objekty)


'''


#zakladna sada


#obsahuje textury pre vsetky kombinacie, rect si robi samo podla okolia


