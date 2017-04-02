import pygame
import ObjektyMapa.objMapa as objMapa
import ObjektyMapa.scale as scale
import random
from tkinter.constants import HORIZONTAL
import logging
import Postavy.smerPostavy as smerPostavy
import Predmety.inventar as inventar
from Predmety import invVyuzPredmetu
import Predmety.predmet as predmet
from Postavy.enumTypPostavy import EnumTypPostavy
from Postavy.smerPostavy import SmerPostavy
import nastavenia
from Postavy import postava
from Textury import textury
from Textury import enumTextura




class Hrac(postava.Postava):
    def __init__(self,hra,surPix, typP,textury,vlastnosti,sirka,vyska):
        self.typPostavy = typP[0]
        super().__init__(hra,surPix,sirka,vyska,True,textury,None,vlastnosti)
        
        
        #LEVEL
        self.skusenosti = 0
        self.dalsiLevelNaSkusenostiach = 1000
        self.levelHraca = 1
        #

        
        #SKUSENOSTI
        #SKUSENOSTI VYROBA: 0-SEKERA, 1-KRUMPAC, 2-MEC, VYUZIVANIE: 3-SEKERA, 4-KRUMPAC, 5-MEC...
        self.zrucnosti = [[0],[0],[0],[0],[0],[0],[0]]#zaobalene v poli aby som sa na to mohol odkazovat ako na objekt
        self.volneZrucnosti = [10]
        
        

        
        self.inventar = inventar.Inventar(20)
        self.inventarRychlyPristup = invVyuzPredmetu.InvVyuzPredmetu(9,self)
        
        self.vlozPredmety()
        
    def dajSkusenosti(self):
        return self.skusenosti
    
    def dajZrucnosti(self):
        return self.zrucnosti
    
    def dajVolneZrucnosti(self):
        return self.volneZrucnosti

        

    def zvysSkusenosti(self,oKolko):
        self.skusenosti +=oKolko
        if self.skusenosti > self.dalsiLevelNaSkusenostiach:
            self.levelHraca += 1
            self.skusenosti -= self.dalsiLevelNaSkusenostiach
            self.dalsiLevelNaSkusenostiach = int(self.dalsiLevelNaSkusenostiach * 1.4)
            self.maxZdravie += 1 
            self.volneVlastnosti[0] += 1
            self.volneZrucnosti[0] += 5
            

    
    def dajLevel(self):
        return self.levelHraca
    

    
    def dajDalsiLevelNaSkusenostiach(self):
        return self.dalsiLevelNaSkusenostiach
    
    def linkMapa(self,mapa):
        self.mapa = mapa
        self.inventarRychlyPristup.linkMapa(self.mapa)
        

    
    def vlozPredmet(self,predmet):
        self.inventar.vlozPredmet(predmet)

    def vlozPredmety(self):
        self.inventar.vlozPredmet(predmet.Predmet(10,12))
        self.inventar.vlozPredmet(predmet.Predmet(13,15))
        self.inventar.vlozPredmet(predmet.Predmet(12,50))
        self.inventar.vlozPredmet(predmet.Predmet(13,2))
        self.inventar.vlozPredmet(predmet.Predmet(13,36))
        self.inventar.vlozPredmet(predmet.Predmet(2000,50))
        self.inventar.vlozPredmet(predmet.Predmet(3001,1))
        self.inventar.vlozPredmet(predmet.Predmet(3000,1))

        
        self.inventarRychlyPristup.vlozPredmet(predmet.Predmet(5,36))
        self.inventarRychlyPristup.vlozPredmet(predmet.Predmet(4000,20))
        self.inventarRychlyPristup.vlozPredmet(predmet.Predmet(3000,1))
        self.inventarRychlyPristup.vlozPredmet(predmet.Predmet(3011,1))
        
    def dajInventarRychlyPristup(self):
        return self.inventarRychlyPristup
    




            
            
        
        
    def initMapu(self): # po inicializovani mapy
        self.dajNoveOkolie()
        

        

    def update(self, *args):
        super().update(args)
        self.inventarRychlyPristup.update()
        print(self.zdravie)
        


        
        
        

        

            

        
        
    def eventy(self):
        
        if not self.jeMrtvy:
            posun = [0,0]
            klavesy = self.hra.manazerOkien.dajKlavesy()
            if klavesy[pygame.K_UP] or klavesy[pygame.K_w]:
                posun[1] +=-1
                
            if klavesy[pygame.K_DOWN] or klavesy[pygame.K_s]:
                posun[1] +=1
                
            if klavesy[pygame.K_LEFT] or klavesy[pygame.K_a]:
                posun[0] +=-1
                
            if klavesy[pygame.K_RIGHT] or klavesy[pygame.K_d]:
                posun[0] +=1
               
            logging.info("Hrac-posunPostavu") 
        
        
            self.posunPostavu(posun[0],posun[1])
        #print (posun)

        
        self.topLeftScaleMap[0] = self.rectTextOblastMapa.x*self.hra.mapa.dajNas()
        self.topLeftScaleMap[1] = self.rectTextOblastMapa.y*self.hra.mapa.dajNas()
        self.topLeftNoScaleMap[0] = self.rectTextOblastMapa.x
        self.topLeftNoScaleMap[1] = self.rectTextOblastMapa.y
        
        logging.info("hrac->mapa-nacitajPolicka")
        self.hra.mapa.nacitajPolicka(self)
        
        


        


    def zmenVyznacenyPredmet(self,cislo):
        self.inventarRychlyPristup.zmenOznacenie(cislo)
        
        
    def klikButton1(self):
        self.inventarRychlyPristup.leftClick()
    def klikButton2(self):
        pass
    def klikButton3(self):
        self.inventarRychlyPristup.rightClick()
    def klikButton4(self):
        pass
    def klikButton5(self):
        pass 
        
    def dajPredmetVRuke(self):
        return self.inventarRychlyPristup.dajOznacenyPredmet()
        


    def stlacena0(self):
        pass #na nule nic nerobim zatial
        
    def stlacena1(self):
        self.zmenVyznacenyPredmet(1)
        
    def stlacena2(self):
        self.zmenVyznacenyPredmet(2)
        
    def stlacena3(self):
        self.zmenVyznacenyPredmet(3)
        
    def stlacena4(self):
        self.zmenVyznacenyPredmet(4)
        
    def stlacena5(self):
        self.zmenVyznacenyPredmet(5)
        
    def stlacena6(self):
        self.zmenVyznacenyPredmet(6)
        
    def stlacena7(self):
        self.zmenVyznacenyPredmet(7)
        
    def stlacena8(self):
        self.zmenVyznacenyPredmet(8)
        
    def stlacena9(self):
        self.zmenVyznacenyPredmet(9)
        
    def stlaceneR(self):
        self.inventarRychlyPristup.stlaceneR()
        
    def vykresliOznacenyPredmet(self,screen):
        self.inventarRychlyPristup.draw(screen)
        
    def smerPostavyPriStati(self):
        pos = pygame.mouse.get_pos()
        mousePos = [pos[0],pos[1]]
        mousePos[0] -= nastavenia.POLOVICNE_ROZLISENIA_X[nastavenia.vybrateRozlisenie]
        mousePos[1] -= nastavenia.POLOVICNE_ROZLISENIA_Y[nastavenia.vybrateRozlisenie]
        if mousePos[0]*2 >mousePos[1]:#pravo spodna cast
            if mousePos[0]*2 > -mousePos[1]:#pravohorna
                self.smer = smerPostavy.SmerPostavy.DOPRAVA
            else:
                self.smer = smerPostavy.SmerPostavy.DOZADU
                
        else: #lavo horna
            if mousePos[0]*2 > -mousePos[1]:#pravohorna
                self.smer = smerPostavy.SmerPostavy.DOPREDU
            else:
                self.smer = smerPostavy.SmerPostavy.DOLAVA
                
                
    def mozeSprintovat(self):
        klavesy = self.hra.manazerOkien.klavesy
        if klavesy[pygame.K_LSHIFT]:
            return True
        else:
            return False
        
        
        