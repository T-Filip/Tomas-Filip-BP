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
        self.scaleNas =scale
        self.nasledujuceMenu = None
        self.predchadzajuceMenu = []
        self.allSprites = pygame.sprite.RenderUpdates()
        
    def dajGroup(self):
        return self.allSprites
        
    def initPozadie(self):
        poz = pygame.image.load('img\\Menu\\MenuOkno.png').convert()
        self.pozadie = pygame.transform.scale(poz,(int(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]),int(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie])))
        
        
    def linkOkna(self, obj):
        logging.info("Menu.menuOkno.MenuOkno.linkOkna -> Linkujem okna")
        self.predchadzajuceMenu.append(obj)
        obj.setPredchadzajuce(self)
        
    def updateMouse(self):
        pass
    
    def update(self):
        self.updateMouse()
        self.allSprites.update()
        
    def setPredchadzajuce(self, obj):
        if self.predchadzajuceMenu != None:
            logging.warning("Menu.menuOkno.MenuOkno.setPredchadzajuce -> prepisovanie predchadzajuceho okna")
        self.predchadzajuceMenu = obj
        

        
    def drawPozadie(self,screen):
        screen.blit(self.pozadie,(0,0))
            
    
    def draw(self,screen):
        self.drawPozadie(screen)
        self.allSprites.draw(screen)
        pygame.display.flip()
        
        
        
    
        
        