#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 4. 3. 2017

@author: T.Filip
'''
import Menu.menuOkno as menuOkno
#from Nastavenia import uvodneNastavenia 
from Textury import textury 
from Nastavenia import nastavenia
#import pygame
import Menu.objMenu as objMenu
#from enum import IntEnum
#import sys
import Postavy.smerPostavy as smerPostavy
import Menu.enumOknaMenu as enumOknaMenu
import Postavy.tvorcaPostav as tvorcaPostavy
from Postavy.enumTypPostavy import EnumTypPostavy






    


def back(self):
        self.menu.prepniMenu(enumOknaMenu.EnumOknaMenu.ZAKLADNE_MENU)

def hracUpdate(self):
    im = textury.FRAME.copy()
    postava = tvorcaPostavy.vytvorPostavu(True,self.args[0],self.menu.farbaTela[self.menu.indexFarbyTela[0]],self.menu.typPostavy[0],
                                          self.menu.cisloTvare[0],self.menu.cisloVlasov[0],self.menu.cisloOci[0],self.menu.cisloPohlavia[0])
    im.blit(postava,(8,8))
    self.menu.postavyHrac[self.args[0]] = postava
    return im
    
    
def startHry(self):
    self.menu.prepniMenu(None)
    self.menu.manazerOkien.vytvorHru(self.menu.postavyHrac,self.menu.vlastnosti,self.menu.typPostavy)
    
class MenuOknoVyberPostavy(menuOkno.MenuOkno):
    def __init__(self,manazerOkien,scale):

        super().__init__(manazerOkien,scale)
        
        
        objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"ŠTART",16,525,600,startHry,scale)
        objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"BACK",16,655,600,back,scale)
        self.vlastnosti = [0,0,0,0]
        
        capTypPostavy = nastavenia.CAP_TYP_POSTAVY
        
        #MUZ - 0 ZENA - 1
        capPohlavia = nastavenia.CAP_POHLAVIE
        capCisloOci = nastavenia.CAP_TVAR
        capCisloVlasov = nastavenia.CAP_VLASY
        capTypTvare = nastavenia.CAP_HLAVA
        
        self.farbaTela = nastavenia.FARBA_TELA
        self.indexFarbyTela = [2]
        self.cisloOci = [0]
        self.cisloVlasov = [0]
        self.cisloTvare = [0]
        self.cisloPohlavia = [0]
        
        self.typPostavy = [EnumTypPostavy.SILNA]
        
        self.postavyHrac = [0,0,0,0,0]
        
        
        kraj = 200
        medzera = 60
        
        self.oknaPostavy = [0 for i in range(5)]
        self.oknaPostavy[0] = objMenu.ObjMenuInfo(self,None,"",16,kraj,150,hracUpdate,[smerPostavy.SmerPostavy.DOPRAVA],scale,1.5)
        self.oknaPostavy[1] = objMenu.ObjMenuInfo(self,None,"",16,kraj+medzera+120,150,hracUpdate,[smerPostavy.SmerPostavy.DOPREDU],scale,1.5)
        self.oknaPostavy[2] = objMenu.ObjMenuInfo(self,None,"",16,kraj+medzera*2+120*2,150,hracUpdate,[smerPostavy.SmerPostavy.DOZADU],scale,1.5)
        self.oknaPostavy[3] = objMenu.ObjMenuInfo(self,None,"",16,kraj+medzera*3+120*3,150,hracUpdate,[smerPostavy.SmerPostavy.SPECIAL],scale,1.5)
        self.oknaPostavy[4] = objMenu.ObjMenuInfo(self,None,"",16,kraj+medzera*4+120*4,150,hracUpdate,[smerPostavy.SmerPostavy.DOLAVA],scale,1.5)
        
        yPixTlacidla = 285
        kraj =115
        medzera = 85
        tlacidla = 220
        
        #TYP POSTAVY
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"Typ postavy",16,140+kraj,yPixTlacidla,scale)
        self.tlacidloSirkaMapy.click()
        objMenu.TlacidloIncDecVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj,yPixTlacidla,False,True,self.typPostavy,capTypPostavy,scale)
        objMenu.TlacidloIncDecVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj,yPixTlacidla,True,True,self.typPostavy,capTypPostavy,scale)
        
        
        #FARBA POSTAVY
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"Farba pleti",16,140+kraj+tlacidla+medzera,yPixTlacidla,scale)
        self.tlacidloSirkaMapy.click()
        capArr = [0,len(self.farbaTela)-1]
        objMenu.TlacidloIncDecVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj+tlacidla+medzera,yPixTlacidla,False,True,self.indexFarbyTela,capArr,scale)
        objMenu.TlacidloIncDecVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj+tlacidla+medzera,yPixTlacidla,True,True,self.indexFarbyTela,capArr,scale)
        
        #Cislo Oci
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"typ očí",16,140+kraj+tlacidla*2+medzera*2,yPixTlacidla,scale)
        self.tlacidloSirkaMapy.click()
        decCisloOci = objMenu.TlacidloIncDecValByVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj+tlacidla*2+medzera*2,yPixTlacidla,False,True,self.cisloOci,capCisloOci,self.cisloPohlavia,scale)
        objMenu.TlacidloIncDecValByVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj+tlacidla*2+medzera*2,yPixTlacidla,True,True,self.cisloOci,capCisloOci,self.cisloPohlavia,scale)
        
        #Cislo Vlasov
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"účes",16,140+kraj,yPixTlacidla+55,scale)
        self.tlacidloSirkaMapy.click()
        decCisloVlasov = objMenu.TlacidloIncDecValByVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj,yPixTlacidla+55,False,True,self.cisloVlasov,capCisloVlasov,self.cisloPohlavia,scale)
        objMenu.TlacidloIncDecValByVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj,yPixTlacidla+55,True,True,self.cisloVlasov,capCisloVlasov,self.cisloPohlavia,scale)
        
        #Typ tvare
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"Typ tváre",16,140+kraj+tlacidla+medzera,yPixTlacidla+55,scale)
        self.tlacidloSirkaMapy.click()
        objMenu.TlacidloIncDecVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj+tlacidla+medzera,yPixTlacidla+55,False,True,self.cisloTvare,capTypTvare,scale)
        objMenu.TlacidloIncDecVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj+tlacidla+medzera,yPixTlacidla+55,True,True,self.cisloTvare,capTypTvare,scale)
        
        
        #Pohlavie
        dataPreKontroluZmenyPohlavia = [decCisloOci,decCisloVlasov]
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"Pohlavie",16,140+kraj+tlacidla*2+medzera*2,yPixTlacidla+55,scale)
        self.tlacidloSirkaMapy.click()
        objMenu.TlacidloIncDecVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj+tlacidla*2+medzera*2,yPixTlacidla+55,False,True,self.cisloPohlavia,capPohlavia,scale,dataPreKontroluZmenyPohlavia)
        objMenu.TlacidloIncDecVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj+tlacidla*2+medzera*2,yPixTlacidla+55,True,True,self.cisloPohlavia,capPohlavia,scale,dataPreKontroluZmenyPohlavia)
        

        
    def refresh(self):
        for okno in self.oknaPostavy:
            okno.updateTextury()
        

        #s1.fill((255, 0, 0), None, pygame.BLEND_RGBA_MULT)
        
    def vykresliVlastnosti(self,screen):
        #scaleRec
        font = textury.dajFont(int(25*self.scaleRes))
        vlastnostiTypPostavy = nastavenia.VLASTNOSTI_POSTAVY_TYP_POSTAVY[self.typPostavy[0]]
        vlastnostiPohlavie = nastavenia.VLASTNOSTI_POSTAVY_POHLAVIE[self.cisloPohlavia[0]]  
        vlastnosti = nastavenia.VLASTNOSTI_POSTAVY
        pocetVlastnosti = 4
        x= 400*self.scaleRes
        y= 0
        
        for i in range (pocetVlastnosti):  
            y +=1
            self.vlastnosti[i] = vlastnostiTypPostavy[i] + vlastnostiPohlavie[i]      
            text = vlastnosti[i] + ": " + str(self.vlastnosti[i])                                  
            textSurf = font.render(text,1, nastavenia.BLACK)
            #textX = int(self.rect.width/3 - textSurf.get_width()/2)*self.scaleRes
            textY = 380 + 30*y 
            textY = textY*self.scaleRes
            screen.blit(textSurf,(x,textY))
            
            if y >= pocetVlastnosti / 2:
                x = 730 * self.scaleRes
                y = 0
            
            
        
        
    def draw(self, screen):
        menuOkno.MenuOkno.draw(self, screen)
        self.vykresliVlastnosti(screen)
        
        #uvodneNastavenia.Tlacidlo(self,[s1   ,s2],"",16,100,100,test,scale)
        

        
        
        
     