'''
Created on 15. 3. 2017

@author: T.Filip
'''
from Predmety import inventar
from Predmety import predmet
import pygame
import math

class InventarOznPredmet(inventar.Inventar):
    def __init__(self,velkost,hrac):
        self.mapa = None
        self.hrac = hrac
        self.polePredmetov = [None for i in range (velkost)]
        super().__init__(velkost)
        self.polePredmetov[0].zmenOznacene(True)
        self.oznacenyIndex = 0
        self.imageOznPredmetu = None
        self.reinitImageOznPredmet()
        #self.starePolickoveSurMysky = [0,0]
        self.scaleRes = 1
        self.jeNacerveno = True
        self.scale = 1
        
    def update(self):
        if self.oznPredmet == None:
            return
        
        k1 = self.kontrolaKolizierOznPredmetu()
        k2 = self.kontrolaZmenyPriblizenia()

        
        
        if k1 or k2:
            self.reinitImageOznPredmet()
            
            
    def kontrolaKolizierOznPredmetu(self):
        sur = self.mapa.dajPolickoveSurMysky()
        okolie = self.mapa.dajOkolieMysky()
        if okolie == None:
            if self.jeNacerveno:
                return False#uz je nacerveno netreba prekreslovat
            self.jeNacerveno = True
            return True
        #print("---------------------------------------")
        scale = self.mapa.dajScaleNas()
        infPredmetu = self.polePredmetov[self.oznacenyIndex].dajPredmet().dajInf()
        rectO = infPredmetu.dajObjOblastMapa()
        #rectText = infPredmetu.dajImgPredm
        rectObjVMyske = pygame.Rect(rectO.x,rectO.y,rectO.width,rectO.height)
        velkostTexObjektu = infPredmetu.dajImgPredm().get_size()
        pos = pygame.mouse.get_pos()
        #topLeftNoScale= self.mapa.dajTopLeftNoScale()
        nacitanaMapa = self.mapa.dajNacitanuMapu()
        rectTopLeftPolicka = self.mapa.dajTopLeftPolicko().dajRect()
        relatMysX= pos[0] - rectTopLeftPolicka.x + rectTopLeftPolicka.width
        relatMysY= pos[1] - rectTopLeftPolicka.y + rectTopLeftPolicka.height
        #print("relat mys na mape" + str(relatMysX) + "  " + str(relatMysY))
        relatMysX = relatMysX/scale
        relatMysY = relatMysY/scale
        #print("relat mys na mape + scale" + str(relatMysX) + "  " + str(relatMysY))
        #x = pos[0]-int(self.imageOznPredmetu.get_width()*self.mapa.dajScaleNas()/3)+topLeftNoScale[0]
        #y = pos[1]-int(self.imageOznPredmetu.get_height()*self.mapa.dajScaleNas()/3)+topLeftNoScale[1]
        #x = pos[0]-int(velkostTexObjektu[0]/3)+topLeftNoScale[0]
        #y = pos[1]-int(velkostTexObjektu[1]/3)+topLeftNoScale[1]
        x = relatMysX + nacitanaMapa.x
        y = relatMysY + nacitanaMapa.y
        #print("pozicia mysky na mape" + str(x) + "  " + str(y))
        x -= velkostTexObjektu[0]/3
        y -= velkostTexObjektu[1]/3

        #print("topleft pozicia obj na mape" + str(x) + "  " + str(y))
        #print ("povodny rect :" + str(rectObjVMyske))
        rectObjVMyske = rectObjVMyske.move(x,y)
        #print("topleft rect myska" + str(rectObjVMyske.x) + "  " + str(rectObjVMyske.y))
        
        
        #print("nacitana mapa:" + str(nacitanaMapa))
        #print("scale:" + str(self.mapa.dajScaleNas()))
        #print("Velksot okolia " + str(len(okolie)))
        #print("rect myska:" + str(rectObjVMyske))
        #print("rect topLeftNoScale:" + str(topLeftNoScale))
        trebaPrekreslit = False
        staraKolizia = self.jeNacerveno
        self.jeNacerveno = False
        for sprite in okolie:
            kol = sprite.dajObjOblastMapa().colliderect( rectObjVMyske)
            #print("objekt:" + str(sprite.dajObjOblastMapa()))
            if kol:
                self.jeNacerveno = True
                break;
            
        #kontrola vzdialenosti
        hrac = self.hrac.dajTextOblastMapa() # vzdialenost medzi objetovou a texturovou 
        vzdialenost = math.sqrt((hrac.centerx-rectObjVMyske.centerx)**2 + (hrac.centery-rectObjVMyske.centery)**2)
        #print (vzdialenost)
        if vzdialenost >192:
            self.jeNacerveno = True
        
        #aby sa to neprekreslovalo zbytocne ak to uz je v stave v akom to potrebujeme mat je tu tato kontrola ktora zabezbeci aby sa to zbytocne neprekreslovalo
        if staraKolizia != self.jeNacerveno:
            return True
        else:
            return False
        
        #self.topLeftObjMyska = (x,y)
        #inak nastala zmena
        self.starePolickoveSurMysky = sur
    def kontrolaZmenyPriblizenia(self):
        scaleNas = self.mapa.dajScaleNas()
        if self.scale != scaleNas:
            self.scale = scaleNas
            return True
        return False

    
        
    def reinitImageOznPredmet(self):
        self.oznPredmet = self.polePredmetov[self.oznacenyIndex].dajPredmet()
        if self.oznPredmet == None:
            return
        texOriginal = self.oznPredmet.dajImgNaMape()
        size = texOriginal.get_size()
        w = int(size[0]*self.mapa.dajScaleNas())
        h = int(size[1]*self.mapa.dajScaleNas())
        #self.imageOznPredmetu = pygame.Surface((w,h),pygame.SRCALPHA)
        self.scaleRes = self.mapa.dajScaleNas()
        self.imageOznPredmetu = pygame.transform.scale(texOriginal,(w,h))
        if self.jeNacerveno:
            self.imageOznPredmetu.fill((255, 50, 50,100), None, pygame.BLEND_RGBA_MULT)
        else:
            self.imageOznPredmetu.fill((100, 100, 100,100), None, pygame.BLEND_RGBA_MULT)
        
        
        #mapa sa vytvara az po vytvoreni hraca preto dodatocne linkovanie
    def linkMapa(self,mapa):
        self.mapa = mapa
        
    def zmenOznacenie(self,cislo):
        cis = cislo - 1
        if self.oznacenyIndex == cis:
            return
        else:
            self.polePredmetov[self.oznacenyIndex].zmenOznacene(False)
            self.polePredmetov[cis].zmenOznacene(True)
            self.oznacenyIndex = cis
            self.reinitImageOznPredmet()
        
        
    def initMiesta(self, velkost):
        
        for i in range(velkost):
            pred = predmet.MiestoPredmetuOznacitelne(self.sloty,self)
            self.polePredmetov[i] = pred
            
            


        
        
        
            
    def draw (self,screen):
        if self.oznPredmet == None:
            return
        
        pos = pygame.mouse.get_pos()
        x = pos[0]-int(self.imageOznPredmetu.get_width()/3)
        y = pos[1]-int(self.imageOznPredmetu.get_height()/3)
        self.topLeftObjMyska = (x,y)
        
        screen.blit(self.imageOznPredmetu,self.topLeftObjMyska)

        
    
            
        
    
    
