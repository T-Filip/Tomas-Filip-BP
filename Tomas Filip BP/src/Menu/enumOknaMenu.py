'''
Created on 7. 3. 2017

@author: T.Filip
'''


from enum import IntEnum

'''
Kazde okno ma svoj kluc v dictionary
rozdelujem okno v hre a okno v menu
'''
class EnumOknaMenu(IntEnum):
    ZAKLADNE_MENU = 0
    VYBER_POSTAVY = 1
    