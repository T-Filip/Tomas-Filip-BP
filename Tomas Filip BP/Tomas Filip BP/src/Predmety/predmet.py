'''
Created on 9. 3. 2017

@author: T.Filip
'''

import pygame
import ObjektyMapa.infObjekty as infObjekty
import textury
import nastavenia
from _operator import pos

class Predmet (pygame.sprite.Sprite):
    def __init__(self,id,pocetKusov = 1):
        self.inf = infObjekty.INF_OBJ_MAPA[id]
        self.id = id
        self.miestoPrePredmet = None
        #self.miestoPrePredmet = miesto
        #self.miestoPrePredmet.predmet = self

        
        

        #self.rect = pygame.Rect((64,64))
        #self.image = self.inf.dajImgPredm()
        self.pocetKusov = pocetKusov
        pygame.sprite.Sprite.__init__(self)
        
    def setPocetKusov(self, ks, maPrekreslit = True):
        self.pocetKusov = ks
        if maPrekreslit:
            self.aktualizujGrafiku()
        
        
    def zmenPocetKusovO(self,ks):
        self.pocetKusov += ks
        kolkoZobralo = ks
        if self.pocetKusov <= 0:
            self.kill()
            self.miestoPrePredmet.vymazPredmet()
            return kolkoZobralo - self.pocetKusov
        elif self.pocetKusov > self.inf.stackKapacita:
            kolkoZobralo -= self.pocetKusov - self.inf.stackKapacita
            self.pocetKusov = self.inf.stackKapacita
        self.aktualizujGrafiku()
        return kolkoZobralo
           
    def dajId(self):
        return self.id
            
    def dajPocetKusov(self):
        return self.pocetKusov
    

        

    def dajStackKapacitu(self):
        return self.inf.dajStackKapacitu()
    
    def vlozDoGroup(self,group):#treba mi to?
        self.kill()
        self.add(group)
        
    def vlozDoMiesta(self,miesto):
        miesto.vlozPredmet(self)
        
    def zlucPredmety (self,pred):
        kolkoZobralo = self.zmenPocetKusovO(pred.dajPocetKusov())
        pred.zmenPocetKusovO(-kolkoZobralo)

        
    def aktualizujGrafiku(self):
        self.aktualizujPoziciu()
        pom = self.inf.dajImgPredm().copy()
        textSurf = textury.dajFont(int(self.rect.width/3.5)).render(str(self.pocetKusov),1, nastavenia.BLACK)
        textX = self.rect.width-textSurf.get_width()-2
        textY = self.rect.height-textSurf.get_height()-1
        self.image = pygame.transform.scale(pom,(self.rect.width,self.rect.height))
        self.image.blit(textSurf,(textX,textY))
        
    def aktualizujPoziciu(self):
        self.rect = self.miestoPrePredmet.dajRectPrePredmet()
        
        
    '''
    metoda vyuzivana ak pedmet nie je v groupe .. hlavne ak hrac "drzi" predmet v myske
    '''
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        
        
        
class MiestoPrePredmet:
    def __init__(self,groupa):
        self.grupaPrePredmety = groupa # predmety sa vykresluju aj ked toto miesto nie 
        self.predmet = None
        
        
    def vlozPredmet(self,pred):
        pred.kill()
        self.predmet = pred
        if pred.miestoPrePredmet != None:
            pred.miestoPrePredmet.predmet = None
        self.predmet.miestoPrePredmet = self
        self.predmet.aktualizujGrafiku()
        self.vlozDoGroup()

        
    def vydajPredmet(self):
        self.predmet.miestoPrePredmet = None
        return self.predmet
        
    def vlozDoGroup(self):
        self.predmet.vlozDoGroup(self.grupaPrePredmety)#ked tam uz je nic sa nestane

    def vymazPredmet(self):
        self.predmet = None
        
    def update(self):
        pass
    
    def dajRectPrePredmet(self):
        pass
    
    
    
class MiestoPrePredmetMyska(MiestoPrePredmet):
    def __init__(self):
        MiestoPrePredmet.__init__(self,None)
        self.posunX = 0
        self.posunY = 0
        self.mousePos = (100,100)
        self.velkostStrany = 64
        self.posMys = (0,0)
        self.groupPredmet = pygame.sprite.RenderPlain()#lebo musi byt v grupe aby sa dobre kreslilo
        
    def update(self, posMys):
        self.posMys = posMys
        
    def vlozPredmet(self, pred,posunX,posunY,velkostSt):
        self.posunX = posunX
        self.posunY = posunY
        self.velkostStrany = velkostSt
        self.groupPredmet.empty()
        MiestoPrePredmet.vlozPredmet(self, pred)

        
    def vymazPredmet(self):
        MiestoPrePredmet.vymazPredmet(self)
        self.groupPredmet.empty()

        
        
        
    def initMousePosition(self,pos):
        self.mousePos = pos
        
        '''
    def reinit(self,x,y, velkostStrany):
        self.posunX = x
        self.posunY = y
        self.velkostStrany = velkostStrany
        '''
        
    def dajRectPrePredmet(self):
        pos = pygame.mouse.get_pos()
        return pygame.Rect(pos[0]-self.posunX,pos[1]-self.posunY,self.velkostStrany,self.velkostStrany)
        
    def vlozDoGroup(self):
        self.groupPredmet.add(self.predmet)

        
class MiestoPredmetu (pygame.sprite.Sprite,MiestoPrePredmet):
    def __init__(self,group,inventar):
        self.inventar = inventar
        self.rect = pygame.Rect(0,0,64,64)
        pygame.sprite.Sprite.__init__(self,group)
        MiestoPrePredmet.__init__(self,self.inventar.predmety)
        
    def reinit(self,x,y, velkostStrany):
        self.rect = pygame.Rect(x,y,velkostStrany,velkostStrany)
        self.image = pygame.transform.scale(textury.MIESTO_PREDMET,(velkostStrany,velkostStrany)) # vracia novy surf - mozne vylepsit
        
        
    def dajRectPrePredmet(self):
        return self.rect


        