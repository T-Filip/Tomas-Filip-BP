'''
Created on 8. 2. 2017

@author: T.Filip
'''
import nastavenia
import policko
import generator
import pygame
import random
import ObjektyMapa.infObjekty as infObjekty
import mapa as mapa
import logging
from threading import Thread
import math

SINGLETON_MAPA = None #prva mapa .... 

class vytvoreniePolicka:
    def __init__(self,x,y,xCoord,yCoord):
        self.x=x
        self.y=y
        self.xCoord = xCoord
        self.yCoord = yCoord
        
    
    def vytvorPolicko(self,mapa):
        mapa.mapa[self.x][self.y] = mapa.vytvorPolickoNa(self.xCoord,self.yCoord)
        
class initStage2Task:
    def __init__(self,policko):
        self.policko = policko
        
    def initStage2(self):
        self.policko.initStage2()
            


class Mapa:
    def __init__(self,hra):
        if mapa.SINGLETON_MAPA == None:
            mapa.SINGLETON_MAPA = self
        

        self.hra=hra
        self.hrac = hra.hrac
        self.thread = Thread()
        
        
        #atributy ktore uchovavaju stav nacitania a pomocne informacie pre nacitanie
        self.stavNacitania = 0
        self.smerNacitania = 0
        self.prebiehaNacitavanie = False
        self.yStage2 = 0
        self.xStage2 = 0
        self.pomocnaHrana = 0

        
        
        logging.info("init pola mapy")
        self.mapa = [[0 for xPos in range(nastavenia.MAP_SIZE_Y)] for yPos in range(nastavenia.MAP_SIZE_X)] 
        self.topLeftMapa = [0,0]
        self.topLeftCoord = [0,0]
        self.okolieMysly = pygame.sprite.Group()
        #self.lavoHorePixelKamera= [0,0]
        self.starePolickoveSurMysky = [0,0]
        self.zoom = 64 #zakladny zoom
        self.menilSaZoom = False
        self.scaleNasobitel =1
        self.okolieMysky = pygame.sprite.Group()
        #self.minulaPoziciaHraca = [0,0]
        logging.info("initKamera")
        self.initKamera()
        self.Test = pygame.image.load('img/Test32.png').convert()
        self.polickoveSurMysky = [0,0]
        
        #self.generator = generator.Generator(1234)
        logging.info("init generatorov")
        self.inicializaciaGeneratorov()
        logging.info("nacitanie mapy")
        self.nacitajMapu()
        
        self.topLeftNoScale = [0,0] # pozicia kamery v nescalovanom svete pix suradnice jej laveho horneho rohu
        
        logging.info("vytvorenie mapy hotovo")
        
        self.zoomZotrvacnost = 0


    def dajMyskuNaMape(self):
        scale = self.dajScaleNas()
        pos = pygame.mouse.get_pos()
        
        rectTextObjMapaHraca = self.hrac.dajTextOblastMapa()
        rectHraca = self.hrac.dajRect()
        #nacitanaMapa = self.dajNacitanuMapu()
        #rectTopLeftPolicka = self.dajTopLeftMin2Policko().dajRect()
        #relatMysX= pos[0] - rectTopLeftPolicka.x + rectTopLeftPolicka.width*2
        #relatMysY= pos[1] - rectTopLeftPolicka.y + rectTopLeftPolicka.height*2

        #relatMysX = relatMysX/scale
        #relatMysY = relatMysY/scale
        #ret = [relatMysX + nacitanaMapa.x,relatMysY + nacitanaMapa.y]
        #ret = [pos[0]/scale + nacitanaMapa.x,pos[1]/scale + nacitanaMapa.y]
        ret = [(pos[0] - rectHraca.x)/scale + rectTextObjMapaHraca.x,(pos[1] - rectHraca.y)/scale + rectTextObjMapaHraca.y]
        return ret
        

        

    def updateZoom(self):
        
        
        if self.zoomZotrvacnost == 0:
            return
        
        #print("Zotrvacnost")
        #print(self.zoomZotrvacnost)
        self.zoom += int(round(self.zoomZotrvacnost*0.25))
        if self.zoom < 32:
            self.zoom = 32
            self.zoomZotrvacnost = 0
        if self.zoom > 386:
            self.zoom = 386
            self.zoomZotrvacnost = 0
        self.scaleNasobitel = self.zoom /64
        self.menilSaZoom = True
        if self.zoomZotrvacnost>0:
            self.zoomZotrvacnost -= self.zoomZotrvacnost*0.25
            
        if self.zoomZotrvacnost<0:
            self.zoomZotrvacnost -= self.zoomZotrvacnost*0.25
            
        if self.zoomZotrvacnost < 1 and self.zoomZotrvacnost > -1:
            self.zoomZotrvacnost = 0
            

    def dajTopLeftMin2Policko(self):
        sur = self.mapa[self.topLeftMapa[0]][self.topLeftMapa[1]].dajSuradnice()
        #print("suradnice top left mapa :" + str(self.topLeftMapa))
        #print("suradnice top left mapa policko coord:" + str(sur))
        surRoh = [0,0]
        surRoh[0] = sur[0] + 2
        surRoh[1] = sur[1] + 2
        return self.dajPolicko(surRoh)

        
    def zvysZoom(self, i):
        self.zoomZotrvacnost += self.zoom/64 *16
        
    def znizZoom(self, i): 
        self.zoomZotrvacnost -= self.zoom/64 *16
        
    def inicializaciaGeneratorov(self):
        self.random = random.Random(nastavenia.SEED)
        self.generatorBiom = [0 for x in range (0,6)]
        for b in range (0,6):
            self.generatorBiom[b] = generator.Generator(self.random.random())#*9223372036854775807
        self.noiseGen = [generator.Generator(self.random.random(),500,0.3),generator.Generator(self.random.random(),800,0.4),generator.Generator(self.random.random(),800,0.4)]
        
        self.generatorPreMobky = generator.Generator(self.random.random(),150,0.95)
        
    def dajNoiseMobkaNa(self,x,y):
        return self.generatorPreMobky.noise(x, y)
        
    def dajZoom(self):
        return self.zoom
    def dajScaleNas (self):
        return self.scaleNasobitel
    
    def updatePolickoveSuradniceMysky(self):
        #ulozi suradnice policka na ktore ukazuje myska
        pos = pygame.mouse.get_pos()
        x = self.kamera.x + pos[0]
        y = self.kamera.y + pos[1]
        self.polickoveSurMysky = [int(x/self.zoom),int(y/self.zoom)]

        
    def dajPolickoveSurMysky(self):
        return self.polickoveSurMysky
    
    def update(self):
        self.updatePolickoveSuradniceMysky()
        self.skontrolujPolickoNaMyske()
        
    def dajNas(self):
        return self.scaleNasobitel
    
    def nacitajPolicka(self,hrac):
        #ak sa hrac pohol prilis istym smerom je potrebne nacitat nove policka 
        #hracy =hrac.rectTextOblastMapa.centery
        #mapay = self.nacitanaMapa.centery 
        
        
        if self.prebiehaNacitavanie:
            #print("A")
            if self.smerNacitania == 3:
                self.nacitajPolickaHorePostupne()
            elif self.smerNacitania == 2:
                self.nacitajPolickaVlavoPostupne()
            elif self.smerNacitania == 1:
                self.nacitajPolickaVpravoPostupne()
            elif  self.smerNacitania == 0:
                self.nacitajPolickaDolePostupne()
            
        else:
            #print("B")
            rozdiel = hrac.rectTextOblastMapa.centerx - self.nacitanaMapa.centerx 
            rozdiel2 = hrac.rectTextOblastMapa.centery - self.nacitanaMapa.centery 
            i = 0
            absRozdiel = math.fabs(rozdiel)
            absRozdiel2 = math.fabs(rozdiel2)
            if absRozdiel > absRozdiel2:
                if rozdiel > 32: 
                    i += 1
                    logging.info("Mapa-nacitajPolicka Vpravo")
                    hrac.suradnice[0]+=1
                    #if not self.thread.isAlive():
                    #    self.thread=Thread(target = self.nacitajPolickaVpravo)
                    #    self.thread.start()
                    #self.nacitajPolickaVpravo()
                    self.nacitajPolickaVpravoInit()
                    
                    
                        
                elif rozdiel < -32:
                    logging.info("Mapa-nacitajPolicka VLavo")
                    hrac.suradnice[0]-=1
                    #if not self.thread.isAlive():
                    #    self.thread=Thread(target = self.nacitajPolickaVlavo)
                    #    self.thread.start()
                    #self.nacitajPolickaVlavo()
                    self.nacitajPolickaVlavoInit()
                    self.nacitajPolickaVlavoPostupne()
                    
                if absRozdiel > 128:
                    self.nacitajPolicka(hrac)
    
            else:
            
                if rozdiel2 > 32:
                    logging.info("Mapa-nacitajPolicka Dole")
                    hrac.suradnice[1]+=1
                    #if not self.thread.isAlive():
                    #    self.thread=Thread(target = self.nacitajPolickaDole)
                    #    self.thread.start()
                    #self.nacitajPolickaDole()
                    self.nacitajPolickaDoleInit()
                    self.nacitajPolickaDolePostupne()
        
        
                    
                elif rozdiel2 < -32:
                    logging.info("Mapa-nacitajPolicka Hore")
                    hrac.suradnice[1]-=1
                    #if not self.thread.isAlive():
                    #    self.thread=Thread(target = self.nacitajPolickaHore)
                    #    self.thread.start()
                    
                    #self.nacitajPolickaHore()
                    self.nacitajPolickaHoreInit()
                    self.nacitajPolickaHorePostupne()
                    #self.nacitajPolickaHorePostupne()
                    
                if absRozdiel2 > 128:
                    self.nacitajPolicka(hrac)
                




            
    def skontrolujPolickoNaMyske(self,nutnaKontrola = False):
        sur = self.dajPolickoveSurMysky()
        if not nutnaKontrola:
            if sur[0] == self.starePolickoveSurMysky[0] and sur[1] == self.starePolickoveSurMysky[1]:
                return
            #inak nastala zmena
        self.starePolickoveSurMysky = sur
        self.okolieMysky = self.dajObjektyVOblasti(3, sur[0], sur[1])
        
    def dajOkolieMysky(self):
        return self.okolieMysky
    
    def dajObjektNaMyske(self):
        okolieMysky = self.dajOkolieMysky()
        if okolieMysky == None:
            return
        pos = self.dajMyskuNaMape()
        for obj in okolieMysky:
            if obj.dajTextOblastMapa().collidepoint(pos[0],pos[1]):
                return obj
        return None
            
            
    def nacitajPolickaDoleInit(self):
        print("DOLE")
        #self.yStage2 = self.topLeftMapa[1]
        self.prebiehaNacitavanie = True
        #self.topLeftMapa[1] += 1
        #self.topLeftCoord[1] +=1
        self.yCoord = self.topLeftCoord[1] +nastavenia.MAP_SIZE_Y
        self.xCoord = self.topLeftCoord[0]
        #if self.topLeftMapa[1] < 0:
            #nastavenie na dol ak by bola mimo pole
            #self.topLeftMapa[1] = nastavenia.MAP_SIZE_Y-1
            
        self.indexNacitania = self.topLeftMapa[0]
        self.stavNacitania = 0
        self.smerNacitania = 0

    def nacitajPolickaDolePostupne(self):
        print("DOLE POSTUPNE")
        print(self.indexNacitania)
        if self.stavNacitania == 0:
            
            
            if self.indexNacitania >= nastavenia.MAP_SIZE_X:
                self.indexNacitania = 0
                self.stavNacitania = 1
            else:
                self.nacitajPolicko(self.indexNacitania,self.topLeftMapa[1])
                self.indexNacitania += 1
                self.xCoord += 1
        elif self.stavNacitania == 1:
            if self.indexNacitania >= self.topLeftMapa[0]:
                self.topLeftMapa[1] += 1
                self.topLeftCoord[1] += 1
                
                if self.topLeftMapa[1] >= nastavenia.MAP_SIZE_Y:
                    #nastavenie na dol ak by bola mimo pole
                    self.topLeftMapa[1] = 0
                #self.nacitanaMapa = self.nacitanaMapa.move(0,64)
        
                self.yStage2 =self.topLeftMapa[1]-2
                print("topleft Y = " + str(self.topLeftMapa[1]))
                print("init yStage2 = " + str(self.yStage2))
                
                if self.yStage2<0:
                    self.yStage2 += nastavenia.MAP_SIZE_Y
                    
                self.pomocnaHrana = nastavenia.MAP_SIZE_X
                if self.topLeftMapa[0] <= 0:
                    self.pomocnaHrana -=1
                
                
                
                
                self.indexNacitania = self.topLeftMapa[0]+1
                self.stavNacitania = 2

            else:
                self.nacitajPolicko(self.indexNacitania,self.topLeftMapa[1])
                self.indexNacitania += 1
                self.xCoord +=1
        
                    
        elif self.stavNacitania == 2:
            
            if self.indexNacitania >= self.pomocnaHrana:
                self.indexNacitania = 0
                self.stavNacitania = 3
            else:
                print("stg2 - " + str(self.indexNacitania) + "  " + str(self.yStage2))
                self.mapa[self.indexNacitania][self.yStage2].initStage2() 
                self.indexNacitania += 1

        else:
            
            if self.indexNacitania >= self.topLeftMapa[0]-1:
                self.nacitanaMapa = self.nacitanaMapa.move(0, 64)
                self.prebiehaNacitavanie = False
            else:
                print("stg2 - " + str(self.indexNacitania) + "  " + str(self.yStage2))
                self.mapa[self.indexNacitania][self.yStage2].initStage2() 
                self.indexNacitania += 1
         
    def nacitajPolickaDole(self):

        yCoord = self.topLeftCoord[1] +nastavenia.MAP_SIZE_Y
        xCoord = self.topLeftCoord[0]
        
        for x in range (self.topLeftMapa[0],nastavenia.MAP_SIZE_X):

            self.mapa[x][self.topLeftMapa[1]].uloz()
            self.mapa[x][self.topLeftMapa[1]] = self.vytvorPolickoNa(xCoord,yCoord)
            xCoord +=1
                
        for x in range (0,self.topLeftMapa[0]):

            self.mapa[x][self.topLeftMapa[1]].uloz()
            self.mapa[x][self.topLeftMapa[1]] = self.vytvorPolickoNa(xCoord ,yCoord)
            xCoord +=1
            
            
        self.topLeftMapa[1] += 1
        self.topLeftCoord[1] += 1
        if self.topLeftMapa[1] >= nastavenia.MAP_SIZE_Y:
            #nastavenie na dol ak by bola mimo pole
            self.topLeftMapa[1] = 0
        #self.nacitanaMapa = self.nacitanaMapa.move(0,64)

        yStage2 =self.topLeftMapa[1]-2
        
        if yStage2<0:
            yStage2 += nastavenia.MAP_SIZE_Y
            
        pravaStrana = nastavenia.MAP_SIZE_X
        

        if self.topLeftMapa[0] <= 0:
            pravaStrana -=1
            
        for x in range (self.topLeftMapa[0]+1,pravaStrana):
            self.mapa[x][yStage2].initStage2()  
   
       
        for x in range (0,self.topLeftMapa[0]-1):
            self.mapa[x][yStage2].initStage2()
            
        self.nacitanaMapa = self.nacitanaMapa.move(0,64)
 
    def nacitajPolickaHoreInit(self):
        print("HORE")
        self.yStage2 = self.topLeftMapa[1]
        self.prebiehaNacitavanie = True
        self.topLeftMapa[1] -= 1
        self.topLeftCoord[1] -=1
        self.yCoord = self.topLeftCoord[1]
        self.xCoord = self.topLeftCoord[0]
        if self.topLeftMapa[1] < 0:
            #nastavenie na dol ak by bola mimo pole
            self.topLeftMapa[1] = nastavenia.MAP_SIZE_Y-1
            
        self.indexNacitania = self.topLeftMapa[0]
        self.stavNacitania = 0
        self.smerNacitania = 3

    def nacitajPolickaHorePostupne(self):
        print(self.indexNacitania)
        if self.stavNacitania == 0:
            
            
            if self.indexNacitania >= nastavenia.MAP_SIZE_X:
                self.indexNacitania = 0
                self.stavNacitania = 1
            else:
                self.nacitajPolicko(self.indexNacitania,self.topLeftMapa[1])
                self.indexNacitania += 1
                self.xCoord += 1
        elif self.stavNacitania == 1:
            if self.indexNacitania >= self.topLeftMapa[0]:
                self.indexNacitania = self.topLeftMapa[0]+1
                self.stavNacitania = 2
                self.pomocnaHrana = nastavenia.MAP_SIZE_X
                if self.topLeftMapa[0] == 0:
                    self.pomocnaHrana -= 1
                    print("AAAA")
                    print(self.indexNacitania)
                    print(self.pomocnaHrana)
            else:
                self.nacitajPolicko(self.indexNacitania,self.topLeftMapa[1])
                self.indexNacitania += 1
                self.xCoord +=1
        
                    
        elif self.stavNacitania == 2:
            
            if self.indexNacitania >= self.pomocnaHrana:
                self.indexNacitania = 0
                self.stavNacitania = 3
            else:
                print("stg2 - " + str(self.indexNacitania) + "  " + str(self.yStage2))
                self.mapa[self.indexNacitania][self.yStage2].initStage2() 
                self.indexNacitania += 1

        else:
            
            if self.indexNacitania >= self.topLeftMapa[0]-1:
                self.nacitanaMapa = self.nacitanaMapa.move(0,-64)
                self.prebiehaNacitavanie = False
            else:
                print("stg2 - " + str(self.indexNacitania) + "  " + str(self.yStage2))
                self.mapa[self.indexNacitania][self.yStage2].initStage2() 
                self.indexNacitania += 1
                
                
                
                
    #operacia ktora sa casto opakuje na roznych miestach 
    #koli tomu ze to prebieha postupne mnozstvo udajov sa uklada do pamate triedy preto netreba parametre
    def nacitajPolicko(self,xPole,yPole):
        self.mapa[xPole][yPole].uloz()
        print("nacitavam policko:" + str(xPole) + "  " + str(yPole))
        self.mapa[xPole][yPole] = self.vytvorPolickoNa(self.xCoord ,self.yCoord)

                
        
    def nacitajPolickaHore(self):
        
        yStage2 = self.topLeftMapa[1]
        self.topLeftMapa[1] -= 1
        self.topLeftCoord[1] -=1
        yCoord = self.topLeftCoord[1]
        xCoord = self.topLeftCoord[0]
        if self.topLeftMapa[1] < 0:
            #nastavenie na dol ak by bola mimo pole
            self.topLeftMapa[1] = nastavenia.MAP_SIZE_Y-1
            
        for x in range (self.topLeftMapa[0],nastavenia.MAP_SIZE_X):

            self.mapa[x][self.topLeftMapa[1]].uloz()
            self.mapa[x][self.topLeftMapa[1]] = self.vytvorPolickoNa(xCoord ,yCoord)
            xCoord += 1
                
        for x in range (0,self.topLeftMapa[0]):

            self.mapa[x][self.topLeftMapa[1]].uloz()
            self.mapa[x][self.topLeftMapa[1]] = self.vytvorPolickoNa(xCoord,yCoord)
            xCoord += 1
            
        pravaStrana = nastavenia.MAP_SIZE_X
        
        if self.topLeftMapa[0] <= 0:
            pravaStrana -= 1 

            
        for x in range (self.topLeftMapa[0]+1,pravaStrana):
            self.mapa[x][yStage2].initStage2() 
  
       
        for x in range (0,self.topLeftMapa[0]-1):
            self.mapa[x][yStage2].initStage2()

        self.nacitanaMapa = self.nacitanaMapa.move(0,-64)




    def nacitajPolickaVlavoInit(self):
        self.prebiehaNacitavanie = True
        self.xStage2 = self.topLeftMapa[0]
        self.topLeftMapa[0] -=1
        self.topLeftCoord[0] -= 1
        if self.topLeftMapa[0] < 0:
            self.topLeftMapa[0] = nastavenia.MAP_SIZE_X-1
        
        self.yCoord = self.topLeftCoord[1]
        self.xCoord = self.topLeftCoord[0]
        self.stavNacitania = 0
        self.smerNacitania = 2
        self.indexNacitania = self.topLeftMapa[1]

    def nacitajPolickaVlavoPostupne(self):
        print(self.indexNacitania)
        if self.stavNacitania == 0:
            
            if self.indexNacitania >= nastavenia.MAP_SIZE_Y:
                self.indexNacitania = 0
                self.stavNacitania = 1
            else:
                self.nacitajPolicko(self.topLeftMapa[0], self.indexNacitania)
                self.indexNacitania += 1
                self.yCoord += 1
                
        elif self.stavNacitania == 1:
            if self.indexNacitania >= self.topLeftMapa[1]:
                self.indexNacitania = self.topLeftMapa[1]+1
                self.stavNacitania = 2
                self.pomocnaHrana = nastavenia.MAP_SIZE_Y
                #print("pomocna hrana " + str(self.pomocnaHrana))
                if self.topLeftMapa[1] <= 0:
                    self.pomocnaHrana -= 1
                    print("AAAA")
                    print(self.indexNacitania)
                    print(self.pomocnaHrana)
            else:
                self.nacitajPolicko(self.topLeftMapa[0], self.indexNacitania)
                self.indexNacitania += 1
                self.yCoord +=1
        
                    
        elif self.stavNacitania == 2:
            
            if self.indexNacitania >= self.pomocnaHrana:
                self.indexNacitania = 0
                self.stavNacitania = 3
            else:
                #print("stg2 - " + str(self.indexNacitania) + "  " + str(self.yStage2))
                self.mapa[self.xStage2][self.indexNacitania].initStage2() 
                self.indexNacitania += 1
    
        else:
            
            if self.indexNacitania >= self.topLeftMapa[1]-1:
                self.nacitanaMapa = self.nacitanaMapa.move(-64,0)
                self.prebiehaNacitavanie = False
            else:
                #print("stg2 - " + str(self.indexNacitania) + "  " + str(self.yStage2))
                self.mapa[self.xStage2][self.indexNacitania].initStage2() 
                self.indexNacitania += 1
            
        
    def nacitajPolickaVlavo(self):
        xStage2 = self.topLeftMapa[0]
        self.topLeftMapa[0] -=1
        self.topLeftCoord[0] -= 1
        if self.topLeftMapa[0] < 0:
            self.topLeftMapa[0] = nastavenia.MAP_SIZE_X-1
        
        yCoord = self.topLeftCoord[1]
        xCoord = self.topLeftCoord[0]
            
        for y in range (self.topLeftMapa[1],nastavenia.MAP_SIZE_Y):
            self.mapa[self.topLeftMapa[0]][y].uloz()
            self.mapa[self.topLeftMapa[0]][y] = self.vytvorPolickoNa(xCoord,yCoord)
            yCoord += 1
            
        for y in range (0,self.topLeftMapa[1]):
            self.mapa[self.topLeftMapa[0]][y].uloz()
            self.mapa[self.topLeftMapa[0]][y] = self.vytvorPolickoNa(xCoord,yCoord)
            yCoord += 1
            
         
  
        dolnaStrana = nastavenia.MAP_SIZE_Y
        if self.topLeftMapa[1] <= 0:
            dolnaStrana -= 1
            
        for y in range (self.topLeftMapa[1]+1,dolnaStrana):
            self.mapa[xStage2][y].initStage2()  
 
       
        for y in range (0,self.topLeftMapa[1]-1):
            self.mapa[xStage2][y].initStage2()
            
        self.nacitanaMapa = self.nacitanaMapa.move(-64,0)



    def nacitajPolickaVpravoInit(self):
        print("VPRAVO")
        self.prebiehaNacitavanie = True
        self.yCoord = self.topLeftCoord[1]
        self.xCoord = self.topLeftCoord[0] + nastavenia.MAP_SIZE_X
        self.stavNacitania = 0
        self.smerNacitania = 1
        self.indexNacitania = self.topLeftMapa[1]
        #zvysujem uz tu aby pocas nacitavania bolo mozne zistit kde to policko je
        self.topLeftMapa[0] +=1
        self.topLeftCoord[0] += 1
        if self.topLeftMapa[0] >= nastavenia.MAP_SIZE_X:
            self.topLeftMapa[0] = 0

    def nacitajPolickaVpravoPostupne(self):
        print(self.indexNacitania)
        if self.stavNacitania == 0:
            
            if self.indexNacitania >= nastavenia.MAP_SIZE_Y:
                self.indexNacitania = 0
                self.stavNacitania = 1
            else:
                xVPoli = self.topLeftMapa[0]-1
                if xVPoli < 0:
                    xVPoli += nastavenia.MAP_SIZE_X
                self.nacitajPolicko(xVPoli, self.indexNacitania)
                self.indexNacitania += 1
                self.yCoord += 1
                
        elif self.stavNacitania == 1:
            if self.indexNacitania >= self.topLeftMapa[1]:
                self.indexNacitania = self.topLeftMapa[1]+1
                print("index nacitania do A: " + str(self.indexNacitania))
                self.stavNacitania = 2
                self.pomocnaHrana = nastavenia.MAP_SIZE_Y
                #self.topLeftMapa[0] +=1
                #self.topLeftCoord[0] += 1
                self.xStage2 = self.topLeftMapa[0] -2
                if self.xStage2<0:
                    self.xStage2 += nastavenia.MAP_SIZE_X

                if self.topLeftMapa[1] <= 0:
                    self.pomocnaHrana -= 1
                    print("AAAA")
                    print(self.indexNacitania)
                    print(self.pomocnaHrana)
            else:
                xVPoli = self.topLeftMapa[0]-1
                if xVPoli < 0:
                    xVPoli += nastavenia.MAP_SIZE_X
                self.nacitajPolicko(xVPoli, self.indexNacitania)
                self.indexNacitania += 1
                self.yCoord +=1
        
                    
        elif self.stavNacitania == 2:
            
            if self.indexNacitania >= self.pomocnaHrana:
                self.indexNacitania = 0
                self.stavNacitania = 3
                print("Konci A")
            else:
                print("stg2A - " + str(self.xStage2) + "  " + str(self.indexNacitania))
                self.mapa[self.xStage2][self.indexNacitania].initStage2() 
                self.indexNacitania += 1
    
        else:
            
            if self.indexNacitania >= self.topLeftMapa[1]-1:
                self.nacitanaMapa = self.nacitanaMapa.move(64,0)
                self.prebiehaNacitavanie = False
                print("konciB")
            else:
                print("stg2B - " + str(self.xStage2) + "  " + str(self.indexNacitania))
                self.mapa[self.xStage2][self.indexNacitania].initStage2() 
                self.indexNacitania += 1

    def nacitajPolickaVpravo(self):
        
        
        
        yCoord = self.topLeftCoord[1]
        xCoord = self.topLeftCoord[0] + nastavenia.MAP_SIZE_X
        
        
  
        for y in range (self.topLeftMapa[1],nastavenia.MAP_SIZE_Y):
            self.mapa[self.topLeftMapa[0]][y].uloz()
            self.mapa[self.topLeftMapa[0]][y] = self.vytvorPolickoNa(xCoord,yCoord)
 
            #task = vytvoreniePolicka(self.topLeftMapa[0],y,xCoord,yCoord)
            #self.hra.zoznamNacitanie[task] = task
            yCoord += 1
            

        for y in range (0,self.topLeftMapa[1]):
            self.mapa[self.topLeftMapa[0]][y].uloz()
            self.mapa[self.topLeftMapa[0]][y] = self.vytvorPolickoNa(xCoord,yCoord)

            #task = vytvoreniePolicka(self.topLeftMapa[0],y,xCoord,yCoord)
            #self.hra.zoznamNacitanie[task] = task
            yCoord += 1
            
            
 
        self.topLeftMapa[0] +=1
        self.topLeftCoord[0] += 1
        if self.topLeftMapa[0] >= nastavenia.MAP_SIZE_X:
            self.topLeftMapa[0] = 0
      
        xStage2 = self.topLeftMapa[0] -2
        if xStage2<0:
            xStage2 += nastavenia.MAP_SIZE_X
           

        dolnaStrana = nastavenia.MAP_SIZE_Y
        if self.topLeftMapa[1] <= 0:
            dolnaStrana -=1
 
        for y in range (self.topLeftMapa[1]+1,dolnaStrana):
            #print("x" + str(xStage2) + "  y" + str(y))

            self.mapa[xStage2][y].initStage2() 

            #a =  initStage2Task(self.mapa[xStage2][y])
            #self.hra.zoznamStage2[a] = a 
 

        for y in range (0,self.topLeftMapa[1]-1):
            self.mapa[xStage2][y].initStage2()

            #a =  initStage2Task(self.mapa[xStage2][y])
            #self.hra.zoznamStage2[a] = a 
            
        self.nacitanaMapa = self.nacitanaMapa.move(64,0)

            




    def scale(self):
        i =5 # to ani netreba ci? 
        
        
    
        
        '''
        Prvotne nacitanie.
        '''
    def nacitajMapu(self):
        #rohX = int(self.hra.hrac.pixeloveUmiestnenieNaMape[0]/64-nastavenia.MAP_SIZE_X/2)
        #rohY = int(self.hra.hrac.pixeloveUmiestnenieNaMape[1]/64-nastavenia.MAP_SIZE_Y/2)
        self.topLeftCoord[0] = int(self.hra.hrac.suradnice[0]-nastavenia.MAP_SIZE_X/2)
        self.topLeftCoord[1] = int(self.hra.hrac.suradnice[1]-nastavenia.MAP_SIZE_Y/2)
        #print("Top left: " + str(self.topLeftCoord[0]) + "  " + str(self.topLeftCoord[1]))
        self.nacitanaMapa = pygame.Rect(self.topLeftCoord[0]*64, self.topLeftCoord[1]*64, nastavenia.MAP_SIZE_X*64, nastavenia.MAP_SIZE_Y*64) #rect predstavujuci nacitanu oblast
        #print(str(rohX) + "  " + str(rohY))
        logging.info("nacitavanie policok")
        #for x, stlpec in enumerate(self.mapa):
        #    for y, policko in enumerate(stlpec):
        #        self.mapa[x][y] = self.vytvorPolickoNa(self.topLeftCoord[0]+x,self.topLeftCoord[1]+y)

        for x in range (0,len(self.mapa)):
            for y in range (0, len(self.mapa[x])):
                self.mapa[x][y] = self.vytvorPolickoNa(self.topLeftCoord[0]+x,self.topLeftCoord[1]+y)
                print("nacitane: " + str(x) + " " + str(y))




        logging.info("policka stage2")
        for x, stlpec in enumerate(self.mapa):
            if x<=0 or x>=len(self.mapa)-1:
                continue
            for y, policko in enumerate(stlpec):
                if y>0 and y<len(stlpec)-1:
                    self.mapa[x][y].initStage2()
                    
                    
    def dajNacitanuMapu(self):
        return self.nacitanaMapa#pixelova mapa ktora je nacitana
        
    def vytvorPolickoNa(self,x,y):
        #bud nacitat alebo generator
        noise = [0 for b in range (0,6)]
        
        for biom in range (0,6):
            noise[biom] = self.generatorBiom[biom].noise(x,y)
            
        index = self.najdiIndexNajvacsieho(noise)
        noise = [self.noiseGen[0].noise(x, y),self.noiseGen[1].noise(x, y),self.noiseGen[2].noise(x, y)]
        return policko.Policko(self,(x,y),noise,index)
    
    def najdiIndexNajvacsieho(self, list):
        index = 0
        hodnotaMax=list[0]
        a=len(list)
        for i in range (0,a): 
            if hodnotaMax<list[i]:
                hodnotaMax = list[i]
                index = i
        return index
    
    
      
        
        '''
        self.lavoHorePixelKamera[0] = hrac.pixeloveUmiestnenieNaMape[0] - self.minulaPoziciaHraca[0]
        self.lavoHorePixelKamera[1] = hrac.pixeloveUmiestnenieNaMape[1] - self.minulaPoziciaHraca[1]
        self.minulaPoziciaHraca = hrac.pixeloveUmiestnenieNaMape
        
        '''
        
    def updateKamera(self,hrac):
        topLeftScaleMap = hrac.dajTopLeftScaleMap()
        topLeftNoScaleMap = hrac.dajTopLeftNoScaleMap()
        
        self.kamera.x = topLeftScaleMap[0] - int(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/2) +self.zoom/4
        self.kamera.y = topLeftScaleMap[1] - int(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]/2) +self.zoom/4
        
        self.topLeftNoScale[0] = topLeftNoScaleMap[0] - int(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/2) +self.zoom/4
        self.topLeftNoScale[1] = topLeftNoScaleMap[1] - int(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]/2) +self.zoom/4
        
    def dajTopLeftNoScale(self):
        return self.topLeftNoScale
        
    def dajKamera(self):
        return self.kamera
        
    def initKamera(self):
        #self.lavoHorePixelKamera[0] = self.hrac.pixeloveUmiestnenieNaMape[0] - nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/2
        #self.lavoHorePixelKamera[1] = self.hrac.pixeloveUmiestnenieNaMape[1] - nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]/2
        
        self.kamera = pygame.Rect(self.hrac.rectTextOblastMapa.x - nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/2,
                                  self.hrac.rectTextOblastMapa.y - nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]/2,
                                  nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie],
                                  nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie])
        
        
    def updatniPoziciu(self,topLeftScaleMap,rect):
        rect.x = topLeftScaleMap[0] - self.kamera.x
        #rect.y = self.kamera.y - topLeftScaleMap[1] # menim smer y suradnice hore sa znizuje
        rect.y = topLeftScaleMap[1] -self.kamera.y
                
    def dajOkolie (self, surNaMape):
        #vrati 8 policok naokolo policka v parametri
        #nekontroluje fazu policka
        #pri tolkych volaniach vhodna optimalizacia?
        zoznam = [self.dajPolicko((surNaMape[0]+1,surNaMape[1])),
            self.dajPolicko((surNaMape[0]+1,surNaMape[1]+1)),
            self.dajPolicko((surNaMape[0],surNaMape[1]+1)),
            self.dajPolicko((surNaMape[0]-1,surNaMape[1]+1)),
            self.dajPolicko((surNaMape[0]-1,surNaMape[1])),
            self.dajPolicko((surNaMape[0]-1,surNaMape[1]-1)),
            self.dajPolicko((surNaMape[0],surNaMape[1]-1)),
            self.dajPolicko((surNaMape[0]+1,surNaMape[1]-1)),
            ]
        return zoznam
    
    def dajObjektyVOblasti(self,radius,stredX,stredY):
        #vrati vsetky policka v danom radiuse
        #radius = 1 vrati 1 policko
        #radiu 2 vrati 9 policok
        # 3- 25   4 - 49 ...
        xLHranica = stredX - radius + 1
        xPHranica = stredX + radius
        yHHranica = stredY - radius + 1
        yDHranica = stredY + radius
        group = pygame.sprite.Group()
        try:
            for x in range (xLHranica,xPHranica):
                for y in range (yHHranica,yDHranica):
                        group.add(self.dajPolicko((x,y)).dajVlastneObjekty())
        except:
            return None # dane policka nemusia byt nacitane
            
        return group
            
    def dajPolicko(self, surNaMape ):
        sur = [surNaMape[0],surNaMape[1]]
        #print("suradnice top left coord:" + str(self.topLeftCoord))
        sur[0] -= self.topLeftCoord[0]
        sur[1] -= self.topLeftCoord[1]
        if sur[0]<0 or sur[1]<0 or sur[0]>=nastavenia.MAP_SIZE_X or sur[1] >= nastavenia.MAP_SIZE_Y :
            #print("NONE")
            return None
        
        sur[0] += self.topLeftMapa[0]
        sur[1] += self.topLeftMapa[1]
        if sur[0] >= nastavenia.MAP_SIZE_X:
            sur[0] -= nastavenia.MAP_SIZE_X
        if sur[1] >= nastavenia.MAP_SIZE_Y:
            sur[1] -= nastavenia.MAP_SIZE_Y
        a =  self.mapa[sur[0]][sur[1]]
        return a
        
        