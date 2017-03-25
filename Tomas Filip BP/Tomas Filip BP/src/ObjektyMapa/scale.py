'''
Created on 19. 2. 2017

@author: T.Filip
'''

import pygame

#abstraktna trieda ktorej ulohou je zabezpecit objektu moznost scalovania pri zmene zoomu v hre
class ObjScale:
    
    #metoda prisposobi texturu scalovaniu
    #je nutne aby trieda obsahovala zalohu textury
    def scale(self,nasobitel):
        #nasobitel je vzdy od zakladu 64x64 ????
        self.updateTopLeft(nasobitel)
        #zmena velkosti vykreslovaneho objektu
        self.updateRectSize(nasobitel)
        #prekreslenie obrazku zo zalohy
        self.updateImage()
        try:
            self.addUpdate()
        except:
            pass
     
    def addUpdate(self):
        raise NotImplemented
    
    def updateImage(self):
        self.image = pygame.transform.scale(self.imageZaloha,(self.rect.width, self.rect.height))
     
    def updateRectSize(self,nasobitel):
        self.rect.width = self.rectTextOblastMapa.width*nasobitel
        self.rect.height = self.rectTextOblastMapa.height*nasobitel
        
    def updateTopLeft(self,nasobitel):
        self.topLeftScaleMap[0] = self.rectTextOblastMapa.x*nasobitel
        self.topLeftScaleMap[1] = self.rectTextOblastMapa.y*nasobitel
                
    def updateScreenPosition (self, mapa): 
        mapa.updatniPoziciu(self.topLeftScaleMap,self.rect)
        
    def updateLayer(self):
        self.hra.dajAktivBlitGroup().change_layer(self,self.rectTextOblastMapa.y+30)
        
        
class ObjScaleViacTextur (ObjScale):
    
    def updateImage(self):
        self.image = pygame.transform.smoothscale(self.imageZaloha[self.smer],(self.rect.width, self.rect.height))    
        #print((self.rect.width, self.rect.height))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        