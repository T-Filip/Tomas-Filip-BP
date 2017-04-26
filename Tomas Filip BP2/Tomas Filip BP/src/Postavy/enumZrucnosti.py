'''
Created on 30. 3. 2017

@author: T.Filip
'''
from enum import IntEnum

class EnumZrucnosti(IntEnum):
    #SKUSENOSTI VYROBA: 0-SEKERA, 1-KRUMPAC, 2-MEC, VYUZIVANIE: 3-SEKERA, 4-KRUMPAC, 5-MEC...
    VYROBA_STAVEBNYCH_OBJEKTOV = 0
    VYROBA_SEKERA = 1
    VYROBA_KRUMPAC = 2
    VYROBA_MEC = 3
    VYUZITIE_SEKERA = 4
    VYUZITIE_KRUMPAC = 5
    VYUZITIE_MEC = 6
    