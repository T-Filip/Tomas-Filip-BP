'''
Created on 15. 2. 2017

@author: T.Filip
'''

import pygame
from ObjektyMapa import mapa
from ObjektyMapa import scale
import copy
from Textury import textury
import logging
from Predmety.enumTypMaterialu import EnumTypMaterialu
import Predmety.tazenie as tazenie
#from ObjektyMapa.enumSmerObjektu import EnumSmerObjektu
import Predmety.animacia as animacia
import ObjektyMapa.metodyPredmety as metodyPredmety




INF_OBJ_MAPA = {}
objMapaScalovanie = pygame.sprite.Group() # mnozina objektov na mape ktorym je nutne menit poziciu na obrazovke pri pohybe hraca (tak ako policka alebo aj samotnemu hracovi)
infObjScalovanie = {}# mnozina infObj ktore su momentalne pouzivane a pre zobrazenie potrebuju scalovat
nextID = 0



'''
Identifikacny system - zakladna  trieda 
'''
class Inf():
    def __init__(self,imgPredmet = None, stackKapacita = 64):
        self.stackKapacita = stackKapacita
        
        self.initImgPredmet(imgPredmet)
        
        
    
    def initImgPredmet(self,imgPredmet):
        if imgPredmet == None:
            img = self.dajImgNaInitPredmet()
            if img != None:
                self.imgPredmet = img
            else:
                self.imgPredmet = textury.PREDMET_BEZ_TEXTURY
        else:
            self.imgPredmet = imgPredmet
    
    def dajImgPredm(self,cislo = 0):
        return self.imgPredmet
    
    def dajObjOblastMapa(self):
        return pygame.Rect(0,0,0,0)
    
    def dajImgNaInitPredmet(self):
        return None
    
    def dajStackKapacitu(self):
        return self.stackKapacita
    

'''
dodatocne informacie ku predmtom ktore hrac moze pozivat zatial len health potion
'''
class InfPozivatelne(Inf):
    def __init__(self,metoda, imgPredmet = None, stackKapacita = 64):
        self.zjedzPredmetMetoda = metoda
        super().__init__(imgPredmet, stackKapacita)
        
    def zjedzPredmet(self,hrac):
        self.zjedzPredmetMetoda(hrac)


#def metoda na zjedenie predmetu - mimo triedy koli predpokladu potreby roznym podobnych metod    
def zvysHpHracovi(hrac):
    hrac.zvysZdravie(25)
    
    
    
'''
informacie o nastrojoch mec sekera krumpac a ich rozne typy
vhodneNaMaterial je dic ktory obsahuje ako kluc typ materialu a ako hodnotu cislo medzi 0-1 ktore indikuje ako velmi vie pomoct pri tazeni daneho materialu
ak sa typ materialu v tomto zozname nenachadza tak je to 0
'''
class InfNastroje(Inf):
    def __init__(self,animacia,vhodneNa,imgAnimacia = None,imgPredmet = None, stackKapacita = 1):
        self.animacia = animacia
        self.vhodneNaMaterial = vhodneNa

        super().__init__(imgPredmet, stackKapacita)
        if imgAnimacia == None: # ak nema specialny img pre animaciu pouzije sa imgPredmet alebo default textura
            self.imgAnimacia = self.imgPredmet
        else:
            self.imgAnimacia = imgAnimacia
            
    def dajVhodneNaMaterial(self):
        return self.vhodneNaMaterial
            
    def dajAnimaciu(self):
        return self.animacia
    
    def dajImgAnimacie(self):
        return self.imgAnimacia
    

    
    
'''
abstraktna trieda obsahuje spolocne vlastnosti preo bjekty na mape aj pre celopolickove aj pre bezne
'''
   
class InfNaMape(Inf):
    def __init__(self,material,imgPredmet = None, stackKapacita = 64,trieda = None,metodaRightClick = None):
        self.material = material
        self.objNaMape(trieda)
        self.metodaRightClick = metodaRightClick
        super().__init__(imgPredmet, stackKapacita)
        
    def dajMaterial(self):
        return self.material
    
    def objNaMape(self,trieda = None):
        import ObjektyMapa.objMapa as objMapa
        self.objMapa = objMapa.ObjMapa
        
    def dajMetoduRightClick(self):
        return self.metodaRightClick

    


