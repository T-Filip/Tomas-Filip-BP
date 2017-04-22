'''
Created on 3. 2. 2017

@author: T.Filip
'''

import pygame
from Nastavenia import nastavenia
import hra
import time
import os
import math
import logging
import Menu.menuOknoVyberPostavy as menuOknoVyberPostavy
import Menu.menuOknoZakladMenu as menuOknoZakladMenu
import Menu.enumOknaMenu as enumOknaMenu
import Menu.enumOknaHra as enumOknaHra
import Menu.menuOknoInventar as menuOknoInventar
from Textury import  texturyPolicka
from Menu.MenuOknoZrucnosti import MenuOknoZrucnosti
from Menu import menuOknoVlastnosti
from Menu.MenuOknoNapoveda import MenuOknoNapoveda
import Textury.textury as textury




class ManazerOkien:
    def __init__(self):
        logging.info("initManazera")
        pygame.event.get()
        self.klavesy = pygame.key.get_pressed()
        self.pressedMouse = pygame.mouse.get_pressed()
        self.predKlavesy  = pygame.key.get_pressed()
        self.events()
        self.jePauza = True # na zaciatku hry pauza
        
        self.kolkoByMaloBytFPS = 30 # iba pre spodne vyrovnavanie
        
        
        mode = pygame.DOUBLEBUF
        if nastavenia.windowIndex == 0:
            mode += pygame.FULLSCREEN + pygame.HWSURFACE
        elif nastavenia.borderIndex == 0:
            mode += pygame.NOFRAME

        logging.info("init screen")
        self.screen = pygame.display.set_mode((nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie], nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]),
                                              mode )

        self.clona = pygame.Surface((nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie], nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]),pygame.SRCALPHA)
        self.clona.fill((100,100,100,150))
        logging.info("init textury policiek")
        texturyPolicka.initTextury()
        self.hra = None
        self.casPoslednehoUpdatu = 0

        
        self.maximalnyCasDoDalsiehoFramu = 1/30
        pygame.display.set_caption(nastavenia.UVODNE_NASTAVENIA_TITLE)
        #self.clock = pygame.time.Clock()

        self.vykreslilaSaAktualizacia = False
        
        self.timeUP = time.time()

        self.initMenuOkna()
        logging.info("initDone")

        



    def dajKlavesy(self):
        return self.klavesy
        

    def dajHru(self):
        return self.hra
   
   
    '''
    inicializuje okna v hre 
    '''
    def initMenuOkna(self):
        sc =nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/1280

        self.zakladneMenu = menuOknoZakladMenu.MenuOknoZakladMenu(self,sc)
        self.oknoMenu = self.zakladneMenu
        self.oknoVHre = None

        self.zoznamOkienMenu = {}
        self.zoznamOkienMenu[enumOknaMenu.EnumOknaMenu.VYBER_POSTAVY] = menuOknoVyberPostavy.MenuOknoVyberPostavy(self,sc)
        self.zoznamOkienMenu[enumOknaMenu.EnumOknaMenu.ZAKLADNE_MENU] = self.zakladneMenu
        
        self.zoznamOkienHra = {}
        self.zoznamOkienHra[enumOknaHra.EnumOknaHra.INVENTAR] = menuOknoInventar.MenuOknoInventar(self,sc)
        self.zoznamOkienHra[enumOknaHra.EnumOknaHra.VLASTNOSTI] = menuOknoVlastnosti.MenuOknoVlastnosti(self,sc,0.4,0.5)
        self.zoznamOkienHra[enumOknaHra.EnumOknaHra.ZRUCNOSTI] = MenuOknoZrucnosti(self,sc,0.4,0.7)
        self.zoznamOkienHra[enumOknaHra.EnumOknaHra.NAPOVEDA] = MenuOknoNapoveda(self,sc)
       
        
        
        
    def vytvorHru(self,texturyHraca,vlastnosti,typP):
        logging.info("vytvorenie instancie hry")
        self.hra = hra.Hra(self, self.screen, texturyHraca,vlastnosti,typP)
        self.prepniMenuVHre(enumOknaHra.EnumOknaHra.NAPOVEDA)
        
    def dajOknoHra(self,kluc):
        return self.zoznamOkienHra[kluc]
    
    def dajOknoMenu(self,kluc):
        return self.zoznamOkienMenu[kluc]
    
    def dajPressedMouse(self):
        return self.pressedMouse
    
        



    '''
    Zakladny herny cyklus toci sa kolko pc vladze.
    Pokial nestiha ubera z fps pokial vsak fps klesne prilis pod priblizne 15 fps uz sa bude redukovat rychlost hry aby hra vobec bezala
    '''
    def run(self):
        self.niejeUkoncena = True
        pocDrawPoUpdate = 0
        self.nextTick = 1/nastavenia.RYCHLOST_HRY
        self.rychlostHry = nastavenia.RYCHLOST_HRY
        timeLastTick = time.time()
        timeNextTick =  timeLastTick + self.nextTick
        self.casPoslednehoVykreslenia = time.time()+1

        
        while self.niejeUkoncena:
            if self.mozeUpdatnut(timeNextTick):
                self.vykreslilaSaAktualizacia = False
                timeNextTick += self.nextTick
                timeLastTick = time.time()
                #try:
                if self.oknoMenu != None:
                    logging.info("Menu-update")
                    self.oknoMenu.update()
                    
                elif not self.jePauza:
                    logging.info("TICK")
                    self.update()
                    if self.oknoVHre != None:
                        self.oknoVHre.update()
                    
                logging.info("ManazerOkien-eventy")
                self.events()

            else:
            #if True: # docasne koli debugovaniu
                self.vykreslilaSaAktualizacia = True
                self.casPoslednehoVykreslenia = time.time()
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
                
           
    '''
    Kontrola ci moze prebehnut update. Aby nevznikaly prilis velke medzery medzi obrazkami
    '''     
    def mozeUpdatnut(self,timeNextTick):
        if time.time() > timeNextTick:
            vysledok = True
        else: 
            vysledok = False
            
        #if self.hra != None:
            
            '''
            fps = self.hra.dajFPS()
            print("kolko by malo byt fps: " + str(self.kolkoByMaloBytFPS))
            print(self.rychlostHry)
            if fps < self.kolkoByMaloBytFPS:
                self.rychlostHry -= 1
                if self.rychlostHry < 10:
                    self.rychlostHry = 10
                scaleRychlost = self.rychlostHry/nastavenia.RYCHLOST_HRY*400#0-400
                self.kolkoByMaloBytFPS = math.log(math.sqrt(scaleRychlost))*10
                self.nextTick = 1/self.rychlostHry
            else:
                self.rychlostHry += 1
                if self.rychlostHry > nastavenia.RYCHLOST_HRY:
                    self.rychlostHry = nastavenia.RYCHLOST_HRY
                scaleRychlost = self.rychlostHry/nastavenia.RYCHLOST_HRY*400#0-400
                self.kolkoByMaloBytFPS = math.log(math.sqrt(scaleRychlost))*10
                self.nextTick = 1/self.rychlostHry
                '''
                
        if (time.time()-self.casPoslednehoVykreslenia) > self.maximalnyCasDoDalsiehoFramu :
                
                if self.vykreslilaSaAktualizacia:
                    #ak sa uz vykreslila naco znovu vykreslovat
                    logging.info("vynuteny update")#iba v pripade kde ma hra malo fps
                    return True # update
                else:
                    logging.info("vynuteny frame")#krizova situacia
                    return False
                
                
            
            
        '''
        #ak dlho nebol frame tak ho vnuti za cenu spomalenia hry
        if self.hra != None:
            self.maximalnyCasDoDalsiehoFramu -= 0.001
            if self.maximalnyCasDoDalsiehoFramu < 0.025:
                self.maximalnyCasDoDalsiehoFramu = 0.025
            if (time.time()-self.casPoslednehoVykreslenia) > self.maximalnyCasDoDalsiehoFramu :
                logging.info("vynuteny frame")
                vysledok = False
                print("VynutenyFrame")
                koefUpdate = (time.time() -self.casPoslednehoUpdatu)*nastavenia.RYCHLOST_HRY
                if koefUpdate > 1.2: #1 pri rychlosti akej by mal 
                    #self.maximalnyCasDoDalsiehoFramu += 0.005
                    self.maximalnyCasDoDalsiehoFramu = math.log(koefUpdate)/10+0.02  
                    print(koefUpdate)
                    print(self.maximalnyCasDoDalsiehoFramu)

        '''
                
        
        return vysledok
    
    def dajCasOdPoslednehoFramu(self):
        return time.time() - self.casPoslednehoVykreslenia
            
    def prepniMenu(self, enumLink):
        if enumLink == None:
            self.oknoMenu = None
        else:
            self.oknoMenu = self.zoznamOkienMenu[enumLink]
            self.oknoMenu.reinit()
            
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
                if self.oknoVHre != None:
                    self.oknoVHre.close()
                self.oknoVHre = okno
                self.oknoVHre.reinit(self.hra.dajHraca())
                
            
    def dajEventy(self):
        return self.eventy
           
           
    '''
    spracuje eventy
    ''' 
    def events(self):
        self.eventy  = pygame.event.get()
        for event in self.eventy:
            if event.type == pygame.QUIT:
                if self.niejeUkoncena:
                    self.niejeUkoncena = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.klikButton1()
                if event.button == 2:
                    self.klikButton2()
                elif event.button == 3:
                    self.klikButton3()
                elif event.button == 4:
                    self.klikButton4()
                elif event.button == 5:
                    self.klikButton5()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.oknoMenu != None:
                        self.prepniMenu(None)
                    else:
                        self.prepniMenu(enumOknaMenu.EnumOknaMenu.ZAKLADNE_MENU)
                elif event.key == pygame.K_i :
                    self.prepniMenuVHre(enumOknaHra.EnumOknaHra.INVENTAR)
                elif event.key == pygame.K_v :
                    self.prepniMenuVHre(enumOknaHra.EnumOknaHra.VLASTNOSTI)
                elif event.key == pygame.K_b :
                    self.prepniMenuVHre(enumOknaHra.EnumOknaHra.ZRUCNOSTI)
                elif event.key == pygame.K_n :
                    self.prepniMenuVHre(enumOknaHra.EnumOknaHra.NAPOVEDA)
                elif event.key == pygame.K_p :
                    self.jePauza = not self.jePauza
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
                elif event.key == pygame.K_r:
                    self.hra.stlaceneR()
                    
                     
                
                    

        self.predKlavesy = self.klavesy
        self.klavesy = pygame.key.get_pressed()
        self.pressedMouse = pygame.mouse.get_pressed()
        pygame.event.pump()
        
    def setJePauza (self,bool):
        self.jePauza = bool
        
    def klikButton1(self):
        self.volajMetoduVOknach("updateClickLeft")
        if self.hra != None:
            self.hra.klikButton1()
            
        
        
    def klikButton2(self):
        if self.hra != None:
            self.hra.klikButton2()
    def klikButton3(self):
        self.volajMetoduVOknach("updateClickRight")
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
        
    '''
    v otvorenych oknach vola metodu ktoru dostal ako parameter
    '''
    def volajMetoduVOknach(self,key):
        if self.oknoMenu != None:
            getattr(self.oknoMenu,key)()
        if self.oknoVHre != None:
            getattr(self.oknoVHre,key)()
        
    def update(self):
        
        self.casPoslednehoUpdatu = time.time()
        logging.info("Hra-update")
        if self.hra!=None:
            self.hra.update()
            self.hra.dajMapu().update()
        
        
    def draw(self):
        
        self.screen.fill((0,0,0))
        if self.hra!=None:
            self.hra.vykresliHru()
        if self.jePauza:
            #self.screen.fill((100,100,100,150))
            self.screen.blit(self.clona,(0,0))
            font = textury.dajFont(40)
            textSurf = font.render("Pauza",1, nastavenia.BLACK)
            x = self.screen.get_width() - textSurf.get_width() - 15
            self.screen.blit(textSurf,(x,15))
            
 


        

 
 




        