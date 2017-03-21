'''
Created on 15. 2. 2017

@author: T.Filip
'''
import pygame
import ObjektyMapa.scale as scale
import ObjektyMapa.infObjekty as infObjekty
import random
import policko
import nastavenia
import mapa
from ObjektyMapa.enumSmerObjektu import EnumSmerObjektu 
import logging
#from ObjektyMapa.infObjekty import InfObj








class ObjMapa(pygame.sprite.Sprite):
    def __init__(self,policko,id,pixSurPolickoCenter,invVyuzitiePredmetov = None,suToSuradniceCenter = False):
        self.id = id
        self.invVyuzitiePredmetov = invVyuzitiePredmetov

        
        
        
        self.policka = [policko]
        self.initInf()
        if suToSuradniceCenter:
            centX = self.inf.rectObjOblastMapa.width / 2
            centY = self.inf.rectObjOblastMapa.height / 2
        else:
            centX = 0
            centY = 0
        
        self.pixSurMapa = (pixSurPolickoCenter[0]+policko.rectTextOblastMapa.x-centX,pixSurPolickoCenter[1]+policko.rectTextOblastMapa.y-centY)
        self.pixSurPolicko = [pixSurPolickoCenter[0]-centX,pixSurPolickoCenter[1]-centY]
        
        self.initTextOblast()
        self.topLeftScaleMap = [self.rectTextOblastMapa.x,self.rectTextOblastMapa.y]
        self.initSprite()
        self.initObjOblast()
        
    def initInf(self):
        self.inf = infObjekty.INF_OBJ_MAPA[self.id]
        if not isinstance(self.inf, infObjekty.InfObj):
            logging.warn("nepodarilo sa pomocou vlozeneho id ziskat inf ktore je instanciou InfObj")
        
    def dajKoeficienRychlosti(self):
        return self.inf.rychlostPrechodu
    
    def dajCasTazenia(self):
        return self.inf.dajCasTazenia()
        
    def vlozDo(self,grupa):  
        self.add(grupa)
        
    def initSprite(self):
        pygame.sprite.Sprite.__init__(self,self.policka[0].objMapaBlit,self.policka[0].mapa.hra.allSprites)#,self.policka[0].objMapaVlastne
        self.initImage()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.pixSurPolicko) #centruje na vlastne policko
        
    def initImage(self):
        self.image = self.inf.img
        
    def dajRectTextOblastMapa(self):
        return self.rectTextOblastMapa
        
    def dajInfRectObjOblastMapa(self): # aby som to mohol prepisat
        return self.inf.rectObjOblastMapa  
    
    def initObjOblast(self):
        self.rectObjOblastMapa = self.dajInfRectObjOblastMapa().copy()
        self.rectObjOblastMapa = self.rectObjOblastMapa.move(self.pixSurMapa)
        
    def dajRozmery(self):
        return self.inf.dajRozmery()
        
        
    def initTextOblast(self):
        rozmery = self.dajRozmery()
        self.rectTextOblastMapa = pygame.Rect(self.pixSurMapa[0],self.pixSurMapa[1],rozmery[0],rozmery[1])
        
    def akciaRightClick(self):
        met = self.inf.dajMetoduRightClick()
        if met != None:
            return met(self)
        return False # vrati false ak sa nic nevykona aby sa mohlo stavat
        
        
    def dajNasRychlosti(self):
        return self.inf.rychlostPrechodu
        
        
    def initStage2(self):
        pass
    
    def linkPolicko(self,policko):
        #self.policka.append(policko)
        self.add(policko.objMapaBlit)
        self.policka.append(policko)
        #self.add(policko.objektyMapaCudzie)
        


        
    def centrujDoRect(self,rect):
        self.rect = pygame.Rect(self.rectTextOblastMapa.x-rect.x,self.rectTextOblastMapa.y-rect.y,self.rect.width,self.rect.height)
        

    def dajObjOblastMapa(self):
        return self.rectObjOblastMapa
    def dajTextOblastMapa(self):
        return self.rectTextOblastMapa
    
    def kill(self, trebaPrekreslit = False):
        #self.inf.sprite.remove(self)
        pygame.sprite.Sprite.kill(self)
        for policko in self.policka:
            policko.initImg(trebaPrekreslit)

        
    def dajDrop(self,hrac):
        drop = self.inf.dajDrop()
        drop[0](drop[1],hrac)





