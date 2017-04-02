'''
Created on 13. 3. 2017

@author: T.Filip
'''
import Crafting.akciaPoCrafte as akciaPoCrafte
from Crafting.enumKwargsRecept import EnumKwargsRecept
from Postavy.enumZrucnosti import EnumZrucnosti
import Crafting.akciaOtvorenie as akciaOtvorenie



'''
Predstavuje informacie o tom z coho sa da co vyrobit
'''
class Recept():
    def __init__(self,id,material,produkt,nazov,nauceny = False, metodaPoVycrafteni = None,metodaNaOtvorenie = None,kwargs=None):
        self.kwargs = kwargs#dodatocne argumenty ktore by metody mohli potrebovat - aby som na kazdu metodu nevyuzival smecialnu metodu 
        self.metodaNaOtvorenie = metodaNaOtvorenie
        self.metodaPoCrafte = metodaPoVycrafteni
        self.id = id
        self.material = material
        self.produkt = produkt
        self.nazov = nazov
        self.jeNauceny = nauceny
        if self.jeNauceny == False and self.metodaNaOtvorenie != None:
            global ZoznamNeotvorenychReceptov
            ZoznamNeotvorenychReceptov[self.id] = self
        
        
    def setNauceny (self,nauc):
        self.nauceny = nauc
        
    def dajMaterial(self):
        return self.material
    def dajProdukt(self):
        return self.produkt
    
    def cekniOtvorenie(self,hrac):
        #nemusi sa kontrolovat ci tu metodu mame pretoze ak ju nemame tato metoda sa nebude volat pretoze nebude v zozname ZoznamNeotvorenychReceptov
        if self.metodaNaOtvorenie(self,hrac):
            self.jeNauceny = True
            return True
        else:
            return False
    
    def vykonajAkciuPoCrafte(self,hrac):
        if self.metodaPoCrafte != None:
            self.metodaPoCrafte(self, hrac)
        
        
        
ZOZNAM_RECEPTOV = {}

#vsetky recepty ktore treba kontrolovat ci sa nemozu otvorit
#pozor ak je oznaceny ako otvoreny na zaciatku alebo nema metodu na otvorenie tento recept sa nebude nachadzat v tomto zozname a teda sa nebude ani kontrolovat
ZoznamNeotvorenychReceptov = {} 

def initRecepty(hrac):
    zrucnostiHraca = hrac.dajZrucnosti()
    ZOZNAM_RECEPTOV[1] = Recept(1,[[2000,1],[2001,1],[2002,3]],[[3000,1]],"drevena sekera",True,
                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, None,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_SEKERA],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.2})
    
    ZOZNAM_RECEPTOV[2] = Recept(2,[[2001,2],[2100,3]],[[3001,1]],"kamenna sekera",False,
                                                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_SEKERA],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.3,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_SEKERA],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:20})
    
    ZOZNAM_RECEPTOV[3] = Recept(3,[[2001,2],[2101,12]],[[3002,1]],"zelezna sekera",False,
                                                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_SEKERA],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.6,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_SEKERA],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:50})
    
    ZOZNAM_RECEPTOV[4] = Recept(4,[[2001,2],[2102,12]],[[3003,1]],"zlata sekera",False,
                                                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_SEKERA],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:1,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_SEKERA],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:80})
    
    ZOZNAM_RECEPTOV[5] = Recept(5,[[2000,1],[2001,1],[2002,4]],[[3004,1]],"dreveny krumpac",True,
                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, None,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_KRUMPAC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.2})
    
    ZOZNAM_RECEPTOV[6] = Recept(6,[[2001,2],[2100,4]],[[3005,1]],"kamenny krumpac",False,
                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_KRUMPAC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.35,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_KRUMPAC],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:30})
    
    ZOZNAM_RECEPTOV[7] = Recept(7,[[2001,2],[2101,16]],[[3006,1]],"zelezny krumpac",False,
                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_KRUMPAC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.6,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_KRUMPAC],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:60})
    
    ZOZNAM_RECEPTOV[8] = Recept(8,[[2001,2],[2102,16]],[[3007,1]],"zlaty krumpac",False,
                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_KRUMPAC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:1,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_KRUMPAC],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:85})
    
    ZOZNAM_RECEPTOV[9] = Recept(9,[[2000,1],[2001,3],[2002,1]],[[3008,1]],"dreveny mec",True,
                                akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, None,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_MEC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.2})
    
    ZOZNAM_RECEPTOV[10] = Recept(10,[[2001,1],[2100,7],[2101,2]],[[3009,1]],"kamenny mec",False,   
                                 akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_MEC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.3,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_MEC],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:20})
    
    ZOZNAM_RECEPTOV[11] = Recept(11,[[2001,1],[2101,22]],[[3010,1]],"zelezny mec",False,
                                 akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_MEC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.7,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_MEC],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:50})
    
    ZOZNAM_RECEPTOV[12] = Recept(12,[[2001,1],[2102,20],[2101,2]],[[3011,1]],"zlaty mec",False,
                                 akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_MEC],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:1,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_MEC],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:80})
    
    ZOZNAM_RECEPTOV[13] = Recept(13,[[2000,5]],[[2001,3],[2002,2]],"deska",True)
    
    ZOZNAM_RECEPTOV[14] = Recept(14,[[2000,3]],[[2002,3]],"palica",True)
    
    ZOZNAM_RECEPTOV[15] = Recept(15,[[2000,4],[2001,8],[2100,6]],[[4000,1],[2002,3]],"dvere",False,
                                 akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_STAVEBNYCH_OBJEKTOV],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.8,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_STAVEBNYCH_OBJEKTOV],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:10})
    
    ZOZNAM_RECEPTOV[16] = Recept(16,[[2000,7],[2002,14]],[[4001,1]],"barikada",True,
                                 akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, None,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_STAVEBNYCH_OBJEKTOV],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.3})
    ZOZNAM_RECEPTOV[17] = Recept(17,[[2000,12],[2001,16]],[[4002,1],[2002,6]],"dreveny mur",False,
                                 akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_STAVEBNYCH_OBJEKTOV],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:0.5,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_STAVEBNYCH_OBJEKTOV],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:30})
    ZOZNAM_RECEPTOV[18] = Recept(18,[[2100,60],[3007,1]],[[4003,1],[3007,1]],"kamenny mur",False,
                                 akciaPoCrafte.zvysenieSkusenostiStavanieObjektov, akciaOtvorenie.skontrolujStavOdomknutiePodlaHodnoty,
                                 {EnumKwargsRecept.SKUSENOST_NA_ZMENENIE:zrucnostiHraca[EnumZrucnosti.VYROBA_STAVEBNYCH_OBJEKTOV],
                                  EnumKwargsRecept.SANCA_NA_ZMENENIE:1,
                                  EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE:zrucnostiHraca[EnumZrucnosti.VYROBA_STAVEBNYCH_OBJEKTOV],
                                  EnumKwargsRecept.HODNOTA_ODOMKNUTIE:60})
    
    ZOZNAM_RECEPTOV[19] = Recept(19,[[1,1],[2,5]],[[3,2],[4,2]],"volne",True)
    ZOZNAM_RECEPTOV[20] = Recept(20,[[1,1],[2,5]],[[3,2],[4,2]],"volne",True)

def skontrolujOtvorenieReceptov(hrac):
    global ZoznamNeotvorenychReceptov
    for kluc,recept in ZoznamNeotvorenychReceptov.copy().items():
        if recept.cekniOtvorenie(hrac):
            del ZoznamNeotvorenychReceptov[kluc]







