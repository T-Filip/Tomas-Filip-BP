#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 1. 4. 2017

@author: T.Filip
'''
from Menu.menuOkno import MenuOknoHra
import Menu.objMenu as objMenu
import Textury.textury as textury
from Nastavenia import nastavenia


class MenuOknoZrucnosti(MenuOknoHra):
    def __init__(self,manazerOkien,scale, sirkaCast = 0.5,vyskaCast = 0.68):
        super().__init__(manazerOkien, scale, sirkaCast, vyskaCast)
        
        
        
    def reinit(self, hrac):
        MenuOknoHra.reinit(self, hrac)
        x= self.topLeftXPredScale + 80
        y= self.topLeftYPredScale - 40
        zvKonst = 50

        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajZrucnosti()[0],self.hrac.dajVolneZrucnosti(),[0,100],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajZrucnosti()[1],self.hrac.dajVolneZrucnosti(),[0,100],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajZrucnosti()[2],self.hrac.dajVolneZrucnosti(),[0,100],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajZrucnosti()[3],self.hrac.dajVolneZrucnosti(),[0,100],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajZrucnosti()[4],self.hrac.dajVolneZrucnosti(),[0,100],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajZrucnosti()[5],self.hrac.dajVolneZrucnosti(),[0,100],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajZrucnosti()[6],self.hrac.dajVolneZrucnosti(),[0,100],self.scaleRes)

        
    def close(self):
        self.allSprites.empty()
        self.hrac.reinitVlastnosti()
        
        
    def vykresliZrucnosti(self,screen):
        
        font = textury.dajFont(int(25*self.scaleRes))  
        zrucnosti = nastavenia.ZRUCNOSTI # text
        x= (self.topLeftXPredScale + 150)*self.scaleRes
        y= (self.topLeftYPredScale - 35)*self.scaleRes
        zvKonst = (50*self.scaleRes)

        zrucnostiHraca = self.hrac.dajZrucnosti()
        for i in range (len(zrucnostiHraca)):
            text = zrucnosti[i] + ": " + str(zrucnostiHraca[i])                                 
            textSurf = font.render(text,1, nastavenia.BLACK)
            screen.blit(textSurf,(x,y))
            y += zvKonst
            
    def vykresliVolneZrucnosti(self,screen):
        font = textury.dajFont(int(25*self.scaleRes))
        text = "Voľné zručnosti: " + str(self.hrac.dajVolneZrucnosti()[0])                                 
        textSurf = font.render(text,1, nastavenia.BLACK)
        x= int(self.rect.x + (self.rect.width - textSurf.get_width())/2)
        y= self.rect.y + self.rect.height - int(45*self.scaleRes)
        screen.blit(textSurf,(x,y))
        
    def vykresliLevel(self,screen):
        font = textury.dajFont(int(20*self.scaleRes))
        text = "Level: " + str(self.hrac.dajLevel()) + "    Skúsenosti: " + str(self.hrac.dajSkusenosti()) + "/" + str(self.hrac.dajDalsiLevelNaSkusenostiach())                                  
        textSurf = font.render(text,1, nastavenia.BLACK)
        x= int(self.rect.x + (self.rect.width - textSurf.get_width())/2)
        y= self.rect.y + self.rect.height - int(70*self.scaleRes)
        screen.blit(textSurf,(x,y))
            
            
    def draw(self, screen):
        MenuOknoHra.draw(self, screen)
        self.vykresliNadpis(screen, "Zručnosti")
        self.vykresliZrucnosti(screen)
        self.vykresliVolneZrucnosti(screen)
        self.vykresliLevel(screen)