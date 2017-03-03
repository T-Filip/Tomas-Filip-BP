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

        pygame.init()
        nastavenia.FONT_1_16 = pygame.font.Font("font\\armalite.ttf",16)
        nastavenia.FONT_1_13 = pygame.font.Font("font\\armalite.ttf",13)
        nastavenia.FONT_1_10 = pygame.font.Font("font\\armalite.ttf",10)
        self.klavesy = pygame.key.get_pressed()
        self.predKlavesy  = pygame.key.get_pressed()
        mode = 0#pygame.DOUBLEBUF 
        if nastavenia.windowIndex == 0:
            mode += pygame.FULLSCREEN + pygame.HWSURFACE
        elif nastavenia.borderIndex == 0:
            mode += pygame.NOFRAME
            
        mode = 0
     

        logging.info("init screen")
        self.screen = pygame.display.set_mode((nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie], nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]),
                                              mode )
        
        
        logging.info("init texstury polisiek")
        texturyPolicka.initTextury()








        #self.screen.set_alpha(None)#nie na opengl surf
        
        pygame.display.set_caption(nastavenia.UVODNE_NASTAVENIA_TITLE)
        self.clock = pygame.time.Clock()
        
        logging.info("vytvorenie instancie hry")
        self.hra = hra.Hra(self, self.screen)
        
        

        
        #p1 = Process(target=tred,args=(self,))
        #p1.start()
        
        

        #t = threading.Thread(target=tred,args=(self,))


        #t.start()

        
        self.timeUP = time.time()
        
        #print("manazer Init done")
        
        logging.info("initDone")

    def run(self):
        
        
        
        self.niejeUkoncena = True
        timeLastTick = time.time()
        timeNextTick =  timeLastTick + 0.01 # 100 tickov za sekundu
        pocDrawPoUpdate = 0
        nextTick = 1/120
        gc.collect(0)
        while self.niejeUkoncena:
            #self.clock.tick(200)

            if time.time() > timeNextTick:
                timeNextTick += nextTick
                timeLastTick = time.time()
                #try:
                logging.info("TICK")
                self.update()
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
                logging.info("FRAME")
                self.draw()
                    #except:
                    #    print("Exception Draw")
                        
                    #pocDrawPoUpdate += 1


            #print("sdfjdsfkjdaskjgnkasjgnkjraswmgnraengmknaerwtgkawgnkjawofkljngoklaswdngmjdnasgkjndfasgdfasyghttfgrtgrtg")
            
            #for i in range (1,100000):
            #    i = 5
            
            
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.niejeUkoncena:
                    self.niejeUkoncena = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:

                    self.hra.mapa.zvysZoom()
                elif event.button == 5:
                    self.hra.mapa.znizZoom()

        self.predKlavesy = self.klavesy
        self.klavesy = pygame.key.get_pressed()
        pygame.event.pump()
        
    def update(self):
        
        logging.info("ManazerOkien-eventy")
        self.events()
        logging.info("Hra-update")
        self.hra.update()
        
    def draw(self):
        self.screen.fill((0,0,0))
        self.hra.vykresliHru()



        

 
 




        