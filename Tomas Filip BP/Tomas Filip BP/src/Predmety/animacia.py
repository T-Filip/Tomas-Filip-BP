'''
Created on 18. 3. 2017

@author: T.Filip
'''
import pygame
from Predmety.enumTypAnimacie import EnumTypAnimacie
from Postavy.smerPostavy import SmerPostavy


class Animacia(pygame.sprite.Sprite):
    def __init__(self,hrac):
        self.hrac = hrac
        self.image = None
        self.rect = None
        self.layer = 0
        self.aktivBlitGroup = self.hrac.dajHru().dajAktivBlitGroup()
        self.inf = None
        pygame.sprite.Sprite.__init__(self)
        
        

        
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
        
    def update(self,inf):
        poz = self.hrac.dajSuradnicePreAnimaciu()
        smerPostavy = self.hrac.dajSmerPostavy()
        layerHraca = self.hrac.dajLayer()
        if self.inf != inf:
            self.reinit(inf)
            
        
        
        self.tickAnimacie += 1
        self.animacia(self.inf,self.tickAnimacie,self,poz[0],poz[1],self.hrac.dajHru().dajMapu().dajScaleNas())
        
        self.aktivBlitGroup.add(self)
        if smerPostavy == smerPostavy.DOZADU:
            if self.layer != layerHraca -10:
                self.zmenLayer(layerHraca - 10)
                self.layer = layerHraca-10
        else:
            if self.layer != layerHraca+1:
                self.zmenLayer(layerHraca+1)
                self.layer = layerHraca+1

        
        
    def setImg(self,img):
        self.image = img
        
    def setRect(self,rect):
        self.rect = rect
        
    def ukonciAnimaciu(self):
        self.aktivBlitGroup.remove(self)
        





'''
parameter inf musi but instancia InfObjektNastroj alebo musi obsahovat img pre animaciu
metoda vyuziva 1 img a vracia zrotovany img

'''
def rotacia360(inf,tick,animacia,x,y,scale):
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
    
    
    
def opacnaSkakavaRotacia(inf,tick,animacia,x,y,scale):
    uhol = tick % 360
    uhol = 360 - uhol
    org = inf.dajImgAnimacie()
    siz = org.get_size()
    ret = pygame.Surface((siz[0]*2,siz[1]*2),pygame.SRCALPHA)
    ret.blit(org,(int(siz[0]/2),siz[1]))
    ret = pygame.transform.rotate(ret,uhol)
    roz = 64*scale
    ret = pygame.transform.scale(ret,(roz,roz))
    #najprv sa to prekresli do vhodne velkeho obrazka aby po rotovani nebolo nutne menit rect da sa optimalizovat ale takto jednoduchsie
    animacia.setImg(ret)
    topLeftX = x - siz[0]
    rect = pygame.Rect(x - ret.get_width()/2,y - ret.get_height()/2,ret.get_width(),ret.get_height())
    animacia.setRect(rect)
    

#key: enum value: metoda vytvarania animacie
ZOZNAM_ANIMACII = {}

ZOZNAM_ANIMACII[EnumTypAnimacie.ROTACIA360] = rotacia360


        
