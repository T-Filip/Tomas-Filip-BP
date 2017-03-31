'''
Created on 4. 3. 2017

@author: T.Filip
'''
import pygame
import logging
import nastavenia
#import manazerOkien
from Textury import textury


class MenuOkno():
    def __init__(self,manazerOkien,scale, rect = None):
        if rect == None:
            self.rect = pygame.Rect(0,0,nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie],nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie])
        else:
            self.rect = rect
        print ("menuOkno rect:")
        print (self.rect)
        self.initPozadie()
        self.manazerOkien = manazerOkien
        self.scaleRes =scale
        self.allSprites = pygame.sprite.RenderUpdates()

        
    def prepniMenu(self,menoMenu):
        self.manazerOkien.prepniMenu(menoMenu)
        
    def dajGroup(self):
        return self.allSprites
        
    def initPozadie(self):
        self.pozadie = pygame.transform.scale(textury.MENU_OKNO,(self.rect.width,self.rect.height))
       
       
    '''
    zmenRecept sa vola vzdy po zmiznuti okna v hre (nie v menu)
    ''' 
    def close(self):
        pass
        
        
    def updateClickLeft(self):
        pos = pygame.mouse.get_pos()
        sprites_pod_myskou = [s for s in self.allSprites if s.rect.collidepoint(pos)]
        self.volajMetodu(sprites_pod_myskou, "mouseClicked")
        
    def updateClickRight(self):
        pass
        
    def updateHover(self):
        pos = pygame.mouse.get_pos()
        sprites_pod_myskou = [s for s in self.allSprites if s.rect.collidepoint(pos)]
        self.volajMetodu(sprites_pod_myskou,"mouseOnSprite")
       
    def volajMetodu (self,objekty,zmenRecept):
        if len(objekty) < 1:
            return
            
        met = getattr(objekty[0],zmenRecept)
        for sp in objekty:
            met();
    
    def update(self):
        #self.updateMouse()
        self.allSprites.update()
        self.updateHover()
        
    def klikolNaOkno(self, pos):
        return self.rect.collidepoint(pos)
        
    def vykresliNadpis(self,screen,text):
        font = textury.dajFont(int(30*self.scaleRes)) 
        text = text                               
        textSurf = font.render(text,1, nastavenia.BLACK)
        x = self.rect.x + (self.rect.width - textSurf.get_width())/2
        y = self.rect.y + 30
        screen.blit(textSurf,(x,y))
        
    def drawPozadie(self,screen):
        screen.blit(self.pozadie,(self.rect.x,self.rect.y))
            
    '''
    def draw(self,screen):
        self.drawPozadie(screen)
        self.allSprites.draw(screen)
    '''
    def draw(self,screen):
        self.drawPozadie(screen)
        self.allSprites.draw(screen)
        
        
    def refresh(self):
        pass
        
        
        
class MenuOknoHra(MenuOkno):
    def __init__(self,manazerOkien, scale, sirka = 0.5, vyska = 0.5):
        self.nastalReinit = False
        x = nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]
        y = nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]
        self.sirkaPodiel = sirka
        self.vyskaPodiel = vyska
         #tlacidla maju vlastne scalovania preto nie je vhodne scalovat ich poziciu 
         #tieto atributy predstavuju pozicu pri rozliseni 1280/720 
        self.topLeftXPredScale = int((1280 - (self.sirkaPodiel*1280))/2)
        self.topLeftYPredScale = int((720 - (self.sirkaPodiel*720))/2)
        sirkaOkna = sirka*x
        vyskaOkna = vyska*y
        topLeftX = int((x - sirkaOkna)/2)
        topLeftY = int((y - vyskaOkna)/2)
        rect = pygame.Rect(topLeftX, topLeftY, sirkaOkna, vyskaOkna )
        super().__init__(manazerOkien, scale, rect)
        
    def reinit(self,hrac):
        self.hrac = hrac
        self.nastalReinit = True
        
    def draw(self, screen):
        if self.nastalReinit:
            MenuOkno.draw(self, screen)
        

        
        
        
    
        
        