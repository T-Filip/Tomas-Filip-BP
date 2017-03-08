'''
Created on 4. 3. 2017

@author: T.Filip
'''
import pygame
import logging
import nastavenia
import manazerOkien



class MenuOkno:
    def __init__(self,manazerOkien,scale):
        self.initPozadie()
        self.manazerOkien = manazerOkien
        self.scaleRes =scale
        self.allSprites = pygame.sprite.RenderUpdates()
        
    def prepniMenu(self,menoMenu):
        self.manazerOkien.prepniMenu(menoMenu)
        
    def dajGroup(self):
        return self.allSprites
        
    def initPozadie(self):
        poz = pygame.image.load('img\\Menu\\MenuOkno.png').convert()
        self.pozadie = pygame.transform.scale(poz,(int(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]),int(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie])))
        
        '''
    def linkOkna(self, obj):
        logging.info("Menu.menuOkno.MenuOkno.linkOkna -> Linkujem okna")
        self.predchadzajuceMenu.append(obj)
        obj.setPredchadzajuce(self)
        '''
        
    def updateMouse(self):
        pos = pygame.mouse.get_pos()
        sprites_pod_myskou = [s for s in self.allSprites if s.rect.collidepoint(pos)]
        self.volajMetodu(sprites_pod_myskou,"mouseOnSprite")
        eventy = self.manazerOkien.dajEventy()
        for ev in eventy: 
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.volajMetodu(sprites_pod_myskou, "mouseClicked")
       
    def volajMetodu (self,objekty,metoda):
        if len(objekty) < 1:
            return
            
        met = getattr(objekty[0],metoda)
        for sp in objekty:
            met();
    
    def update(self):
        self.updateMouse()
        self.allSprites.update()
        
        '''
    def setPredchadzajuce(self, obj):
        if self.predchadzajuceMenu != None:
            logging.warning("Menu.menuOkno.MenuOkno.setPredchadzajuce -> prepisovanie predchadzajuceho okna")
        self.predchadzajuceMenu = obj
        '''

        
    def drawPozadie(self,screen):
        screen.blit(self.pozadie,(0,0))
            
    
    def draw(self,screen):
        self.drawPozadie(screen)
        self.allSprites.draw(screen)
        pygame.display.flip()
        
    def refresh(self):
        pass
        
        
        
    
        
        