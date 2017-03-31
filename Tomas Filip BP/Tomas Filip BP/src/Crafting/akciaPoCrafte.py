'''
Created on 30. 3. 2017

@author: T.Filip
'''
from Postavy import enumSkusenosti
import random

#metody ktore ma recept v sebe ulozene sa vykonaju po vykonani Crafting
#ich ucel je vacsinou zvysit schopnosti hraca

def zvysenieSkusenostiStavanieObjektov(hrac):
    skusenosti  = hrac.dajSkusenosti()
    if random.random() < 0.6:
        return
    skusenosti[enumSkusenosti.EnumSkusenosti.VYROBA_KRUMPAC] += 1