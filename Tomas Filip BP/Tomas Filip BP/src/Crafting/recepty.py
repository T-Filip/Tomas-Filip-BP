'''
Created on 13. 3. 2017

@author: T.Filip
'''


'''
Predstavuje informacie o tom z coho sa da co vyrobit
'''
class Recept():
    def __init__(self,id,material,produkt,nazov,nauceny = False, metodaPoVycrafteni = None,metodaNaOtvorenie = None,args = None):
        self.args = args#dodatocne argumenty ktore by metody mohli potrebovat - aby som na kazdu metodu nevyuzival smecialnu metodu 
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
    
    def mozeSaOtvorit(self,hrac):
        if self.metodaNaOtvorenie:
            self.jeNauceny = True
            return True
        else:
            return False
    
    def vykonajAkciuPoCrafte(self,hrac):
        if self.metodaPoCrafte != None:
            self.metodaPoCrafte(hrac)
        
        
        
ZOZNAM_RECEPTOV = {}

#vsetky recepty ktore treba kontrolovat ci sa nemozu otvorit
#pozor ak je oznaceny ako otvoreny na zaciatku alebo nema metodu na otvorenie tento recept sa nebude nachadzat v tomto zozname a teda sa nebude ani kontrolovat
ZoznamNeotvorenychReceptov = {} 


ZOZNAM_RECEPTOV[1] = Recept(1,[[2000,1],[2001,1],[2002,3]],[[3000,1]],"drevena sekera",True)
ZOZNAM_RECEPTOV[2] = Recept(2,[[2001,2],[2100,3]],[[3001,1]],"kamenna sekera",True)
ZOZNAM_RECEPTOV[3] = Recept(3,[[2001,2],[2101,12]],[[3002,1]],"zelezna sekera",True)
ZOZNAM_RECEPTOV[4] = Recept(4,[[2001,2],[2102,12]],[[3003,1]],"zlata sekera",True)
ZOZNAM_RECEPTOV[5] = Recept(5,[[2000,1],[2001,1],[2002,4]],[[3004,1]],"drieveny krumpac",True)
ZOZNAM_RECEPTOV[6] = Recept(6,[[2001,2],[2100,4]],[[3005,1]],"kamenny krumpac",True)
ZOZNAM_RECEPTOV[7] = Recept(7,[[2001,2],[2101,16]],[[3006,1]],"zelezny krumpac",True)
ZOZNAM_RECEPTOV[8] = Recept(8,[[2001,2],[2102,16]],[[3007,1]],"zlaty krumpac",True)
ZOZNAM_RECEPTOV[9] = Recept(9,[[2000,1],[2001,3],[2002,1]],[[3008,1]],"dreveny mec",True)
ZOZNAM_RECEPTOV[10] = Recept(10,[[2001,1],[2100,7],[2101,2]],[[3009,1]],"kamenny mec",True)

ZOZNAM_RECEPTOV[11] = Recept(11,[[2001,1],[2101,22]],[[3010,1]],"zelezny mec",True)
ZOZNAM_RECEPTOV[12] = Recept(12,[[2001,1],[2102,20],[2101,2]],[[3011,1]],"zlaty mec",True)
ZOZNAM_RECEPTOV[13] = Recept(13,[[2000,5]],[[2001,3],[2002,2]],"deska",True)
ZOZNAM_RECEPTOV[14] = Recept(14,[[2000,3]],[[2002,3]],"palica",True)
ZOZNAM_RECEPTOV[15] = Recept(15,[[2000,4],[2001,8],[2100,6]],[[4000,1],[2002,3]],"dvere",True)
ZOZNAM_RECEPTOV[16] = Recept(16,[[2000,7],[2002,14]],[[4001,1]],"barikada",True)
ZOZNAM_RECEPTOV[17] = Recept(17,[[2000,12],[2001,16]],[[4002,1],[2002,6]],"dreveny mur",True)
ZOZNAM_RECEPTOV[18] = Recept(18,[[2100,60],[3007,1]],[[4003,1],[3007,1]],"kamenny mur",True)
ZOZNAM_RECEPTOV[19] = Recept(19,[[1,1],[2,5]],[[3,2],[4,2]],"volne",True)
ZOZNAM_RECEPTOV[20] = Recept(20,[[1,1],[2,5]],[[3,2],[4,2]],"volne",True)

def skontrolujOtvorenieReceptov(hrac):
    global ZoznamNeotvorenychReceptov
    for kluc,recept in ZoznamNeotvorenychReceptov.items():
        if recept.mozeSaOtvorit(hrac):
            del ZoznamNeotvorenychReceptov[kluc]







