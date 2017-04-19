'''
Created on 18. 3. 2017

@author: T.Filip
'''
import random
from Predmety.predmet import Predmet
from Postavy.enumZrucnosti import EnumZrucnosti

'''
Zoznam metod pre vypocty tazenia
Metody drop sa vyuzivaju ako parametri pri vytvarani roznych objektov - je vala druhov objektov a kazdy z nich moze davat rozlisny drop v rozlisnych poctoch s inou nahodou a pod

'''



def vypocitajDlzkuTazenia(tazenyObjekt,nastroj,hrac):
    from ObjektyMapa.infObjekty import InfNastroje
    #NASTROJ
    if isinstance(nastroj, InfNastroje):
        materialObj = nastroj.dajInf().dajMaterial()
        vhodneNaMat = nastroj.dajInf().dajVhodneNaMaterial()
        try:
            koeficientNastroja = vhodneNaMat[materialObj]
        except: # neni o tom zaznam znamena ze 0
            koeficientNastroja = 0
    else:
        koeficientNastroja = 0
        
    #SKUSENOSTI HRAC
    vlastnosti = hrac.dajZrucnosti()
    if nastroj != None:
        idNastroja = nastroj.dajId()
        #cez id asi zdlhave lepsie by bolo asi mat atribut pre typ zbrane ...
        #lepsie by bolo pytat zrucnost cez hraca alebo pod co ak pridam nastroj? vhodne prerobit
        indexZrucnosti = -1
        if idNastroja >= 3000 and idNastroja <=3003:
            indexZrucnosti = EnumZrucnosti.VYUZITIE_SEKERA
            zrucnosti = vlastnosti[indexZrucnosti][0]
        elif idNastroja <= 3007:
            indexZrucnosti = EnumZrucnosti.VYUZITIE_KRUMPAC
            zrucnosti = vlastnosti[indexZrucnosti][0]
        elif idNastroja <= 3011:
            print("MEC")
            indexZrucnosti = EnumZrucnosti.VYUZITIE_MEC
            zrucnosti = vlastnosti[indexZrucnosti][0]
        else:
            zrucnosti = 0  
            
        if indexZrucnosti >= 0 and random.random() < 0.01:
            print("ZVYSUJEM")
            hrac.zvysZrucnosti(indexZrucnosti,1)
            
        if koeficientNastroja == 0:
            zrucnost = zrucnosti/2 
        nasobokZrucnosti = (100 - zrucnost) / 100
            
            
    else:
        nasobokZrucnosti = 1
            
    casTazeniaObjektu = tazenyObjekt.dajInf().dajCasTazenia()
    vyslednyCas = casTazeniaObjektu + casTazeniaObjektu * nasobokZrucnosti  + (1 - koeficientNastroja) * casTazeniaObjektu
    return vyslednyCas
          



def passMet(args,hrac):
    pass # aby som za kazdym nemusel cekovat ci tam nieco je 

def dropVelkyKamenTyp0(args,hrac):
    hrac.vlozPredmet(Predmet(2100,int(random.triangular(1,12,3)))) 
    if random.random() < 0.4:
        hrac.vlozPredmet(Predmet(2101,int(random.triangular(0,3,0.5)))) 
    if random.random() < 0.05:
        hrac.vlozPredmet(Predmet(2102,int(random.triangular(0,3,0.5))))  
        
def dropStrednyKamenTyp0(args,hrac):
    hrac.vlozPredmet(Predmet(2100,int(random.triangular(1,8,2)))) 
    if random.random() < 0.2:
        hrac.vlozPredmet(Predmet(2101,int(random.triangular(0,4,0.5)))) 
    if random.random() < 0.02:
        hrac.vlozPredmet(Predmet(2102,int(random.triangular(0,3,0.5))))  
        
def dropMalyKamenTyp0(args,hrac):
    hrac.vlozPredmet(Predmet(2100,int(random.triangular(1,4,1)))) 
    if random.random() < 0.1:
        hrac.vlozPredmet(Predmet(random.randint(105,112),1)) 
    if random.random() < 0.1:
        hrac.vlozPredmet(Predmet(2101,int(random.triangular(0,3,0.5)))) 
  
  
def dropVelkyKamenTyp1(args,hrac):
    hrac.vlozPredmet(Predmet(2100,int(random.triangular(1,6,2)))) 
    if random.random() < 0.7:
        hrac.vlozPredmet(Predmet(2101,int(random.triangular(0,6,1)))) 
    if random.random() < 0.15:
        hrac.vlozPredmet(Predmet(2102,int(random.triangular(0,3,0.5))))  
        
def dropStrednyKamenTyp1(args,hrac):
    hrac.vlozPredmet(Predmet(2100,int(random.triangular(1,4,1.5)))) 
    if random.random() < 0.5:
        hrac.vlozPredmet(Predmet(2101,int(random.triangular(0,5,0.5)))) 
    if random.random() < 0.1:
        hrac.vlozPredmet(Predmet(2102,int(random.triangular(0,3,0.5))))  
        
def dropMalyKamenTyp1(args,hrac):
    hrac.vlozPredmet(Predmet(2100,int(random.triangular(1,2,1)))) 
    if random.random() < 0.1:
        hrac.vlozPredmet(Predmet(random.randint(113,125),1))
    if random.random() < 0.3:
        hrac.vlozPredmet(Predmet(2101,int(random.triangular(0,4,0.5)))) 
        
def dropStrom(args,hrac):
    if random.random() < 0.65:
        hrac.vlozPredmet(Predmet(2000,int(random.triangular(1,4,2))))
        hrac.vlozPredmet(Predmet(2002,int(random.triangular(1,3,1))))  
    else:
        hrac.vlozPredmet(Predmet(2002,int(random.triangular(2,6,3)))) #ak nepadne poriadne drevo padne viac palic 
        
def dropKvietokBiom0(args,hrac):
    hrac.vlozPredmet(Predmet(2202,int(random.triangular(1,7,2.5)))) 
    if random.random() < 0.02:
        hrac.vlozPredmet(Predmet(2200,1))
    if random.random() < 0.1:
        hrac.vlozPredmet(Predmet(2201,1))
    
def dropKvietokBiom1(args,hrac):
    hrac.vlozPredmet(Predmet(2202,int(random.triangular(0,2,0.5))))      
    hrac.vlozPredmet(Predmet(2201,1))
        
def dropKvietokBiom2(args,hrac):
    hrac.vlozPredmet(Predmet(2202,int(random.triangular(0,3,1)))) 
    if random.random() < 0.3:
        hrac.vlozPredmet(Predmet(2200,1))

        
def dropKvietokBiom3(args,hrac):
    hrac.vlozPredmet(Predmet(2202,int(random.triangular(1,7,2.5)))) 
    if random.random() < 0.1:
        hrac.vlozPredmet(Predmet(2200,1))
    if random.random() < 0.02:
        hrac.vlozPredmet(Predmet(2201,1))
        
def dropKvietokBiom4(args,hrac):
    hrac.vlozPredmet(Predmet(2202,int(random.triangular(0,2,0.5)))) 
    hrac.vlozPredmet(Predmet(2200,1))

        
def dropKvietokBiom5(args,hrac):
    hrac.vlozPredmet(Predmet(2202,int(random.triangular(1,3,1)))) 
    if random.random() < 0.3:
        hrac.vlozPredmet(Predmet(2201,1))


        
        

  
  
  
    