'''
Created on 18. 3. 2017

@author: T.Filip
'''
import pygame
from Predmety.enumTypAnimacie import EnumTypAnimacie
from Postavy.smerPostavy import SmerPostavy


class Animacia(pygame.sprite.Sprite):
    def __init__(self,hrac,mapa):
        self.hrac = hrac
        self.mapa = mapa
        self.image = None
        self.rect = None
        self.layer = 0
        self.aktivBlitGroup = self.hrac.dajHru().dajAktivBlitGroup()
        self.inf = None
        pygame.sprite.Sprite.__init__(self)
        self.beziAnimacia = False
        
        

        
        '''
        Pripravy sa na novu animaciu a hned ju zacne
        '''
    def reinit(self,inf):
        self.tickAnimacie = 0
        self.layer = self.hrac.dajLayer()
        self.inf = inf
        self.animacia = ZOZNAM_ANIMACII[inf.dajTypAnimacie()]
        self.update(inf)
        
        
    def zmenLayer(self,layer):
        self.aktivBlitGroup.change_layer(self,layer)
        
        
    def initSuradniceAnimacie(self):
        rect = self.hrac.dajRect()
        if self.smerPostavy == SmerPostavy.DOPREDU:
            self.poziciaAnim = [rect.centerx-5,rect.centery-2]
        if self.smerPostavy == SmerPostavy.DOZADU:
            self.poziciaAnim = [rect.centerx+5,rect.centery-5]
        if self.smerPostavy == SmerPostavy.DOPRAVA:
            self.poziciaAnim = [rect.centerx+10,rect.centery]
        if self.smerPostavy == SmerPostavy.DOLAVA:
            self.poziciaAnim = [rect.centerx-10,rect.centery]
        else:
            self.poziciaAnim = [rect.centerx,rect.centery]
        
        
    def update(self,inf):
        self.beziAnimacia = True
        self.smerPostavy = self.hrac.dajSmerPostavy()
        self.initSuradniceAnimacie()
        layerHraca = self.hrac.dajLayer()
        if self.inf != inf:
            self.reinit(inf)
            
        
        
        self.tickAnimacie += 1
        #self.animacia(self.inf,self.tickAnimacie,self,poz[0],poz[1],self.hrac.dajHru().dajMapu().dajScaleNas())
        self.animacia(self)
        
        self.aktivBlitGroup.add(self)
        if self.smerPostavy == SmerPostavy.DOZADU:
            if self.layer != layerHraca -10:
                self.zmenLayer(layerHraca - 10)
                self.layer = layerHraca-10
        else:
            if self.layer != layerHraca+1:
                self.zmenLayer(layerHraca+1)
                self.layer = layerHraca+1

    def dajInfPredmetu(self):
        return self.inf
    
    def dajTickAnimacie(self):
        return self.tickAnimacie
    
    def dajPoziciuAnimacie(self):
        return self.poziciaAnim
    
    def dajMapu(self):
        return self.mapa
    
    def dajSmerPostavy(self):
        return self.smerPostavy
    
    
    
        
    def setImg(self,img):
        self.image = img
        
    def setRect(self,rect):
        self.rect = rect
        
    def ukonciAnimaciu(self):
        if self.beziAnimacia:
            self.aktivBlitGroup.remove(self)
            self.beziAnimacia =False
            self.tickAnimacie = 0
            
            
            #(inf,tick,animacia,x,y,scale,smer):
        





'''
parameter inf musi but instancia InfObjektNastroj alebo musi obsahovat img pre animaciu
metoda vyuziva 1 img a vracia zrotovany img

'''
def rotacia360SAFE(inf,tick,animacia,x,y,scale,smer):

        
        
    uhol = tick % 45
    uhol = uhol*2
    uhol = 360 - uhol
    org = inf.dajImgAnimacie()
    siz = org.get_size()
    ret = pygame.Surface((siz[0]*2,siz[1]*2),pygame.SRCALPHA)
    ret.blit(org,(int(siz[0]/2),0))
    ret = pygame.transform.rotate(ret,uhol)
    roz = int(64*scale)
    ret = pygame.transform.scale(ret,(roz,roz))
    #najprv sa to prekresli do vhodne velkeho obrazka aby po rotovani nebolo nutne menit rect da sa optimalizovat ale takto jednoduchsie
    animacia.setImg(ret)
    topLeftX = x - siz[0]
    rect = pygame.Rect(x - ret.get_width()/2,y - ret.get_height()/2,ret.get_width(),ret.get_height())
    animacia.setRect(rect)
    
    
    
def rotacia360(animacia):
    smer = animacia.dajSmerPostavy()
    inf = animacia.dajInfPredmetu()
    tick = animacia.dajTickAnimacie()
    scale = animacia.dajMapu().dajScaleNas()
    pozicia = animacia.dajPoziciuAnimacie()
    
    uhol = tick % 60
    uhol = uhol*2
    
    
    img = inf.dajImgAnimacie()
    if smer == SmerPostavy.DOZADU or smer == SmerPostavy.DOLAVA:
        img = pygame.transform.flip(img,True,False)
        uhol = 360 + uhol
    else:
        uhol = 360 - uhol

    

    roz = int(64*scale*0.5)
    orgScale = pygame.transform.scale(img,(roz,roz))
    siz = orgScale.get_size()
    ret = pygame.Surface((siz[0]*2,siz[1]*2),pygame.SRCALPHA)
    ret.blit(orgScale,(int(siz[0]/2),0))
    ret = pygame.transform.rotate(ret,uhol)
    retRect = ret.get_rect()
    retRect.center = ret.get_rect().center
    #ret = ret.subsurface(retRect).copy()
    
    #ret = pygame.transform.scale(ret,(roz,roz))
    animacia.setImg(ret)
    topLeftX = pozicia[0] - siz[0]
    rect = pygame.Rect(pozicia[0] - ret.get_width()/2,pozicia[1] - ret.get_height()/2,ret.get_width(),ret.get_height())
    animacia.setRect(rect)
    
    
    
def opacnaSkakavaRotacia(inf,tick,animacia,x,y,scale):
    uhol = tick % 360
    uhol = 360 - uhol
    roz = 64*scale
    org = inf.dajImgAnimacie()
    orgScale = pygame.transform.scale(org,(roz[0],roz[1]))
    siz = orgScale.get_size()
    ret = pygame.Surface((siz[0]*2,siz[1]*2),pygame.SRCALPHA)
    ret.blit(orgScale,(int(siz[0]/2),siz[1]))
    ret = pygame.transform.rotate(ret,uhol)
    
    #ret = pygame.transform.scale(ret,(roz,roz))
    #najprv sa to prekresli do vhodne velkeho obrazka aby po rotovani nebolo nutne menit rect da sa optimalizovat ale takto jednoduchsie
    animacia.setImg(ret)
    topLeftX = x - siz[0]
    rect = pygame.Rect(x - ret.get_width()/2,y - ret.get_height()/2,ret.get_width(),ret.get_height())
    animacia.setRect(rect)
    
    
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
    

#key: enum value: metoda vytvarania animacie
ZOZNAM_ANIMACII = {}

ZOZNAM_ANIMACII[EnumTypAnimacie.ROTACIA360] = rotacia360


        
