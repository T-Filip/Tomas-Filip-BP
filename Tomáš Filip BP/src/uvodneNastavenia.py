# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import pygame
import nastavenia
import sys
import os
#os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"


def ukonci(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        
def zvysRozlisenie(self):
    nastavenia.vybrateRozlisenie += 1;
    if nastavenia.vybrateRozlisenie > len(nastavenia.ROZLISENIA_X) - 1:
        nastavenia.vybrateRozlisenie -= len(nastavenia.ROZLISENIA_X)
    updateTextTlacidloRozlisenie(self.uvodneNastavenia.tlacidloRozlisenie)

def znizRozlisenie(self):
    nastavenia.vybrateRozlisenie -= 1;
    if nastavenia.vybrateRozlisenie < 0:
        nastavenia.vybrateRozlisenie += len(nastavenia.ROZLISENIA_X)
    updateTextTlacidloRozlisenie(self.uvodneNastavenia.tlacidloRozlisenie)
   
        
def updateTextTlacidloRozlisenie(self):
        self.text = str(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie])+ 'x' + str(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie])
        

    



class UvodneNastavenia:
    
    
    def __init__ (self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        
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
        #self.TUN1right = pygame.image.load('img\\uvodneNastavenia\\TUN1right.png').convert_alpha()
        #self.TUN1rightOznacene = pygame.image.load('img\\uvodneNastavenia\\TUN1rightOznacene.png').convert_alpha()
        self.TUN1right = pygame.transform.flip(self.TUN1left,True,False)
        self.TUN1rightOznacene = pygame.transform.flip(self.TUN1leftOznacene,True,False)
        
        
        #tlacidlo1 = TlacidloUNRozlisenie(self, 85, 260)
        self.tlacidloRozlisenie = TUNVseobecne(self,self.TUN1center,"",nastavenia.FONT_28_DAYS_LATER,updateTextTlacidloRozlisenie,140, 270, None)
        self.tlacidloRozlisenie.clickMethod(self.tlacidloRozlisenie)
        TUNVseobecne(self,self.TUN1left,"",nastavenia.FONT_28_DAYS_LATER,znizRozlisenie,85, 270, self.TUN1leftOznacene)
        TUNVseobecne(self,self.TUN1right,"",nastavenia.FONT_28_DAYS_LATER,zvysRozlisenie,275, 270, self.TUN1rightOznacene)
        TUNVseobecne(self,self.TUN2,"CLOSE",nastavenia.FONT_28_DAYS_LATER,ukonci,215, 320, self.TUN2Oznacene)
        TUNVseobecne(self,self.TUN2,"START",nastavenia.FONT_28_DAYS_LATER,ukonci,85, 320, self.TUN2Oznacene)
        
    def run(self):
        #cyklus pre nacitavacie menu
        self.jeNeukonceny = True
        
        while self.jeNeukonceny:
            self.clock.tick(20)
            
            self.keysPressed = pygame.key.get_pressed()
            self.events = pygame.event.get()
            for ev in self.events:
                if ev.type == pygame.QUIT:
                    ukonci()

            jeKliknuty=False;
            for ev in self.events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    jeKliknuty = True;
    
            pos = pygame.mouse.get_pos()
            sprites_pod_myskou = [s for s in self.tlacidla_sprites if s.rect.collidepoint(pos)]
            for sp in sprites_pod_myskou:
                sp.jeOznaceny = True;
                sp.jeKliknuty = jeKliknuty
            
            self.tlacidla_sprites.update()
            
            self.draw()
            


    def draw(self):
        self.screen.blit(self.uvodNastaveniaOkno, (0,0))
        self.tlacidla_sprites.draw(self.screen)
        pygame.display.flip()
        
    
      
    
    


'''

class TlacidloUNRozlisenie(pygame.sprite.Sprite):
    def __init__ (self, UvodneNastavenia, x, y):
        self._layer = 1
        self.jeKliknuty = False
        self.jeOznaceny = False
        self.uvodneNastavenia = UvodneNastavenia
        self.tlacidla = self.uvodneNastavenia.tlacidla_sprites
        #self.image = self.uvodneNastavenia.neoznacene_tlacidlo
        self.image = pygame.Surface([230, 40])
        #surf = pygame.Surface((15,40), pygame.SRCALPHA)   # per-pixel alpha
        self.image.fill((255,255,255,0))                         # notice the alpha value in the color
        #self.image.blit(surf, (40,0))
        #self.image.blit(surf, (175,0))
        pygame.sprite.Sprite.__init__(self, self.tlacidla)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.image.blit(self.uvodneNastavenia.TUN1left, (0, 0))
        #self.image.blit(self.uvodneNastavenia.TUN1center, (40, 0))
        #self.image.blit(self.uvodneNastavenia.TUN1right, (190,0))

        
        self.font = nastavenia.FONT_28_DAYS_LATER
        self.updateText()
        self.update()
        #self.Surf = pygame.Surface((100, 40))
        #W = self.textSurf.get_width()
        #H = self.textSurf.get_height()
        
        
    def update(self):

        
        if self.jeOznaceny:
            pos = pygame.mouse.get_pos()
            
            relatX = (pos[0]- self.rect.x)
            if (relatX < 40):
                self.image.blit(self.uvodneNastavenia.TUN1leftOznacene, (0, 0))
                if self.jeKliknuty:
                    self.znizRozlisenie()
                    self.updateText()
                    
            
            elif (relatX > 190):
                self.image.blit(self.uvodneNastavenia.TUN1rightOznacene, (190, 0))
                if self.jeKliknuty:
                    self.zvysRozlisenie()
                    self.updateText()
            
                
            
        else:
            self.image.blit(self.uvodneNastavenia.TUN1left, (0, 0))
            self.image.blit(self.uvodneNastavenia.TUN1right, (190, 0))

        self.jeOznaceny = False
        self.jeKliknuty = False
    
    
    def zvysRozlisenie(self):
        nastavenia.vybrateRozlisenie += 1;
        if nastavenia.vybrateRozlisenie > len(nastavenia.ROZLISENIA_X) - 1:
            nastavenia.vybrateRozlisenie -= len(nastavenia.ROZLISENIA_X)
        
    def znizRozlisenie(self):
        nastavenia.vybrateRozlisenie -= 1;
        if nastavenia.vybrateRozlisenie < 0:
            nastavenia.vybrateRozlisenie += len(nastavenia.ROZLISENIA_X)
            
    def updateText(self):
        
        self.textSurf = self.font.render(str(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie])+ 'x' + str(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]), 1, nastavenia.BLACK)
        textX = (150 - self.textSurf.get_width())/2 + 40
        textY = (40 - self.textSurf.get_height())/2
        self.image.blit(self.uvodneNastavenia.TUN1center, (55, 0))
        
        self.image.blit(self.textSurf, (textX, textY))
        







'''

class TUNVseobecne(pygame.sprite.Sprite):
    def __init__(self,UvodneNastavenia,img1,text,font,metodaClick,x,y,img2 = None):
        self.uvodneNastavenia = UvodneNastavenia
        pygame.sprite.Sprite.__init__(self, self.uvodneNastavenia.tlacidla_sprites)
        self.image1 = img1
        if img2 == None:
            self.image2 = img1
        else:
            self.image2 = img2
        self.image = pygame.Surface(self.image1.get_size())
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.jeOznaceny = False
        self.jeKliknuty = False
        self.clickMethod = metodaClick
        self.font = font
        self.text = text
        self.update()
        self.updateText()
        
        
    def update(self):
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
            size = self.image1.get_size()
            self.textSurf = self.font.render(self.text,1, nastavenia.BLACK)
            textX = (size[0] - self.textSurf.get_width())/2
            textY = (size[1] - self.textSurf.get_height())/2
            self.image.blit(self.textSurf, (textX, textY))
        
        