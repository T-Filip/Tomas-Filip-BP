# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import pygame
import sys
import os
from enum import Enum
import nastavenia
from Textury import textury
import Menu.objMenu as objMenu

#os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

        


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
    
def zmenTextRychlostHry(self):
    self.text = "Rychlost " + str(nastavenia.RYCHLOST_HRY)
    self.updateText()
    self.prekresli()
    
def zvysRychlostHry(self):
    nastavenia.RYCHLOST_HRY += 10
    if nastavenia.RYCHLOST_HRY > 160:
        nastavenia.RYCHLOST_HRY = 160
    zmenTextRychlostHry(self.menu.tlacidloRychlostHry)

def znizRychlostHry(self):
    nastavenia.RYCHLOST_HRY -= 10
    if nastavenia.RYCHLOST_HRY < 40:
        nastavenia.RYCHLOST_HRY = 40
    zmenTextRychlostHry(self.menu.tlacidloRychlostHry)
    
        


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


        #objMenu(self,[self.TUN2,self.TUN2Oznacene],"Testujeme",nastavenia.FONT_1_16,50,50)
        objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"CLOSE",16,215,320,ukonci)
        objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"START",16,85,320,tlacidloStart)
        self.tlacidloRozlisenie = objMenu.Tlacidlo(self,[textury.TUN1center],"",16,140,270,zmenTextRozlisenia)
        self.tlacidloRozlisenie.click()
        objMenu.Tlacidlo(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85,270,znizRozlisenie)
        objMenu.Tlacidlo(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275,270,zvysRozlisenie)
        
        #fullscreen border
        tlacidloWindow = objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"",13,85,220,zmenTextFullScreen)
        tlacidloWindow.text = nastavenia.WINDOW[nastavenia.windowIndex]
        tlacidloWindow.updateText()
        tlacidloWindow.prekresli()
        self.tlacidloBorder = objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene,textury.TUN2Oznacene2],"",13,215,220,zmenTextBorder)
        self.tlacidloBorder.text = nastavenia.BORDER[nastavenia.borderIndex]
        if nastavenia.windowIndex == 0:
            self.tlacidloBorder.setLock(True)
            #self.tlacidloBorder.nastalaZmena()
        self.tlacidloBorder.updateText()
        self.tlacidloBorder.prekresli()
        
        #tlacidla sirka mapy
        self.tlacidloSirkaMapy = objMenu.Tlacidlo(self,[textury.TUN1center],"",16,140,170,zmenTextSirkyMapy)
        self.tlacidloSirkaMapy.click()
        objMenu.Tlacidlo(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85,170,znizSirkuMapy)
        objMenu.Tlacidlo(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275,170,zvysSirkuMapy)
        
        #tlacidla vyska mapy
        self.tlacidloVyskaMapy = objMenu.Tlacidlo(self,[textury.TUN1center],"",16,140,120,zmenTextVyskyMapy)
        self.tlacidloVyskaMapy.click()
        objMenu.Tlacidlo(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85,120,znizVyskuMapy)
        objMenu.Tlacidlo(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275,120,zvysVyskuMapy)
        
        #tlacidla rychlost hry
        self.tlacidloRychlostHry = objMenu.Tlacidlo(self,[textury.TUN1center],"",16,140,70,zmenTextRychlostHry)
        self.tlacidloRychlostHry.click()
        objMenu.Tlacidlo(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85,70,znizRychlostHry)
        objMenu.Tlacidlo(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275,70,zvysRychlostHry)

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
                    ukonci(self)
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
        
    def volajMetodu (self,objekty,zmenRecept):
        if len(objekty) < 1:
            return
            
        met = getattr(objekty[0],zmenRecept)
        for sp in objekty:
            met();
             
        

        



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        