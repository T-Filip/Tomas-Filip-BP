'''
Created on 9. 3. 2017

@author: T.Filip
'''

import pygame
#import ObjektyMapa.infObjekty as infObjekty
from Textury import textury
from Nastavenia import nastavenia
#from _operator import pos
from Textury import enumTextura

class Predmet (pygame.sprite.Sprite):
    def __init__(self,id,pocetKusov = 1):
        import ObjektyMapa.infObjekty as infObjekty
        #mutual top-level imports -> predmety su zavisle na datach ktore su obsiahnute v triedach v module InfObjekty tie vsak obsahuju metody a data ktore su zavisle na predmetoch takze sa to cykli
        self.inf = infObjekty.INF_OBJ_MAPA[id]
        self.id = id
        self.miestoPrePredmet = None
        self.pocetKusov = pocetKusov
        pygame.sprite.Sprite.__init__(self)
        
    def setPocetKusov(self, ks, maPrekreslit = True):
        self.pocetKusov = ks
        if maPrekreslit:
            self.aktualizujGrafiku()
        
        
    def zmenPocetKusovO(self,ks):
        self.pocetKusov += ks
        kolkoZobralo = ks
        if self.pocetKusov <= 0:
            self.kill()
            self.miestoPrePredmet.vymazPredmet()
            return kolkoZobralo - self.pocetKusov
        elif self.pocetKusov > self.inf.stackKapacita:
            kolkoZobralo -= self.pocetKusov - self.inf.stackKapacita
            self.pocetKusov = self.inf.stackKapacita
        self.aktualizujGrafiku()
        return kolkoZobralo
           
    def dajId(self):
        return self.id
            
    def dajPocetKusov(self):
        return self.pocetKusov
    
    def dajImgNaMape(self):
        return self.inf.dajImgNaMape()
    
    def dajImgPredm(self,cislo=0):
        return self.inf.dajImgPredm(cislo)
    
    def dajInf (self):
        return self.inf

        

    def dajStackKapacitu(self):
        return self.inf.dajStackKapacitu()
    
    def vlozDoGroup(self,group):#treba mi to?
        self.kill()
        self.add(group)
        
    def vlozDoMiesta(self,miesto):
        miesto.vlozPredmet(self)
    
    
    '''
    jeden predmet sa zrusi a v jednom sa zmeni pocet
    '''    
    def zlucPredmety (self,pred):
        kolkoZobralo = self.zmenPocetKusovO(pred.dajPocetKusov())
        pred.zmenPocetKusovO(-kolkoZobralo)

    '''
    najma pri zmene poctu treba aktualizovat grafiku aby bolo viditelne realne cislo ktore vyznacuje pocet kusov
    '''  
    def aktualizujGrafiku(self):
        self.aktualizujPoziciu()
        pom = self.inf.dajImgPredm().copy()
        textSurf = textury.dajFont(int(self.rect.width/3.5)).render(str(self.pocetKusov),1, nastavenia.BLACK)
        textX = self.rect.width-textSurf.get_width()-2
        textY = self.rect.height-textSurf.get_height()-1
        self.image = pygame.transform.scale(pom,(self.rect.width,self.rect.height))
        self.image.blit(textSurf,(textX,textY))
        
    def aktualizujPoziciu(self):
        self.rect = self.miestoPrePredmet.dajRectPrePredmet()
        
        
    '''
    metoda vyuzivana ak pedmet nie je v groupe .. hlavne ak hrac "drzi" predmet v myske
    '''
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        
        
        
'''
Trieda ktora predstavuje miesto na ktore sa moze vlozit predmet
'''        
class MiestoPrePredmet:
    def __init__(self,groupa):
        self.grupaPrePredmety = groupa # predmety sa vykresluju aj ked toto miesto nie 
        self.predmet = None
        
        
    def vlozPredmet(self,pred):
        pred.kill()
        self.predmet = pred
        if pred.miestoPrePredmet != None:
            pred.miestoPrePredmet.predmet = None
        self.predmet.miestoPrePredmet = self
        self.predmet.aktualizujGrafiku()
        self.vlozDoGroup()

    def dajPredmet(self):
        return self.predmet
        
    def vydajPredmet(self):
        self.predmet.miestoPrePredmet = None
        return self.predmet
        
    def vlozDoGroup(self):
        self.predmet.vlozDoGroup(self.grupaPrePredmety)#ked tam uz je nic sa nestane

    def vymazPredmet(self):
        self.predmet = None
        
    def update(self):
        pass
    
    def dajRectPrePredmet(self):
        pass
    
    
