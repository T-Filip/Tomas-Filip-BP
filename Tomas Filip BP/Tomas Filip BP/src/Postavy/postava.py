'''
Created on 23. 3. 2017

@author: T.Filip
'''
import pygame
import ObjektyMapa.scale as scale
import Postavy.smerPostavy as smerPostavy
import nastavenia as nastavenia
import Postavy.tvorcaPostav as tvorcaPostav
import math

class Postava(pygame.sprite.Sprite, scale.ObjScaleViacTextur):
    def __init__(self,hra,surPix,sirka,vyska,jeToHrac,textury = None,mapa = None):
        self.mapa = mapa #hrac si linkuje mapu neskor
        self.hra = hra
        self.suradnice = [int(surPix[0]/64),int(surPix[1]/64)]
        self.image = pygame.Surface((sirka,vyska))
        self.rect = self.image.get_rect()
        self.smer = smerPostavy.SmerPostavy.DOPREDU
        self.imageZaloha = textury
        
        self.typPostavy = 0 #!!!!!!!
        
        self.rectTextOblastMapa = self.image.get_rect()
        self.rectTextOblastMapa = self.rectTextOblastMapa.move(surPix[0],surPix[1])
        
        if not jeToHrac and textury == None:
            self.vygenerujTextury()#!!!!
            
        pygame.sprite.Sprite.__init__(self,self.hra.dajAktivBlitGroup(),self.hra.dajPostavyGroup())
        
        
            #obj oblast sa nachadza kvazi pod nohami, vzhladom na styl textur je obj oblast momentalne z casti mimo texturovej oblasti - zo spodnej casti textury pretrcaa
        self.rectObjOblastZaloha = None #fixna poloha voci texturovej oblasti pri pouziti na mapa je potrebne vyuzit aktualizovanu verziu
        self.initObjOblast(sirka, vyska)
        
        self.vlastnosti = [[0],[0],[0],[0]] #!!!!!!!!
        self.volneVlastnosti = [3]
        self.reinitVlastnosti()
        
        self.aktualizujObjOblast()
        self.topLeftScaleMap = [self.rect.x, self.rect.y]
        self.topLeftNoScaleMap = self.topLeftScaleMap.copy()
        self.scale(1)#da sa aj lepsie
       
        self.suradnicePolicka = [int(surPix[0]/64),int(surPix[1]/64)]
        self.objMapaNaokolo = pygame.sprite.Group()
        
        self.topLeftDouble = list(surPix) # uklada sa umiestnenie hraca top left ... je to spojite cislo koli rychlosti pretypuje sa vzdy do int ked treba posunut
        
        
        self.vydrz = self.capVydrz # len 1. krat
        if self.mapa != None:
            self.scale(self.mapa.dajNas())   
            
            
    def dajHodnotuHluku(self):
        return 1         
            
            
            
    def updateScreenPosition(self, mapa):
        scale.ObjScaleViacTextur.updateScreenPosition(self, mapa)
        #naviac aj skontroluje ci je este stale na platne 
        
        if not self.mapa.dajNacitanuMapu().colliderect(self.rectTextOblastMapa):
            self.kill()

            
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
    
    def dajInventar(self):
        return self.inventar
            
    def initObjOblast(self,sirka,vyska):
        self.rectObjOblastZaloha = pygame.Rect(0,0,sirka,vyska)
        
    
    
    def vygenerujTextury(self):
        self.imageZaloha = [tvorcaPostav.vytvorPostavu(False, 0, 1, 0, 0, 1, 1, 0)
                            ,tvorcaPostav.vytvorPostavu(False, 1, 1, 0, 0, 1, 1, 0)
                            ,tvorcaPostav.vytvorPostavu(False, 2, 1, 0, 0, 1, 1, 0)
                            ,tvorcaPostav.vytvorPostavu(False, 3, 1, 0, 0, 1, 1, 0)
                            ,tvorcaPostav.vytvorPostavu(False, 4, 1, 0, 0, 1, 1, 0)]
            
            
            
    def dajVzdialenostOdPostavy(self,postava):
        pos = postava.dajObjOblastMapa()
        return math.sqrt((self.dajObjOblastMapa().centerx-pos.centerx)**2 + (self.dajObjOblastMapa().centery-pos.centery)**2)
        

    def dajSmerPostavy(self):
        return self.smer
    
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
    
    def update(self):
        pass
    
    
    def aktualizujObjOblast(self):
        #aktualizacia rect obj oblasti
        self.rectObjOblast = pygame.sprite.Rect(self.rectTextOblastMapa.x+self.rectObjOblastZaloha.x,
                                                self.rectTextOblastMapa.y+self.rectObjOblastZaloha.y,
                                                self.rectObjOblastZaloha.width, self.rectObjOblastZaloha.height)
        
        
        
        
    def dajNoveOkolie(self):
        self.objMapaNaokolo = self.hra.mapa.dajObjektyVOblasti(3,self.suradnice[0],self.suradnice[1])
        
        
        #mozna menasia optimalizacia .. meni sa len 1/5 okolia no napriek tomu vytvaram nove 
    def posunObjNaokoloDoprava(self):
        self.dajNoveOkolie()
    def posunObjNaokoloDolava(self):
        self.dajNoveOkolie()
    def posunObjNaokoloHore(self):
        self.dajNoveOkolie()
    def posunObjNaokoloDole(self):
        self.dajNoveOkolie()
        
    def collideOkolie(self,sprite1,sprite2):
        koliz =  sprite1.dajObjOblastMapa().colliderect(sprite2.dajObjOblastMapa())
        if koliz:
            self.pocKoefRychlosti +=1
            koef = sprite2.dajKoeficienRychlosti()
            self.priemSucKoefRychl += koef
            
            if koef == 0:
                return True
            else:
                return False
        
            
    def nastalaKoliziaSOkolim(self):
        #zisti koliziu a vypocita koeficien upravy rychlosti
        if self.objMapaNaokolo == None:
            return True
        kolizia = pygame.sprite.spritecollide(self, self.objMapaNaokolo, False, self.collideOkolie)
        if self.pocKoefRychlosti > 0:
            self.koeficienRychlosti = self.priemSucKoefRychl/self.pocKoefRychlosti
            self.priemSucKoefRychl = 0
            self.pocKoefRychlosti = 0
        else:
            self.koeficienRychlosti = 1
        return kolizia
    
    def dajObjOblastMapa(self):
        return self.rectObjOblast
        

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
            
            capRychlosti = self.zvysRychlostPohybu(horizontal,vertical) 
                
            if self.smerPohybu[0] > capRychlosti[0] * self.koeficienRychlosti:
                self.smerPohybu[0] = capRychlosti[0] * self.koeficienRychlosti
            if self.smerPohybu[0] < -capRychlosti[0] * self.koeficienRychlosti:
                self.smerPohybu[0] = -capRychlosti[0]  * self.koeficienRychlosti
                
            if self.smerPohybu[1] > capRychlosti[1] * self.koeficienRychlosti:
                self.smerPohybu[1] = capRychlosti[1]* self.koeficienRychlosti
            if self.smerPohybu[1] < -capRychlosti[1] * self.koeficienRychlosti:
                self.smerPohybu[1] = -capRychlosti[1]* self.koeficienRychlosti
            
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
                self.smerPostavyPriStati()
                        
            
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
            
            
    def smerPostavyPriStati(self):
        pass
            
    def zvysRychlostPohybu(self,horizontal,vertical):
        if self.mozeSprintovat() and self.jeSprintPovoleny:
            capRychlosti = [self.maxRychlostSprint, self.maxRychlostSprint]
            self.smerPohybu[0] += self.zrychlenieSprint * vertical 
            self.smerPohybu[1] += self.zrychlenieSprint * horizontal 
            
        else:
            capRychlosti = [self.maxRychlost, self.maxRychlost]
            self.smerPohybu[0] += self.zrychlenie * vertical 
            self.smerPohybu[1] += self.zrychlenie * horizontal
            
        return capRychlosti
        
            
            
    def dajLayer(self):
        return self.rectTextOblastMapa.y+30
    
    def mozeSprintovat(self):
        False
    

            
            