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
from ObjektyMapa.infObjekty import InfObj








class ObjMapa(pygame.sprite.Sprite):
    def __init__(self,policko,id,pixSurPolicko):
        self.id = id
        
        
        
        self.policka = [policko]
        self.initInf()
        self.pixSurMapa = (pixSurPolicko[0]+policko.rectTextOblastMapa.x,pixSurPolicko[1]+policko.rectTextOblastMapa.y)
        self.pixSurPolicko = pixSurPolicko
        
        self.initTextOblast()
        self.topLeftScaleMap = [self.rectTextOblastMapa.x,self.rectTextOblastMapa.y]
        self.initSprite()
        self.initObjOblast()
        
    def initInf(self):
        self.inf = infObjekty.INF_OBJ_MAPA[self.id]
        if not isinstance(self.inf, infObjekty.InfObj):
            i = 5
        
        
    def vlozDo(self,grupa):  
        self.add(grupa)
        
    def initSprite(self):
        pygame.sprite.Sprite.__init__(self,self.policka[0].objMapaBlit,self.policka[0].objMapaVlastne)
        self.initImage()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.pixSurPolicko) #centruje na vlastne policko
        
    def initImage(self):
        self.image = self.inf.img
        
        
    def dajRectObjOblastMapa(self): # aby som to mohol prepisat
        return self.inf.rectObjOblastMapa  
    
    def initObjOblast(self):
        self.rectObjOblastMapa = self.dajRectObjOblastMapa().copy()
        self.rectObjOblastMapa = self.rectObjOblastMapa.move(self.pixSurMapa)
        
        
    def initTextOblast(self):
        self.rectTextOblastMapa = pygame.Rect(self.pixSurMapa[0],self.pixSurMapa[1],self.inf.img.get_width(),self.inf.img.get_height())
        
        
    def dajNasRychlosti(self):
        return self.inf.rychlostPrechodu
        
        
    def initStage2(self):
        raise NotImplemented
    
    def linkPolicko(self,policko):
        self.policka.append(policko)
        self.add(policko.objMapaBlit)
        self.add(policko.objektyMapaCudzie)
        


        
    def centrujDoRect(self,rect):
        self.rect = pygame.Rect(self.rectTextOblastMapa.x-rect.x,self.rectTextOblastMapa.y-rect.y,self.rect.width,self.rect.height)
        

    def dajObjOblastMapa(self):
        return self.rectObjOblastMapa
    def dajTextOblastMapa(self):
        return self.rectTextOblastMapa
    
    def kill(self):
        #self.inf.sprite.remove(self)
        pygame.sprite.Sprite.kill(self)





#tento objek si neberie rect objektu (nie textury) z informacii o id objektu pretoze kazdy potrebuje mat vlastny
class ObjMapaVlastInf(ObjMapa):
    def __init__(self, policko, id, pixSurPolicko,inf):
        self.inf = inf
        ObjMapa.__init__(self, policko, id, pixSurPolicko)
        
    def initInf(self):
        pass
        
        
class ObjMapaVlastInfPozadie(ObjMapaVlastInf):
    def __init__(self, policko, id, pixSurPolicko,inf,pozadiePolicka,rectPoz=None):
        if rectPoz == None:
            self.rectPozadia = [inf.img.get_rect()]
        else:
            self.rectPozadia = rectPoz
            
        self.pozadiePolicka = pozadiePolicka
        super().__init__(policko, id, pixSurPolicko, inf)
        
    def initImage(self):
        img = self.inf.img
        self.image = pygame.Surface(img.get_size(),pygame.SRCALPHA)
        self.vykresliPozadie()
        self.image.blit(img,(0,0))
        
    def vykresliPozadie(self):
        pocRectPoz = len(self.rectPozadia)
        for i in range (pocRectPoz):
            self.image.blit(self.pozadiePolicka,(self.rectPozadia[i].x,self.rectPozadia[i].y),(self.pixSurPolicko[0],self.pixSurPolicko[1],self.rectPozadia[i].width,self.rectPozadia[i].height))
       

        
    
        
        
        
    
    
#vykresluje sa aktivne v kazdom frame aby za to hrac mohol "zajst"
class ObjMapaAktivPrek(ObjMapa,scale.ObjScale):
    def __init__(self,policko,id,pixSurPolicko):
        super().__init__(policko,id,pixSurPolicko)
        #pygame.sprite.Sprite.add(self.inf.ulozSprite(self))
        #infObjekty.objMapaScalovanie.add(self)
        self.scale(mapa.SINGLETON_MAPA.dajNas())

        
    def initSprite(self):
        pygame.sprite.Sprite.__init__(self,self.policka[0].objMapaVlastne,self.inf.sprites,infObjekty.objMapaScalovanie)
        self.inf.aktualizujData()
        self.image = self.inf.img
        self.rect = self.image.get_rect()
        
    def initStage2(self):
        group = self.policka[0].mapa.hra.dajAktivBlitGroup()
        group.add(self,layer = self.rectObjOblastMapa.y)
        pygame.sprite.Sprite.add(group)
        
    def updateImage(self):
        pass
        
    def kill(self):

        ObjMapa.kill(self)
        
    def newRefImg (self):
        self.image = self.inf.img
        
    def updateRectSize(self, nasobitel):
        pass

        

        

        
    
    
    
    
    
 
        
        
        
        
        
        
    
    
    