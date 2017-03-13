'''
Created on 13. 3. 2017

@author: T.Filip
'''


'''
Predstavuje informacie o tom z coho sa da co vyrobit
'''
class Recept():
    def __init__(self,id,material,produkt,nazov,nauceny = False):
        self.id = id
        self.material = material
        self.produkt = produkt
        self.nazov = nazov
        self.jeNauceny = nauceny
        
        
    def setNauceny (self,nauc):
        self.nauceny = nauc
        
    def dajMaterial(self):
        return self.material
    def dajProdukt(self):
        return self.produkt
        
        
        
ZOZNAM_RECEPTOV = {}

ZOZNAM_RECEPTOV[1] = Recept(1,[[1,1],[2,5],[9,9]],[[3,2],[4,2]],"dake stromy",True)
ZOZNAM_RECEPTOV[2] = Recept(2,[[10,2],[13,5],[12,10]],[[100,10],[110,5]],"aaa",True)
ZOZNAM_RECEPTOV[3] = Recept(3,[[3,1],[2,5]],[[3,2],[4,2]],"dak",True)
ZOZNAM_RECEPTOV[4] = Recept(3,[[1,3],[2,5]],[[3,2],[4,2]],"da1k",True)
ZOZNAM_RECEPTOV[5] = Recept(3,[[1,4],[2,5]],[[3,2],[4,2]],"da5k")
ZOZNAM_RECEPTOV[6] = Recept(3,[[5,1],[2,5]],[[3,2],[4,2],[4,2],[4,2],[4,2]],"daghk",True)
ZOZNAM_RECEPTOV[7] = Recept(3,[[6,1],[2,5]],[[3,2],[4,2],[5,2],[6,2],[7,2],[8,2]],"dgfgak",True)
ZOZNAM_RECEPTOV[8] = Recept(3,[[9,2],[2,5]],[[3,2],[4,2]],"dadgk")
ZOZNAM_RECEPTOV[9] = Recept(3,[[5,3],[5,5]],[[3,2],[4,2]],"ddaak")
ZOZNAM_RECEPTOV[10] = Recept(3,[[1,1],[3,5]],[[3,2],[4,2]],"dcxcak",True)

ZOZNAM_RECEPTOV[11] = Recept(1,[[1,1],[2,5]],[[3,2],[4,2]],"dake stromy",True)
ZOZNAM_RECEPTOV[12] = Recept(2,[[1,1],[2,5]],[[3,2],[4,2]],"aaa")
ZOZNAM_RECEPTOV[13] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"dak")
ZOZNAM_RECEPTOV[14] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"da1k")
ZOZNAM_RECEPTOV[15] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"da5k")
ZOZNAM_RECEPTOV[16] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"daghk",True)
ZOZNAM_RECEPTOV[17] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"dgfgak")
ZOZNAM_RECEPTOV[18] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"dadgk")
ZOZNAM_RECEPTOV[19] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"ddaak",True)
ZOZNAM_RECEPTOV[20] = Recept(3,[[1,1],[2,5]],[[3,2],[4,2]],"dcxcak")









