'''
Created on 23. 3. 2017

@author: T.Filip
'''
import Postavy.postava as postava
import pygame
import random
from Postavy.stavMobky import StavMobky
from Postavy import stavMobky
import nastavenia
from Postavy.smerPostavy import SmerPostavy
import math
from pip.status_codes import SUCCESS


class Npc(postava.Postava):
    def __init__(self,hra, surPix, sirka, vyska, textury = None, mapa = None):
        super().__init__(hra, surPix, sirka, vyska, False, textury, mapa)
        self.add(self.hra.dajGroupPreMobky())
        self.initStavMobky()
        
        
        self.spomalovanie = 0.02#v postave sa to inicializuje tu sa tomu len meni hodnota
        
        self.hlbaSpanku = 9
        self.nasledovat = None
        self.nahananaPostava = None
        self.dohlad = 200 #v pixeloch
        
        self.posunPostavyX = 0
        self.posunPostavyY = 0
        
        
    def initStavMobky(self):
        ran = random.random()
        if ran<0.2:
            self.stavMobky = StavMobky.SPI
        elif ran < 0.4:
            self.stavMobky = StavMobky.PRECHADZA_SA
        else:
            self.stavMobky = StavMobky.STOJI
        
        
        
        
    def update(self):
        self.posunPostavu(self.posunPostavyX, self.posunPostavyY)
        
    def zvysRychlostPohybu(self,horizontal,vertical):
        klavesy = self.hra.manazerOkien.klavesy
        if klavesy[pygame.K_LSHIFT] and self.jeSprintPovoleny:
            capRychlosti = [self.maxRychlostSprint*horizontal,self.maxRychlostSprint*vertical]
            self.smerPohybu[0] += self.zrychlenieSprint * vertical 
            self.smerPohybu[1] += self.zrychlenieSprint * horizontal 
            
        else:
            capRychlosti = [self.maxRychlost*horizontal,self.maxRychlost*vertical]
            self.smerPohybu[0] += self.zrychlenie * vertical 
            self.smerPohybu[1] += self.zrychlenie * horizontal
            
        return capRychlosti
    
    def updateZmenStav(self):
        #update v ktorom moze menit stav
        if self.stavMobky == StavMobky.SLEDUJE_HLUK:
            self.zmenStavSledujeHLuk()
        elif self.stavMobky == StavMobky.STOJI:
            self.zmenStavStoji()
        elif self.stavMobky == StavMobky.PRECHADZA_SA:
            self.zmenStavPrechadzka()
        elif self.stavMobky == StavMobky.NAHANA_HRACA:
            self.zmenStavNahanaHraca()
        elif self.stavMobky == StavMobky.SPI:
            self.zmenStavSpi()
            
            
        
        
        
    def zmenStavSpi(self):
        self.cekniHluk()
    
    
    def zmenStavStoji(self):
        ran = random.random()
        if ran < 0.02:
            self.stavMobky = StavMobky.SPI
            self.hlbaSpanku = random.randint(10,50)
        elif ran< 0.04:
            self.stavMobky = StavMobky.PRECHADZA_SA
            
        self.cekniHluk()
        self.cekniHraca()

        
    def zmenStavPrechadzka(self):
        ran = random.random()
        if ran < 0.2:
            self.stavMobky = StavMobky.STOJI
        self.cekniHluk()
        self.cekniHraca()
        
    
    
    def zmenStavSledujeHLuk(self):
        ran = random.random()
        if ran<0.1:
            self.stavMobky = StavMobky.PRECHADZA_SA
        self.cekniHraca()
        
        
    def zmenStavNahanaHraca(self):
        ran = random.random()
        if ran < 0.1:
            self.stavMobky = StavMobky.SLEDUJE_HLUK
            self.cekniHraca()
    
    
    
    def cekniHluk(self):
        hCent = self.hra.dajHlukoveCentra()
        hodnoty = self.hra.dajHodnotyHlukovychCentier()
        
        vyskaHluku = 0
        nasledovatel = None
        
        for cent in hCent:
            hod = hodnoty[cent[0]]
            leader = cent[0]
            vzdialenost = self.dajVzdialenostOdPostavy(leader)
            
            if vzdialenost <= 128:
                koefVzdialenosti = 1
            else:
                koefVzdialenosti = 128/vzdialenost
                
            hluk = hod*koefVzdialenosti
            if hluk>vyskaHluku:
                vyskaHluku = hluk
                nasledovatel = leader
                
        if vyskaHluku > self.hlbkaSpanku and random.random() < 0.75:
            self.nasledovatel = nasledovatel
            self.stavMobky = StavMobky.SLEDUJE_HLUK
            
            
            #ak ma na dohlad hraca prepne stav na nahananie
    def cekniHraca(self):
        hrac = self.hra.dajHraca()
        vzdialenost = self.dajVzdialenostOdPostavy(hrac)
        objHrac = hrac.dajObjOblastMapa()
        if self.dohlad < vzdialenost:
            return # je prilis daleko
        poz = [objHrac.centerx,objHrac.centery]
        poz[0] -= nastavenia.POLOVICNE_ROZLISENIA_X[nastavenia.vybrateRozlisenie]
        poz[1] -= nastavenia.POLOVICNE_ROZLISENIA_Y[nastavenia.vybrateRozlisenie]
        
        if poz[0]*2 >poz[1]:#pravo spodna cast
            if poz[0]*2 > -poz[1]:#pravohorna
                if self.smer == SmerPostavy.DOPRAVA:
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA
            else:
                if self.smer == SmerPostavy.DOZADU:
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA 
                
        else: #lavo horna
            if poz[0]*2 > -poz[1]:#pravohorna
                if self.smer == SmerPostavy.DOPREDU:
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA
            else:
                if self.smer == SmerPostavy.DOLAVA:
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA
                    
                    
    def smerPostavyPriStati(self):
        if self.stavMobky == StavMobky.SPI:
            self.smer = SmerPostavy.SPECIAL
            
        #inak ostava ako zostalo stat
        
        
    def mozeSprintovat(self):
        #ak je aspon v 50 dohladu
        if self.stavMobky == StavMobky.NAHANA_HRACA:
            vzdialenost = self.nahananaPostava.dajVzdialenostOdPostavy(self)
            if vzdialenost <= self.dohlad/2:
                return True
            
        return False
            

    def updateCinnostStavu(self):
        if self.stavMobky == StavMobky.SLEDUJE_HLUK:
            self.cinnostSledujHluk()
            print("sleduje hluk")
        elif self.stavMobky == StavMobky.STOJI:
            self.cinnostStoji()
            print("stoji")
        elif self.stavMobky == StavMobky.PRECHADZA_SA:
            self.cinnostPrechadzka()
            print("prech")
        elif self.stavMobky == StavMobky.NAHANA_HRACA:
            self.cinnostNahanaHraca()
            print("nahana")
        elif self.stavMobky == StavMobky.SPI:
            self.cinnostSpi()
            print("spri")
            
            
    def cinnostSledujHluk(self):
        ret = self.dajSmerNaPostavu(self.nasledovatel)
        self.posunPostavyX = ret[0]
        self.posunPostavyY = ret[1]
        
        
    
    def cinnostStoji(self):
        self.posunPostavyX = 0
        self.posunPostavyY = 0
    
    def cinnostPrechadzka(self):
        #novy vektor
        self.posunPostavyX = random.random()-0.5
        self.posunPostavyY = random.random()-0.5
        #priemer vektorov
        self.posunPostavyX = self.posunPostavyX/2
        self.posunPostavyY = self.posunPostavyY/2
        

    def cinnostNahanaHraca(self):
        ret = self.dajSmerNaPostavu(self.nahananaPostava)
        self.posunPostavyX = ret[0]
        self.posunPostavyY = ret[1]
        
        
    def dajSmerNaPostavu(self,postava):
        objNasl = postava.dajObjOblastMapa()
        xDir = math.fabs(objNasl.centerx - self.dajObjOblastMapa().centerx)
        yDir = math.fabs(objNasl.centery - self.dajObjOblastMapa().centery)
        suc = xDir + yDir
        return (xDir/suc,yDir/suc)

        
            
    def cinnostSpi(self):
        self.cinnostStoji()
        self.smer = SmerPostavy.SPECIAL
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
    