'''
Created on 23. 3. 2017

@author: T.Filip
'''
import pygame
import ObjektyMapa.scale as scale
from Postavy.smerPostavy import SmerPostavy
import nastavenia as nastavenia
import Postavy.tvorcaPostav as tvorcaPostav
from Postavy.enumTypPostavy import EnumTypPostavy
import math
import random
import logging

class Postava(pygame.sprite.Sprite, scale.ObjScaleViacTextur):
    def __init__(self,hra,surPix,sirka,vyska,jeToHrac,textury = None,mapa = None,vlastnosti = None):
        self.mapa = mapa #hrac si linkuje mapu neskor
        self.hra = hra
        self.suradnice = [int(surPix[0]/64),int(surPix[1]/64)]
        self.image = pygame.Surface((sirka,vyska))
        self.rect = self.image.get_rect()
        self.smer = SmerPostavy.DOPREDU
        self.imageZaloha = textury
        
        self.jeMrtvy = False



        
        self.typPostavy = 0
        
        self.vydavanyHluk = 0
        
        self.rectTextOblastMapa = self.image.get_rect()
        self.rectTextOblastMapa = self.rectTextOblastMapa.move(surPix[0],surPix[1])
        
        if not jeToHrac and textury == None:
            self.vygenerujTextury()
            
        
            
        pygame.sprite.Sprite.__init__(self,self.hra.dajAktivBlitGroup(),self.hra.dajPostavyGroup())
        
        
            #obj oblast sa nachadza kvazi pod nohami, vzhladom na styl textur je obj oblast momentalne z casti mimo texturovej oblasti - zo spodnej casti textury pretrcaa
        self.rectObjOblastZaloha = None #fixna poloha voci texturovej oblasti pri pouziti na mapa je potrebne vyuzit aktualizovanu verziu
        self.initObjOblast(sirka, vyska)

        if vlastnosti != None:
            self.vlastnosti = [[vlastnosti[0]],[vlastnosti[1]],[vlastnosti[2]],[vlastnosti[3]]] #potrebne ich zaobalit 
            
        #HP
        zd = 80 + 5*self.typPostavy + 5*self.vlastnosti[0][0]
        self.zdravie = zd
        self.maxZdravie = zd
        #
            
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
            
            
    def setTypPostavy(self,enumTyp):
        self.typPostavy = enumTyp
        
    def setVlastnosti(self,vlastnosti):
        self.vlastnosti = vlastnosti
            
    def dajHp(self):
        return self.zdravie
    
    def dajMaxHp(self):
        return self.maxZdravie
            
    def initObjOblast(self,sirka,vyska):

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
            
            
    def dajHodnotuHluku(self):
        return self.vydavanyHluk    
    
    def utlmenieHluku(self):
        self.vydavanyHluk -= 0.1
        if self.vydavanyHluk < 0:
            self.vydavanyHluk = 0 
            
            
            
    def updateScreenPosition(self, mapa):
        scale.ObjScaleViacTextur.updateScreenPosition(self, mapa)
        #naviac aj skontroluje ci je este stale na platne 
        
        if not self.mapa.dajNacitanuMapu().colliderect(self.rectTextOblastMapa):
            self.kill()

            
    def reinitVlastnosti(self):
        self.capVydrz = self.vlastnosti[3][0]*50+100
        
        self.maxRychlostSprint = 1.3+self.vlastnosti[2][0]*0.2
        self.maxRychlost = 0.8+self.vlastnosti[2][0]*0.15
        self.zrychlenie = self.maxRychlost/20
        self.zrychlenieSprint = self.maxRychlostSprint/15
        
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
    
    def dajVlastnosti(self):
        return self.vlastnosti
    
    def dajInventar(self):
        return self.inventar
            
    #def initObjOblast(self,sirka,vyska):
    #    self.rectObjOblastZaloha = pygame.Rect(0,0,sirka,vyska)
        
    
    
    def vygenerujTextury(self):
        
        self.imageZaloha = tvorcaPostav.vytvorPostavuRandom(False,self)
        '''
        cap = random.randint(0,len(nastavenia.FARBA_TELA)-1)
        farbaTela = nastavenia.FARBA_TELA[cap]
        cap = nastavenia.CAP_TYP_POSTAVY
        typPostavy = random.randint(cap[0],cap[1])
        cap = nastavenia.CAP_POHLAVIE
        pohlavie = random.randint(cap[0],cap[1])
        cap = nastavenia.CAP_TVAR[pohlavie]
        tvar = random.randint(cap[0],cap[1])
        cap = nastavenia.CAP_VLASY[pohlavie]
        vlasy = random.randint(cap[0],cap[1])
        cap = nastavenia.CAP_HLAVA
        hlava = random.randint(cap[0],cap[1])
        

        self.imageZaloha = [tvorcaPostav.vytvorPostavu(False, 0, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                            ,tvorcaPostav.vytvorPostavu(False, 1, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                            ,tvorcaPostav.vytvorPostavu(False, 2, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                            ,tvorcaPostav.vytvorPostavu(False, 3, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                            ,tvorcaPostav.vytvorPostavu(False, 4, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)]
        '''
            
            
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
    
    def update(self,*args):
        #args [0] = modulo 100
        self.utlmenieHluku()

    
    
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
            
    def collidePostavy(self,sprite1,sprite2):
        return sprite1.dajObjOblastMapa().colliderect(sprite2.dajObjOblastMapa())
    
            
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
    
    
    
    
    def pobuchajPostavy(self,zoznamPostav):
        #v zozname sa nachadza aj hrac
        print("pobuchajPostavy-nefunguje spravne - nepouzivat")
        return
        for postava in zoznamPostav:
            if postava == self:
                continue
            vzdialenost = self.dajVzdialenostOdPostavy(postava)
            if vzdialenost == 0:
                vzdialenost = 1
            silaOdpudivosti = math.log(vzdialenost/25)#-vzdialenost/20+1
            objOblastPostavy = postava.dajObjOblastMapa()
            vektorOdstrknutia = [objOblastPostavy.centerx-self.rectObjOblast.centerx,objOblastPostavy.centery-self.rectObjOblast.centery]
            suc = math.fabs(vektorOdstrknutia[0])+math.fabs(vektorOdstrknutia[1])
            if suc == 0:
                suc = 1
            vektorOdstrknutia[0] = vektorOdstrknutia[0]/suc*silaOdpudivosti*3#vektor uz ma aj silu taktiez vzhladom na vzdialenost
            vektorOdstrknutia[1] = vektorOdstrknutia[1]/suc*silaOdpudivosti*3
            postava.pozmenSmerPohybu(vektorOdstrknutia)
            
            
    def pozmenSmerPohybu(self,smer):
        self.smerPohybu[0] += smer[0]
        self.smerPohybu[0] += smer[1]
        
    def udelPoskodenie(self,poskodenie):
        if poskodenie <= 0:
            return 
        self.zdravie -= poskodenie
        if self.zdravie <= 0:
            self.zdravie = 0
            self.jeMrtvy = True
            self.upravSpecialMrtvy()
            self.smer = SmerPostavy.SPECIAL
            self.updateImage()
            self.kill()
            self.pocetTickovVymazania = random.triangular(1000,4000,2500) + self.hra.dajPocetTickov()
            mpg = self.hra.dajMrtvePostavy()
            self.add(mpg)
            self.vydavanyHluk = 0
            self.hra.zrusNahananie(self)
            
    def zvysZdravie(self,oKolko):
        self.zdravie += oKolko
        if self.zdravie > self.maxZdravie:
            self.zdravie = self.maxZdravie
            
    def upravSpecialMrtvy(self):
        tvorcaPostav.upravSpecialNaKrv(self.imageZaloha[3])#len ju upravy bez toho aby robil kopia a pod... kazda postava ma originalne textury
        
    def cekniVymazaniePostavy(self):
        if self.jeMrtvy and self.pocetTickovVymazania < self.hra.dajPocetTickov():
            self.kill()
    
    
    def jePostavaMrtva(self):
        return self.jeMrtvy
        
    def dajPotencialnuSiluBuchnutia(self):
        if self.typPostavy == EnumTypPostavy.UZKA:
            return [self.smerPohybu[0]*0.1,self.smerPohybu[1]*0.1]
        elif self.typPostavy == EnumTypPostavy.FIT:
            return [self.smerPohybu[0]*0.2,self.smerPohybu[1]*0.2]
        elif self.typPostavy == EnumTypPostavy.SILNA:
            return [self.smerPohybu[0]*0.3,self.smerPohybu[1]*0.3]
        
        
        #usetri zlozitost budem iterovat cez zoznam iba raz inak by som musel raz a potom este jeden krat v podzozname
    def odstrcBlizkePostavy(self):
        postavy = self.hra.dajPostavyGroup()
        #ret = False
        for postava in postavy:
            if postava == self:
                continue
            vzdialenost = self.dajVzdialenostOdPostavy(postava)
            if vzdialenost > 30:
                continue
            if vzdialenost <= 0:
                vzdialenost = 1
                
            silaOdpudivosti = -math.log(vzdialenost/31)#-vzdialenost/20+1
            self.aktualizujObjOblast()
            objOblastPostavy = postava.dajObjOblastMapa()
            vektorOdstrknutia = [objOblastPostavy.centerx-self.rectObjOblast.centerx,objOblastPostavy.centery-self.rectObjOblast.centery]
            suc = math.fabs(vektorOdstrknutia[0])+math.fabs(vektorOdstrknutia[1])
            if suc == 0:
                suc = 1
                
            #print(silaOdpudivosti)
            vektorOdstrknutia[0] = vektorOdstrknutia[0]/suc*silaOdpudivosti#vektor uz ma aj silu taktiez vzhladom na vzdialenost
            vektorOdstrknutia[1] = vektorOdstrknutia[1]/suc*silaOdpudivosti
            postava.pozmenSmerPohybu(vektorOdstrknutia)
            
        
    
    def dajObjOblastMapa(self):
        self.aktualizujObjOblast()
        return self.rectObjOblast
        

    def posunPostavu(self,horizontal,vertical):
        zalohaSmer = self.smer
        self.aktualizujObjOblast()
        
        nastalaKoliziaSOkolim = self.nastalaKoliziaSOkolim()
        
        if horizontal == 0:
            if self.smerPohybu[0] > 0:
                self.smerPohybu[0] -= self.spomalovanie
                if self.smerPohybu[0]<0:
                    self.smerPohybu[0]=0
                    
            if self.smerPohybu[0] < 0:
                self.smerPohybu[0] += self.spomalovanie
                if self.smerPohybu[0]>0:
                    self.smerPohybu[0]=0
                    
        if vertical == 0:
            if self.smerPohybu[1] > 0:
                self.smerPohybu[1] -= self.spomalovanie
                if self.smerPohybu[1]<0:
                    self.smerPohybu[1]=0
                    
            if self.smerPohybu[1] < 0:
                self.smerPohybu[1] += self.spomalovanie
                if self.smerPohybu[1]>0:
                    self.smerPohybu[1]=0
            
        
        

        if nastalaKoliziaSOkolim:#ak je zoznam vobec niecim naplneny
            
            #self.stare
            if not self.jeKoliznyStav:
                self.jeKoliznyStav=True
                self.koliznySmerPohybu[0] = -self.smerPohybu[0]*0.2
                self.koliznySmerPohybu[1] = -self.smerPohybu[1]*0.2
                
            self.smerPohybu[0] = self.koliznySmerPohybu[0]
            self.smerPohybu[1] = self.koliznySmerPohybu[1]
            self.smerPohybu[0] += horizontal*0.03
            self.smerPohybu[1] += vertical*0.03
        else:
            self.jeKoliznyStav=False
            self.odstrcBlizkePostavy()
            #postavyGroup = self.hra.dajPostavyGroup()
            #zoznamBuchnutych = pygame.sprite.spritecollide(self, postavyGroup, False,self.collidePostavy)
            #if len(zoznamBuchnutych)>1:
                #nastala kolizia s hracmi
                #self.pobuchajPostavy(zoznamBuchnutych)
            '''
            if not self.jeKoliznyStavSHracom:
                self.jeKoliznyStavSHracom = True
                self.koliznySmerPohybu[0] = self.smerPohybu[0]*-0.1
                self.koliznySmerPohybu[1] = self.smerPohybu[1]*-0.1
            
            self.smerPohybu[0] = self.koliznySmerPohybu[0]+horizontal*0.05
            self.smerPohybu[1] = self.koliznySmerPohybu[1]+vertical*0.05
            '''
                

            capRychlosti = self.zvysRychlostPohybu(horizontal,vertical) 
                
            if self.smerPohybu[0] > capRychlosti[0] * self.koeficienRychlosti:
                self.smerPohybu[0] = capRychlosti[0] * self.koeficienRychlosti
                #self.smerPohybu[0] -= self.spomalovanie*3 #nebude sa to zarovnavat do capu ale bude miesto toho spomalovat
            if self.smerPohybu[0] < -capRychlosti[0] * self.koeficienRychlosti:
                self.smerPohybu[0] = -capRychlosti[0]  * self.koeficienRychlosti
                #self.smerPohybu[0] += self.spomalovanie*3
                
            if self.smerPohybu[1] > capRychlosti[1] * self.koeficienRychlosti:
                self.smerPohybu[1] = capRychlosti[1]* self.koeficienRychlosti
                #self.smerPohybu[1] -= self.spomalovanie*3
            if self.smerPohybu[1] < -capRychlosti[1] * self.koeficienRychlosti:
                self.smerPohybu[1] = -capRychlosti[1]* self.koeficienRychlosti
                #self.smerPohybu[1] += self.spomalovanie*3
                     
            
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
        
        #pomHor = abs(self.smerPohybu[0])
        #pomVer = abs(self.smerPohybu[1])
        
        #self.smer = SmerPostavy.DOPREDU
        if horizontal >= 0:
            
            if vertical >= 0:
                #++
                if horizontal*2 > vertical:
                    self.smer = SmerPostavy.DOPRAVA
                else:
                    self.smer = SmerPostavy.DOPREDU
            
            elif self.smerPohybu[1] <= 0:
                #+-
                if horizontal*2 > math.fabs(vertical):
                    self.smer = SmerPostavy.DOPRAVA
                else:
                    self.smer = SmerPostavy.DOZADU
            
        elif horizontal <= 0:
            
            if self.smerPohybu[1] >= 0:
                #-+
                if math.fabs(horizontal)*2 > vertical:
                    self.smer = SmerPostavy.DOLAVA
                else:
                    self.smer = SmerPostavy.DOPREDU
            
            
            elif self.smerPohybu[1] <= 0:
                #--
                if math.fabs(horizontal)*2 > math.fabs(vertical):
                    self.smer = SmerPostavy.DOLAVA
                else:
                    self.smer = SmerPostavy.DOZADU

        self.smerPostavyPriStati(horizontal, vertical)

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
            
        if self.smer != zalohaSmer:
            self.updateImage()
            
            #ak dycha nahlas vydava hluk ktory pritahuje npc
        self.vydavanyHluk += 0.05
        if self.vydrz < self.capVydrz/4:
            self.vydavanyHluk += 0.05
        elif self.vydrz < self.capVydrz/8:
            self.vydavanyHluk += 0.1
        elif self.vydrz < self.capVydrz/12:
            self.vydavanyHluk += 0.2
        
            # velkost postavy ovplyvnuje vydavany zvuk pri behani

        self.vydavanyHluk += self.typPostavy * 0.05

            
            

            
    def smerPostavyPriStati(self,horizontal,vertical):
        pass
            
    def zvysRychlostPohybu(self,horizontal,vertical):
        if self.mozeSprintovat() and self.jeSprintPovoleny:
            capRychlosti = [self.maxRychlostSprint, self.maxRychlostSprint]
            self.smerPohybu[0] += self.zrychlenieSprint * horizontal
            self.smerPohybu[1] += self.zrychlenieSprint * vertical 
            
        else:
            capRychlosti = [self.maxRychlost, self.maxRychlost]
            self.smerPohybu[0] += self.zrychlenie * horizontal
            self.smerPohybu[1] += self.zrychlenie * vertical
            
        return capRychlosti
        
            
            
    def dajLayer(self):
        return self.rectTextOblastMapa.y+30
    
    def mozeSprintovat(self):
        False
    

            
            