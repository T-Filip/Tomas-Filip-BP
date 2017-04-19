'''
Created on 15. 3. 2017

@author: T.Filip
'''
from Predmety import inventar
from Predmety import predmet
import pygame
import math
from ObjektyMapa import objMapa
import logging
from ObjektyMapa.infObjekty import InfObjScale, InfNaMape, InfNastroje,\
    InfPozivatelne
from Predmety.enumTypMaterialu import EnumTypMaterialu
import random

import Predmety.tazenie as tazenie
from Predmety.animacia import Animacia
from Postavy.enumZrucnosti import EnumZrucnosti


class InvVyuzPredmetu(inventar.Inventar):
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
        
        self.tickLeftclick = -1
        self.leftClickObj = None
        self.zakazUtokuDo = 0
        
        self.tazenyObjekt = None
        self.casTazenia = 0
        self.posledneTazenie = 0 #tick v ktorom sa naposledy tazilo
        
        self.cisloTexturyOznPredm = 0#tlacidlo R incrementuje a metoda co dava texturu pomocou modula vrati spravnu texturu
        
        
        self.beziAnimacia = False
        
    def update(self):
        self.updateTexturyOznPredmetu()
        self.eventy()
        
    def eventy(self):
        if self.hrac.dajHru().dajManazerOkien().jeVykresleneNejakeMenu():
            return
        self.beziAnimacia = False
        #print("--------------")
        #print(self.beziAnimacia)
        manazer = self.hrac.dajHru().dajManazerOkien()
        pressMouse = manazer.dajPressedMouse()
        
        
        if pressMouse[0] == True:
            self.utok()
            self.vykonajAnimaciu()



        if not self.beziAnimacia:
            self.animacia.ukonciAnimaciu()
            
    def vykonajAnimaciu(self):
        pred = self.polePredmetov[self.oznacenyIndex].dajPredmet()
        if pred == None:
            return # Mozno animacia ruk ak tam nie je predmet
            
        inf = pred.dajInf()
        if isinstance(inf, InfNastroje):
            self.animacia.update(inf)
            self.beziAnimacia = True
            #print(self.beziAnimacia)
        
        
    def dajOznacenyPredmet(self):
        return self.polePredmetov[self.oznacenyIndex]
        
    def updateTexturyOznPredmetu(self):
        predmet = self.polePredmetov[self.oznacenyIndex].dajPredmet()
        if predmet == None or not isinstance(predmet.dajInf(), InfNaMape):
            self.oznPredmet = None
            return
        
        k1 = self.kontrolaKolizieOznPredmetu()
        k2 = self.kontrolaZmenyPriblizenia()

        
        
        if k1 or k2:
            self.reinitImageOznPredmet()
            
    def kontrolaKolizieOznPredmetu(self):
        sur = self.mapa.dajPolickoveSurMysky()
        okolie = self.mapa.dajOkolieMysky()
        if okolie == None:
            if self.jeNacerveno:
                return False#uz je nacerveno netreba prekreslovat
            self.jeNacerveno = True
            return True
        #print("---------------------------------------")
        #scale = self.mapa.dajScaleNas()

        infPredmetu = self.polePredmetov[self.oznacenyIndex].dajPredmet().dajInf()
        rectO = infPredmetu.dajObjOblastMapa()
        rectObjVMyske = pygame.Rect(rectO.x,rectO.y,rectO.width,rectO.height)
        velkostTexObjektu = infPredmetu.dajImgPredm().get_size()
        #pos = pygame.mouse.get_pos()

        #nacitanaMapa = self.mapa.dajNacitanuMapu()
        #rectTopLeftPolicka = self.mapa.dajTopLeftPolicko().dajRect()
        #relatMysX= pos[0] - rectTopLeftPolicka.x + rectTopLeftPolicka.width
        #relatMysY= pos[1] - rectTopLeftPolicka.y + rectTopLeftPolicka.height

        myskaNaMape = self.mapa.dajMyskuNaMape()

        myskaNaMape[0] -= velkostTexObjektu[0]/3
        myskaNaMape[1] -= velkostTexObjektu[1]/3

        rectObjVMyske = rectObjVMyske.move(myskaNaMape[0],myskaNaMape[1])

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
        texOriginal = self.oznPredmet.dajImgPredm(self.cisloTexturyOznPredm)
        size = texOriginal.get_size()
        #print("size:" + str(size))
        #print (self.mapa.dajScaleNas())
        w = int(size[0]*self.mapa.dajScaleNas())
        h = int(size[1]*self.mapa.dajScaleNas())
        #self.imageOznPredmetu = pygame.Surface((w,h),pygame.SRCALPHA)
        #self.scaleRes = self.mapa.dajScaleNas()
        self.imageOznPredmetu = pygame.transform.scale(texOriginal,(w,h))
        if self.jeNacerveno:
            self.imageOznPredmetu.fill((255, 50, 50,100), None, pygame.BLEND_RGBA_MULT)
        else:
            self.imageOznPredmetu.fill((100, 100, 100,100), None, pygame.BLEND_RGBA_MULT)
        
        
        #mapa sa vytvara az po vytvoreni hraca preto dodatocne linkovanie
    def linkMapa(self,mapa):
        self.mapa = mapa
        self.vytvorAnimaciu()#trosku jednoduchsi pristup k informaciam ak ma animacia priamy pristup k instancii mapy
        
    def vytvorAnimaciu(self):
        self.animacia = Animacia(self.hrac,self.mapa)
        
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
        
        
    def rightClickNaObj(self):
        obj = self.mapa.dajObjektNaMyske()
        if obj!=None:
            return obj.akciaRightClick() # ak sa ziadna akcia nevykona vrati False a pokracuje sa v stavani inak sa stavanie rusi
        else:
            return False
        
        
        '''
        Stavanie predmetu co je v ruke
        '''
    def rightClick(self):
        if self.hrac.dajHru().dajManazerOkien().jeVykresleneNejakeMenu():
            return
        
        if self.rightClickNaObj():
            return # ak sa vykona akcia na nejaky objekt uz sa dalen nestavia 
        else:
            self.vyuziPredmet()
        
    def dajCisloTextury(self):
        return self.cisloTexturyOznPredm
        
        
    def vyuziPredmet(self):
        
        if self.jeNacerveno:
            return
        predmet = self.polePredmetov[self.oznacenyIndex].dajPredmet()
        if predmet == None:
            return
        infPredmetu = predmet.dajInf()
        if isinstance(infPredmetu, InfPozivatelne):
            infPredmetu.zjedzPredmet(self.hrac)
            predmet.zmenPocetKusovO(-1)
            return
            
        if not isinstance(infPredmetu,InfNaMape):
            return
            #pretoze dalej sa uz zaoberam s pracou s predmetom ako keby to bol infNaMape - klasika ten predmet polozi
        
        
        
        velkostTexObjektu = infPredmetu.dajImgPredm(self.cisloTexturyOznPredm).get_size()

        myskaNaMape = self.mapa.dajMyskuNaMape()
        myskaNaMape[0] -= velkostTexObjektu[0]/3
        myskaNaMape[1] -= velkostTexObjektu[1]/3
        suradnicePolicka= [int(myskaNaMape[0]//64),int(myskaNaMape[1]//64)]
        policko = self.mapa.dajPolicko(suradnicePolicka)
        
        if policko == None:
            logging.warning("Inventar oznaceny prdmet - vytvorenie objekty - right click -> Policko na ktorom sa ma vytvorit obj je None  pozn.zatial osetrene ale preco k tomu dochadza?")
            return
        
        predmet.zmenPocetKusovO(-1)
        self.hrac.zvysSkusenosti(10)
        #_(self,policko,id,pixSurPolickoCenter,suToSuradniceCenter = False):
        
        topLeft = (myskaNaMape[0]-suradnicePolicka[0]*64,myskaNaMape[1]-suradnicePolicka[1]*64)

        
        #kontrolu uz je zbytocne vykonavat kedze to nezbehne ak je objekt nacerveno a teda ze kontrola ukazala ze tam sa neda stavat - na druhu stranu vyzera ze koli zaokruhlovaniu alebo nejakej inej chyba je to o pixel posunute
        policko.vytvorObjekt(predmet.dajId(),topLeft,self,False,infPredmetu,False)
        
        self.mapa.skontrolujPolickoNaMyske(True)#Nutne nove okolie koli zmene
        
    
        
        
    def utok(self):
        #print("UTOK")
        aktualnyTick = self.hrac.dajHru().dajPocetTickov()
        if aktualnyTick < self.zakazUtokuDo:
            return
        postavy = self.hrac.dajHru().dajPostavyGroup()
        #mousePos = pygame.mouse.get_pos()
        myskaNaMape = self.mapa.dajMyskuNaMape()
        #print("---------------------------")
        #print("Myska na mape: " + str(myskaNaMape))
        #print()
        ###kontakt s postavami
        if postavy != None:
            for postava in postavy:
                if postava == self.hrac:#spravit zoznam bez hraca?
                    continue
                col = postava.dajRectTextOblastMapa().collidepoint(myskaNaMape)
                if col:
                    self.zakazUtokuDo = aktualnyTick + 180#1.8 sek pri normalnej rychlosti
                    self.zautocNaPostavu(postava)
                    self.hrac.zvysSkusenosti(int(random.triangular(15,200,50)))
                    
                    idNastroja = self.polePredmetov[self.oznacenyIndex].dajPredmet().dajId()
                    if idNastroja >= 3000 and idNastroja <=3003:
                        indexZrucnosti = EnumZrucnosti.VYUZITIE_SEKERA
                    elif idNastroja <= 3007:
                        indexZrucnosti = EnumZrucnosti.VYUZITIE_KRUMPAC
                    elif idNastroja <= 3011:
                        indexZrucnosti = EnumZrucnosti.VYUZITIE_MEC

                        
                    if indexZrucnosti >= 0:
                        self.hrac.zvysZrucnosti(indexZrucnosti,1)
                    
                    return
            
        okolieMysky = self.mapa.dajOkolieMysky()
        if okolieMysky != None:
            for obj in okolieMysky:
                col = obj.dajRectTextOblastMapa().collidepoint(myskaNaMape)
                if col: # ak trafil texturu objektu
                    #print(obj.dajRectTextOblastMapa())
                    pocTick = self.hrac.dajHru().dajPocetTickov()
                    #print(pocTick)
                    #print(self.posledneTazenie)
                    if self.posledneTazenie != pocTick-1:
                        self.casTazenia = 0
                    self.posledneTazenie = pocTick
                    if self.tazenyObjekt == obj:
                        self.casTazenia +=1
                        if self.casTazenia >= tazenie.vypocitajDlzkuTazenia(obj, self.polePredmetov[self.oznacenyIndex].dajPredmet(), self.hrac):
                            obj.dajDrop(self.hrac)
                            self.hrac.zvysSkusenosti(15)
                            obj.kill(True)
                        
                    else:
                        self.tazenyObjekt = obj
                        self.casTazenia = 0
                        
                    break#staci jedna kolizia
        

        
    def leftClick(self):
        return
        if self.hrac.dajHru().dajManazerOkien().jeVykresleneNejakeMenu():
            return
        
    def stlaceneR(self):
        self.cisloTexturyOznPredm += 1
        self.reinitImageOznPredmet()
        
        #self.tickLeftclick = -1
        #self.leftClickObj = None
        #print("left click")

        
        #utoci hrac na postavu v parametri kedze mobky funguju inak ich combat je implementovany v triede npc
        #kvazi utok ale na predmety funguje trosku inak a metody na vypocitanie tazenia predmetov su v module tazenie
    def zautocNaPostavu(self,postava):
        predmet = self.dajOznacenyPredmet().dajPredmet()
        if predmet != None:
            infPred = predmet.dajInf()
            if isinstance(infPred, InfNastroje):
                vhodneNaMaterial = self.dajOznacenyPredmet().dajPredmet().dajInf().dajVhodneNaMaterial()
                try:
                    koeficienPredmetu = vhodneNaMaterial[EnumTypMaterialu.MASO]
                except:    
                    koeficienPredmetu = 0
            else:
                koeficienPredmetu = 0
        else:
            koeficienPredmetu = 0
            
        koeficienSilyHraca = self.hrac.dajVlastnosti()[3][0]/10
        
        dmg = int(((koeficienPredmetu + koeficienSilyHraca)/2)*random.gauss(40,8))
        postava.udelPoskodenie(dmg)

            

            
        
        
        
    
            
        
    
    
