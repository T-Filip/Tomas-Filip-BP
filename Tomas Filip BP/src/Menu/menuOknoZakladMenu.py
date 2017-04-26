'''
Created on 7. 3. 2017

@author: T.Filip
'''
import Menu.menuOkno as menuOkno
import Menu.objMenu as objMenu
from Textury import textury
import pygame
import sys
import Menu.enumOknaMenu as enumOknaMenu
import Nastavenia.nastavenia as nastavenia
import random

def ukonci(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        
def novaHra(self):
    nastavenia.SEED = random.random()
    self.menu.prepniMenu(enumOknaMenu.EnumOknaMenu.VYBER_POSTAVY)
    
def navratDoHry(self):
    self.menu.manazerOkien.prepniMenu(None)

class MenuOknoZakladMenu(menuOkno.MenuOkno):
        def __init__(self,manazerOkien,scale):
            super().__init__(manazerOkien,scale)
            objMenu.Tlacidlo(self,[textury.MENU_TLACIDLO,textury.MENU_TLACIDLO_OZNACENE],"Nova hra",16,460,120,novaHra,scale,2)
            self.tlacidloNavratDoHry = objMenu.Tlacidlo(self,[textury.MENU_TLACIDLO,textury.MENU_TLACIDLO_OZNACENE,textury.MENU_TLACIDLO_LOCKNUTE],"Navrat do hry",16,460,210,navratDoHry,scale,2)
            objMenu.Tlacidlo(self,[textury.MENU_TLACIDLO,textury.MENU_TLACIDLO_OZNACENE],"Exit",16,460,300,ukonci,scale,2)
            self.tlacidloNavratDoHry.setLock(True)
            
        def reinit(self):
            if self.manazerOkien.dajHru() != None:
                self.tlacidloNavratDoHry.setLock(False)
            else:
                self.tlacidloNavratDoHry.setLock(True)
            
            
        
        