'''
Created on 3. 2. 2017

@author: T.Filip
'''

import pygame
import nastavenia
import hra
import time
import os
import texturyPolicka
import ObjektyMapa.infObjekty as infObjekty
import logging
import gc
import Menu.menuOkno as menuOkno
import Menu.menuOknoVyberPostavy as menuOknoVyberPostavy
import textury
import Menu.menuOknoZakladMenu as menuOknoZakladMenu
import Menu.enumOknaMenu as enumOknaMenu


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
        
        self.klavesy = pygame.key.get_pressed()
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

        
        
        '''
        Inicializacia vsetkych okien Menu v hre a ...
        veberPostavy
        zakladneMenu
        '''
    def initMenuOkna(self):
        self.zoznamOkienMenu = {}
        sc =nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/1280
        self.zoznamOkienMenu[enumOknaMenu.EnumOknaMenu.VYBER_POSTAVY] = menuOknoVyberPostavy.MenuOknoVyberPostavy(self,sc)
        self.zakladneMenu = menuOknoZakladMenu.MenuOknoZakladMenu(self,sc)
        self.zoznamOkienMenu[enumOknaMenu.EnumOknaMenu.ZAKLADNE_MENU] = self.zakladneMenu
        
        self.oknoMenu = self.zakladneMenu
        self.oknoVHre = None
        
        
    def vytvorHru(self,texturyHraca):
        logging.info("vytvorenie instancie hry")
        self.hra = hra.Hra(self, self.screen, texturyHraca)

    def run(self):
        
        
        
        self.niejeUkoncena = True
        timeLastTick = time.time()
        timeNextTick =  timeLastTick + 0.01 # 100 tickov za sekundu
        pocDrawPoUpdate = 0
        nextTick = 1/100
        gc.collect(0)
        while self.niejeUkoncena:
            #self.clock.tick(200)
            
            

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
                    
                logging.info("ManazerOkien-eventy")
                self.events()
                #except Exception as e :
                 #   print("Exception Updated")
                #pocDrawPoUpdate = 0
            else:
                '''
                if pocDrawPoUpdate > 0:
                    #zbytocne vykreslovat to iste ziaden update neprebehol
                    cas = int(round(timeNextTick-time.time()*1000))
                    if cas < 0:
                        continue
                    pygame.time.wait(cas*0.95)
                    
                else:
                    #try:
                    '''
                
                if self.oknoMenu != None:
                    logging.info("draw Menu okno")
                    self.oknoMenu.draw(self.screen)
                else:
                    logging.info("FRAME")
                    self.draw()
                    #except:
                    #    print("Exception Draw")
                        
                    #pocDrawPoUpdate += 1


            #print("sdfjdsfkjdaskjgnkasjgnkjraswmgnraengmknaerwtgkawgnkjawofkljngoklaswdngmjdnasgkjndfasgdfasyghttfgrtgrtg")
            
            #for i in range (1,100000):
            #    i = 5
            
    def prepniMenu(self, enumLink):
        if enumLink == None:
            self.oknoMenu = None
        else:
            self.oknoMenu = self.zoznamOkienMenu[enumLink]
            
    def dajEventy(self):
        return self.eventy
            
    def events(self):
        self.eventy  = pygame.event.get()
        for event in self.eventy:
            if event.type == pygame.QUIT:
                if self.niejeUkoncena:
                    self.niejeUkoncena = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if self.hra != None:
                        self.hra.mapa.zvysZoom(1)
                elif event.button == 5:
                    if self.hra != None:
                        self.hra.mapa.znizZoom(1)

        self.predKlavesy = self.klavesy
        self.klavesy = pygame.key.get_pressed()
        pygame.event.pump()

        
        
    def update(self):
        
        
        logging.info("Hra-update")
        if self.hra!=None:
            self.hra.update()
        
    def draw(self):
        self.screen.fill((0,0,0))
        if self.hra!=None:
            self.hra.vykresliHru()



        

 
 




        