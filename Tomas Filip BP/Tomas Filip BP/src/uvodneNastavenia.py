# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import pygame
import nastavenia
import sys
import os
from enum import Enum
from nastavenia import UVODNE_NASTAVENIA_VYSKA
#os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

class LastUpdate(Enum):
    UPDATE = 1
    HOVER = 2
    CLICK = 3
        


def ukonci(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        
def zvysRozlisenie(self):
    nastavenia.vybrateRozlisenie += 1;
    if nastavenia.vybrateRozlisenie > len(nastavenia.ROZLISENIA_X) - 1:
        nastavenia.vybrateRozlisenie -= len(nastavenia.ROZLISENIA_X)
    zmenTextRozlisenia(self.menu.tlacidloRozlisenie)


def znizRozlisenie(self):
    nastavenia.vybrateRozlisenie -= 1;
    if nastavenia.vybrateRozlisenie < 0:
        nastavenia.vybrateRozlisenie += len(nastavenia.ROZLISENIA_X)
    zmenTextRozlisenia(self.menu.tlacidloRozlisenie)
    
   
        
def zmenTextRozlisenia(self):
        self.text = str(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie])+ 'x' + str(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie])
        self.updateText()
        self.prekresli()
        
def krizikNeguj(self):
    self.variable[0] = not self.variable[0]

def krizikNegujKrizik(self):
    self.uvodneNastavenia.krizikFullScreen[0] = not self.uvodneNastavenia.krizikFullScreen[0]
    
def zmenTextFullScreen(self):
    if nastavenia.windowIndex == 0:
        nastavenia.windowIndex = 1
        self.text = nastavenia.WINDOW[1]
        self.menu.tlacidloBorder.setLock(False)
        #self.menu.tlacidloBorder.nastalaZmena()
    else:   
        nastavenia.windowIndex = 0
        self.text = nastavenia.WINDOW[0]
        self.menu.tlacidloBorder.setLock(True)
        #self.menu.tlacidloBorder.nastalaZmena()
        
    
    self.updateText()
    self.prekresli()
    
def zmenTextBorder(self):
    if nastavenia.borderIndex == 0:
        nastavenia.borderIndex = 1
        self.text = nastavenia.BORDER[1]
    else:   
        nastavenia.borderIndex = 0
        self.text = nastavenia.BORDER[0]
        
    self.updateText()
    self.prekresli()

    
def ukonciUvodneNastavenia(self):
    self.menu.jeNeukonceny = False;
    
def tlacidloStart(self):
    self.menu.jeNeukonceny = False;



