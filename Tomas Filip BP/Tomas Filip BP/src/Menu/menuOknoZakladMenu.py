'''
Created on 7. 3. 2017

@author: T.Filip
'''
import Menu.menuOkno as menuOkno
import Menu.objMenu as objMenu
import textury
import pygame
import sys
import Menu.enumOknaMenu as enumOknaMenu

def ukonci(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        
def novaHra(self):
    self.menu.prepniMenu(enumOknaMenu.EnumOknaMenu.VYBER_POSTAVY)

class MenuOknoZakladMenu(menuOkno.MenuOkno):
        def __init__(self,manazerOkien,scale):
            super().__init__(manazerOkien,scale)
            objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"Nova hra",16,540,120,novaHra,scale,1.75)
            objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"Close",16,540,210,ukonci,scale,1.75)
        