'''
necelopolickove objekty na mape este nescalovane vyuzivane na kvietky niektore kamene a tak

'''
#InfObj = namTupDef("InfObj", "img rectObjOblastMapa rychlostPrechodu pocPouzivajucich", {'pocPouzivajucich':0})
class InfObj(InfNaMape):
    def __init__(self,img,material,casTazenia,drop, rectObjOblastMapa = None, rychlostPrechodu = 1,imgPredmet = None, stackKapacita = 64,trieda = None,metodaRightClick = None):
        self.casTazenia = casTazenia
        self.drop = drop
        self.initImg(img)
        super().__init__(material,imgPredmet, stackKapacita,trieda,metodaRightClick)

        self.initRectOblastMapa(rectObjOblastMapa)
        
        self.rychlostPrechodu = rychlostPrechodu
        
    def dajImgNaInitPredmet(self):
        return self.img
  
        
    def initImg(self,img):
        self.img = img

        
    def initRectOblastMapa(self,rectObjOblastMapa):
        if rectObjOblastMapa == None:
            self.rectObjOblastMapa = self.img.get_rect()
        else:
            self.rectObjOblastMapa = rectObjOblastMapa #relativna pozicia v img

        
    def dajRozmery(self):
        return [self.img.get_width(),self.img.get_height()]
        
    def dajCasTazenia(self):
        return self.casTazenia
        
    def dajImgNaMape(self):
        return self.img
    
    def dajObjOblastMapa(self,index = 0):#relativne vzhladom na to ze je to pre kazdy objekt .. na mape znamena ze tam nie ja zahrnuty scale
        return self.rectObjOblastMapa
    


    def dajDrop(self):
        return self.drop

        #_(self,img,material,casTazenia,drop, rectObjOblastMapa = None, rychlostPrechodu = 1,imgPredmet = None, stackKapacita = 64,trieda = None,metodaRightClick = None):
        '''
        abstraktna trieda ktora nededi ziaden scale ale mai mplementovane metody zavisle na tomto dedeni
        potomci tejto triedy dedia rozny scale
        '''
class InfObjBezScale(InfObj):
    def __init__(self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):
        self.imgZaloha = img.copy()
        infObjScalovanie[self]=self
        self.sprites = pygame.sprite.Group()#zoznam vsetkych objektov ktore pouzivaju toto inf
        super().__init__(img,material,casTazenia,drop, rectObjOblastMapa, rychlostPrechodu,stackKapacita,stackKapacita,trieda,metodaRightClick)
        
    def dajImgPredm(self,cislo = 0):
        return self.dajImgZaloha()
    
    #override pretoze sa meni zdroj... povodny sa teraz scaluje a preto by boli rozmery zavisle od scalu
    def dajRozmery(self):
        return [self.dajImgZaloha().get_width(),self.dajImgZaloha().get_height()]
    
    def dajImgZaloha(self,index=0):
        return self.imgZaloha
        
    def scale(self,nas):
        self.img = pygame.transform.scale(self.dajImgZaloha(),(int(self.dajImgZaloha().get_width()*nas),int( self.dajImgZaloha().get_height()*nas)))
        #print(str(int(self.imgZaloha.get_width()*nas)))
        for sp in self.sprites:
            sp.scale(nas)
            sp.newRefImg()

    #metoda sa vola pri vytvarani noveho objektu v mape s aktivnym prekreslovanim, kedze data objektov ktore nie su pouzivane sa nescaluju je potrebne tak urobit na zaciatku ich pouzivania
    def aktualizujData(self): 
        if len(self.sprites) <= 1:#kedze sa data aktualizuju pri vstupe do stage 2 a vzhladom na to ze aktualizacia prebieha pre vsetky objekty tak to staci volat iba ak je pocet pouzivajucich prave 1
            self.scale(mapa.MAPA.dajNas())


    
    