class UvodneNastavenia:
    
    
    def __init__ (self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        
        #for mode in pygame.display.list_modes():
        #    print(mode)
        
        nastavenia.FONT_28_DAYS_LATER = pygame.font.Font("font\\28DaysLater.ttf",18)
        self.screen = pygame.display.set_mode((nastavenia.UVODNE_NASTAVENIA_SIRKA,nastavenia.UVODNE_NASTAVENIA_VYSKA ),pygame.NOFRAME)
       
        pygame.display.set_caption(nastavenia.UVODNE_NASTAVENIA_TITLE)
        self.clock = pygame.time.Clock()
        self.tlacidla_sprites = pygame.sprite.LayeredUpdates()
        
        self.uvodNastaveniaOkno = pygame.image.load('img\\uvodneNastavenia\\uvodNastaveniaOkno.png').convert_alpha()
        
        self.TUN1center = pygame.image.load('img\\uvodneNastavenia\\TUN1center.png').convert_alpha()
        self.TUN1left = pygame.image.load('img\\uvodneNastavenia\\TUN1left.png').convert_alpha()
        self.TUN1leftOznacene = pygame.image.load('img\\uvodneNastavenia\\TUN1leftOznacene.png').convert_alpha()
        self.TUN2 = pygame.image.load('img\\uvodneNastavenia\\TUN2.png').convert_alpha()
        self.TUN2Oznacene = pygame.image.load('img\\uvodneNastavenia\\TUN2Oznacene.png').convert_alpha()
        self.TUN3 = pygame.image.load('img\\uvodneNastavenia\\TUN3.png').convert_alpha()
        self.TUN3Krizik = pygame.image.load('img\\uvodneNastavenia\\TUN3Krizik.png').convert_alpha()
        self.TUN2Oznacene2 = pygame.image.load('img\\uvodneNastavenia\\TUN2Oznacene2.png').convert_alpha()
        #self.TUN1right = pygame.image.load('img\\uvodneNastavenia\\TUN1right.png').convert_alpha()
        #self.TUN1rightOznacene = pygame.image.load('img\\uvodneNastavenia\\TUN1rightOznacene.png').convert_alpha()
        self.TUN1right = pygame.transform.flip(self.TUN1left,True,False)
        self.TUN1rightOznacene = pygame.transform.flip(self.TUN1leftOznacene,True,False)
        
        '''
        #tlacidlo1 = TlacidloUNRozlisenie(self, 85, 260)
        self.tlacidloRozlisenie = TUNVseobecne(self,self.TUN1center,"",nastavenia.FONT_28_DAYS_LATER,zmenTextRozlisenia,140, 270, None)
        self.tlacidloRozlisenie.clickMethod(self.tlacidloRozlisenie)
        TUNVseobecne(self,self.TUN1left,"",nastavenia.FONT_28_DAYS_LATER,znizRozlisenie,85, 270, self.TUN1leftOznacene)
        TUNVseobecne(self,self.TUN1right,"",nastavenia.FONT_28_DAYS_LATER,zvysRozlisenie,275, 270, self.TUN1rightOznacene)
        TUNVseobecne(self,self.TUN2,"CLOSE",nastavenia.FONT_28_DAYS_LATER,ukonci,215, 320, self.TUN2Oznacene)
        TUNVseobecne(self,self.TUN2,"START",nastavenia.FONT_28_DAYS_LATER,ukonci,85, 320, self.TUN2Oznacene)
        TUNVseobecne(self,self.TUN2,"Full screen",nastavenia.FONT_28_DAYS_LATER,krizikNegujKrizik,85, 220, self.TUN2Oznacene,160,40)
        self.krizikFullScreen = [False,True]
        TUNVKrizik(self,self.TUN3,"",nastavenia.FONT_28_DAYS_LATER,krizikNeguj,275, 220,self.krizikFullScreen ,self.TUN3Krizik)
        '''
        Tlacidlo(self,[self.TUN2,self.TUN2Oznacene],"Testujeme",nastavenia.FONT_28_DAYS_LATER,50,50)
        TlacidloClickMethod(self,[self.TUN2,self.TUN2Oznacene],"CLOSE",nastavenia.FONT_28_DAYS_LATER,215,320,ukonci)
        TlacidloClickMethod(self,[self.TUN2,self.TUN2Oznacene],"START",nastavenia.FONT_28_DAYS_LATER,85,320,tlacidloStart)
        self.tlacidloRozlisenie = TlacidloClickMethod(self,[self.TUN1center],"",nastavenia.FONT_28_DAYS_LATER,140,270,zmenTextRozlisenia)
        self.tlacidloRozlisenie.click()
        TlacidloClickMethod(self,[self.TUN1left,self.TUN1leftOznacene],"",nastavenia.FONT_28_DAYS_LATER,85,270,znizRozlisenie)
        TlacidloClickMethod(self,[self.TUN1right,self.TUN1rightOznacene],"",nastavenia.FONT_28_DAYS_LATER,275,270,zvysRozlisenie)
        tlacidloWindow = TlacidloClickMethod(self,[self.TUN2,self.TUN2Oznacene],"",nastavenia.FONT_28_DAYS_LATER,85,220,zmenTextFullScreen)
        tlacidloWindow.text = nastavenia.WINDOW[nastavenia.windowIndex]
        tlacidloWindow.updateText()
        tlacidloWindow.prekresli()
        self.tlacidloBorder = TlacidloClickMethod(self,[self.TUN2,self.TUN2Oznacene,self.TUN2Oznacene2],"",nastavenia.FONT_28_DAYS_LATER,215,220,zmenTextBorder)
        self.tlacidloBorder.text = nastavenia.BORDER[nastavenia.borderIndex]
        if nastavenia.windowIndex == 0:
            self.tlacidloBorder.setLock(True)
            #self.tlacidloBorder.nastalaZmena()
        self.tlacidloBorder.updateText()
        self.tlacidloBorder.prekresli()
        
    def run(self):
        #cyklus pre nacitavacie menu
        self.jeNeukonceny = True
        
        
        
        while self.jeNeukonceny:
            self.clock.tick(20)
            
            self.keysPressed = pygame.key.get_pressed()
            self.events = pygame.event.get()

            pos = pygame.mouse.get_pos()
            sprites_pod_myskou = [s for s in self.tlacidla_sprites if s.rect.collidepoint(pos)]
            self.volajMetodu(sprites_pod_myskou,"mouseOnSprite")

            for ev in self.events:
                if ev.type == pygame.QUIT:
                    ukonci()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.volajMetodu(sprites_pod_myskou, "mouseClicked")
    

                
            
            self.tlacidla_sprites.update()
            
            self.draw()
            
        pygame.display.quit()
        pygame.quit()


    def draw(self):
        self.screen.blit(self.uvodNastaveniaOkno, (0,0))
        self.tlacidla_sprites.draw(self.screen)
        pygame.display.flip()
        
    def volajMetodu (self,objekty,metoda):
        if len(objekty) < 1:
            return
            
        met = getattr(objekty[0],metoda)
        for sp in objekty:
            met();
        
    
      
    
    





class TUNVseobecne(pygame.sprite.Sprite):
    def __init__(self,UvodneNastavenia,img1,text,font,metodaClick,x,y,img2 = None,sirka = None,vyska = None):
        self.uvodneNastavenia = UvodneNastavenia
        pygame.sprite.Sprite.__init__(self, self.uvodneNastavenia.tlacidla_sprites)
        self.image1 = img1
        if img2 == None:
            self.image2 = img1
        else:
            self.image2 = img2
        
        self.image = pygame.Surface(self.image1.get_size())    
        self.rect = self.image.get_rect()
        self.trebaScalovat = False;
        if vyska is not None:
            self.rect.height = vyska
            self.trebaScalovat = True;
        if sirka is not None  :
            self.rect.width = sirka
            self.trebaScalovat = True;
        
        
            
            
        #self.image = pygame.Surface(self.image1.get_size())
        #self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jeOznaceny = False
        self.jeKliknuty = False
        self.clickMethod = metodaClick
        self.font = font
        self.text = text
        self.update()


        
    def update(self):
        if self.trebaScalovat:
            
            if self.jeOznaceny:
                self.image = pygame.transform.scale(self.image2, (self.rect.width, self.rect.height))
            else:
                self.image = pygame.transform.scale(self.image1,(self.rect.width, self.rect.height))
            
        else:
            if self.jeOznaceny:
                self.image.blit(self.image2,(0,0))
            else:
                self.image.blit(self.image1,(0,0))
        
        if self.jeKliknuty:
            self.clickMethod(self)
        self.jeOznaceny = False
        self.jeKliknuty = False
        self.updateText()
        
        
        
    def updateText(self):
        
            size = self.image.get_size()
            self.textSurf = self.font.render(self.text,1, nastavenia.BLACK)
            textX = (size[0] - self.textSurf.get_width())/2
            textY = (size[1] - self.textSurf.get_height())/2
            self.image.blit(self.textSurf, (textX, textY))
        
class TUNVKrizik(TUNVseobecne):
    def __init__(self,UvodneNastavenia,img1,text,font,metodaClick,x,y,variableBoolean,img2 = None,sirka = None,vyska = None):
        self.variable = variableBoolean;
        super().__init__(UvodneNastavenia, img1, text, font, metodaClick, x, y, img2,sirka,vyska)
        
    
    def update(self):
        if self.variable[0]:
            self.image.blit(self.image2,(0,0))
        else:
            self.image.blit(self.image1,(0,0))

        
        if self.jeKliknuty:
            self.clickMethod(self)
        #self.jeOznaceny = False
        self.jeKliknuty = False
        #self.updateText()
        
        
class Tlacidlo(pygame.sprite.Sprite):
    def __init__(self,Menu,imgs,text,font,sirka,vyska):
        self.menu = Menu
        pygame.sprite.Sprite.__init__(self,self.menu.tlacidla_sprites)
        self.images = imgs
        self.imageIndex = 0
        self.image = pygame.Surface(self.images[0].get_size())   
        self.rect = self.image.get_rect()
        self.rect.x = sirka
        self.rect.y = vyska
        self.font = font
        
        #Stav tlacidla
        self.trebaUpdate = True
        self.text = text
        self.jeLocknuty = False;
        self.jeClicknuty = False;
        self.jeNaNomMys = False;
        
        
        self.indexTextury = 0
        self.lastUpdate = -1
        
        self.update()
        
    def mouseOnSprite(self):
        if self.jeLocknuty:
            return
        if self.lastUpdate is LastUpdate.HOVER:
            return
        self.lastUpdate = LastUpdate.HOVER
        if len(self.images) > 1:
            self.hover()
        
    def hover(self):
        self.jeNaNomMys = True;



    def mouseClicked(self):
        if self.jeLocknuty:
            return
        if self.lastUpdate is LastUpdate.CLICK:
            return
        self.lastUpdate = LastUpdate.CLICK
        self.click()#metoda pre override
            
    def click(self):
        self.jeClicknuty = True
        
    def prekresli(self):
        self.image.blit(self.images[self.imageIndex],(0,0))
        self.image.blit(self.textSurf, (self.textX, self.textY))
        
    def updateText(self):
        size = self.image.get_size()
        self.textSurf = self.font.render(self.text,1, nastavenia.BLACK)
        self.textX = (size[0] - self.textSurf.get_width())/2
        self.textY = (size[1] - self.textSurf.get_height())/2
        
    '''
    Umoznuje zablokovat tlacidlo
    '''        
    def setLock (self, hodnota):
        if hodnota == self.jeLocknuty:
            return
        self.jeLocknuty = hodnota
        self.trebaUpdate = True
        
    def nastalaZmena(self): #nastavZmenu
        self.trebaUpdate = True

    def nutnyUpdate(self):
            self.lastUpdate = LastUpdate.UPDATE
            self.trebaUpdate = False


            if self.jeLocknuty and len(self.images) > 2 and self.images[2] is not None:
                self.imageIndex = 2
                
                
            else:
                if self.jeNaNomMys and len(self.images) > 1 and self.images[1] is not None:
                    self.imageIndex = 1
                    self.trebaUpdate = True # hover moze zmiznut alebo potom informovat tlacidlo o zmiznuti hover
                else:
                    self.imageIndex = 0
                
            
            self.updateText()
            self.prekresli()
          
    def update(self):
        if self.trebaUpdate == True or self.lastUpdate is not LastUpdate.UPDATE:
            self.nutnyUpdate()
        
        self.jeClicknuty = False
        self.jeNaNomMys = False
        
        
        
        
'''
okrem bezneho tlacidla ma moznost ako parameter prijat funkciu ktora sa vykona pri kliknuti na tlacidlo
'''
class TlacidloClickMethod (Tlacidlo):
    def __init__(self,Menu,imgs,text,font,sirka,vyska,metoda):
        self.clickMetoda = metoda
        super().__init__(Menu,imgs,text,font,sirka,vyska)
       
    def click(self):
        self.clickMetoda(self)
        



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        