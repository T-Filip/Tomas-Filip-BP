'''
Created on 11. 3. 2017

@author: T.Filip
'''
import Predmety.predmet as predmet
import pygame



'''
Stara sa o predmety v okne o ich presun a tak
Pri kliku prezrie ci nebolo kliknute na predmet ak ano vlozi sa tento predmet do miestaPrePredmetMyska (zdedeneho) nasledne sa tento predmet pohybuje s myskou az kym sa nevykona potrebna akcia so zmenenim tohto stavu
'''
class PracaSPredmetmi (predmet.MiestoPrePredmetMyska):
    def __init__(self):
        super().__init__()
        self.oknaInventare = [] # miesto kde je potrebne vhodit vsetky mozne okna inventarov
        self.oknaInventareDraw = [] # kedze niektore okna inventarov sa vykresluju za inach okolnosti a za inych podmienok je obcas potrebne aby sa nevykreslovali vsetky preto specialny zoznam pre vykreslovanie
        self.posledneMiestoPredmetu = None # ak je v myske nejaky predmet je potrebne aby sme si pamatali odkial bol vzaty 

    def clickRight(self):
        if self.predmet == None: # click ziaden predmet
            #ak nema predmet musime pozriet ci na nejaky klikol
            pos = pygame.mouse.get_pos()
            stlacenyPredmet = self.dajPrvyPredmetNa(pos)
            
            if stlacenyPredmet != None: # ak na nejaky klikol zoberie sa jeho polovica
                pom = int(stlacenyPredmet.pocetKusov / 2)
                if pom > 0:
                    pred = predmet.Predmet(stlacenyPredmet.id,pom)
                    rectPredmetu = stlacenyPredmet.rect
                    #print ("rect predmetu " + str(rectPredmetu) ) 
                    
                    self.vlozPredmet(pred, pos[0]-rectPredmetu.x, pos[1]-rectPredmetu.y, rectPredmetu.width)
                    stlacenyPredmet.zmenPocetKusovO(-pom)

                        
                        
        else: # click a mame predmet
            pos = pygame.mouse.get_pos()
            stlacenySlot = self.dajPrvySlotNa(pos)
            if stlacenySlot != None: # ak sme neklikli mimo slotu
                if stlacenySlot.predmet == None: # iba ak slot nema predmet .. ak by mal tak ako? maximalne vymenit by sa dalo ale dat jeden asi nije teda iba ak su idecka rovnake
                    stlacenySlot.vlozPredmet(predmet.Predmet(self.predmet.dajId(),1))
                    self.predmet.pocetKusov -= 1
                    if self.predmet.pocetKusov < 1:
                        self.predmet = None # predmet sa maze dali sme posledny kus
                    
                    
                elif stlacenySlot.predmet.id == self.predmet.id: # ak maju idcka rovnake 
                    #if stlacenySlot.predmet.dajPocetKusov() >= self.predmet.dajStackKapacitu(): # ci je tam miesto na dalsi kus
                    #    return # nie je miesto
                    kolkoZobralo = self.predmet.zmenPocetKusovO(-1)
                    stlacenySlot.predmet.zmenPocetKusovO(-kolkoZobralo)
                    
        if hasattr(self, "craftCheck"):
            self.craftCheck()

                    
    def clickLeft(self):
        if self.predmet == None: # nastal click a myska nedrzi ziaden predmet
            pos = pygame.mouse.get_pos()
            stlacenyPredmet = self.dajPrvyPredmetNa(pos)
            if stlacenyPredmet != None:
                self.posledneMiestoPredmetu = stlacenyPredmet.miestoPrePredmet
                rectPredmetu = stlacenyPredmet.rect
                self.vlozPredmet(stlacenyPredmet, pos[0]-rectPredmetu.x, pos[1]-rectPredmetu.y, rectPredmetu.width)
                
        else: #v ruke mame predmet
            pos = pygame.mouse.get_pos()
            stlacenySlot = self.dajPrvySlotNa(pos)
            if stlacenySlot == None: # ak klikol mimo
                #skontrolujeme ci klikol na okno 
                if self.klikolNaOkno(pos):#ak klikol na okno predmet sa vrati do povodnemho miesta 
                    #print("A")
                    self.posledneMiestoPredmetu.vlozPredmet(self.predmet)
                    self.posledneMiestoPredmetu.predmet.aktualizujPoziciu()
                    self.predmet = None
                else: #ak klikol mimo predmet sa maze
                    #print("B")
                    self.predmet.kill()
                    self.predmet = None
                    
                    
            elif stlacenySlot.predmet == None: # v slote nie je ziaden predmet
                #print("C")
                stlacenySlot.vlozPredmet(self.predmet)
                #self.predmet = None
                
            else: # v slote nieco je ak su id rozne nasleduje vymena predmetu co je v ruka za predmet ktory je v slote ak je id rovnake len sa to spocita
                if stlacenySlot.predmet.id == self.predmet.id: # su rovnake spocita sa a zbytok na 64 sa necha ak je zbytok 0 tak sa predmet maze 
                    #print("E")
                    stlacenySlot.predmet.zlucPredmety(self.predmet)
                
                else:
                    #print("D")
                    pomPred = stlacenySlot.vydajPredmet()
                    stlacenySlot.vlozPredmet(self.predmet)
                    rectPredmetu = pomPred.rect
                    self.vlozPredmet(pomPred, pos[0]-rectPredmetu.x, pos[1]-rectPredmetu.y, rectPredmetu.width)

        if hasattr(self, "craftCheck"):
            self.craftCheck()
            
    def dajOknaInventare(self):
        return self.oknaInventare
            
    def dajPrvySlotNa(self,pos):
        for inv in self.oknaInventare:
            for slot in inv.inventar.sloty:
                if slot.rect.collidepoint(pos):
                    return slot  
            
        return None
            
            
    def dajPrvyPredmetNa(self, pos):
        for inv in self.oknaInventare:
            for predmet in inv.inventar.predmety:
                if predmet.rect.collidepoint(pos):
                    return predmet  
            
        return None
    
    def vlozOkno(self,okno):
        self.oknaInventare.append(okno)
        
    def vlozOknoDraw(self,okno):
        self.oknaInventareDraw.append(okno)
    
    
    '''
    vykresli vsetky predmety vo vsetkych inventaroch aj s predmetom ktory drzi myska
    '''
    def draw(self,screen):
        for inv in self.oknaInventareDraw:
            inv.draw(screen)
        
        if self.predmet != None:
            self.initMousePosition(pygame.mouse.get_pos())
            #print("kreslim predmet v myske")
            #print(self.predmet.rect)
            #print(self.mousePos)
            self.predmet.aktualizujPoziciu()
            self.groupPredmet.draw(screen)

            
            
    def reinit(self, hrac):
        pass
        #for inv in self.oknaInventare:
        #    inv.reinit(hrac.dajInventar())
        
    