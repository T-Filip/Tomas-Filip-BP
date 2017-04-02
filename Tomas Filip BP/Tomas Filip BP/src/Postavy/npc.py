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
import time
from generator import GeneratorNescalovany
from Postavy.enumTypPostavy import EnumTypPostavy




class Npc(postava.Postava):
    def __init__(self,hra, surPix, sirka, vyska, textury = None, mapa = None):
        super().__init__(hra, surPix, sirka, vyska, False, textury, mapa)
        self.add(self.hra.dajGroupPreMobky())
        self.initStavMobky()
        
        self.moduloKusanie = random.randint(0,99)#sanca na kusnutie sa odohrava raz za sekundu .. aby sa kazda mobka nesnazila o kusnutie naraz 
        
        self.spomalovanie = 0.02#v postave sa to inicializuje tu sa tomu len meni hodnota
        
        self.hlbkaSpanku = 9
        self.nasledovat = None
        self.nahananaPostava = None
        self.dohlad = 200 #v pixeloch
        
        self.posunPostavyX = 0
        self.posunPostavyY = 0
        
        
        
        #Prechadzka
        self.casPrechadzania = 0
        self.tickPrechadzania = 9999
        self.a = random.randint(300,800)
        self.b = random.random()/2+0.25
        self.initGeneratoraPreChodenie()
        ##########
        
        
    def prestanNahanat(self,postava):
        if self.nahananaPostava == postava:
            self.stavMobky = StavMobky.STOJI
        
    def initGeneratoraPreChodenie(self):
        self.generatorPohybu = GeneratorNescalovany(random.random(),self.a,self.b)

        
    def initStavMobky(self):
        ran = random.random()
        self.stavMobky = StavMobky.PRECHADZA_SA
        return
        if ran<0.05:
            self.stavMobky = StavMobky.SPI
        elif ran < 0.4:
            self.stavMobky = StavMobky.PRECHADZA_SA
        else:
            self.stavMobky = StavMobky.STOJI
        
        
    def reinitVlastnosti(self):
        self.capVydrz = self.vlastnosti[3][0]*20+100
        
        self.maxRychlostSprint = 0.2+self.vlastnosti[2][0]*0.1
        self.maxRychlost = 0.1+self.vlastnosti[2][0]*0.05
        self.zrychlenie = self.maxRychlost/16
        self.zrychlenieSprint = self.maxRychlostSprint/12
        
        self.spomalovanie = 0.15 # ako rychlo clovek brzdi 
        if self.typPostavy == EnumTypPostavy.SILNA:
            self.spomalovanie = 0.2
        elif self.typPostavy == EnumTypPostavy.FIT:
            self.spomalovanie = 0.18
        elif self.typPostavy == EnumTypPostavy.UZKA:
            self.spomalovanie = 0.16
        
        self.smerPohybu=[0,0]
        self.jeSprintPovoleny = True
        self.jeKoliznyStav = False
        self.obnovovanieVydrze = 0.2+self.vlastnosti[3][0]*0.1
        self.koliznySmerPohybu = [0,0]
        self.koeficienRychlosti = 1
        
        self.priemSucKoefRychl = 0
        self.pocKoefRychlosti = 0
        
    def update(self,*args):
        super().update(args)
        if not self.jeMrtvy:
            self.posunPostavu(self.posunPostavyX, self.posunPostavyY)
        

            
        
    def zvysRychlostPohybu(self,horizontal,vertical):
        if self.mozeSprintovat() and self.jeSprintPovoleny:
            capRychlosti = [math.fabs(self.maxRychlostSprint*horizontal),math.fabs(self.maxRychlostSprint*vertical)]
            self.smerPohybu[0] += self.zrychlenieSprint * horizontal 
            self.smerPohybu[1] += self.zrychlenieSprint * vertical 
            
        else:
            capRychlosti = [math.fabs(self.maxRychlost*horizontal),math.fabs(self.maxRychlost*vertical)]
            #print(self.zrychlenie * horizontal )
            self.smerPohybu[0] += self.zrychlenie * horizontal 
            self.smerPohybu[1] += self.zrychlenie * vertical
            
        return capRychlosti
    
    def updateZmenStav(self):
        #update v ktorom moze menit stav
        #print("update stav")
        #print(self.smer)
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
            
        #vykonava sa menej casto preto vydavanie zvuku tuna ale kusok vyssie percenta
                #npc moze vydat nejaky zvuk
        nah =random.random() 
        if nah < 0.02:
            self.vydavanyHluk += 50
        elif nah < 0.05:
            self.vydavanyHluk += 30
        elif nah < 0.1:
            self.vydavanyHluk += 10
            
            
        
        
        
    def zmenStavSpi(self):
        self.cekniHluk()
    
    
    def zmenStavStoji(self):
        ran = random.random()
        if ran < 0.0:
            self.stavMobky = StavMobky.SPI
            self.hlbaSpanku = random.randint(10,50)
        elif ran< 0.10:
            self.stavMobky = StavMobky.PRECHADZA_SA
            
        self.cekniHluk()
        self.cekniHraca()

        
    def zmenStavPrechadzka(self):
        ran = random.random()
        if ran < 0.1:
            self.stavMobky = StavMobky.STOJI
        self.cekniHluk()
        self.cekniHraca()
        
    
    
    def zmenStavSledujeHLuk(self):
        ran = random.random()
        if ran<0.1:
            self.stavMobky = StavMobky.PRECHADZA_SA
        self.cekniHluk()#ak by bol iny, vacsi zdroj hluku
        self.cekniHraca()
        
        
    def zmenStavNahanaHraca(self):
        ran = random.random()
        if ran < 0.15:
            self.stavMobky = StavMobky.SLEDUJE_HLUK
            self.nasledovatel = self.nahananaPostava
            self.cekniHraca()
            if self.stavMobky != StavMobky.NAHANA_HRACA:
                group = self.hra.dajGroupMobkyNahanajuceHraca()
                group.remove(self)
    
    
    
    def cekniHluk(self):
        if random.random() < 0.4:
            return
        hCent = self.hra.dajHlukoveCentra()
        hodnoty = self.hra.dajHodnotyHlukovychCentier()
        
        vyskaHluku = 0
        nasledovatel = None
        
        for cent in hCent.values():
            hod = hodnoty[cent[0]]
            leader = cent[0]
            if leader == self:
                continue
            vzdialenost = self.dajVzdialenostOdPostavy(leader)
            
            if vzdialenost <= 128:
                koefVzdialenosti = 1
            else:
                koefVzdialenosti = 128/vzdialenost
                
            hluk = hod*koefVzdialenosti
            if hluk>vyskaHluku:
                vyskaHluku = hluk
                nasledovatel = leader
                
        if self.stavMobky == StavMobky.SPI:
            if vyskaHluku > self.hlbkaSpanku:
                self.nasledovatel = nasledovatel
                self.stavMobky = StavMobky.SLEDUJE_HLUK
        else:
            if nasledovatel == None:
                self.nasledovat = None
            
            else:
                self.nasledovatel = nasledovatel
                self.stavMobky = StavMobky.SLEDUJE_HLUK
            
            
            #ak ma na dohlad hraca prepne stav na nahananie
    def cekniHraca(self):
        hrac = self.hra.dajHraca()
        vzdialenost = self.dajVzdialenostOdPostavy(hrac)
        objHrac = hrac.dajObjOblastMapa()
        #print("CEKUJEM HRACA")
        #print("pozeram sa na " + str(self.smer))
        if self.dohlad < vzdialenost:
            #print("je prilis daleko")
            return # je prilis daleko
        poz = [objHrac.centerx,objHrac.centery]
        poz[0] -= self.rectObjOblast.centerx
        poz[1] -= self.rectObjOblast.centery
        
        if poz[0]*2 >poz[1]:#pravo spodna cast
            if poz[0]*2 > -poz[1]:#pravohorna
                #print("hrac je vpravo")
                if self.smer == SmerPostavy.DOPRAVA:
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA
                    
            else:
                #print("hrac je vzadu")
                if self.smer == SmerPostavy.DOZADU:
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA 
                
        else: #lavo horna
            if poz[0]*2 > -poz[1]:#pravohorna
                if self.smer == SmerPostavy.DOPREDU:
                    #print("hrac je vpredu")
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA
            else:
                #print("hrac je vlavo")
                if self.smer == SmerPostavy.DOLAVA:
                    self.nahananaPostava = hrac
                    self.stavMobky = StavMobky.NAHANA_HRACA
                    
        group = self.hra.dajGroupMobkyNahanajuceHraca()
        self.add(group)
        
                    
                    
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
            #print("sleduje hluk")
        elif self.stavMobky == StavMobky.STOJI:
            self.cinnostStoji()
            #print("stoji")
        elif self.stavMobky == StavMobky.PRECHADZA_SA:
            self.cinnostPrechadzka()
            #print("prech")
        #elif self.stavMobky == StavMobky.NAHANA_HRACA:
            #self.cinnostNahanaHraca()  ## cinnost hraca ked nahana sa vykonava pravidelne v kazdom update nakolko je nuttne aby jeho pohyb bol updatovany casto
            #print("nahana")
        elif self.stavMobky == StavMobky.SPI:
            self.cinnostSpi()
            #print("spri")
            
            
    def cinnostSledujHluk(self):
        ret = self.dajSmerNaPostavu(self.nasledovatel)
        self.posunPostavyX = ret[0]
        self.posunPostavyY = ret[1]
        
        
    
    def cinnostStoji(self):
        self.posunPostavyX = 0
        self.posunPostavyY = 0
    
    def cinnostPrechadzka(self):

        if self.casPrechadzania < time.time():
            self.initGeneratoraPreChodenie()#len zmeni seed
            noiseX = self.generatorPohybu.noise(self.tickPrechadzania, 0)
            noiseY = self.generatorPohybu.noise(0,self.tickPrechadzania)
            noise = math.fabs(noiseX) + math.fabs(noiseY) + 0.1 # ak by nahodou bolo blizko 0
            noise = noise**2
            self.casPrechadzania = time.time()+1/noise


            
        self.tickPrechadzania += 1
        self.posunPostavyX = self.generatorPohybu.noise(self.tickPrechadzania, 0)/3
        self.posunPostavyY = self.generatorPohybu.noise(0, self.tickPrechadzania)/3
        
        #print("---------------")
        #print(self.posunPostavyX)
        #print(self.posunPostavyY)

        
    

        

        

    def cinnostNahanaHraca(self,modulo100):
        if self.nahananaPostava == None:
            return
        ret = self.dajSmerNaPostavu(self.nahananaPostava)
        vzdialenost = self.dajVzdialenostOdPostavy(self.nahananaPostava)
        if vzdialenost>70:
            self.posunPostavyX = ret[0]
            self.posunPostavyY = ret[1]
        else:
            koef = vzdialenost/70
            self.posunPostavyX = ret[0]*koef
            self.posunPostavyY = ret[1]*koef
            if self.moduloKusanie == modulo100:
                if random.random() > koef:
                    self.nahananaPostava.udelPoskodenie(int(random.gauss(10,5)))
        
    def ublizNahananejPostave(self,postava):
        pass
        
    def dajSmerNaPostavu(self,postava):
        objNasl = postava.dajObjOblastMapa()
        xDir = objNasl.centerx - self.dajObjOblastMapa().centerx
        yDir = objNasl.centery - self.dajObjOblastMapa().centery
        suc = math.fabs(xDir) + math.fabs(yDir)
        if suc == 0:
            ret = (0,0)
        else:
            ret =  (xDir/suc,yDir/suc)
        return ret

        
            
    def cinnostSpi(self):
        self.cinnostStoji()
        self.smer = SmerPostavy.SPECIAL
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
    