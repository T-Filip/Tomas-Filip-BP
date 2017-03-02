'''
Created on 3. 2. 2017

@author: T.Filip
'''

import pygame
import nastavenia
import hra
import threading
from multiprocessing import Process, Queue
import time
import queue
import traceback,sys
import os

import texturyPolicka
import ObjektyMapa.infObjekty as infObjekty
#


def tred (manazerOkien):
    while True:
         manazerOkien.hra.vykresliHru()
         #manazerOkien.hra.update()

class ManazerOkien:
    def __init__(self):
        print("Manaze init start")
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        nastavenia.FONT_1_16 = pygame.font.Font("font\\armalite.ttf",16)
        nastavenia.FONT_1_13 = pygame.font.Font("font\\armalite.ttf",13)
        nastavenia.FONT_1_10 = pygame.font.Font("font\\armalite.ttf",10)
        self.klavesy = pygame.key.get_pressed()
        self.predKlavesy  = pygame.key.get_pressed()
        mode = pygame.DOUBLEBUF 
        if nastavenia.windowIndex == 0:
            mode += pygame.FULLSCREEN + pygame.HWSURFACE
        elif nastavenia.borderIndex == 0:
            mode += pygame.NOFRAME
     

        self.screen = pygame.display.set_mode((nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie], nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]),
                                              mode )
        texturyPolicka.initTextury()


        pole = [[0 for i in range (1000)]  for i in range (1000)]
        for i in range (1000):
            for j in range (1000):
                pole[i][j] = 9





        #self.screen.set_alpha(None)#nie na opengl surf
        
        pygame.display.set_caption(nastavenia.UVODNE_NASTAVENIA_TITLE)
        self.clock = pygame.time.Clock()
        self.hra = hra.Hra(self, self.screen)
        
        
        queue = Queue()
        
        #p1 = Process(target=tred,args=(self,))
        #p1.start()
        
        

        t = threading.Thread(target=tred,args=(self,))


        #t.start()

        
        self.timeUP = time.time()
        
        print("manazer Init done")
        
    

    def run(self):
        self.niejeUkoncena = True
        timeLastTick = time.time()
        timeNextTick =  timeLastTick + 0.01 # 100 tickov za sekundu
        while self.niejeUkoncena:
            if time.time() > timeNextTick:
                timeNextTick += 0.01
                timeLastTick = time.time()
                
                self.update()
            else:
                self.draw()
            

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
        
        self.events()
        self.hra.update()
        
    def draw(self):
        self.screen.fill((0,0,0))
        self.hra.vykresliHru()



        

 
 




        