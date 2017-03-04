'''
Created on 4. 3. 2017

@author: T.Filip
'''
import Menu.menuOkno as menuOkno
import uvodneNastavenia 
import textury
import nastavenia
import pygame

def test():
    pass

class MenuOknoVyberPostavy(menuOkno.MenuOkno):
    def __init__(self,manazerOkien,scale):
        super().__init__(manazerOkien,scale)
        uvodneNastavenia.TlacidloClickMethod(self,[textury.TUN2,textury.TUN2Oznacene],"CLOSE",16,525,320,test,scale)
        uvodneNastavenia.TlacidloClickMethod(self,[textury.TUN2,textury.TUN2Oznacene],"CLOSE",16,655,320,test,scale)
        
        
    def updateMouse(self):
        pos = pygame.mouse.get_pos()
        sprites_pod_myskou = [s for s in self.allSprites if s.rect.collidepoint(pos)]
        self.volajMetodu(sprites_pod_myskou,"mouseOnSprite")
       
    def volajMetodu (self,objekty,metoda):
        if len(objekty) < 1:
            return
            
        met = getattr(objekty[0],metoda)
        for sp in objekty:
            met(); 