'''

miesto na ktorom sa vykresluje predmet ked ho hrac drzi v myske
'''   
class MiestoPrePredmetMyska(MiestoPrePredmet):
    def __init__(self):
        MiestoPrePredmet.__init__(self,None)
        self.posunX = 0
        self.posunY = 0
        self.mousePos = (100,100)
        self.velkostStrany = 64
        self.posMys = (0,0)
        self.groupPredmet = pygame.sprite.RenderPlain()#lebo musi byt v grupe aby sa dobre kreslilo
        
    def update(self, posMys):
        self.posMys = posMys
        
    def vlozPredmet(self, pred,posunX,posunY,velkostSt):
        self.posunX = posunX
        self.posunY = posunY
        self.velkostStrany = velkostSt
        self.groupPredmet.empty()
        MiestoPrePredmet.vlozPredmet(self, pred)

        
    def vymazPredmet(self):
        MiestoPrePredmet.vymazPredmet(self)
        self.groupPredmet.empty()

        
        
        
    def initMousePosition(self,pos):
        self.mousePos = pos
        

    '''
    vrati miesto kde by sa predmet mal nachadzat - a teda miesto kde sa nachadza samotne miesto pre predmet
    '''   
    def dajRectPrePredmet(self):
        pos = pygame.mouse.get_pos()
        return pygame.Rect(pos[0]-self.posunX,pos[1]-self.posunY,self.velkostStrany,self.velkostStrany)
        
    def vlozDoGroup(self):
        self.groupPredmet.add(self.predmet)

        
class MiestoPredmetu (pygame.sprite.Sprite,MiestoPrePredmet):
    def __init__(self,group,inventar):
        self.inventar = inventar
        self.rect = pygame.Rect(0,0,64,64)
        pygame.sprite.Sprite.__init__(self,group)
        MiestoPrePredmet.__init__(self,self.inventar.predmety)
        
    def reinit(self,x,y, velkostStrany):
        self.rect = pygame.Rect(x,y,velkostStrany,velkostStrany)
        self.updateImage(velkostStrany)
        
    def updateImage(self,velkostStrany):
        self.image = textury.dajTexturu(enumTextura.EnumTextura.MIESTO_PREDMET, velkostStrany,velkostStrany)
        
    def dajRectPrePredmet(self):
        return self.rect
    
class MiestoPredmetuOznacitelne (MiestoPredmetu):
    def __init__(self,group,inventar):
        self.jeOznacene = False
        self.nastalReinit = False
        super().__init__(group, inventar)
        
    def updateImage(self,velkostStrany):
        if not self.nastalReinit:
            return
        if self.jeOznacene:
            self.image = textury.dajTexturu(enumTextura.EnumTextura.MIESTO_PREDMET_OZNACENY, self.velkostStrany, self.velkostStrany)
        else:
            self.image = textury.dajTexturu(enumTextura.EnumTextura.MIESTO_PREDMET, self.velkostStrany, self.velkostStrany)
            
    def reinit(self, x, y, velkostStrany):
        self.nastalReinit = True
        self.velkostStrany = velkostStrany
        MiestoPredmetu.reinit(self, x, y, velkostStrany)
            
        
    def zmenOznacene(self,hodnota):
        if hodnota != self.jeOznacene:
            self.jeOznacene = hodnota
            self.updateImage(0)
    


        