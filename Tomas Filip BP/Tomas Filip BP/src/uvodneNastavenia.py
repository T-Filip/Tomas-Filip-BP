# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import pygame
import sys
import os
from enum import Enum
import nastavenia
import textury

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
        self.text = str(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie])+ ' x ' + str(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie])
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
    
def zmenTextSirkyMapy(self):
    self.text = "Sirka " + str(nastavenia.MAP_SIZE_X)
    self.updateText()
    self.prekresli()
    
def zmenTextVyskyMapy(self):
    self.text = "Vyska " + str(nastavenia.MAP_SIZE_Y)
    self.updateText()
    self.prekresli()

def zvysSirkuMapy(self):
    nastavenia.MAP_SIZE_X += 1
    if nastavenia.MAP_SIZE_X > 40:
        nastavenia.MAP_SIZE_X = 40
    zmenTextSirkyMapy(self.menu.tlacidloSirkaMapy)
        
def znizSirkuMapy(self):
    nastavenia.MAP_SIZE_X -= 1
    if nastavenia.MAP_SIZE_X < 8:
        nastavenia.MAP_SIZE_X = 8
    zmenTextSirkyMapy(self.menu.tlacidloSirkaMapy)
        
def zvysVyskuMapy(self):
    nastavenia.MAP_SIZE_Y += 1
    if nastavenia.MAP_SIZE_Y > 40:
        nastavenia.MAP_SIZE_Y = 40
    zmenTextVyskyMapy(self.menu.tlacidloVyskaMapy)
        
def znizVyskuMapy(self):
    nastavenia.MAP_SIZE_Y -= 1
    if nastavenia.MAP_SIZE_Y < 8:
        nastavenia.MAP_SIZE_Y = 8
    zmenTextVyskyMapy(self.menu.tlacidloVyskaMapy)
        


class UvodneNastavenia:
    
    
    def __init__ (self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        
        #for mode in pygame.display.list_modes():
        #    print(mode)
        
        
        self.screen = pygame.display.set_mode((nastavenia.UVODNE_NASTAVENIA_SIRKA,nastavenia.UVODNE_NASTAVENIA_VYSKA ),pygame.NOFRAME)
        textury.init()
        
        nastavenia.FONT_1_16 = pygame.font.Font("font\\armalite.ttf",16)
        nastavenia.FONT_1_13 = pygame.font.Font("font\\armalite.ttf",13)
       
        pygame.display.set_caption(nastavenia.UVODNE_NASTAVENIA_TITLE)
        self.clock = pygame.time.Clock()
        self.tlacidla_sprites = pygame.sprite.LayeredUpdates()

        self.uvodNastaveniaOkno = pygame.image.load('img\\uvodneNastavenia\\uvodNastaveniaOkno.png').convert_alpha()
        '''
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


        #Tlacidlo(self,[self.TUN2,self.TUN2Oznacene],"Testujeme",nastavenia.FONT_1_16,50,50)
        TlacidloClickMethod(self,[textury.TUN2,textury.TUN2Oznacene],"CLOSE",16,215,320,ukonci)
        TlacidloClickMethod(self,[textury.TUN2,textury.TUN2Oznacene],"START",16,85,320,tlacidloStart)
        self.tlacidloRozlisenie = TlacidloClickMethod(self,[textury.TUN1center],"",16,140,270,zmenTextRozlisenia)
        self.tlacidloRozlisenie.click()
        TlacidloClickMethod(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85,270,znizRozlisenie)
        TlacidloClickMethod(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275,270,zvysRozlisenie)
        
        #fullscreen border
        tlacidloWindow = TlacidloClickMethod(self,[textury.TUN2,textury.TUN2Oznacene],"",13,85,220,zmenTextFullScreen)
        tlacidloWindow.text = nastavenia.WINDOW[nastavenia.windowIndex]
        tlacidloWindow.updateText()
        tlacidloWindow.prekresli()
        self.tlacidloBorder = TlacidloClickMethod(self,[textury.TUN2,textury.TUN2Oznacene,textury.TUN2Oznacene2],"",13,215,220,zmenTextBorder)
        self.tlacidloBorder.text = nastavenia.BORDER[nastavenia.borderIndex]
        if nastavenia.windowIndex == 0:
            self.tlacidloBorder.setLock(True)
            #self.tlacidloBorder.nastalaZmena()
        self.tlacidloBorder.updateText()
        self.tlacidloBorder.prekresli()
        
        #tlacidla sirka mapy
        self.tlacidloSirkaMapy = TlacidloClickMethod(self,[textury.TUN1center],"",16,140,170,zmenTextSirkyMapy)
        self.tlacidloSirkaMapy.click()
        TlacidloClickMethod(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85,170,znizSirkuMapy)
        TlacidloClickMethod(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275,170,zvysSirkuMapy)
        
        #tlacidla vyska mapy
        self.tlacidloVyskaMapy = TlacidloClickMethod(self,[textury.TUN1center],"",16,140,120,zmenTextVyskyMapy)
        self.tlacidloVyskaMapy.click()
        TlacidloClickMethod(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85,120,znizVyskuMapy)
        TlacidloClickMethod(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275,120,zvysVyskuMapy)

    def dajGroup(self):
        return self.tlacidla_sprites
        
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
                    ukonci()#parameter? 
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.volajMetodu(sprites_pod_myskou, "mouseClicked")
    

                
            
            self.tlacidla_sprites.update()
            
            self.draw()
            
        #pygame.display.quit()
        #pygame.quit()


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
             
        
class Tlacidlo(pygame.sprite.Sprite):
    def __init__(self,Menu,imgs,text,fontVelkost,sirka,vyska,scale=1):
        self.scaleNas = scale 
        self.menu = Menu
        pygame.sprite.Sprite.__init__(self,self.menu.dajGroup())
        self.images = [0 for i in range (len(imgs))]
 
        for i in range (len(imgs)):
            self.images[i] = pygame.transform.scale(imgs[i],(int(imgs[i].get_width() * self.scaleNas),int(imgs[i].get_height() * self.scaleNas)))
        self.imageIndex = 0
        self.image = pygame.Surface(self.images[0].get_size())   
        self.rect = self.image.get_rect()
        self.rect.x = sirka * self.scaleNas
        self.rect.y = vyska * self.scaleNas
        
        self.font = textury.dajFont(int(fontVelkost*self.scaleNas))
        
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
    def __init__(self,Menu,imgs,text,font,sirka,vyska,metoda,scale = 1):
        self.clickMetoda = metoda
        super().__init__(Menu,imgs,text,font,sirka,vyska,scale)
       
    def click(self):
        self.clickMetoda(self)
        



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        