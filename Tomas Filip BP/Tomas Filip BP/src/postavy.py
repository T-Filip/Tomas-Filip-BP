import pygame
import ObjektyMapa.objMapa as objMapa
import ObjektyMapa.scale as scale
import random
from tkinter.constants import HORIZONTAL
import logging



class Hrac(pygame.sprite.Sprite, scale.ObjScale):
    def __init__(self,hra,surPix, rectObjektovaOblast):
        self.suradnice = [int(surPix[0]/64),int(surPix[1]/64)]
        self.hra = hra
        pygame.sprite.Sprite.__init__(self,self.hra.dajAktivBlitGroup())
        self.image = pygame.Surface((64,64))
        self.rect = self.image.get_rect()
        
        self.imageZaloha = pygame.Surface((64,64))
        self.imageZaloha.fill((200,100,0))
        self.rectTextOblastMapa = self.image.get_rect()
        self.rectTextOblastMapa = self.rectTextOblastMapa.move(surPix[0],surPix[1])
        
        self.rectObjOblastZaloha = rectObjektovaOblast #fixna poloha voci texturovej oblasti pri pouziti na mapa je potrebne vyuzit aktualizovanu verziu
        self.aktualizujObjOblast()
        #self.rectTextOblastMapa.x = surPix[0]
        #self.rectTextOblastMapa.y = surPix[1]
        self.topLeftScaleMap = [self.rect.x, self.rect.y]
        #self.rect.x = sur[0]#?
        #self.rect.y = sur [1]
        self.scale(1)#da sa aj lepsie
        #self.pixeloveUmiestnenieNaMape = sur # pixel ktory urcuje jeho polohu - stred hitboxu
       
        self.suradnicePolicka = [int(surPix[0]/64),int(surPix[1]/64)]
        self.objMapaNaokolo = pygame.sprite.Group()
        
        self.topLeftDouble = list(surPix) # uklada sa umiestnenie hraca top left ... je to spojite cislo koli rychlosti pretypuje sa vzdy do int ked treba posunut
        
        self.vydrz = 400
        self.capVydrz = 400
        self.maxRychlostSprint = 2.5#3
        self.maxRychlost = 1.8#2 
        self.zrychlenie = 0.2
        self.zrychlenieSprint = 0.3
        self.spomalovanie = 0.15 # ako rychlo clovek brzdi 
        self.smerPohybu=[0,0]
        self.jeSprintPovoleny = True
        self.jeKoliznyStav = False
        self.obnovovanieVydrze = 1 # v percentach
        self.koliznySmerPohybu = [0,0]
        self.koeficienRychlosti = 1
        
        self.priemSucKoefRychl = 0
        self.pocKoefRychlosti = 0
        


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
        i = 6
        #self.hra.mapa.updatniPoziciu(self.topLeftScaleMap,self.rect)
        #print("hrac: " + str(self.rectTextOblastMapa))
        #self.rect.x = self.pixeloveUmiestnenieNaMape[0] - self.hra.mapa.lavoHorePixelKamera[0]-32
        #self.rect.y = self.pixeloveUmiestnenieNaMape[1] - self.hra.mapa.lavoHorePixelKamera[1]-32
        #print ("hrac suradnice pix: " + str(self.pixeloveUmiestnenieNaMape[0]) + " " + str(self.pixeloveUmiestnenieNaMape[1]))
        #print ("hrac vykreslovanie: " + str(self.rect.x) + " " + str(self.rect.y))
        
    def aktualizujObjOblast(self):
        #aktualizacia rect obj oblasti
        self.rectObjOblast = pygame.sprite.Rect(self.rectTextOblastMapa.x+self.rectObjOblastZaloha.x,
                                                self.rectTextOblastMapa.y+self.rectObjOblastZaloha.y,
                                                self.rectObjOblastZaloha.width, self.rectObjOblastZaloha.height)
        
        
        
        
    def dajNoveOkolie(self):
        
        
        mapa = self.hra.mapa
        self.objMapaNaokolo = pygame.sprite.Group()
        for x in range (self.suradnice[0]-2,self.suradnice[0]+3):
            for y in range (self.suradnice[1]-2,self.suradnice[1]+3):
                    self.objMapaNaokolo.add(mapa.dajPolicko((x,y)).dajVlastneObjekty())
                    
        #print("pocet obj okolie: " + str(len(self.objMapaNaokolo)))
        
        
        
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
            if self.vydrz > 50:
                self.jeSprintPovoleny = True
        
        
        if self.vydrz<0:
            self.jeSprintPovoleny = False
            
        
        
        if self.vydrz > self.capVydrz:
            self.vydrz = self.capVydrz
        
        #if nastalaKolizia:
        #print("smer pohybu:" + str(self.smerPohybu))
            
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
        
        klavesy = self.hra.manazerOkien.klavesy
        if klavesy[pygame.K_UP] or klavesy[pygame.K_w]:
            posun[1] +=-1
            
        if klavesy[pygame.K_DOWN] or klavesy[pygame.K_s]:
            posun[1] +=1
            
        if klavesy[pygame.K_LEFT] or klavesy[pygame.K_a]:
            posun[0] +=-1
            
        if klavesy[pygame.K_RIGHT] or klavesy[pygame.K_d]:
            posun[0] +=1
           
        logging.info("Hrac-posunPostavu") 
        self.posunPostavu(posun[0],posun[1])
        #print (posun)

        
        self.topLeftScaleMap[0] = self.rectTextOblastMapa.x*self.hra.mapa.dajNas()
        self.topLeftScaleMap[1] = self.rectTextOblastMapa.y*self.hra.mapa.dajNas()
        
        logging.info("hrac->mapa-nacitajPolicka")
        self.hra.mapa.nacitajPolicka(self)
        
        
        logging.info("hrac-changelayer")
        #DOROBIT HITBOX NA rect hitboxu
        self.hra.dajAktivBlitGroup().change_layer(self,self.rectTextOblastMapa.y+30)

        
        
        
        