'''

Uz scalovany objekt na prostredi vyuzivane na stromy niektore kamene a pod
'''
class InfObjScale(InfObjBezScale,scale.ObjScale):
    def __init__(self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):
        
        super().__init__(img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet,stackKapacita,trieda,metodaRightClick)
     
    '''
    inicializacia triedy ktora ja s touto triedou plne kompatibilna
    import koli cyklu
    '''   
    def objNaMape(self,trieda = None):
        import ObjektyMapa.objMapa as objMapa
        self.objMapa = objMapa.ObjMapaAktivPrek
        
    
'''
rovnako ako infobjscale ale jedna sa o viac textur ktore treba scalovat resp netreba niektore .... asi mohlo byt pod jednym
vyuziva sa na dvere barikady mury postavy
'''
class InfObjScaleViacImg(InfObjBezScale,scale.ObjScaleViacTextur):
    def __init__(self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):
        self.imgZaloha = img # pole obrazkov .. pre kazdy smer jeden
        super().__init__(img,rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet,stackKapacita,trieda,metodaRightClick)

    def dajImgNaInitPredmet(self):
        return self.img[0]

    def objNaMape(self,trieda = None):
        import ObjektyMapa.objMapa as objMapa
        self.objMapa = objMapa.ObjMapaAktivPrekViacImg
        
    def dajImgZaloha(self,index=0):
        return self.imgZaloha[index]
    
    def dajRozmery(self,smer):
        return [self.imgZaloha[smer].get_width(),self.imgZaloha[smer].get_height()]
    
    def initRectOblastMapa(self,rectObjOblastMapa):
        self.rectObjOblastMapa = rectObjOblastMapa # pole rectov

    def dajObjOblastMapa(self,index = 0):#relativne vzhladom na to ze je to pre kazdy objekt .. na mape znamena ze tam nie ja zahrnuty scale
        return self.rectObjOblastMapa[index]
    
    def dajImgPredm(self,cislo = 0):
        #kedze predmet neviem kolko je moznych textur riesene cez modulo
        cis = cislo % len(self.imgZaloha)
        return self.dajImgZaloha(cis)

    def initImg(self,img):
        self.img = img
    

        
    def scale(self,nas):
        
        for index in range (len(self.img)):
            self.img[index] = pygame.transform.scale(self.dajImgZaloha(index),(int(self.dajImgZaloha(index).get_width()*nas),int( self.dajImgZaloha(index).get_height()*nas)))
        
        #print(str(int(self.imgZaloha.get_width()*nas)))
        for sp in self.sprites:
            sp.scale(nas)
            sp.newRefImg()





'''
spolocne informacie pre celopolickove objekty - momentalne vyuzivany len potomok
'''  
#informacie o celopolickovych objektoch - obsahuju niekolko InfObj a to o kazdom jeho kusku
class InfObjCelPol(InfNaMape):
    def __init__(self,material,casTazenia,drop,zoznam,texturaPolicka):
        self.infObjekty = zoznam
        self.drop = drop
        self.casTazenia = casTazenia
        self.texturaPolicka = texturaPolicka # Tato textura sa vyuzije ak su vsade naokolo policka objekty s tymto id
        super().__init__(material)
        
    def dajDrop(self):
        return self.drop
        
    '''
    
    Celopolickove objekty ktore maju aj pozadie aby splyvali - vyuzivane na vodu jej plaz je ciastocne transparentna aby to viac splyvalo - spomaluje hru dost
    '''
class InfObjCelPolPozadie(InfObjCelPol):
    def __init__(self,material,casTazenia,drop,zoznam,texturaPolicka,pozadie,zozRectPoz = None):
        self.pozadie = pozadie
        self.rectPozadia = zozRectPoz
        super().__init__(material,casTazenia,drop,zoznam,texturaPolicka)
        
        
    
        
