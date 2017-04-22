'''
Created on 21. 3. 2017

@author: T.Filip
'''
from ObjektyMapa.enumSmerObjektu import EnumSmerObjektu

def zmenSmerDveri(self):
    if self.smer == EnumSmerObjektu.HORIZONTALNE:
        self.smer = EnumSmerObjektu.VERTIKALNE
    else:
        self.smer = EnumSmerObjektu.HORIZONTALNE
    
    self.initImage()
    self.initObjOblast()
    self.initTextOblast()
    


    return True