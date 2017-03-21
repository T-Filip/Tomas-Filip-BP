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
    
    
    '''
    if self.prvotnySmer == EnumSmerObjektu.HORE:
        if self.smer == EnumSmerObjektu.HORE:
            self.smer = EnumSmerObjektu.VLAVO
        else:
            self.smer = self.prvotnySmer
    elif self.prvotnySmer == EnumSmerObjektu.DOLE:
        if self.smer == EnumSmerObjektu.DOLE:
            self.smer = EnumSmerObjektu.VPRAVO
        else:
            self.smer = self.prvotnySmer
    elif self.prvotnySmer == EnumSmerObjektu.VLAVO:
        if self.smer == EnumSmerObjektu.VLAVO:
            self.smer = EnumSmerObjektu.DOLE
        else:
            self.smer = self.prvotnySmer
    elif self.prvotnySmer == EnumSmerObjektu.VPRAVO:
        if self.smer == EnumSmerObjektu.VPRAVO:
            self.smer = EnumSmerObjektu.HORE
        else:
            self.smer = self.prvotnySmer
    '''
    self.initImage()
    self.initObjOblast()
    self.initTextOblast()
    


    return True