#InfObjCeloPolickoveSpajanie = namTupDef("InfObjCeloPolickoveSpajanie", "img rychlostPrechodu pocPouzivajucich",{'pocPouzivajucich':0})




def vlozInf (obj):
    global nextID
    INF_OBJ_MAPA[nextID] = obj
    #print(nextID)
    nextID +=1
    
def dajInf(id):
    try:
        return INF_OBJ_MAPA[id]
    except:
        logging.warn("Chyba pri ziskavani inf objektu podla ID")
        return None
  


'''        
inicializacia vsetkych spolocnych informacii
v metode pretoze sa to nemoze vykonat pri importe kedze este v tom case este nie je inicializovany pygame
'''
def nacitajTexturyObjMapa():


    global nextID

#-------------------STOROMY----------------
    stromy = pygame.image.load('img/objektyMapa/Stromy.png').convert_alpha()
    texturaStromov = [pygame.Surface((48,64),pygame.SRCALPHA) for i in range (0,18)]

#self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):

    #rectStromov = pygame.Rect(16,16,16,32)#relativna hodnota v texturovej oblasti, zatial docasne rovnake pre vsetky stromy .. docasne? 
    rectStromov = pygame.Rect(16,48,16,16)
    id = 0
    for x in range (0,6):
        for y in range (0,3):
            texturaStromov[id].blit(stromy,(0,0),(48*x,64*y,48,64))
            vlozInf(InfObjScale(texturaStromov[id],rectStromov,0.5,EnumTypMaterialu.DREVO,150,[tazenie.dropStrom,[10,4,1]]))
            id+=1



#------------------------KVIETKY-------------------
    nextID = 50
    kvietky = pygame.image.load('img/objektyMapa/kvietky.png').convert_alpha()
    rect = pygame.Rect(4,10,8,6)
    texturaKvietkov = [pygame.Surface((16,16),pygame.SRCALPHA) for i in range (0,6)]
    metody = [tazenie.dropKvietokBiom0,tazenie.dropKvietokBiom1,tazenie.dropKvietokBiom2,tazenie.dropKvietokBiom3,tazenie.dropKvietokBiom4,tazenie.dropKvietokBiom5]
    for y in range (0,6):
        texturaKvietkov[y].blit(kvietky,(0,0),(0,16*y,16,16))
        vlozInf(InfObj(texturaKvietkov[y],EnumTypMaterialu.KVIETOK,20,[metody[y],[10,4,1]],rect,0.95))

    

