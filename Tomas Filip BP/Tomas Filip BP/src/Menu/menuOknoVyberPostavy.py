'''
Created on 4. 3. 2017

@author: T.Filip
'''
import Menu.menuOkno as menuOkno
import uvodneNastavenia 
import textury 
import nastavenia
import pygame
import Menu.objMenu as objMenu
from enum import IntEnum
import sys
import Postavy.smerPostavy as smerPostavy
import Menu.enumOknaMenu as enumOknaMenu






    
class TypPostavy(IntEnum):
    UZKA = 0
    FIT = 1
    SILNA = 2

def back(self):
        self.menu.prepniMenu(enumOknaMenu.EnumOknaMenu.ZAKLADNE_MENU)

def hracUpdate(self):
    im = self.menu.frame.copy()
    postavy = self.menu.postavy
    tvare = self.menu.tvare
    
    #postava = pygame.Surface((64,64),pygame.SRCALPHA)
    
    smerPostavy = self.args[0]
    if smerPostavy==4:
        smerPostavy = 2
    #telo
    postavaMala = pygame.Surface((64,64),pygame.SRCALPHA)
    postavaMala.blit(postavy,(0,0),(int(64*smerPostavy),int(64*self.menu.typPostavy[0]),64,64))
    #farbatela
    farbaPostavy = pygame.Surface((64,64),pygame.SRCALPHA)
    farbaPostavy.blit(postavy,(0,0),(int(64*smerPostavy+256),int(64*self.menu.typPostavy[0]),64,64))
    farbaPostavy.fill(self.menu.farbaTela[self.menu.indexFarbyTela[0]], None, pygame.BLEND_RGBA_MULT)
    
    postavaMala.blit(farbaPostavy,(0,0))
    
    #HLAVA
    hlava = pygame.Surface((32,32),pygame.SRCALPHA)
    hlava.blit(tvare,(0,0),(64*self.menu.cisloTvare[0],0,32,32))
    
    #farbaHlavy
    farbaHlavy = pygame.Surface((32,32),pygame.SRCALPHA)
    farbaHlavy.blit(tvare,(0,0),(32+ 64*self.menu.cisloTvare[0],0,32,32))
    farbaHlavy.fill(self.menu.farbaTela[self.menu.indexFarbyTela[0]], None, pygame.BLEND_RGBA_MULT)

    
    hlava.blit(farbaHlavy,(0,0))
    
    #oci
    hlava.blit(tvare,(0,0),(int(32*smerPostavy+256*self.menu.cisloPohlavia[0]),int(32+32*self.menu.cisloOci[0]),32,32))
    #vlasy
    hlava.blit(tvare,(0,0),(int(32*smerPostavy+128+256*self.menu.cisloPohlavia[0]),int(32+32*self.menu.cisloVlasov[0]),32,32))

    
    if smerPostavy==2:
        posHlava = (12,4)
    else:
        posHlava = (16,4)
        
    postavaMala.blit(hlava,posHlava)
    
    if self.args[0] == 4:
        postavaMala = pygame.transform.flip(postavaMala, True, False)
    
    self.menu.postavyHrac[self.args[0]] = postavaMala
    
    #pygame.transform.scale(postavaMala,(64,64),postava)
    #pygame.transform.scale2x(postavaMala,postava)
    
    
    
    im.blit(postavaMala,(8,8))
    
    return im
    
    
def startHry(self):
    self.menu.prepniMenu(None)
    self.menu.manazerOkien.vytvorHru(self.menu.postavyHrac)
    
    
    

class MenuOknoVyberPostavy(menuOkno.MenuOkno):
    def __init__(self,manazerOkien,scale):

        super().__init__(manazerOkien,scale)
        
        self.postavy = pygame.image.load('img\\Postavy\\postavyNew.png').convert_alpha()  
        self.tvare = pygame.image.load('img\\Postavy\\tvareNew.png').convert_alpha() 
        self.frame = pygame.image.load('img\\Postavy\\frame.png').convert_alpha() 
        

        
        objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"START",16,525,600,startHry,scale)
        objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene],"BACK",16,655,600,back,scale)
        
        
                #vcetne
        capTypPostavy = [0,2]
        #capSmerPostavy = 4
        
        #MUZ - 0 ZENA - 1
        capPohlavia = [0,1]
        capCisloOci = [[0,1],[0,1]]
        capCisloVlasov = [[0,1],[0,1]]
        capTypTvare = [0,1]
        
        
        
        self.farbaTela = [(255,220,100),(255,220,140),(253,210,130),(216,170,130),(200,140,100),(180,110,60),(140,90,50)] 
        self.indexFarbyTela = [2]
        self.cisloOci = [0]
        self.cisloVlasov = [0]
        self.cisloTvare = [0]
        self.cisloPohlavia = [0]
        
        self.typPostavy = [TypPostavy.SILNA]
        
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
        
        #TYP POSTAVY init__(self,Menu,imgs,text,font,sirka,vyska,zvysovatHore,cykliSa,hodnota,cap,scale = 1):
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
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"typ oci",16,140+kraj+tlacidla*2+medzera*2,yPixTlacidla,scale)
        self.tlacidloSirkaMapy.click()
        decCisloOci = objMenu.TlacidloIncDecValByVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj+tlacidla*2+medzera*2,yPixTlacidla,False,True,self.cisloOci,capCisloOci,self.cisloPohlavia,scale)
        objMenu.TlacidloIncDecValByVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj+tlacidla*2+medzera*2,yPixTlacidla,True,True,self.cisloOci,capCisloOci,self.cisloPohlavia,scale)
        
        #Cislo Vlasov
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"uces",16,140+kraj,yPixTlacidla+55,scale)
        self.tlacidloSirkaMapy.click()
        decCisloVlasov = objMenu.TlacidloIncDecValByVal(self,[textury.TUN1left,textury.TUN1leftOznacene],"",16,85+kraj,yPixTlacidla+55,False,True,self.cisloVlasov,capCisloVlasov,self.cisloPohlavia,scale)
        objMenu.TlacidloIncDecValByVal(self,[textury.TUN1right,textury.TUN1rightOznacene],"",16,275+kraj,yPixTlacidla+55,True,True,self.cisloVlasov,capCisloVlasov,self.cisloPohlavia,scale)
        
        #Typ tvare
        self.tlacidloSirkaMapy = objMenu.objMenu(self,[textury.TUN1center],"Typ tvare",16,140+kraj+tlacidla+medzera,yPixTlacidla+55,scale)
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
        
        
        
        #uvodneNastavenia.Tlacidlo(self,[s1   ,s2],"",16,100,100,test,scale)
        

        
        
        
     