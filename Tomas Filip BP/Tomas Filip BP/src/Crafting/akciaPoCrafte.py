'''
Created on 30. 3. 2017

@author: T.Filip
'''
from Crafting.enumKwargsRecept import EnumKwargsRecept
import random

#metody ktore ma recept v sebe ulozene sa vykonaju po vykonani Crafting
#ich ucel je vacsinou zvysit schopnosti hraca





def zvysenieSkusenostiStavanieObjektov(self,hrac):
    if random.random() < self.kwargs[EnumKwargsRecept.SANCA_NA_ZMENENIE]:
        self.kwargs[EnumKwargsRecept.SKUSENOST_NA_ZMENENIE][0] += 1
    