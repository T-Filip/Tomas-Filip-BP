'''
Created on 9. 2. 2017

@author: T.Filip
'''
import pygame
import nastavenia
import texturyPolicka
import random
import ObjektyMapa.objMapa as objMapa
import ObjektyMapa.scale as scale
import ObjektyMapa.celoPolObj as celoPolObj



def collideTextOblastMapa(sprite1, sprite2):
    return sprite1.dajTextOblastMapa().colliderect(sprite2.dajTextOblastMapa())

def collideObjOblastMapa(sprite1,sprite2):

    return sprite1.dajObjOblastMapa().colliderect(sprite2.dajObjOblastMapa())


class Policko(pygame.sprite.Sprite,scale.ObjScale):
    def __init__(self,mapa,sur,noise,biom):
        
        self.noise = noise
        self.biom = biom
        self.suradnice = sur
        self.mapa = mapa
        self.jeStage2 = False
        
        
        self.celPolObj = None
        self.objMapaBlit = pygame.sprite.LayeredUpdates()
        self.objektyMapaCudzie = pygame.sprite.Group()
        self.objMapaVlastne = pygame.sprite.Group()#vsetky objekty ktore patria tomuto policku ... aj celopolickove? 
        
        

        

        self.objektyMapaPrekryvajuce = pygame.sprite.Group()#grupa pre objekty ktore sa budu vykreslovat samostatne tak ayb za ne hrac mohol zajst
        
        self.rectTextOblastMapa = pygame.Rect(self.suradnice[0]*64,self.suradnice[1] * 64,64,64)
        self.vytvorObjMapa()
        
        
    def dajTextOblastMapa(self):
        return self.rectTextOblastMapa
        
    def vytvorObjMapa(self):
        #predcasne vytvori vsetky objekty na mape - potom sa budu preriedovat ak sa budu prelinat
        #print("Policko vytvorObjMapa() - doimplementovat")
        rand = random.Random(self.noise)
        r = rand.randint(0, 99)
        
        #dddddd
        
        
        
        if self.noise < 0.5:
            self.celPolObj = celoPolObj.CeloPolObjPoz(self,200) 
            return

        #a = self.suradnice
        #if a[0] == 22 and a[1]== -27:
            #self.celPolObj = celoPolObj.CeloPolObjPoz(self,19)

        else:
            r = rand.randint(0, 99)
            if r < 6:
                objMapa.ObjMapaAktivPrek(self,0,(-20,20))
            elif r < 10:
                objMapa.ObjMapaAktivPrek(self,100,(-20,20))
            #nemozno vytvorit celo pol uz v stage 1 ved nemame okolie
            # najprv rozhodnut ci tam nejake ma byt alebo nie a az tak ho vytvorit
            
        
            
        #!!! pri kazdom novom objekte cekovat ci sa nepretoto
        # najprv vygenerovat celopolickove dristy
        r = rand.randint(0, 99)
        #if r < 10:
            #objMapa.ObjMapaAktivPrek(self,0,(-20,20))
        #elif r < 15:
            #objMapa.ObjMapaAktivPrek(self,18,(-20,20))
            
            #objMapa.ObjMapa(self,0,(-20,20))
        
    def dajIdCeloPol(self):
        if self.celPolObj != None:
            return self.celPolObj.dajId()
        else:
            return -1
        
        
    def preriedObjMapa(self):
        #print("Policko preriedObjMapa() - doimplementovat")
        
        if self.suradnice[0]==0 and self.suradnice[1]==-20:
            i=1
        
        
        for policko in self.okolie:
            if self.noise > policko.noise:
                continue # ma prioritu nemusi sa nicoho vzdat

            #nasledne odstranujeme vsetky policka ktore zasahuju do inych pretoze mensia priorita            
            pygame.sprite.groupcollide(self.objMapaVlastne, policko.objMapaVlastne, True, False, collideObjOblastMapa)
                
    
    def polinkujObjekty(self):
        
        for policko in self.okolie:
            p1 = pygame.sprite.spritecollide(self, policko.objMapaBlit, False, collideTextOblastMapa)
            p2 = pygame.sprite.spritecollide(self, policko.objektyMapaPrekryvajuce, False, collideTextOblastMapa)
            
            for obj in p1:
                obj.linkPolicko(self)
            for obj in p2:
                obj.linkPolicko(self)
    
    def initStage2 (self):
        if not self.jeStage2:
            self.jeStage2 = True
            a = self.suradnice
            if a[0] == 27 and a[1]== -29:
                i =5
            
            
            self.okolie = self.mapa.dajOkolie(self.suradnice)
            self.preriedObjMapa()
            self.polinkujObjekty()
            self.initImg()
            pygame.sprite.Sprite.__init__(self,self.mapa.hra.polickaSprites)
            
            self.rect = self.image.get_rect()
            #self.rectTextOblastMapa = self.image.get_rect()
            
            #self.rectTextOblastMapa.x = self.suradnice[0]*64
            #self.rectTextOblastMapa.y = self.suradnice[1] * 64
            
            self.topLeftScaleMap = [self.rectTextOblastMapa.x,self.rectTextOblastMapa.y]
            
            
            for policko in self.objMapaVlastne:
                try:
                    policko.initStage2()
                except:
                    pass
            
            
            
            self.scale(self.mapa.scaleNasobitel)

    def initImg(self):
        self.imageZaloha = pygame.Surface((64,64))
        self.imageZaloha.blit(texturyPolicka.POLICKO_TRAVA[self.biom],(0,0))
        #self.imageZaloha = texturyPolicka.POLICKO_TRAVA[self.biom]
        
        
        if self.celPolObj != None:
            self.celPolObj.stage2(self.okolie)
        for obj in self.objMapaBlit:
            obj.centrujDoRect(self.rectTextOblastMapa)
        self.objMapaBlit.draw(self.imageZaloha)
        self.image = self.imageZaloha
       

    def addUpdate(self):
        if nastavenia.DEBUG:
            #aalines nechce krelit na kraje surface preto takto
            pygame.draw.line(self.image,nastavenia.RED,(0,0),(0,63))
            pygame.draw.line(self.image,nastavenia.RED,(0,0),(63,0))
            pygame.draw.line(self.image,nastavenia.RED,(63,0),(63,63))
            pygame.draw.line(self.image,nastavenia.RED,(0,63),(63,63))
            font = nastavenia.FONT_28_DAYS_LATER_10
            #font = pygame.font.SysFont("monospace", 13)
            textSuradnice = str(self.suradnice[0]) + " " + str(self.suradnice[1])
            if self.celPolObj != None:
                textSuradnice += " A"
            
            textSurf = font.render(textSuradnice, 1, (255,255,50))
            self.image.blit(textSurf, (2, 2))


    def update(self, *args):  
        i=1
        
    def updatePozicie(self,mapa):
        mapa.updatniPoziciu(self.topLeftScaleMap,self.rect)
        
    def uloz(self):
        if self.jeStage2:
            self.kill()
        for obj in self.objMapaVlastne:
            obj.kill()
            
        
        # treba dorobit 
        # ulozi resp urobi co treba pred tym ako sa tato instancia vymaze 
