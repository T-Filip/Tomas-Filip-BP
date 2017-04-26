'''
Created on 20. 3. 2017

@author: T.Filip
'''


from enum import IntEnum


'''
predmety ako dvere barikada alebo mur sa mozu otacat a maju zatial len 2 smery
'''
class EnumSmerObjektu(IntEnum):
    HORIZONTALNE = 0
    VERTIKALNE = 1