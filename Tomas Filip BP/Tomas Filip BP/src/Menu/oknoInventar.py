'''
Created on 10. 3. 2017

@author: T.Filip
'''
import logging

class OknoInventar():
    def __init__(self,rect,hranica = 256):
        self.hranica = hranica
        self.rect = rect
        self.inventar = None
        self.nastalReinit = False
        
    def reinit(self,inventar,hranica = 256):
        self.hranica = hranica
        self.nastalReinit = True
        self.inventar = inventar
        
        
        sloty = self.inventar.dajSloty()
        
        pocetPotrebnychFlekov = len(self.inventar.dajSloty())
        
        medzera = 4
        pocX = 0
        pocY = 0
        #scale = 0.2
        sirka = self.rect.width
        vyska = self.rect.height
        esteNieJeVysledok = True
        velkostStrany = 0
        while esteNieJeVysledok:
            velkostStrany += 1
            pocetNaSirku = int((sirka - medzera) / (velkostStrany + medzera))
            pocetNaVysku = int((vyska - medzera) / (velkostStrany + medzera))
            pocetMoznychFlekov = pocetNaSirku * pocetNaVysku
            if pocetMoznychFlekov < pocetPotrebnychFlekov or velkostStrany > self.hranica:
                esteNieJeVysledok = False
                velkostStrany -= 1
                
        pocetNaSirku = int((sirka - medzera) / (velkostStrany + medzera))
        pocetNaVysku = int((vyska - medzera) / (velkostStrany + medzera))


        
        krajnaMedzeraX = int((sirka - (pocetNaSirku*(velkostStrany+medzera)-medzera))/2)
        krajnaMedzeraY = int((vyska - (pocetNaVysku*(velkostStrany+medzera)-medzera))/2)
          
            
        xSur = self.rect.x +krajnaMedzeraX
        ySur = self.rect.y +krajnaMedzeraY
        
        for slot in sloty:
            slot.reinit(xSur,ySur,velkostStrany)
            xSur += velkostStrany + medzera
            if (xSur + velkostStrany) > (self.rect.x + self.rect.width):
                xSur = self.rect.x +krajnaMedzeraX
                ySur = ySur + velkostStrany + medzera
            
            
        predmety = self.inventar.dajPredmety()
        for pr in predmety:
            pr.aktualizujGrafiku()
            
    def draw(self,screen):
        if self.nastalReinit:
            self.inventar.sloty.draw(screen)
            self.inventar.predmety.draw(screen)
            
    def dajInventar(self):
        return self.inventar
        

