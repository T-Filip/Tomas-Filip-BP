'''
Created on 9. 2. 2017

@author: T.Filip
'''
import pygame
from Nastavenia import nastavenia
from Textury import texturyPolicka
import random
import ObjektyMapa.objMapa as objMapa
import ObjektyMapa.scale as scale
import ObjektyMapa.celoPolObj as celoPolObj
import logging
import ObjektyMapa.infObjekty as infObjekty
#from ObjektyMapa.infObjekty import InfObj
from Postavy.npc import Npc



def collideTextOblastMapa(sprite1, sprite2):
    return sprite1.dajTextOblastMapa().colliderect(sprite2.dajTextOblastMapa())

def collideObjOblastMapa(sprite1,sprite2):
    return sprite1.dajObjOblastMapa().colliderect(sprite2.dajObjOblastMapa())


class Policko(pygame.sprite.Sprite,scale.ObjScale):
    def __init__(self,mapa,sur,noise,biom):
        
        self.okolie = None
        self.noise = noise
        self.biom = biom
        self.suradnice = sur
        self.mapa = mapa
        self.jeStage2 = False
        
        
        self.celPolObj = None
        self.objMapaBlit = pygame.sprite.LayeredUpdates()
        self.objektyMapaCudzie = pygame.sprite.Group()
        self.objMapaVlastne = pygame.sprite.Group()#vsetky objekty ktore patria tomuto policku ... aj celopolickove? 
        
        

        

        self.objektyMapaPrekryvajuce = pygame.sprite.Group()#grupa pre objekty ktore sa budu vykreslovat samostatne tak ayb za ne hrac mohol zajst
        
        self.rectTextOblastMapa = pygame.Rect(self.suradnice[0]*64,self.suradnice[1] * 64,64,64)
        self.vytvorObjMapa()
        
        if self.celPolObj != None:
            self.maCelopolObj = True
            self.idCelopolObj = self.celPolObj.id
        else:
            self.maCelopolObj = False
            self.idCelopolObj = 0
            
        
    def dajVlastneObjekty(self):
        return self.objMapaVlastne
        
    def dajTextOblastMapa(self):
        return self.rectTextOblastMapa
    
    def dajSuradnice(self):
        return self.suradnice
     
    '''
    vytvara objekty na mape 
    predcasne vytvori vsetky objekty na mape - potom sa budu preriedovat ak sa budu prelinat
    '''   
    def vytvorObjMapa(self):
        
        #print("Policko vytvorObjMapa() - doimplementovat")
        rand = random.Random(self.noise[1])
        if self.noise[0] > 0.34 and self.noise[0] < 0.35:
            self.celPolObj = celoPolObj.CeloPolObjPoz(self,200) 
        elif self.noise[0] > 0.49 and self.noise[0] < 0.51:
            self.celPolObj = celoPolObj.CeloPolObjPoz(self,200) 
        elif self.noise[0] > 0.7 and self.noise[0] < 0.71:
            self.celPolObj = celoPolObj.CeloPolObjPoz(self,200)
        else:
            if self.biom == 0:
                self.vytvorObjMapaBiom0(rand)
            elif self.biom == 1:
                self.vytvorObjMapaBiom1(rand)
            elif self.biom == 2:
                self.vytvorObjMapaBiom2(rand)
            elif self.biom == 3:
                self.vytvorObjMapaBiom3(rand)
            elif self.biom == 4:
                self.vytvorObjMapaBiom4(rand)
            elif self.biom == 5:
                self.vytvorObjMapaBiom5(rand)

        if self.celPolObj != None:
            self.celPolObj.kill()#zachovam len texturu - momentalne nie je interakcia s vodou
            
            
    def vytvorObjMapaBiom0(self,rand):
        #vela zelene
        #menej kamena vela fillera
        if self.noise[2] > 0.495 and self.noise[2] < 0.4955:
            self.vytvorKamenolom (rand,0.495,0.505)
        elif self.noise[2] > 0.39 and self.noise[2] < 0.3905:
            self.vytvorKamenolom (rand,0.39,0.393,1)
        elif self.noise[2] > 0.62 and self.noise[2] < 0.621:
            self.vytvorKamenolom (rand,0.62,0.625,0)
        elif rand.random() < 0.005:
            self.vytvorKamenolom (rand,0,0,rand.randint(0,1),rand.triangular(30,70,50))
        else:
            if self.noise[1] > 0.47 and self.noise[1] < 0.53:
                self.vytvorLes(rand, 0.47, 0.53)
            else:
                self.vytvorFiller0(rand)
                    
    def vytvorObjMapaBiom1(self,rand):
        #plains 
        #podobne ako biom 0
        # skoro ziaden les
        
        #slobo zelena
        if self.noise[2] > 0.5 and self.noise[2] < 0.50005:
                self.vytvorKamenolom (rand,0.5,0.50005)
        else:
            if self.noise[1] > 0.495 and self.noise[1] < 0.505:
                self.vytvorLes(rand, 0.495, 0.505)
            else:
                self.vytvorFiller(rand)
    def vytvorObjMapaBiom2(self,rand):
        #slobo zelena
        if self.noise[2] > 0.495 and self.noise[2] < 0.4955:
            self.vytvorKamenolom (rand,0.495,0.4955)
        elif self.noise[2] > 0.39 and self.noise[2] < 0.3905:
            self.vytvorKamenolom (rand,0.39,0.3905,1)
        elif self.noise[2] > 0.62 and self.noise[2] < 0.621:
            self.vytvorKamenolom (rand,0.62,0.621,0)
        elif rand.random() < 0.005:
            self.vytvorKamenolom (rand,0,0,rand.randint(0,1),rand.triangular(30,70,50))
        else:
            if self.noise[1] > 0.47 and self.noise[1] < 0.53:
                self.vytvorLes(rand, 0.47, 0.53)
            elif self.noise[1] > 0.35 and self.noise[1] < 0.375:
                self.vytvorLes(rand, 0.35, 0.375)
            elif self.noise[1] > 0.72 and self.noise[1] < 0.76:
                self.vytvorLes(rand, 0.72, 0.76)
            else:
                self.vytvorFiller0(rand)
                    
    def vytvorObjMapaBiom3(self,rand):
        if self.noise[2] > 0.495 and self.noise[2] < 0.4955:
            self.vytvorKamenolom (rand,0.495,0.4955)
        elif self.noise[2] > 0.39 and self.noise[2] < 0.3905:
            self.vytvorKamenolom (rand,0.39,0.3905,1)
        elif self.noise[2] > 0.62 and self.noise[2] < 0.621:
            self.vytvorKamenolom (rand,0.62,0.621,0)
        elif rand.random() < 0.003:
            self.vytvorKamenolom (rand,0,0,rand.randint(0,1),rand.triangular(30,70,50))
        else:
            if self.noise[1] > 0.465 and self.noise[1] < 0.535:
                self.vytvorLes(rand, 0.465, 0.535)
            elif self.noise[1] > 0.353 and self.noise[1] < 0.37:
                self.vytvorLes(rand, 0.353, 0.37)
            elif self.noise[1] > 0.725 and self.noise[1] < 0.755:
                self.vytvorLes(rand, 0.725, 0.755)
            else:
                self.vytvorFiller0(rand)
    def vytvorObjMapaBiom4(self,rand):
        if self.noise[1] > 0.46 and self.noise[1] < 0.54:
            self.vytvorLes(rand, 0.46, 0.54)
        elif self.noise[1] > 0.345 and self.noise[1] < 0.372:
            self.vytvorLes(rand, 0.345, 0.372)
        elif self.noise[1] > 0.72 and self.noise[1] < 0.76:
            self.vytvorLes(rand, 0.72, 0.76)
        elif self.noise[1] > 0.4 and self.noise[1] < 0.415:
            self.vytvorLes(rand, 0.4, 0.415)
        elif self.noise[1] > 0.6 and self.noise[1] < 0.62:
            self.vytvorLes(rand, 0.6, 0.62)
        else:
            self.vytvorFiller0(rand)
                
    def vytvorObjMapaBiom5(self,rand):
        if self.noise[2] > 0.49 and self.noise[2] < 0.51:
            self.vytvorKamenolom (rand,0.49,0.51)
        elif self.noise[2] > 0.39 and self.noise[2] < 0.398:
            self.vytvorKamenolom (rand,0.39,0.398,1)
        elif self.noise[2] > 0.62 and self.noise[2] < 0.63:
            self.vytvorKamenolom (rand,0.62,0.63,0)
        elif rand.random() < 0.02:
            self.vytvorKamenolom (rand,0,0,rand.triangular(15,90,55))
        else:
            if self.noise[1] > 0.47 and self.noise[1] < 0.53:
                self.vytvorLes(rand, 0.47, 0.53)
            elif self.noise[1] > 0.349 and self.noise[1] < 0.37:
                self.vytvorLes(rand, 0.349, 0.37)
            elif self.noise[1] > 0.725 and self.noise[1] < 0.75:
                self.vytvorLes(rand, 0.725, 0.75)
            elif self.noise[1] > 0.45 and self.noise[1] < 0.41:
                self.vytvorLes(rand, 0.45, 0.41)
            elif self.noise[1] > 0.65 and self.noise[1] < 0.615:
                self.vytvorLes(rand, 0.65, 0.615)
            else:
                self.vytvorFiller(rand)
    def vytvorFiller0(self,rand):
        nah = rand.random()
        if nah< 0.7:
            self.vytvorNahodnyKvietok(rand)
        elif nah< 0.4:
            self.vytvorNahodnyKvietok(rand)
        elif nah <0.15:
            self.vytvorNahodnyKvietok(rand)
        nah = rand.random()
        if nah < 0.01:
            self.VytvorNahodnyStrom(rand)
        nah = rand.random()
        if nah < 0.01:
            self.vytvorMaliKamen(rand)
            
            
    def vytvorFiller1(self,rand):
        nah = rand.random()
        if nah< 0.85:
            self.vytvorNahodnyKvietok(rand)
        elif nah< 0.45:
            self.vytvorNahodnyKvietok(rand)
        elif nah <0.10:
            self.vytvorNahodnyKvietok(rand)
        nah = rand.random()
        if nah < 0.015:
            self.VytvorNahodnyStrom(rand)
        nah = rand.random()
        if nah < 0.005:
            self.vytvorMaliKamen(rand)
    def vytvorFiller2(self,rand):
        nah = rand.random()
        if nah< 0.5:
            self.vytvorNahodnyKvietok(rand)
        elif nah< 0.1:
            self.vytvorNahodnyKvietok(rand)
        nah = rand.random()
        if nah < 0.03:
            self.VytvorNahodnyStrom(rand)
        nah = rand.random()
        if nah < 0.03:
            self.vytvorMaliKamen(rand)
        nah = rand.random()
        if nah < 0.015:
            self.vytvorStrednykamen(rand)
        nah = rand.random()
        if nah < 0.01:
            self.vytvorVelkyKamen(rand)
    def vytvorFiller3(self,rand):
        nah = rand.random()
        if nah< 0.4:
            self.vytvorNahodnyKvietok(rand)
        elif nah< 0.1:
            self.vytvorNahodnyKvietok(rand)
        nah = rand.random()
        if nah < 0.04:
            self.VytvorNahodnyStrom(rand)
        nah = rand.random()
        if nah < 0.04:
            self.vytvorMaliKamen(rand)
        nah = rand.random()
        if nah < 0.015:
            self.vytvorStrednykamen(rand)
        nah = rand.random()
        if nah < 0.02:
            self.vytvorVelkyKamen(rand)
    def vytvorFiller4(self,rand):
        nah = rand.random()
        if nah < 0.75:
            return
        nah = rand.random()
        if nah< 0.6:
            self.vytvorNahodnyKvietok(rand)
        elif nah< 0.15:
            self.vytvorNahodnyKvietok(rand)
        nah = rand.random()
        if nah < 0.1:
            self.VytvorNahodnyStrom(rand)
    def vytvorFiller5(self,rand):
        nah = rand.random()
        if nah< 0.6:
            self.vytvorNahodnyKvietok(rand)
        elif nah< 0.25:
            self.vytvorNahodnyKvietok(rand)
        elif nah< 0.05:
            self.vytvorNahodnyKvietok(rand)
        nah = rand.random()
        if nah < 0.075:
            self.VytvorNahodnyStrom(rand)
        nah = rand.random()
        if nah < 0.05:
            self.vytvorMaliKamen(rand)
        nah = rand.random()
        if nah < 0.015:
            self.vytvorStrednykamen(rand)
        nah = rand.random()
        if nah < 0.01:
            self.vytvorVelkyKamen(rand)

    def dajRect(self):
        return self.rect
    
    '''
    posatara sa ovlozenia objektu taktiez kontroluje ci dany objekt moze do tohto policka byt vlozeny
    '''       
    def vlozObj(self,obj, maSaPrekreslit = False,kontrolaSOkolim = True):  
        if kontrolaSOkolim:
            #vhodne kontrolovat aj v inych polickach ale zatial nepouzivane
            col = pygame.sprite.spritecollideany(obj, self.objMapaVlastne,collideObjOblastMapa)
        else:
            col = None
            
        if col == None:
            obj.vlozDo(self.objMapaVlastne)
        else:
            obj.kill()
            #print("MAZEM")
            return
        
        if maSaPrekreslit:
            if not isinstance(obj, objMapa.ObjMapaAktivPrek):#ak sa prekresluje aktivne tak sa linkovat nemoze
                self.polikujObjekt(obj,True)#ak sa ma prekreslit treba aby sa prekreslil aj na ostatnych polickach
            self.initImg(True)#True aby sa hned pouzil aj scale policka
            
    def vytvorKamenolom (self,rand,lavaH,pravaH,typ=None,nah=None):
        #Noise sa nachadza medzi hodnotami lavaH a pravaH
        if typ == None:
            typ = rand.randint(0,1)
            
        if nah == None:
            bodNoise = self.noise[2] - lavaH
            bodA = 0
            bodB = pravaH - lavaH
            stred = bodB/2
            
            if bodNoise> stred:
                bodNoise -= stred
                
            try:
                bodNoise = int(bodNoise*(100/stred))
            except:
                return
            
            if bodNoise < 1:
                #print("KONIEEEEC")
                return
            
            nah = rand.randint(1,bodNoise)
        else:
            nah = int(nah)
        


        if nah > 60:
            self.vytvorVelkyKamen(rand,typ)
        if nah > 30:
            self.vytvorStrednykamen(rand,typ)
        if nah > 85:
            self.vytvorMaliKamen(rand,typ)
        if nah > 50:
            self.vytvorMaliKamen(rand,typ)
        if nah > 20:
            self.vytvorMaliKamen(rand,typ)
        if nah > 5:
            self.vytvorMaliKamen(rand,typ)
            
        
            
    def vytvorLes(self,rand,lavaH,pravaH,nah = None):
        #Noise sa nachadza medzi hodnotami lavaH a pravaH
        if nah == None:
            #print(self.noise[1])
            bodNoise = self.noise[1] - lavaH
            bodA = 0
            bodB = pravaH - lavaH
            stred = bodB/2
            
            if bodNoise> stred:
                bodNoise -= stred
                
            #print("BOD NOISE")
            #print (bodNoise)
            #print("STRED")
            #print  (stred)
                
            #bodNoise = int(bodNoise*(100/stred))
            bodNoise = int(bodNoise/stred*100)
            #print("NOVY BOD NOISE")
            #print (bodNoise)
            if bodNoise <= 1:
                #print("KONIEEEEC")
                return
            nah = rand.randint(1,bodNoise)
            
        else:
            nah = int(nah)
        #print("StromyAAAAA")
        #print(nah) 
        #print()
        if nah > 10:
            id = rand.randint(self.biom*3,self.biom*3+2)
            self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            
        nah = rand.randint(1,bodNoise)
        if nah > 25:
            id = rand.randint(self.biom*3,self.biom*3+2)
            self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            
        nah = rand.randint(1,bodNoise)
        if nah > 50:
            id = rand.randint(self.biom*3,self.biom*3+2)
            self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            
        if nah > 75:
            id = rand.randint(self.biom*3,self.biom*3+2)
            self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
        
    def vytvorNahodnyKvietok(self,rand):
        id = 50 + self.biom # toto zbytocne sa rata pri viacerych kvietkoch v policku
        self.vlozObj(objMapa.ObjMapa(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
        
    def VytvorNahodnyStrom(self,rand):
        id = rand.randint(self.biom*3,self.biom*3+2)
        self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
     
    '''
    univerzalny filler - vytvori nieco na mape
    vyuzivaju sa len specializovane - tento sa nevyuziva
    '''   
    def vytvorFiller(self,rand):
        
        #-----------STROMY-------
        nah = rand.randint(0,99)
        if nah<1:
            nah = rand.triangular(0,100,70)
            if nah<35:
                id = rand.randint(self.biom*3,self.biom*3+2)
                self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
                
            if nah<10:
                id = rand.randint(self.biom*3,self.biom*3+2)
                self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            if nah<5:
                id = rand.randint(self.biom*3,self.biom*3+2)
                self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            
            id = rand.randint(self.biom*3,self.biom*3+2)
            self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True)  )
            
 
            
            
         #---------------KVIETKY---------   
        nah = rand.randint(0,99)
        if nah<65:
            koef = 0
            if self.biom == 1:
                koef -= 25
            elif self.biom ==3:
                koef +=50
            elif self.biom ==4:
                koef +=100
            elif self.biom ==4:
                koef +=25
                
            nah = rand.randint(0,99)
            id = 50 + self.biom
            
            if nah<50:
                self.vlozObj(objMapa.ObjMapa(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            if nah<25:
                self.vlozObj(objMapa.ObjMapa(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
                
            if nah<5:
                self.vlozObj(objMapa.ObjMapa(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            
            if nah<2:
                self.vlozObj(objMapa.ObjMapa(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
            
            

        
        #-------SUTRE----------
        nah = rand.triangular(0,100,80)
        if nah<3:
            typ = rand.randint(0,1)
            nah = rand.randint(0,99)
            
            if nah<10:
                self.vytvorVelkyKamen(rand,typ)
           
            nah = rand.randint(0,100) 
            if nah<25:
                self.vytvorStrednykamen(rand,typ)
                
            nah = int(rand.triangular(0,2,10)) 
            for i in range (nah):
                self.vytvorMaliKamen(rand,typ)
                
    '''            
    #alternativa pre vloz objekt akurat si ten objekt vytvori sam - vhodne ak pri vytvarani nie je jasne ake vykreslovanie vytvarany objekt potrebuje
    #vytvarany objekt sa hned hodi do stage 2
    '''
    def vytvorObjekt(self,id,suradnice,invVyuzitiePredmetov,suToSuradniceStredu=False,inf = None,nastaneKontrolaSOkolim = True):
        if inf == None:
            inf = infObjekty.dajInf(id)
            
        if not isinstance(inf, infObjekty.InfNaMape):
            logging.warning("Policko - vytvor objekt inf objektu nie potomkom InfNaMape")
            
        trieda = inf.objMapa
        obj = trieda(self,id,suradnice,invVyuzitiePredmetov,suToSuradniceStredu)
        self.vlozObj(obj,True)
        
        obj.initStage2()
            
            
    def vytvorVelkyKamen(self,rand,typ=None):
        if typ == None:
            typ = rand.randint(0,1)
            
        id = rand.randint(0,2)#012
        id += 100 + typ*13
        self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
        
    def vytvorStrednykamen(self,rand,typ=None):
        if typ == None:
            typ = rand.randint(0,1)
        id = rand.randint(0,1)
        id += 103 + typ*13
        self.vlozObj(objMapa.ObjMapaAktivPrek(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
        
    def vytvorMaliKamen(self,rand,typ=None):
        if typ == None:
            typ = rand.randint(0,1)
        id = rand.randint(0,7)
        id += 105 + typ*13
        self.vlozObj(objMapa.ObjMapa(self,id,(rand.randint(4,60),rand.randint(4,60)),True))
        
    
    
    '''
    objekty sa generuju nahodne a mnohe z nich sa mozu prekryvat tato metoda odstranuje niektore objekty tak aby sa ziaden z nich neprekrival s inym
    
    '''  
    def preriedObjMapa(self):
       
        for policko in self.okolie:
            if self.noise[1] > policko.noise[1]:
                continue # ma prioritu nemusi sa nicoho vzdat

            #nasledne odstranujeme vsetky policka ktore zasahuju do inych pretoze mensia priorita            
            pygame.sprite.groupcollide(self.objMapaVlastne, policko.objMapaVlastne, True, False, collideObjOblastMapa)
                
    
    
    '''
    vsetky objekty v okolitych polickach ktore zasahuju do tohto policka sa linknu s tymto polickom
    '''
    def polinkujObjekty(self):
        for policko in self.okolie:
            p1 = pygame.sprite.spritecollide(self, policko.objMapaBlit, False, collideTextOblastMapa)
            #p2 = pygame.sprite.spritecollide(self, policko.objektyMapaPrekryvajuce, False, collideTextOblastMapa)
            
            for obj in p1:
                obj.linkPolicko(self)

            
            
    '''
    objekt na mape vlozeny ako parameter sa linkne s polikami do ktorych zasahuje
    '''
    def polikujObjekt(self,obj,maSaPrekreslitLinknutePolicko = True):
        for policko in self.okolie:
            if collideTextOblastMapa(policko,obj):
                obj.linkPolicko(policko)
                if maSaPrekreslitLinknutePolicko:
                    policko.initImg(True)
                
    def initStage2 (self):
        surPix = [self.suradnice[0]*64,self.suradnice[1]*64]
        n = self.mapa.dajNoiseMobkaNa(surPix[0],surPix[1])
        if n > 1:
            n -= 1
            if random.random() < n:
                Npc(self.mapa.hra, surPix, 48, 48, None, self.mapa)
        elif random.random() < 0.01:
            Npc(self.mapa.hra, surPix, 48, 48, None, self.mapa)
        
        
        
        if not self.jeStage2:
            logging.info("-Stage2Policko") 
            



            logging.info("Stage2policko- daj okolie") 
            self.okolie = self.dajOkolie()
            
            
            logging.info("Stage2policko- riedenie") 
            self.preriedObjMapa()
            
            logging.info("Stage2policko- linkovanie") 
            self.polinkujObjekty()
 
            
            
            
            logging.info("Stage2policko- img init") 
            self.initImg()
            pygame.sprite.Sprite.__init__(self,self.mapa.hra.polickaSprites,self.mapa.hra.allSprites)
            
            self.rect = self.image.get_rect()

            
            self.topLeftScaleMap = [self.rectTextOblastMapa.x,self.rectTextOblastMapa.y]
            self.jeStage2 = True
            
            
            
            for obj in self.objMapaVlastne:
                try:
                    obj.initStage2()
                except Exception as e:
                    #print("ObjMapa exception stage 2") 
                    pass
            
            
            logging.info("Stage2policko- scale") 
            self.scale(self.mapa.dajScaleNas())
            

            
    def dajIdCeloPol(self):
        if self.maCelopolObj:
            return self.idCelopolObj
            
    def dajOkolie(self):
        if self.okolie == None:
            self.okolie = self.mapa.dajOkolie(self.suradnice)
        return self.okolie

    def initImg(self,maSaScalenut = False):
        self.imageZaloha = pygame.Surface((64,64))
        self.imageZaloha.blit(texturyPolicka.POLICKO_TRAVA[self.biom],(0,0))
        #self.imageZaloha = texturyPolicka.POLICKO_TRAVA[self.biom]
        
        
        if self.celPolObj != None:
            self.celPolObj.stage2(self.dajOkolie())
        for obj in self.objMapaBlit:
            obj.centrujDoRect(self.rectTextOblastMapa)
        self.objMapaBlit.draw(self.imageZaloha)
        self.image = self.imageZaloha
        
        if maSaScalenut and self.jeStage2: # ak nie je v stage 2 je to zbytocne lebo nie je viditelny a pri vstupe do stage 2 sa scalne nanovo
            self.scale(self.mapa.dajScaleNas())
            
            
       
    '''
    
    pridany update koli debugu - zastarale nescalovane
    '''
    def addUpdate(self):
        if nastavenia.DEBUG:
            #aalines nechce krelit na kraje surface preto takto
            pygame.draw.line(self.image,nastavenia.RED,(0,0),(0,63))
            pygame.draw.line(self.image,nastavenia.RED,(0,0),(63,0))
            pygame.draw.line(self.image,nastavenia.RED,(63,0),(63,63))
            pygame.draw.line(self.image,nastavenia.RED,(0,63),(63,63))
            font = nastavenia.FONT_1_10
            #font = pygame.font.SysFont("monospace", 13)
            textSuradnice = str(self.suradnice[0]) + " " + str(self.suradnice[1])
            if self.celPolObj != None:
                textSuradnice += " A"
            
            textSurf = font.render(textSuradnice, 1, (255,255,50))
            self.image.blit(textSurf, (2, 2))


    def update(self, *args):  
        pass
        
    def updatePozicie(self,mapa):
        mapa.updatniPoziciu(self.topLeftScaleMap,self.rect)
    
    
    '''
    vlastne neuklada len porusi linky na objekty tak aby ich garbage collector mohol destruktnut
    '''    
    def uloz(self):

        #i = 0
        for obj in self.objMapaVlastne:
            #i += 1
            obj.kill()
        for obj in self.objMapaBlit:
            obj.kill()
            #i += 1
        for obj in self.objektyMapaCudzie:
            obj.kill()
            #i += 1
        if self.jeStage2:
            self.kill()
            
        #print ("vymL " + str(i))
        
        # treba dorobit 
        # ulozi resp urobi co treba pred tym ako sa tato instancia vymaze 
