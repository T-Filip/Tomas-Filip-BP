'''
Created on 3. 2. 2017

@author: T.Filip
'''

import pygame
import nastavenia
import hra
import time
import os
from Textury import textury
import ObjektyMapa.infObjekty as infObjekty
import logging
import Menu.menuOkno as menuOkno
import Menu.menuOknoVyberPostavy as menuOknoVyberPostavy
import Menu.menuOknoZakladMenu as menuOknoZakladMenu
import Menu.enumOknaMenu as enumOknaMenu
import Menu.enumOknaHra as enumOknaHra
import Menu.menuOknoInventar as menuOknoInventar
from Textury import  texturyPolicka

import ObjektyMapa.infObjekty
from Menu import menuOknoVlastnosti
from Menu.oknoInventar import OknoInventar

#


def tred (manazerOkien):
    while True:
         manazerOkien.hra.vykresliHru()
         #manazerOkien.hra.update()

class ManazerOkien:
    def __init__(self):
        #print("Manaze init start")
        logging.info("initManazera")
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.event.get()
        self.klavesy = pygame.key.get_pressed()
        self.pressedMouse = pygame.mouse.get_pressed()
        self.predKlavesy  = pygame.key.get_pressed()
        self.events()
        mode = 0#pygame.DOUBLEBUF 
        if nastavenia.windowIndex == 0:
            mode += pygame.FULLSCREEN + pygame.HWSURFACE
        elif nastavenia.borderIndex == 0:
            mode += pygame.NOFRAME

        logging.info("init screen")
        self.screen = pygame.display.set_mode((nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie], nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]),
                                              mode )

        
        logging.info("init textury policiek")
        texturyPolicka.initTextury()
        self.hra = None

        
        pygame.display.set_caption(nastavenia.UVODNE_NASTAVENIA_TITLE)
        self.clock = pygame.time.Clock()
        

        
        self.timeUP = time.time()
        
        #print("manazer Init done")
        
        self.initMenuOkna()
        logging.info("initDone")

        



    def dajKlavesy(self):
        return self.klavesy
        
        
        '''
        Inicializacia vsetkych okien Menu v hre a ...
        veberPostavy
        zakladneMenu
        '''
    def initMenuOkna(self):
        sc =nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/1280

        self.zoznamOkienMenu = {}
        self.zoznamOkienMenu[enumOknaMenu.EnumOknaMenu.VYBER_POSTAVY] = menuOknoVyberPostavy.MenuOknoVyberPostavy(self,sc)
        self.zakladneMenu = menuOknoZakladMenu.MenuOknoZakladMenu(self,sc)
        self.zoznamOkienMenu[enumOknaMenu.EnumOknaMenu.ZAKLADNE_MENU] = self.zakladneMenu
        
        self.zoznamOkienHra = {}
        self.zoznamOkienHra[enumOknaHra.EnumOknaHra.INVENTAR] = menuOknoInventar.MenuOknoInventar(self,sc)
        self.zoznamOkienHra[enumOknaHra.EnumOknaHra.VLASTNOSTI] = menuOknoVlastnosti.MenuOknoVlastnosti(self,sc,0.4,0.5)
       
        self.oknoMenu = self.zakladneMenu
        self.oknoVHre = None
        
        
    def vytvorHru(self,texturyHraca,vlastnosti,typP):
        logging.info("vytvorenie instancie hry")
        self.hra = hra.Hra(self, self.screen, texturyHraca,vlastnosti,typP)
        
    def dajOknoHra(self,kluc):
        return self.zoznamOkienHra[kluc]
    
    def dajOknoMenu(self,kluc):
        return self.zoznamOkienMenu[kluc]
    
    def dajPressedMouse(self):
        return self.pressedMouse
        
        
    def dajHru (self) :
        return self.hra

    def run(self):
        
        
        
        self.niejeUkoncena = True
        timeLastTick = time.time()
        timeNextTick =  timeLastTick + 0.01 # 100 tickov za sekundu
        pocDrawPoUpdate = 0
        nextTick = 1/100
        #gc.collect(0)
        while self.niejeUkoncena:
            if time.time() > timeNextTick:
                timeNextTick += nextTick
                timeLastTick = time.time()
                #try:
                if self.oknoMenu != None:
                    logging.info("Menu-update")
                    self.oknoMenu.update()
                    
                else:
                    logging.info("TICK")
                    self.update()
                    if self.oknoVHre != None:
                        self.oknoVHre.update()
                    
                logging.info("ManazerOkien-eventy")
                self.events()

            else:
                if self.oknoMenu != None:
                    logging.info("draw Menu okno")
                    self.oknoMenu.draw(self.screen)
                else:
                    logging.info("FRAME")
                    self.draw()
                    if self.oknoVHre != None:
                        self.oknoVHre.draw(self.screen)
                        
                if self.hra != None: 
                    self.hra.vykresliInfoRoh()
                pygame.display.flip()
            
    def prepniMenu(self, enumLink):
        if enumLink == None:
            self.oknoMenu = None
        else:
            self.oknoMenu = self.zoznamOkienMenu[enumLink]
            
    def prepniMenuVHre (self, enum):
        if self.oknoMenu != None:
            return
        if enum == None:
            self.oknoVHre = None
        else:
            okno = self.zoznamOkienHra[enum]
            if okno == self.oknoVHre: #aby sa tym istym tlacidlo mohlo aj vypnut
                self.oknoVHre.close()
                self.oknoVHre = None
            else:
                self.oknoVHre = okno
                self.oknoVHre.reinit(self.hra.dajHraca())
                
            
    def dajEventy(self):
        return self.eventy
            
    def events(self):
        self.eventy  = pygame.event.get()
        for event in self.eventy:
            if event.type == pygame.QUIT:
                if self.niejeUkoncena:
                    self.niejeUkoncena = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.klikButton1()
                    #if event.button == 2:
                #    self.klikButton2()
                elif event.button == 3:
                    self.klikButton3()
                elif event.button == 4:
                    self.klikButton4()
                elif event.button == 5:
                    self.klikButton5()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.oknoMenu != None:
                        self.oknoMenu = None
                    else:
                        self.oknoMenu = self.zakladneMenu
                elif event.key == pygame.K_i :
                    self.prepniMenuVHre(enumOknaHra.EnumOknaHra.INVENTAR)
                elif event.key == pygame.K_v :
                    self.prepniMenuVHre(enumOknaHra.EnumOknaHra.VLASTNOSTI)
                elif event.key == pygame.K_0:
                    self.hra.stlacena0()
                elif event.key == pygame.K_1:
                    self.hra.stlacena1()    
                elif event.key == pygame.K_2:
                    self.hra.stlacena2()
                elif event.key == pygame.K_3:
                    self.hra.stlacena3()
                elif event.key == pygame.K_4:
                    self.hra.stlacena4()
                elif event.key == pygame.K_5:
                    self.hra.stlacena5()
                elif event.key == pygame.K_6:
                    self.hra.stlacena6()
                elif event.key == pygame.K_7:
                    self.hra.stlacena7()
                elif event.key == pygame.K_8:
                    self.hra.stlacena8()
                elif event.key == pygame.K_9:
                    self.hra.stlacena9()
                    
                     
                
                    

        self.predKlavesy = self.klavesy
        self.klavesy = pygame.key.get_pressed()
        self.pressedMouse = pygame.mouse.get_pressed()
        pygame.event.pump()
        
        
    def klikButton1(self):
        self.volajMetoduVOknach("updateClickLeft")
        if self.hra != None:
            self.hra.klikButton1()
            
        
        
    def klikButton2(self):
        self.volajMetoduVOknach("updateClickRight")
        if self.hra != None:
            self.hra.klikButton2()
    def klikButton3(self):
        if self.hra != None:
            self.hra.klikButton3()
        
    def klikButton4(self):
        if self.hra != None:
            self.hra.mapa.zvysZoom(1)
            self.hra.klikButton4()
    def klikButton5(self):
        if self.hra != None:
            self.hra.mapa.znizZoom(1)
            self.hra.klikButton5()

    def jeVykresleneNejakeMenu(self):
        if self.oknoMenu == None and self.oknoVHre == None:
            return False
        else:
            return True
        
    def volajMetoduVOknach(self,zmenRecept):
        if self.oknoMenu != None:
            getattr(self.oknoMenu,zmenRecept)()
        if self.oknoVHre != None:
            getattr(self.oknoVHre,zmenRecept)()
        
    def update(self):
        
        
        logging.info("Hra-update")
        if self.hra!=None:
            self.hra.update()
            self.hra.dajMapu().update()
        
        
    def draw(self):
        self.screen.fill((0,0,0))
        if self.hra!=None:
            self.hra.vykresliHru()



        

 
 




        