#tento objek si neberie rect objektu (nie textury) z informacii o id objektu pretoze kazdy potrebuje mat vlastny
class ObjMapaVlastInf(ObjMapa):
    def __init__(self, policko, id, pixSurPolicko,inf,suToSurCent = False):
        self.inf = inf
        ObjMapa.__init__(self, policko, id, pixSurPolicko, suToSurCent)
        
    def initInf(self):
        pass
        
        
class ObjMapaVlastInfPozadie(ObjMapaVlastInf):
    def __init__(self, policko, id, pixSurPolicko,inf,pozadiePolicka,rectPoz=None,suToSurCent = False):
        if rectPoz == None:
            self.rectPozadia = [inf.img.get_rect()]
        else:
            self.rectPozadia = rectPoz
            
        self.pozadiePolicka = pozadiePolicka
        super().__init__(policko, id, pixSurPolicko, inf,suToSurCent)
        
    def initImage(self):
        img = self.inf.img
        self.image = pygame.Surface(img.get_size(),pygame.SRCALPHA)
        self.vykresliPozadie()
        self.image.blit(img,(0,0))
        
    def vykresliPozadie(self):
        pocRectPoz = len(self.rectPozadia)
        for i in range (pocRectPoz):
            self.image.blit(self.pozadiePolicka,(self.rectPozadia[i].x,self.rectPozadia[i].y),(self.pixSurPolicko[0],self.pixSurPolicko[1],self.rectPozadia[i].width,self.rectPozadia[i].height))
       

class ObjMapaAktivPrek(ObjMapa,scale.ObjScale):
    def __init__(self,policko,id,pixSurPolicko,invVyuzitiePredmetov, suToSurCent = False):
        super().__init__(policko,id,pixSurPolicko,invVyuzitiePredmetov,suToSurCent)
        #pygame.sprite.Sprite.add(self.inf.ulozSprite(self))
        #infObjekty.objMapaScalovanie.add(self)
        self.scale(mapa.SINGLETON_MAPA.dajNas())

        
    def initSprite(self):
        pygame.sprite.Sprite.__init__(self,self.inf.sprites,infObjekty.objMapaScalovanie,self.policka[0].mapa.hra.allSprites)#,self.policka[0].objMapaVlastne
        self.inf.aktualizujData()
        self.initImage()
        self.rect = self.image.get_rect()
        
    def initStage2(self):
        group = self.policka[0].mapa.hra.dajAktivBlitGroup()
        group.add(self,layer = self.rectObjOblastMapa.y)
        #self.layer = self.rectObjOblastMapa.y
        #pygame.sprite.Sprite.add(group)
        self.add(group)
        
    def updateImage(self):
        pass
        
    def kill(self,trebaPrekreslit = False):
        pygame.sprite.Sprite.kill(self)
        
    def newRefImg (self):
        self.image = self.inf.img
        
    def updateRectSize(self, nasobitel):
        pass
        
    
class ObjMapaAktivPrekViacImg (ObjMapaAktivPrek):
    def __init__(self,policko,id,pixSurPolicko,invVyuzitiePredmetov, suToSurCent = False):
        self.id = id
        self.initInf()
        self.smer = invVyuzitiePredmetov.dajCisloTextury()%len(self.inf.imgZaloha)
        self.prvotnySmer = self.smer
        super().__init__(policko, id, pixSurPolicko,invVyuzitiePredmetov, suToSurCent)
                 
    def dajRozmery(self):
        return self.inf.dajRozmery(self.smer)
    
    def dajInfRectObjOblastMapa(self): 
        return self.inf.rectObjOblastMapa[self.smer]
    
    def initObjOblast(self):
        self.rectObjOblastMapa = self.dajInfRectObjOblastMapa().copy()
        self.rectObjOblastMapa = self.rectObjOblastMapa.move(self.pixSurMapa)
        
    def initImage(self):
        self.image = self.inf.img[self.smer]

    def newRefImg (self):
        self.image = self.inf.img[self.smer]
        
            
        
        

        

        

        
    
    
    
    
    
 
        
        
        
        
        
        
    
    
    