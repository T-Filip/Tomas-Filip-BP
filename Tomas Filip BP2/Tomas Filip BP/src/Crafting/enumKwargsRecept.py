'''
Created on 1. 4. 2017

@author: T.Filip
'''
from enum import IntEnum

#int kluc > string kluc 


'''
kluce do dictionary ktory posielam ako parameter do receptu 
'''
class EnumKwargsRecept (IntEnum):
    SKUSENOST_NA_ZMENENIE = 0
    SANCA_NA_ZMENENIE = 1
    PREMENNA_NA_ODOMKNUTIE = 2
    HODNOTA_ODOMKNUTIE = 3
    
