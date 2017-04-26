'''
Created on 1. 4. 2017

@author: T.Filip
'''
from Crafting.enumKwargsRecept import EnumKwargsRecept

'''
Kazdy recept obsahuje zaobaleny int podla ktoreho sa odomika recept
'''
def skontrolujStavOdomknutiePodlaHodnoty(self,hrac):
    if self.kwargs[EnumKwargsRecept.PREMENNA_NA_ODOMKNUTIE][0] >= self.kwargs[EnumKwargsRecept.HODNOTA_ODOMKNUTIE]:
        return True
    else:
         return False