#---------------------SUTRE---------------
    sutre = pygame.image.load('img/objektyMapa/Sutre.png').convert_alpha()
    
    
    #zacinaju sutre
     
    nextID = 100
    metody = [[tazenie.dropVelkyKamenTyp0,tazenie.dropVelkyKamenTyp1],[tazenie.dropStrednyKamenTyp0,tazenie.dropStrednyKamenTyp1],[tazenie.dropMalyKamenTyp0,tazenie.dropMalyKamenTyp1]]
    for druh in range(0,2):
    
        posun = 76*druh
        #velke
        rect = pygame.Rect(6,20,50,23)
        surf = pygame.Surface((63,45),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(0,30+posun,63,45))
        vlozInf(InfObjScale(surf,rect,0,EnumTypMaterialu.KAMEN,300,[metody[0][druh],[10,4,1]]))
        
        rect = pygame.Rect(10,10,45,30)
        surf = pygame.Surface((60,43),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(67,26+posun,60,43))
        vlozInf(InfObjScale(surf,rect,0,EnumTypMaterialu.KAMEN,300,[metody[0][druh],[10,4,1]]))
        
        rect = pygame.Rect(8,30,18,27)
        surf = pygame.Surface((29,49),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(128,26+posun,29,49))
        vlozInf(InfObjScale(surf,rect,0,EnumTypMaterialu.KAMEN,300,[metody[0][druh],[10,4,1]]))
        
        #stredna1
        rect = pygame.Rect(3,13,25,10)
        surf = pygame.Surface((30,30),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(1,1+posun,30,30))
        vlozInf(InfObjScale(surf,rect,0.2,EnumTypMaterialu.KAMEN,250,[metody[1][druh],[10,4,1]]))
        #stred 2
        
        rect = pygame.Rect(6,11,23,12)
        surf = pygame.Surface((33,24),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(32,0+posun,33,24))
        vlozInf(InfObjScale(surf,rect,0.35,EnumTypMaterialu.KAMEN,200,[metody[1][druh],[10,4,1]]))
        
        #male
        rect = pygame.Rect(2,5,13,7)
        surf = pygame.Surface((17,13),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(64,0+posun,17,13))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,160,[metody[2][druh],[10,4,1]],rect,0.65))
        
        rect = pygame.Rect(1,3,9,5)
        surf = pygame.Surface((13,8),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(64,13+posun,13,8))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,140,[metody[2][druh],[10,4,1]],rect,0.75))
        
        rect = pygame.Rect(5,3,6,5)
        surf = pygame.Surface((12,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(80,0+posun,12,9))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,140,[metody[2][druh],[10,4,1]],rect,0.75))

        
        rect = pygame.Rect(2,3,7,6)
        surf = pygame.Surface((11,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(80,8+posun,11,9))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,150,[metody[2][druh],[10,4,1]],rect,0.7))
        
        rect = pygame.Rect(2,4,9,5)
        surf = pygame.Surface((13,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(91,0+posun,13,9))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,160,[metody[2][druh],[10,4,1]],rect,0.65))
        
        rect = pygame.Rect(3,2,5,5)
        surf = pygame.Surface((10,7),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(90,8+posun,10,7))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,130,[metody[2][druh],[10,4,1]],rect,0.9))
        
        rect = pygame.Rect(1,4,9,5)
        surf = pygame.Surface((13,9),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(76,16+posun,13,9))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,115,[metody[2][druh],[10,4,1]],rect,0.8))
        
        rect = pygame.Rect(2,1,6,4)
        surf = pygame.Surface((8,6),pygame.SRCALPHA)
        surf.blit(sutre,(0,0),(89,15+posun,8,6))
        vlozInf(InfObj(surf,EnumTypMaterialu.KAMEN,100,[metody[2][druh],[10,4,1]],rect,1))
    
    

    
    
    
    #------------------------------------- VODA CELOPOLICKO-------------------------
    #zacinaju celopolicka

    nextID = 200
    pobrezia = pygame.image.load('img/objektyMapa/Pobrezia.png').convert_alpha()
    voda  = pygame.image.load('img/objektyMapa/voda.png').convert_alpha()
    hlbokaVoda = pygame.image.load('img/objektyMapa/hlbokaVoda.png').convert_alpha()
    

    #Zozanm[][]   [tvar][cislotextury]
    #pocet textur variabilny osetrene by malo byt vsade
    texturyCasti = [0 for x in range(3)]
    
    pocetTexturVType = [0 for i in range(3)]
    pocetTexturVType[0] = 3
    pocetTexturVType[1] = 1
    pocetTexturVType[2] = 1
    
    texturyCasti[0] = [0 for y in range(pocetTexturVType[0])]
    texturyCasti[1] = [0 for y in range(pocetTexturVType[1])]
    texturyCasti[2] = [0 for y in range(pocetTexturVType[2])]
    
    zoznamInf = [0 for y in range(12)] 
    for i in range (0,4):
        zoznamInf[i] = [0 for j in range(pocetTexturVType[0])]
    for i in range (4,8):
        zoznamInf[i] = [0 for j in range(pocetTexturVType[1])]
    for i in range (8,12):
        zoznamInf[i] = [0 for j in range(pocetTexturVType[2])]
    zozRect = copy.deepcopy(zoznamInf)
    
    
    for i in range (0,pocetTexturVType[0]):
        texturyCasti[0][i] = pygame.Surface((16,16),pygame.SRCALPHA)
        texturyCasti[0][i].blit(pobrezia,(0,0),(0,i*16,16,16))
                                
    for i in range (0,pocetTexturVType[1]):
        texturyCasti[1][i] = pygame.Surface((16,16),pygame.SRCALPHA)
        texturyCasti[1][i].blit(pobrezia,(0,0),(16,i*16,16,16))
        
    for i in range (0,pocetTexturVType[2]):
        texturyCasti[2][i] = pygame.Surface((16,16),pygame.SRCALPHA)
        texturyCasti[2][i].blit(pobrezia,(0,0),(32,i*16,16,16))

    
    #ROHVODA
    rect = pygame.Rect(10,10,6,6)
    for i in range (0,pocetTexturVType[0]):
        zoznamInf[0][i] = InfObj(texturyCasti[0][i],EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.75)
        zozRect[0][i] = [pygame.Rect(10,10,6,6)]
      
    rect = pygame.Rect(0,10,6,6)
    for i in range (0,pocetTexturVType[0]):
        text = pygame.transform.flip(texturyCasti[0][i],True,False)
        zoznamInf[1][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.75)
        zozRect[1][i] = [pygame.Rect(0,10,6,6)]
      
    rect = pygame.Rect(10,0,6,6)  
    for i in range (0,pocetTexturVType[0]):
        text = pygame.transform.flip(texturyCasti[0][i],False,True)
        zoznamInf[2][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.75)
        zozRect[2][i] = [pygame.Rect(10,0,6,6) ]
        
    rect = pygame.Rect(0,0,6,6)
    for i in range (0,pocetTexturVType[0]):
        text = pygame.transform.flip(texturyCasti[0][i],True,True)
        zoznamInf[3][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.75)
        zozRect[3][i] = [pygame.Rect(0,0,6,6) ]
        
        
    #ROVNOVODA
    rect = pygame.Rect(0,10,16,6)
    for i in range (0,pocetTexturVType[1]):
        zoznamInf[4][i] = InfObj(texturyCasti[1][i],EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.6)
        zozRect[4][i] = [pygame.Rect(0,10,16,6) ]

        
    rect = pygame.Rect(10,0,6,16)
    for i in range (0,pocetTexturVType[1]):
        text = pygame.transform.rotate(texturyCasti[1][i],90)
        zoznamInf[5][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.6)
        zozRect[5][i] = [pygame.Rect(10,0,6,16) ]

    
    rect = pygame.Rect(0,0,16,6)
    for i in range (0,pocetTexturVType[1]):
        text = pygame.transform.rotate(texturyCasti[1][i],270)
        zoznamInf[6][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.6)
        #zozRect[6][i] = [pygame.Rect(0,0,16,6) ]
        zozRect[6][i] = [pygame.Rect(0,0,6,16)]
    
    rect = pygame.Rect(0,0,6,16)
    for i in range (0,pocetTexturVType[1]):
        text = pygame.transform.rotate(texturyCasti[1][i],180)
        zoznamInf[7][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],rect,0.6)
        #zozRect[7][i] = [pygame.Rect(0,0,6,16)]
        zozRect[7][i] = [pygame.Rect(0,0,16,6) ]
       
    #ROHZEM 
    for i in range (0,pocetTexturVType[2]):
        zoznamInf[8][i] = InfObj(texturyCasti[2][i],EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],None,0.6)
        zozRect[8][i] = [pygame.Rect(0,0,16,6),pygame.Rect(0,6,6,10),pygame.Rect(6,6,5,5) ]
        

    for i in range (0,pocetTexturVType[2]):
        text = pygame.transform.rotate(texturyCasti[2][i],90)
        zoznamInf[9][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],None,0.6)
        #zozRect[9][i] = [ ]
        zozRect[9][i] = [pygame.Rect(0,10,16,6),pygame.Rect(0,0,6,10),pygame.Rect(5,6,5,5) ]
    

    for i in range (0,pocetTexturVType[2]):
        text = pygame.transform.rotate(texturyCasti[2][i],270)
        zoznamInf[10][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],None,0.6)
        #zozRect[10][i] = [ ]
        zozRect[10][i] = [pygame.Rect(0,0,16,6),pygame.Rect(10,6,6,10),pygame.Rect(5,6,5,5) ]

    for i in range (0,pocetTexturVType[2]):
        text = pygame.transform.rotate(texturyCasti[2][i],180)
        zoznamInf[11][i] = InfObj(text,EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],None,0.6)
        zozRect[11][i] = [pygame.Rect(0,10,16,6),pygame.Rect(10,0,6,10),pygame.Rect(5,5,5,5) ]
        
    
        
    
    
        
    
    celoPolVoda = InfObjCelPolPozadie(EnumTypMaterialu.VODA,500,[tazenie.passMet,[10,4,1]],zoznamInf,hlbokaVoda,voda,zozRect)
    vlozInf(celoPolVoda)
    
    
    #----------------------------MATERIAL--------------------
    
    
    
    
            #-------------DREVO-----------------
    predmety = pygame.image.load('img/Predmety/predmety.png').convert_alpha()
    nextID = 2000
    
    
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(0,64,64,64))
    vlozInf(Inf(predmText,64))
    
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(64,64,64,64))
    vlozInf(Inf(predmText,64))
    
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(192,0,64,64))
    vlozInf(Inf(predmText,64))
    
    
    
            #---------------SUTRE--------------
    nextID = 2100
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(128,64,64,64))
    vlozInf(Inf(predmText,64))
    
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(192,64,64,64))
    vlozInf(Inf(predmText,64))
    
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(256,64,64,64))
    vlozInf(Inf(predmText,64))
    
    
    #----------------------KVIETKY PREDMETY -----------
    nextID = 2200
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(256,0,64,64))
    vlozInf(Inf(predmText,64))
    
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(320,0,64,64))
    vlozInf(Inf(predmText,64))
    
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(384,0,64,64))
    vlozInf(Inf(predmText,64))
    
    
    #----------------------POZIVATINY
    nextID = 2300
    #hp potion
    predmText = pygame.Surface((64,64),pygame.SRCALPHA)
    predmText.blit(predmety,(0,0),(448,0,64,64))
    vlozInf(InfPozivatelne(zvysHpHracovi,predmText,64))








