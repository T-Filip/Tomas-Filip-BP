'''
Created on 9. 3. 2017

@author: T.Filip
'''



from enum import IntEnum


'''
kazde okno ma svoj vlastny kluc do dictionary
'''
class EnumOknaHra(IntEnum):
    INVENTAR = 0
    VLASTNOSTI = 1
    ZRUCNOSTI = 2
    NAPOVEDA = 3