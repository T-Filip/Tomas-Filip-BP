'''
Created on 9. 2. 2017

@author: T.Filip
'''
import pygame
import nastavenia
from Textury import texturyPolicka
import random
import ObjektyMapa.objMapa as objMapa
import ObjektyMapa.scale as scale
import ObjektyMapa.celoPolObj as celoPolObj
import logging
import ObjektyMapa.infObjekty as infObjekty
from ObjektyMapa.infObjekty import InfObj



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
        
    def vytvorObjMapa(self):
        #predcasne vytvori vsetky objekty na mape - potom sa budu preriedovat ak sa budu prelinat
        #print("Policko vytvorObjMapa() - doimplementovat")
        rand = random.Random(self.noise)
        r = rand.randint(0, 99)
        
        #dddddd
        
        #print(self.noise)

    
        if self.noise < 0.40:
            self.celPolObj = celoPolObj.CeloPolObjPoz(self,200) 
            pass
        elif self.noise < 0.43:
            pass
        elif self.noise < 0.445:
            self.vytvorFiller(rand)
        elif self.noise < 0.465:
            self.vytvorLes(rand, 0.445, 0.465)
        elif self.noise < 0.475:
            self.vytvorFiller(rand)
        elif self.noise < 0.489:
            pass
        elif self.noise < 0.49:
            self.vytvorKamenolom(rand, 0.482, 0.49,0)
        elif self.noise < 0.527:
            pass
        elif self.noise < 0.53:
            self.celPolObj = celoPolObj.CeloPolObjPoz(self,200) 
        elif self.noise < 0.545:
            pass
        elif self.noise < 0.55:
            self.vytvorFiller(rand)
        elif self.noise < 0.59:
            self.vytvorFiller(rand)
        elif self.noise < 0.6:
            self.vytvorLes(rand, 0.55, 0.6)
        elif self.noise < 0.61:
            self.vytvorFiller(rand)
        elif self.noise < 0.64:
            pass
        elif self.noise < 0.65:
            self.vytvorFiller(rand)
        elif self.noise < 0.66:
            self.vytvorKamenolom(rand, 0.65, 0.66,1)
        elif self.noise < 0.695:
            pass
        elif self.noise < 0.7:
            self.vytvorFiller(rand)
            pass
        elif self.noise < 0.73:
            self.vytvorFiller(rand)
        else:
            self.celPolObj = celoPolObj.CeloPolObjPoz(self,200)
            pass 
        

    def dajRect(self):
        return self.rect
            
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
            
    def vytvorKamenolom (self,rand,lavaH,pravaH,typ=None):
        #Noise sa nachadza medzi hodnotami lavaH a pravaH
        if typ == None:
            typ = rand.randint(0,1)
        bodNoise = self.noise - lavaH
        bodA = 0
        bodB = pravaH - lavaH
        stred = bodB/2
        
        if bodNoise> stred:
            bodNoise -= stred
            
        bodNoise = int(bodNoise*(100/stred))
        if bodNoise < 1:
            bodNoise = 2
        

        nah = rand.randint(1,bodNoise)
        if nah > 60:
            self.vytvorVelkyKamen(rand,typ)
        nah = rand.randint(1,bodNoise)
        if nah > 30:
            self.vytvorStrednykamen(rand,typ)
        nah = rand.randint(1,bodNoise)
        if nah > 85:
            self.vytvorMaliKamen(rand,typ)
        nah = rand.randint(1,bodNoise)
        if nah > 50:
            self.vytvorMaliKamen(rand,typ)
        nah = rand.randint(1,bodNoise)
        if nah > 20:
            self.vytvorMaliKamen(rand,typ)
        nah = rand.randint(1,bodNoise)
        if nah > 5:
            self.vytvorMaliKamen(rand,typ)
            
        
            
    def vytvorLes(self,rand,lavaH,pravaH):
        #Noise sa nachadza medzi hodnotami lavaH a pravaH
        bodNoise = self.noise - lavaH
        bodA = 0
        bodB = pravaH - lavaH
        stred = bodB/2
        
        if bodNoise> stred:
            bodNoise -= stred
            
        bodNoise = int(bodNoise*(100/stred))
        if bodNoise < 1:
            bodNoise = 2 
        
        nah = rand.randint(1,bodNoise)
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
        
            
        
    def vytvorFiller(self,rand):
        
        #-----------STROMY-------
        nah = rand.randint(0,99)
        if nah<5:
            nah = rand.randint(0,99)
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
        if nah<60:
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
        nah = rand.randint(0,99)
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
                
                
    #alternativa pre vloz objekt akurat si ten objekt vytvori sam - vhodne ak pri vytvarani nie je jasne ake vykreslovanie vytvarany objekt potrebuje
    #vytvarany objekt sa hned hodi do stage 2
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
    def dajIdCeloPol(self):
        if self.celPolObj != None:
            return self.celPolObj.dajId()
        else:
            return -1
    '''
        
    def preriedObjMapa(self):
       
        for policko in self.okolie:
            if self.noise > policko.noise:
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
            #for obj in p2:
            #    obj.linkPolicko(self)
            
            
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
            #self.rectTextOblastMapa = self.image.get_rect()
            
            #self.rectTextOblastMapa.x = self.suradnice[0]*64
            #self.rectTextOblastMapa.y = self.suradnice[1] * 64
            
            self.topLeftScaleMap = [self.rectTextOblastMapa.x,self.rectTextOblastMapa.y]
            self.jeStage2 = True
            
            
            
            for obj in self.objMapaVlastne:
                try:
                    obj.initStage2()
                except Exception as e:
                    print("ObjMapa exception stage 2") 
                    pass
            
            
            logging.info("Stage2policko- scale") 
            self.scale(self.mapa.dajScaleNas())
            
            
            
            #if self.celPolObj != None:
                #print(len(self.objMapaVlastne))
                #self.celPolObj = None
                #for obj in self.objMapaVlastne:
                #    obj.kill()
                #print(len(self.objMapaBlit))
                #for obj in self.objMapaBlit:
                #    obj.kill()
                #print(len(self.objMapaBlit))
                #print(len(self.objMapaVlastne))
                    
            

            
            
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
        i=1
        
    def updatePozicie(self,mapa):
        mapa.updatniPoziciu(self.topLeftScaleMap,self.rect)
        
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