#------------------------------NASTROJE------------------

    nextID = 3000
    #SEKERA
    vhodnost = [{EnumTypMaterialu.DREVO:0.4,EnumTypMaterialu.MASO:0.15},
                {EnumTypMaterialu.DREVO:0.6,EnumTypMaterialu.MASO:0.3},
                {EnumTypMaterialu.DREVO:0.8,EnumTypMaterialu.MASO:0.45},
                {EnumTypMaterialu.DREVO:1,EnumTypMaterialu.MASO:0.6}]
    for i in range (4):
        predmText = pygame.Surface((64,64),pygame.SRCALPHA)
        predmText.blit(predmety,(0,0),(64*i,128,64,64))
        vlozInf(InfNastroje(animacia.rotacia360,vhodnost[i],None,predmText,1))
    
    
    
    #KRUMPAC
    vhodnost = [{EnumTypMaterialu.KAMEN:0.25},
                {EnumTypMaterialu.KAMEN:0.50},
                {EnumTypMaterialu.KAMEN:0.75},
                {EnumTypMaterialu.KAMEN:1}]
    for i in range (4):
        predmText = pygame.Surface((64,64),pygame.SRCALPHA)
        predmText.blit(predmety,(0,0),(i*64,192,64,64))
        vlozInf(InfNastroje(animacia.rotacia360,vhodnost[i],None,predmText,1))
        
        
    #MEC 
    vhodnost = [{EnumTypMaterialu.MASO:0.4},
                {EnumTypMaterialu.MASO:0.6,EnumTypMaterialu.DREVO:0.1},
                {EnumTypMaterialu.MASO:0.8,EnumTypMaterialu.DREVO:0.25},
                {EnumTypMaterialu.MASO:1,EnumTypMaterialu.DREVO:0.45}]   
    for i in range (4):
        predmText = pygame.Surface((64,64),pygame.SRCALPHA)
        predmText.blit(predmety,(0,0),(i*64,256,64,64))
        vlozInf(InfNastroje(animacia.rotacia360,vhodnost[i],None,predmText,1))
    
    
    
    
    
    
    
    
    #--------------------------------DVERE-----------------#4000
    texturaObjektov = pygame.image.load('img/objektyMapa/objekty.png').convert_alpha()
    nextID = 4000
    
    vpravo = pygame.Surface((51,36),pygame.SRCALPHA)
    vlavo = pygame.Surface((51,36),pygame.SRCALPHA)
    hore = pygame.Surface((18,50),pygame.SRCALPHA)
    dole = pygame.Surface((18,50),pygame.SRCALPHA)
    
    vpravo.blit(texturaObjektov,(0,0),(0,0,51,36))
    vlavo.blit(texturaObjektov,(0,0),(51,0,51,36))
    dole.blit(texturaObjektov,(0,0),(0,36,18,60))
    hore.blit(texturaObjektov,(0,0),(18,36,18,60))
    
    #(self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):
    
    rect = [pygame.Rect(1,28,50,8),pygame.Rect(6,10,6,50)]
    vlozInf(InfObjScaleViacImg([vpravo,dole],rect,0,EnumTypMaterialu.DREVO,250,[tazenie.passMet,[10,4,1]],None,64,None,metodyPredmety.zmenSmerDveri))
    
    
    #----------------------BARIKADA # 4001
    vertikalne = pygame.Surface((33,70),pygame.SRCALPHA)
    horizontalne = pygame.Surface((70,33),pygame.SRCALPHA)

    vertikalne.blit(texturaObjektov,(0,0),(0,96,33,70))
    horizontalne.blit(texturaObjektov,(0,0),(38,37,70,33))
    
    #(self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):
    
    rect = [pygame.Rect(5,15,21,52),pygame.Rect(7,6,52,21)]
    vlozInf(InfObjScaleViacImg([vertikalne,horizontalne],rect,0,EnumTypMaterialu.DREVO,250,[tazenie.passMet,[10,4,1]],None,64,None,None))
    
    
    #dreveny mur 4002
    vertikalne = pygame.Surface((12,80),pygame.SRCALPHA)
    horizontalne = pygame.Surface((60,49),pygame.SRCALPHA)

    vertikalne.blit(texturaObjektov,(0,0),(36,73,12,80))
    horizontalne.blit(texturaObjektov,(0,0),(50,70,60,49))
    
    #(self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):
    
    rect = [pygame.Rect(1,28,10,51),pygame.Rect(0,36,60,12)]
    vlozInf(InfObjScaleViacImg([vertikalne,horizontalne],rect,0,EnumTypMaterialu.DREVO,250,[tazenie.passMet,[10,4,1]],None,64,None,None))
    
        #kamenny mur 4003 ---------------------------------------------------------------------------------------
    vertikalne = pygame.Surface((18,80),pygame.SRCALPHA)
    horizontalne = pygame.Surface((60,46),pygame.SRCALPHA)

    vertikalne.blit(texturaObjektov,(0,0),(111,1,18,80))
    horizontalne.blit(texturaObjektov,(0,0),(133,2,60,46))
    
    #(self,img, rectObjOblastMapa, rychlostPrechodu,material,casTazenia,drop,imgPredmet = None,stackKapacita = 64,trieda = None,metodaRightClick = None):
    
    rect = [pygame.Rect(0,27,18,53),pygame.Rect(0,27,60,17)]
    vlozInf(InfObjScaleViacImg([vertikalne,horizontalne],rect,0,EnumTypMaterialu.KAMEN,250,[tazenie.passMet,[10,4,1]],None,64,None,None))
    
    
    
    
'''
Povinne:
rychlostPrechodu # nasobitel ak 0.5 tak sa pohybuje 50% rychlostou (este sa to ale potom priemeruje)
pocPouzivajucich # pocet objektov ktore prave vyuzivau tuto texturu (aby sa nemuseli scalovat vsetky objekty)


'''



