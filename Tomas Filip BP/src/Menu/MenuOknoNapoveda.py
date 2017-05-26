#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on 22. 4. 2017

@author: T.Filip
'''



import Menu.menuOkno as menuOkno
from Textury import textury
import Nastavenia.nastavenia as nastavenia


class MenuOknoNapoveda(menuOkno.MenuOknoHra):
        def __init__(self,manazerOkien,scale, sirkaCast = 0.5,vyskaCast = 0.55):
            super().__init__(manazerOkien, scale, 0.35, 0.5)

        def vykresliNapovedu(self,screen):
            font = textury.dajFont(int(18*self.scaleRes))
            self.medzera = 22*self.scaleRes
            self.y = [self.rect.y+80]
            self.x = [self.rect.x + 40]
            self.vykresliRiadok("P - Pauza",screen,font) 
            self.vykresliRiadok("N - Nápoveda",screen,font) 
            self.vykresliRiadok("I - Inventár",screen,font) 
            self.vykresliRiadok("V - Vlastnosti",screen,font)
            self.vykresliRiadok("B - Zručnosti",screen,font)
            self.vykresliRiadok("R - Rotácia predmetu",screen,font)
            self.vykresliRiadok("W, A, S, D, šipky - Pohyb",screen,font)
            self.vykresliRiadok("Shift - Šprint",screen,font)
            self.vykresliRiadok("ESC - Menu",screen,font) 
            self.vykresliRiadok("kolečko myši - Zoom",screen,font) 
            
        def reinit(self,hrac):
            super().reinit(hrac)
            self.manazerOkien.setJePauza(True)
     
        def close(self):
            self.manazerOkien.setJePauza(False)
                
        def vykresliRiadok(self, text,screen,font):
            textSurf = font.render(text,1, nastavenia.BLACK)
            screen.blit(textSurf,(self.x[0],self.y[0]))
            self.y[0] +=  self.medzera
                
        def draw(self, screen):
            menuOkno.MenuOknoHra.draw(self, screen)
            self.vykresliNadpis(screen,"Nápoveda")
            self.vykresliNapovedu(screen)
