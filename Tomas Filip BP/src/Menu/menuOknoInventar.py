#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 9. 3. 2017

@author: T.Filip
'''

import Menu.menuOkno as menuOkno
import pygame
import Menu.objMenu as objMenu
from Nastavenia import nastavenia
from Textury import textury
import Menu.oknoInventar as oknoInventar
import Predmety.predmet as predmet
import Predmety.inventar as inventar
import Menu.pracaSPredmetmi as pracaSPredmetmi
import Crafting.recepty as recepty


def zmenRecept(tlacidlo):
    tlacidlo.menu.zmenCraft(tlacidlo.args[0])
    
def metodaCraft(tlacidlo):
    tlacidlo.menu.craftCheck()
    if not tlacidlo.jeLocknuty:
        tlacidlo.menu.craft()


'''
Okno inventara v hre
'''
class MenuOknoInventar(menuOkno.MenuOknoHra,pracaSPredmetmi.PracaSPredmetmi):
    def __init__(self,manazerOkien,scale):
         self.predmetVMyskePosunX = 0
         self.predmetVMyskePosunY = 0
         menuOkno.MenuOknoHra.__init__(self,manazerOkien,scale,0.6,0.6)
         pracaSPredmetmi.PracaSPredmetmi.__init__(self)
         predmet.MiestoPrePredmet.__init__(self, None)
         krajnaMedzera = 30*scale
         self.receptyTlacidla = pygame.sprite.Group()
         
         x = int(self.rect.x+krajnaMedzera + self.rect.width/2.5 -15)
         y = self.rect.y+self.rect.height/2
         width = int(self.rect.width - krajnaMedzera - krajnaMedzera - self.rect.width/2.5)
         height = self.rect.height/2 - krajnaMedzera
         rectInv = pygame.Rect(x,
                               y,
                               width, 
                               height)
         #objMenu.ObjMenuInventar(self,[None],"",16, rectInv,1,1)
         self.oknoInventar =oknoInventar.OknoInventar(rectInv)
         self.vlozOkno(self.oknoInventar)
         self.vlozOknoDraw(self.oknoInventar)
         
         y = int(self.rect.y + 120*self.scaleRes)
         matRect = pygame.Rect(x+18,y,130,95)
         self.oknoMaterial = oknoInventar.OknoInventar(matRect)
         
         x = int(self.rect.x + 600*self.scaleRes)

         prodRect = pygame.Rect(x-10,y,130,95)
         self.oknoProdukt = oknoInventar.OknoInventar(prodRect)
         
         x = int(self.topLeftXPredScale + 485)
         y = int(self.topLeftYPredScale + 85)
                  
         self.tlacidloCraft = objMenu.Tlacidlo(self,[textury.TUN2,textury.TUN2Oznacene,textury.TUN2Oznacene2],"craft",29,x,y,metodaCraft,self.scaleRes,0.75)
         self.recept = None
            
         self.craftCheck()


    def draw(self, screen):
        menuOkno.MenuOknoHra.draw(self, screen)
        pracaSPredmetmi.PracaSPredmetmi.draw(self,screen)
        self.vykresliNadpis(screen, "INVENTÁR")
        self.vykresliCraftingText(screen)
        self.oknoMaterial.draw(screen)
        self.oknoProdukt.draw(screen)
         
    
    def vykresliCraftingText(self,screen):
        y = int(self.rect.y + 90*self.scaleRes)
        x = int(self.rect.x + 350*self.scaleRes)
        font = textury.dajFont(int(20*self.scaleRes))  
        #s                               
        textSurf = font.render("materiál",1, nastavenia.BLACK)
        screen.blit(textSurf,(x,y))
        
        x = int(self.rect.x + 600*self.scaleRes)
        textSurf = font.render("produkt",1, nastavenia.BLACK)
        screen.blit(textSurf,(x,y))

    
    def updateClickLeft(self):
        menuOkno.MenuOknoHra.updateClickLeft(self)
        #kliknutie na predmety
        pracaSPredmetmi.PracaSPredmetmi.clickLeft(self)
        
    def updateClickRight(self):
        menuOkno.MenuOknoHra.updateClickRight(self)
        #kliknutie na predmety
        pracaSPredmetmi.PracaSPredmetmi.clickRight(self)

     
    '''
    pri kazdom otvarani okna je nutne iste veci obnovit a podobne 
    '''
    def reinit(self, hrac):
        menuOkno.MenuOknoHra.reinit(self, hrac)
        self.oknoInventar.reinit(hrac.dajInventar())
        pracaSPredmetmi.PracaSPredmetmi.reinit(self,hrac)
        
        for recept in self.receptyTlacidla:
            recept.kill()
        
        recepty.skontrolujOtvorenieReceptov(hrac)
        x = int(self.topLeftXPredScale + 50)
        y = int(self.topLeftYPredScale + 85)
        medzera = 30
        poradie = 1
        
        for key, value in recepty.ZOZNAM_RECEPTOV.items():
             tlac = objMenu.Tlacidlo(self,[textury.CRAFT_ITEM,textury.CRAFT_ITEM_OZN,textury.CRAFT_ITEM_LOCK],value.nazov,12,x,y,zmenRecept,self.scaleRes,1,[value])
             tlac.vlozDoGroup(self.receptyTlacidla)
             if not value.jeNauceny:
                 tlac.setLock(True)
             poradie +=1
             y += medzera
             if poradie == 11:
                 x = int(self.topLeftXPredScale + 50 + 120)
                 y = int(self.topLeftYPredScale + 85)
        
    def update(self):
        menuOkno.MenuOknoHra.update(self)
        #_(self,id,pocetKusov = 1):

    '''
    meni recept za recept v parametri
    '''
    def zmenCraft(self,recept): 
        self.recept = recept
        material = recept.dajMaterial()
        materialLen = len(material)
        inventarMaterial = inventar.Inventar(materialLen)
        
        produkt = recept.dajProdukt()
        produktLen = len(produkt)
        inventarProdukt = inventar.Inventar(produktLen)
        
        for i in range (materialLen):
            inventarMaterial.vlozPredmet(predmet.Predmet(material[i][0], material[i][1]))
            
        for i in range (produktLen):
            inventarProdukt.vlozPredmet(predmet.Predmet(produkt[i][0], produkt[i][1]))
            
        self.oknoMaterial.reinit(inventarMaterial,64)
        self.oknoProdukt.reinit(inventarProdukt,64)
        self.craftCheck()
        
        
    '''
    zisti ci prave vybraty recept je mozne vycraftit - ci ma hrac dostatocny pocet materialov
    '''
    def craftCheck(self):
        okna = self.dajOknaInventare()
        daSaVykraftit = True # predpokladam ze sa da
        #material = self.recept.dajMaterial
        
        if self.recept != None:
            #for okno in self.oknoMaterial:
            inv = self.oknoMaterial.dajInventar()
            if inv == None:
                return
            predmetyMaterial = inv.dajPredmety()
            for predmet in predmetyMaterial:
                potrebneKs = predmet.dajPocetKusov()
                potrebneId = predmet.dajId()
                
                #pre kazde okno co drzi praca s predmetmi musime pozriet ci tam je toho dost
                for okno in okna:
                    predmety = okno.dajInventar().dajPredmety()
                    for predmet in predmety:
                        if predmet.dajId() == potrebneId:
                            potrebneKs -= predmet.dajPocetKusov()
                            
                if potrebneKs > 0:
                    daSaVykraftit = False
                    break;
        else:
            daSaVykraftit = False
        
        if daSaVykraftit:
            self.tlacidloCraft.setLock(False)
        else:
            self.tlacidloCraft.setLock(True)
                            
            
            
    '''
    Metoda ma za ulohu vlozit vycraftene veci z inventara a zaroven odobrat spotrebovane materialy
    ''' 
    def craft(self):
        okna = self.dajOknaInventare()
        #najprv vybrat ... zmensime sancu ze sa predmety do inventara nevojdu
        predmetyMaterial = self.oknoMaterial.dajInventar().dajPredmety()
        for predmet in predmetyMaterial:
            
            for okno in okna:
                okno.dajInventar().vyberPredmet(predmet)
                if predmet.dajPocetKusov() <= 0:
                    break
                
        #vkladanie predmetov
        
        predmetyProdukt = self.oknoProdukt.dajInventar().dajPredmety()
        for predmet in predmetyProdukt:
            
            for okno in okna:
                kolkoOstalo = okno.dajInventar().vlozPredmet(predmet)
                if kolkoOstalo <= 0:
                    break
        self.recept.vykonajAkciuPoCrafte(self.hrac)
        self.zmenCraft(self.recept)
        
        
        
        
        
        
        
        
        
        
        
        
        
        