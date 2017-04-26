'''
Created on 9. 3. 2017

@author: T.Filip
'''

import Predmety.predmet as predmet
import pygame

'''
Trieda ktora uchovava predmety a obsahuje operacie nad predmetmi

'''
class Inventar():
    def __init__(self,velkost):
        self.sloty = pygame.sprite.RenderPlain()
        self.predmety = pygame.sprite.RenderPlain()
        self.initMiesta(velkost)
        
            
    def initMiesta(self,velkost):
        for i in range(velkost):
            predmet.MiestoPredmetu(self.sloty,self)
        
    def vlozPredmet(self,predmet):
        pred = predmet
        pocKusovPred = pred.dajPocetKusov()
        if pocKusovPred <= 0:
            pred.kill()
            return
        
        for slot in self.sloty:
            if slot.predmet == None:
                continue
            if slot.predmet.id == pred.id: 
                #slot.predmet.zmenPocetKusovO(pred.dajPocetKusov())
                kolkoZobralo = slot.predmet.zmenPocetKusovO(pocKusovPred)
                pocKusovPred -= kolkoZobralo
                if pocKusovPred <= 0:
                    pred.kill()
                    return 0
                
                '''
                pred.setPocetKusov(0,False)
                stackKapacita = slot.predmet.dajStackKapacitu()
                if slot.predmet.dajPocetKusov() > stackKapacita:
                    pred.zmenPocetKusovO(slot.predmet.dajPocetKusov() - stackKapacita)
                else:
                    return pred.dajPocetKusov()
                '''
                  
        pred.setPocetKusov(pocKusovPred,False)  
        for slot in self.sloty:
            if slot.predmet == None:
                slot.vlozPredmet(pred)
                return 0 
            
        return predmet.dajPocetKusov()
            

                
                
        
    def dajPocetMiest(self):
        return len(self.sloty)
    
    def dajSloty(self):
        return self.sloty
    
    def dajPredmety(self):
        return self.predmety
    
    
    '''
    Metoda sa ma pokusit vybrat predmet v parametri.
    Vybera co sa da aj ked sa jej nepodari vybrat vsetko.
    '''
    def vyberPredmet(self,pred):
        for predmet in self.predmety:
            if pred.dajId() == predmet.dajId():
                #jedna sa o predmet rovnakeho typu
                predmet.zmenPocetKusovO(- pred.dajPocetKusov())
                if predmet.dajPocetKusov() <= 0:
                    #odstranujeme predmet co ma viac alebo rovnaky pocet kusov 
                    pred.zmenPocetKusovO(abs(predmet.dajPocetKusov()))
                    predmet.kill
                    predmet = None
                else:
                    #odstranujem predmet co ma menej kusov
                    #vymazat ten predmet ci nie?
                    pred.setPocetKusov(0)
                    return
    

    
    
    
    
    
    