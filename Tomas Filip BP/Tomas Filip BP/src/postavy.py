import pygame
import ObjektyMapa.objMapa as objMapa
import ObjektyMapa.scale as scale
import random
from tkinter.constants import HORIZONTAL
import logging
import Postavy.smerPostavy as smerPostavy
import Predmety.inventar as inventar
from Predmety import invVyuzPredmetu
import Predmety.predmet as predmet
from Postavy.enumTypPostavy import EnumTypPostavy
from Postavy.smerPostavy import SmerPostavy
import nastavenia




class Hrac(pygame.sprite.Sprite, scale.ObjScaleViacTextur):
    def __init__(self,hra,surPix, typP,textury,vlastnosti,sirka,vyska):
        self.vlastnosti = [[vlastnosti[0]],[vlastnosti[1]],[vlastnosti[2]],[vlastnosti[3]]] #obalim tie hodnoty do pola  .. ako Integer v jave
        self.suradnice = [int(surPix[0]/64),int(surPix[1]/64)]
        self.hra = hra
        pygame.sprite.Sprite.__init__(self,self.hra.dajAktivBlitGroup(),self.hra.dajPostavyGroup())
        self.inventar = inventar.Inventar(20)
        self.inventarRychlyPristup = invVyuzPredmetu.InvVyuzPredmetu(9,self)
        
        
        self.image = pygame.Surface((sirka,vyska))
        self.rect = self.image.get_rect()
        
        self.smer = smerPostavy.SmerPostavy.DOPREDU
        self.imageZaloha = textury
        


        
        self.rectTextOblastMapa = self.image.get_rect()
        self.rectTextOblastMapa = self.rectTextOblastMapa.move(surPix[0],surPix[1])
        
        
        
        
        #obj oblast sa nachadza kvazi pod nohami, vzhladom na styl textur je obj oblast momentalne z casti mimo texturovej oblasti - zo spodnej casti textury pretrcaa
        self.rectObjOblastZaloha = None #fixna poloha voci texturovej oblasti pri pouziti na mapa je potrebne vyuzit aktualizovanu verziu
        self.typPostavy = typP[0]
        if self.typPostavy == EnumTypPostavy.UZKA:
            x = int(sirka*0.375)
            y = int(vyska*0.85)
            w = int(sirka*0.25)
            h = int(vyska*0.25)
            self.rectObjOblastZaloha = pygame.Rect(x,y,w,h)
        elif self.typPostavy == EnumTypPostavy.FIT:
            x = int(sirka*0.35)
            y = int(vyska*0.8)
            w = int(sirka*0.3)
            h = int(vyska*0.3)
            self.rectObjOblastZaloha = pygame.Rect(x,y,w,h)
        elif self.typPostavy == EnumTypPostavy.SILNA:
            x = int(sirka*0.325)
            y = int(vyska*0.75)
            w = int(sirka*0.35)
            h = int(vyska*0.35)
            self.rectObjOblastZaloha = pygame.Rect(x,y,w,h)
        else:
            logging.warning("vytvaranie objektovej oblasti hraca -> Neznamy typ postavy: " + str(self.typPostavy))
            self.rectObjOblastZaloha = None
            
        
        
        
        self.aktualizujObjOblast()
        #self.rectTextOblastMapa.x = surPix[0]
        #self.rectTextOblastMapa.y = surPix[1]
        self.topLeftScaleMap = [self.rect.x, self.rect.y]
        self.topLeftNoScaleMap = self.topLeftScaleMap.copy()
        #self.rect.x = sur[0]#?
        #self.rect.y = sur [1]
        self.scale(1)#da sa aj lepsie
        #self.pixeloveUmiestnenieNaMape = sur # pixel ktory urcuje jeho polohu - stred hitboxu
       
        self.suradnicePolicka = [int(surPix[0]/64),int(surPix[1]/64)]
        self.objMapaNaokolo = pygame.sprite.Group()
        
        self.topLeftDouble = list(surPix) # uklada sa umiestnenie hraca top left ... je to spojite cislo koli rychlosti pretypuje sa vzdy do int ked treba posunut
        
        self.volneVlastnosti = [3]
        
        
        self.reinitVlastnosti()
        self.vydrz = self.capVydrz # len 1. krat
        
        self.vlozPredmety()
        
        
    def dajRect(self):
        return self.rect
        
    def dajRectTextOblastMapa(self):
        return self.rectTextOblastMapa
        
    def dajHru(self):
        return self.hra
        
    def dajTextOblastMapa(self):
        return self.rectTextOblastMapa
        
        
    def dajTopLeftScaleMap(self):
        return self.topLeftScaleMap
        
    def dajTopLeftNoScaleMap(self):
        return self.topLeftNoScaleMap
        
    def reinitVlastnosti(self):
        self.capVydrz = self.vlastnosti[3][0]*50+100
        
        self.maxRychlostSprint = 1.5+self.vlastnosti[2][0]*0.25
        self.maxRychlost = 1+self.vlastnosti[2][0]*0.2
        self.zrychlenie = self.maxRychlost/10
        self.zrychlenieSprint = self.maxRychlostSprint/8
        
        self.spomalovanie = 0.15 # ako rychlo clovek brzdi 
        if self.typPostavy == 0:
            self.spomalovanie = 0.15 
        elif self.typPostavy == 1:
            self.spomalovanie = 0.13 
        elif self.typPostavy == 2:
            self.spomalovanie = 0.11 
        
        self.smerPohybu=[0,0]
        self.jeSprintPovoleny = True
        self.jeKoliznyStav = False
        self.obnovovanieVydrze = 1+self.vlastnosti[3][0]*0.1
        self.koliznySmerPohybu = [0,0]
        self.koeficienRychlosti = 1
        
        self.priemSucKoefRychl = 0
        self.pocKoefRychlosti = 0
        
    def dajVolneVlastnosti(self):
        return self.volneVlastnosti
    


    def dajSmerPostavy(self):
        return self.smer
    
    '''
    def dajSuradnicePreAnimaciu(self):
        if self.smerPohybu == SmerPostavy.DOPREDU:
            return [self.rect.centerx,self.rect.centery-10]
        if self.smerPohybu == SmerPostavy.DOZADU:
            return [self.rect.centerx,self.rect.centery-10]
        if self.smerPohybu == SmerPostavy.DOPRAVA:
            return [self.rect.centerx+10,self.rect.centery-10]
        if self.smerPohybu == SmerPostavy.DOLAVA:
            return [self.rect.centerx-10,self.rect.centery-10]
        else:
            return [self.rect.centerx,self.rect.centery-10]
    '''
    
    def linkMapa(self,mapa):
        self.mapa = mapa
        self.inventarRychlyPristup.linkMapa(self.mapa)
        
    def dajVlastnosti(self):
        return self.vlastnosti
        
    def dajInventar(self):
        return self.inventar
    
    def vlozPredmet(self,predmet):
        self.inventar.vlozPredmet(predmet)

    def vlozPredmety(self):
        self.inventar.vlozPredmet(predmet.Predmet(10,12))
        self.inventar.vlozPredmet(predmet.Predmet(13,15))
        self.inventar.vlozPredmet(predmet.Predmet(12,50))
        self.inventar.vlozPredmet(predmet.Predmet(13,2))
        self.inventar.vlozPredmet(predmet.Predmet(13,36))
        self.inventar.vlozPredmet(predmet.Predmet(2000,15))
        self.inventar.vlozPredmet(predmet.Predmet(3001,1))
        self.inventar.vlozPredmet(predmet.Predmet(3000,2))

        
        self.inventarRychlyPristup.vlozPredmet(predmet.Predmet(5,36))
        self.inventarRychlyPristup.vlozPredmet(predmet.Predmet(4000,20))
        self.inventarRychlyPristup.vlozPredmet(predmet.Predmet(3000,1))
        
    def dajInventarRychlyPristup(self):
        return self.inventarRychlyPristup


    def collideOkolieHrac(self,sprite1,sprite2):
        koliz =  sprite1.dajObjOblastMapa().colliderect(sprite2.dajObjOblastMapa())
        if koliz:
            self.pocKoefRychlosti +=1
            koef = sprite2.dajKoeficienRychlosti()
            self.priemSucKoefRychl += koef
            
            if koef == 0:
                return True
            else:
                return False
            
            
        
        
    def initMapu(self): # po inicializovani mapy
        self.dajNoveOkolie()
        
    def dajObjOblastMapa(self):
        return self.rectObjOblast
        

    def update(self, *args):
        self.inventarRychlyPristup.update()
        
    def aktualizujObjOblast(self):
        #aktualizacia rect obj oblasti
        self.rectObjOblast = pygame.sprite.Rect(self.rectTextOblastMapa.x+self.rectObjOblastZaloha.x,
                                                self.rectTextOblastMapa.y+self.rectObjOblastZaloha.y,
                                                self.rectObjOblastZaloha.width, self.rectObjOblastZaloha.height)
        
        
        
        
    def dajNoveOkolie(self):
        self.objMapaNaokolo = self.hra.mapa.dajObjektyVOblasti(3,self.suradnice[0],self.suradnice[1])

        
        
        
    def posunObjNaokoloDoprava(self):
        self.dajNoveOkolie()
    def posunObjNaokoloDolava(self):
        self.dajNoveOkolie()
    def posunObjNaokoloHore(self):
        self.dajNoveOkolie()
    def posunObjNaokoloDole(self):
        self.dajNoveOkolie()
        
    def nastalaKoliziaSOkolim(self):
        #zisti koliziu a vypocita koeficien upravy rychlosti
        kolizia = pygame.sprite.spritecollide(self, self.objMapaNaokolo, False, self.collideOkolieHrac)
        if self.pocKoefRychlosti > 0:
            self.koeficienRychlosti = self.priemSucKoefRychl/self.pocKoefRychlosti
            self.priemSucKoefRychl = 0
            self.pocKoefRychlosti = 0
        else:
            self.koeficienRychlosti = 1
        return kolizia
        

    def posunPostavu(self, vertical, horizontal):
        self.aktualizujObjOblast()
        
        nastalaKolizia = self.nastalaKoliziaSOkolim()
        
        if vertical == 0:
            if self.smerPohybu[0] > 0:
                self.smerPohybu[0] -= self.spomalovanie
                if self.smerPohybu[0]<0:
                    self.smerPohybu[0]=0
                    
            if self.smerPohybu[0] < 0:
                self.smerPohybu[0] += self.spomalovanie
                if self.smerPohybu[0]>0:
                    self.smerPohybu[0]=0
                    
        if horizontal == 0:
            if self.smerPohybu[1] > 0:
                self.smerPohybu[1] -= self.spomalovanie
                if self.smerPohybu[1]<0:
                    self.smerPohybu[1]=0
                    
            if self.smerPohybu[1] < 0:
                self.smerPohybu[1] += self.spomalovanie
                if self.smerPohybu[1]>0:
                    self.smerPohybu[1]=0
            
        
        #print ("koef:" + str(self.koeficienRychlosti))
        if nastalaKolizia:
            #print("nastala kolizia")
            if not self.jeKoliznyStav:
                self.jeKoliznyStav=True
                #self.koliznySmerPohybu = [self.smerPohybu[0],self.smerPohybu[1]]
                if self.smerPohybu[0]>0:
                    self.koliznySmerPohybu[0] = -1
                else:
                    self.koliznySmerPohybu[0] = 1
                    
                if self.smerPohybu[1]>0:
                    self.koliznySmerPohybu[1] = -1
                else:
                    self.koliznySmerPohybu[1] = 1
                
                
            self.smerPohybu[0] = self.koliznySmerPohybu[0]*0.35
            self.smerPohybu[1] = self.koliznySmerPohybu[1]*0.35
        else:
            self.jeKoliznyStav=False
            
            klavesy = self.hra.manazerOkien.klavesy
            if klavesy[pygame.K_LSHIFT] and self.jeSprintPovoleny:
                capRychlosti = self.maxRychlostSprint
                self.smerPohybu[0] += self.zrychlenieSprint * vertical 
                self.smerPohybu[1] += self.zrychlenieSprint * horizontal 
                
            else:
                capRychlosti = self.maxRychlost
                self.smerPohybu[0] += self.zrychlenie * vertical 
                self.smerPohybu[1] += self.zrychlenie * horizontal 
                
            if self.smerPohybu[0] > capRychlosti * self.koeficienRychlosti:
                self.smerPohybu[0] = capRychlosti * self.koeficienRychlosti
            if self.smerPohybu[0] < -capRychlosti * self.koeficienRychlosti:
                self.smerPohybu[0] = -capRychlosti  * self.koeficienRychlosti
                
            if self.smerPohybu[1] > capRychlosti * self.koeficienRychlosti:
                self.smerPohybu[1] = capRychlosti* self.koeficienRychlosti
            if self.smerPohybu[1] < -capRychlosti * self.koeficienRychlosti:
                self.smerPohybu[1] = -capRychlosti* self.koeficienRychlosti
            
        if self.smerPohybu[0]>self.smerPohybu[1]:
            maxSmerPohybu = self.smerPohybu[0]
        else:
            maxSmerPohybu = self.smerPohybu[1]
            
        self.vydrz += -maxSmerPohybu + (self.maxRychlost+ 0.1)*self.obnovovanieVydrze # ak sprintuje ubuda ak nie tak ak nebezi max rychlostou tak rastie
        
        if not self.jeSprintPovoleny:
            if self.vydrz > self.capVydrz/8:
                self.jeSprintPovoleny = True
        
        
        if self.vydrz<0:
            self.jeSprintPovoleny = False
            
        
        
        if self.vydrz > self.capVydrz:
            self.vydrz = self.capVydrz
        
        #if nastalaKolizia:
        #print("smer pohybu:" + str(self.smerPohybu))
        
        pomHor = abs(self.smerPohybu[0])
        pomVer = abs(self.smerPohybu[1])
        
        
        if self.smerPohybu[0] != 0:
        
            if self.smerPohybu[0] > 0:
                self.smer = smerPostavy.SmerPostavy.DOPRAVA
                
            else: 
                self.smer = smerPostavy.SmerPostavy.DOLAVA
        else:
            if self.smerPohybu[1] < 0:
                self.smer = smerPostavy.SmerPostavy.DOZADU
            elif self.smerPohybu[1] > 0:
                self.smer = smerPostavy.SmerPostavy.DOPREDU
            else:#hrac sa nehybe pozera za myskou
                pos = pygame.mouse.get_pos()
                mousePos = [pos[0],pos[1]]
                mousePos[0] -= int(nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/2)
                mousePos[1] -= int(nastavenia.ROZLISENIA_Y[nastavenia.vybrateRozlisenie]/2)
                if mousePos[0]*2 >mousePos[1]:#pravo spodna cast
                    if mousePos[0]*2 > -mousePos[1]:#pravohorna
                        self.smer = smerPostavy.SmerPostavy.DOPRAVA
                    else:
                        self.smer = smerPostavy.SmerPostavy.DOZADU
                        
                else: #lavo horna
                    if mousePos[0]*2 > -mousePos[1]:#pravohorna
                        self.smer = smerPostavy.SmerPostavy.DOPREDU
                    else:
                        self.smer = smerPostavy.SmerPostavy.DOLAVA
                       
                    
                
        
        
        
        
        
        
        
        '''
        if pomVer+self.maxRychlost/5 > pomHor :
            #Vertikalne
            if self.smerPohybu[1]<0:
                self.smer = smerPostavy.SmerPostavy.DOZADU
            else:
                self.smer = smerPostavy.SmerPostavy.DOPREDU
            
        else:
            #Horizontalne
            if self.smerPohybu[0]<0:
                self.smer = smerPostavy.SmerPostavy.DOLAVA
            else:
                self.smer = smerPostavy.SmerPostavy.DOPRAVA
        '''
        
            
        self.topLeftDouble[0] += self.smerPohybu[0] 
        self.topLeftDouble[1] += self.smerPohybu[1] 
        self.rectTextOblastMapa= self.rectTextOblastMapa.move(int(self.topLeftDouble[0] - self.rectTextOblastMapa.x), int(self.topLeftDouble[1] - self.rectTextOblastMapa.y))
        
        x = int(self.rectTextOblastMapa.x/64)
        if x != self.suradnice[0]:#zmenil X suradnicu policka
            if x>self.suradnice[0]:
                self.posunObjNaokoloDoprava()
            else:
                self.posunObjNaokoloDolava()   
            self.suradnice[0] = x
            
        y = int(self.rectTextOblastMapa.y/64)
        if y != self.suradnice[1]:#zmenil X suradnicu policka
            if y>self.suradnice[1]:
                self.posunObjNaokoloDole()
            else:
                self.posunObjNaokoloHore()   
            self.suradnice[1] = y
            

        
        
    def eventy(self):
        posun = [0,0]
        
        klavesy = self.hra.manazerOkien.dajKlavesy()
        if klavesy[pygame.K_UP] or klavesy[pygame.K_w]:
            posun[1] +=-1
            
        if klavesy[pygame.K_DOWN] or klavesy[pygame.K_s]:
            posun[1] +=1
            
        if klavesy[pygame.K_LEFT] or klavesy[pygame.K_a]:
            posun[0] +=-1
            
        if klavesy[pygame.K_RIGHT] or klavesy[pygame.K_d]:
            posun[0] +=1
           
        logging.info("Hrac-posunPostavu") 
        
        zalohaSmeru = self.smer
        self.posunPostavu(posun[0],posun[1])
        #print (posun)
        if zalohaSmeru != self.smer:
            self.updateImage()
        
        self.topLeftScaleMap[0] = self.rectTextOblastMapa.x*self.hra.mapa.dajNas()
        self.topLeftScaleMap[1] = self.rectTextOblastMapa.y*self.hra.mapa.dajNas()
        self.topLeftNoScaleMap[0] = self.rectTextOblastMapa.x
        self.topLeftNoScaleMap[1] = self.rectTextOblastMapa.y
        
        logging.info("hrac->mapa-nacitajPolicka")
        self.hra.mapa.nacitajPolicka(self)
        
        
        logging.info("hrac-changelayer")
        #DOROBIT HITBOX NA rect hitboxu
        self.hra.dajAktivBlitGroup().change_layer(self,self.rectTextOblastMapa.y+30)
        
        
    def dajLayer(self):
        return self.rectTextOblastMapa.y+30

    def zmenVyznacenyPredmet(self,cislo):
        self.inventarRychlyPristup.zmenOznacenie(cislo)
        
        
    def klikButton1(self):
        self.inventarRychlyPristup.leftClick()
    def klikButton2(self):
        pass
    def klikButton3(self):
        self.inventarRychlyPristup.rightClick()
    def klikButton4(self):
        pass
    def klikButton5(self):
        pass 
        
        


    def stlacena0(self):
        pass #na nule nic nerobim zatial
        
    def stlacena1(self):
        self.zmenVyznacenyPredmet(1)
        
    def stlacena2(self):
        self.zmenVyznacenyPredmet(2)
        
    def stlacena3(self):
        self.zmenVyznacenyPredmet(3)
        
    def stlacena4(self):
        self.zmenVyznacenyPredmet(4)
        
    def stlacena5(self):
        self.zmenVyznacenyPredmet(5)
        
    def stlacena6(self):
        self.zmenVyznacenyPredmet(6)
        
    def stlacena7(self):
        self.zmenVyznacenyPredmet(7)
        
    def stlacena8(self):
        self.zmenVyznacenyPredmet(8)
        
    def stlacena9(self):
        self.zmenVyznacenyPredmet(9)
        
    def stlaceneR(self):
        self.inventarRychlyPristup.stlaceneR()
        
    def vykresliOznacenyPredmet(self,screen):
        self.inventarRychlyPristup.draw(screen)
        
        
        