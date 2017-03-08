'''
Created on 6. 3. 2017

@author: T.Filip
'''
import pygame
import textury
from enum import Enum
import nastavenia

class LastUpdate(Enum):
    UPDATE = 1
    HOVER = 2
    CLICK = 3

class objMenu(pygame.sprite.Sprite):
    def __init__(self,menu,imgs,text,fontVelkost,xPos,yPos,scaler=1,scale = 1):
        self.scaleRes = scaler
        self.scale = scale
        self.menu = menu
        pygame.sprite.Sprite.__init__(self,self.menu.dajGroup())

        self.initFont(fontVelkost)
        
        self.initImages(imgs)
        self.initRect(xPos,yPos)
        #Stav tlacidla
        self.trebaUpdate = True
        self.text = text
        self.jeLocknuty = False;
        self.jeClicknuty = False;
        self.jeNaNomMys = False;
        
        
        self.indexTextury = 0
        self.lastUpdate = -1
        
        self.update()
        
    def initFont(self,fontVelkost):
        self.font = textury.dajFont(int(fontVelkost*self.scaleRes* self.scale))
        
    def initImages(self,imgs):
        self.images = [0 for i in range (len(imgs))]
 
        for i in range (len(imgs)):
            self.images[i] = pygame.transform.scale(imgs[i],(int(imgs[i].get_width() * self.scaleRes* self.scale),int(imgs[i].get_height() * self.scaleRes * self.scale)))
        self.imageIndex = 0
        self.image = pygame.Surface(self.images[0].get_size())
        
    def initRect(self,xPos,yPos): 
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xPos * self.scaleRes,yPos * self.scaleRes )

        
    def mouseOnSprite(self):
        if self.jeLocknuty:
            return
        if self.lastUpdate is LastUpdate.HOVER:
            return
        self.lastUpdate = LastUpdate.HOVER
        if len(self.images) > 1:
            self.hover()
        
    def hover(self):
        self.jeNaNomMys = True;



    def mouseClicked(self):
        if self.jeLocknuty:
            return
        if self.lastUpdate is LastUpdate.CLICK:
            return
        self.lastUpdate = LastUpdate.CLICK
        self.click()#metoda pre override
            
    def click(self):
        self.jeClicknuty = True
        
    def prekresli(self):
        self.image.blit(self.images[self.imageIndex],(0,0))
        if hasattr(self, "textSurf"):
            self.image.blit(self.textSurf, (self.textX, self.textY))
        
    def updateText(self):
        size = self.image.get_size()
        self.textSurf = self.font.render(self.text,1, nastavenia.BLACK)
        self.textX = (size[0] - self.textSurf.get_width())/2
        self.textY = (size[1] - self.textSurf.get_height())/2
        
    '''
    Umoznuje zablokovat tlacidlo
    '''        
    def setLock (self, hodnota):
        if hodnota == self.jeLocknuty:
            return
        self.jeLocknuty = hodnota
        self.trebaUpdate = True
        
    def nastalaZmena(self): #nastavZmenu
        self.trebaUpdate = True

    def nutnyUpdate(self):
            self.lastUpdate = LastUpdate.UPDATE
            self.trebaUpdate = False


            if self.jeLocknuty and len(self.images) > 2 and self.images[2] is not None:
                self.imageIndex = 2
                
                
            else:
                if self.jeNaNomMys and len(self.images) > 1 and self.images[1] is not None:
                    self.imageIndex = 1
                    self.trebaUpdate = True # hover moze zmiznut alebo potom informovat tlacidlo o zmiznuti hover
                else:
                    self.imageIndex = 0
                
            
            self.updateText()
            self.prekresli()
          
    def update(self):
        if self.trebaUpdate == True or self.lastUpdate is not LastUpdate.UPDATE:
            self.nutnyUpdate()
        
        self.jeClicknuty = False
        self.jeNaNomMys = False
        
        '''
    def refresh(self):#watafak
        self.initImages(self.imagesZaloha)
        self.trebaUpdate = True
        self.text = self.text
        self.jeLocknuty = False;
        self.jeClicknuty = False;
        self.jeNaNomMys = False;
        self.indexTextury = 0
        self.lastUpdate = -1
        self.update()
        '''
        
        
        
        
'''
okrem bezneho tlacidla ma moznost ako parameter prijat funkciu ktora sa vykona pri kliknuti na tlacidlo
'''
class Tlacidlo (objMenu):
    def __init__(self,Menu,imgs,text,font,sirka,vyska,metoda,scaler = 1,scale = 1):
        self.clickMetoda = metoda
        super().__init__(Menu,imgs,text,font,sirka,vyska,scaler,scale)
       
    def click(self):
        self.clickMetoda(self)
        
        
        
        '''
        tlacidlo zvysuje ale znizuje hodnotu ktoru dostalo v parametri
        
        #neplati
        #Vzhladom na to ze tento potomok moze menit data na ktorych zaviasia ine prvky systemu je nutne pri zmene tychto hodnou okontrolovat aj prvky ktore na nich zavisia od toho tuje dalsi parameter kontrola.
        #Obsahuje hodnoty a intervaly v ktorych sa maju pohybovat a to takto [[[hodnota],[interval,interval],[],[],[]]
                                                                             
        '''
class TlacidloIncDecVal (Tlacidlo):
    def __init__(self,Menu,imgs,text,font,sirka,vyska,zvysovatHore,cykliSa,hodnota,cap, scale = 1,kontrola = None):
        metoda = self.zmenHodnotu
        self.maSaZvysitHore = zvysovatHore
        self.hodnota = hodnota
        self.cap = cap
        self.cykliSa = cykliSa
        self.kontrola = kontrola
        super().__init__(Menu, imgs, text, font, sirka, vyska, metoda, scale)
        
    def zmenHodnotu(self,self2):#metoda definovana v nutri takze 2x self
        if self.maSaZvysitHore:
            self.hodnota[0]+=1
            if self.hodnota[0] > self.cap[1]:
                if self.cykliSa:
                    self.hodnota[0] = self.cap[0]
                else:
                    self.hodnota[0] = self.cap[1]
        else:
            self.hodnota[0]-=1
            if self.hodnota[0] < self.cap[0]:
                if self.cykliSa:
                    self.hodnota[0] = self.cap[1]
                else:
                    self.hodnota[0] = self.cap[0]
        
        self.kontrolaPrvkov()
        self.menu.refresh()
        
        
    def kontrolaHodnoty(self):
        if self.hodnota[0] > self.cap[1]:
                if self.cykliSa:
                    self.hodnota[0] = self.cap[0]
                else:
                    self.hodnota[0] = self.cap[1]
        elif self.hodnota[0] < self.cap[0]:
                if self.cykliSa:
                    self.hodnota[0] = self.cap[1]
                else:
                    self.hodnota[0] = self.cap[0]            
           

    def kontrolaPrvkov(self):
        if self.kontrola == None:
            return
        for prv in self.kontrola:
            prv.kontrolaHodnoty()

   
        
        
'''
    Okrem funkcionality ktoru splna TlacidloIncDecVal je tu pridana moznost menit viacere parametre v inak ohranicenom intervale.
    Pri zmene pohlavia sa interval vlasov a oci meni kedze pocet textur pre oci a vlasy moze byt rozny.
    Parameter cap teraz predstavuje 2 rozmerne pole 
    Novy parameter jednorozmerne pole s jednym prvkom ktory oznacuje ktore pole v cap predstavuje momentalny interval ktory ohranicuje menenie hodnotu
    
    
'''
class TlacidloIncDecValByVal (TlacidloIncDecVal):
    def __init__(self,Menu,imgs,text,font,sirka,vyska,zvysovatHore,cykliSa,hodnota,cap,indexIntervalu,scale = 1,kontrola=None):
        self.indexIntervalu = indexIntervalu
        super().__init__(Menu, imgs, text, font, sirka, vyska, zvysovatHore, cykliSa, hodnota, cap, scale,kontrola)
        
    def zmenHodnotu(self, self2):
        if self.maSaZvysitHore:
            self.hodnota[0]+=1
            if self.hodnota[0] > self.cap[self.indexIntervalu[0]][1]:
                if self.cykliSa:
                    self.hodnota[0] = self.cap[self.indexIntervalu[0]][0]
                else:
                    self.hodnota[0] = self.cap[self.indexIntervalu[0]][1]
        else:
            self.hodnota[0]-=1
            if self.hodnota[0] < self.cap[self.indexIntervalu[0]][0]:
                if self.cykliSa:
                    self.hodnota[0] = self.cap[self.indexIntervalu[0]][1]
                else:
                    self.hodnota[0] = self.cap[self.indexIntervalu[0]][0]
        
        self.kontrolaPrvkov()
        self.menu.refresh()
        
    def kontrolaHodnoty(self):
        if self.hodnota[0] > self.cap[self.indexIntervalu[0]][1]:
            if self.cykliSa:
                self.hodnota[0] = self.cap[self.indexIntervalu[0]][0]
            else:
                self.hodnota[0] = self.cap[self.indexIntervalu[0]][1]
        elif self.hodnota[0] < self.cap[self.indexIntervalu[0]][0]:
            if self.cykliSa:
                self.hodnota[0] = self.cap[self.indexIntervalu[0]][1]
            else:
                self.hodnota[0] = self.cap[self.indexIntervalu[0]][0]
        
        

        
    
        
        
            
        
        
        
'''
     je ulohou je podavat informacie pouzivatelovy za pomocou textury ktoru je mozne updatovat   
'''
class ObjMenuInfo (objMenu):
    def __init__(self,Menu, imgs, text, fontVelkost, sirka, vyska, metoda,args,scaler=1, scale=1):
        self.metUpdateTex = metoda
        self.args = args
        super().__init__(Menu, imgs, text, fontVelkost, sirka, vyska, scaler, scale)
        
        
        
    def initImages(self, imgs):
        self.updateTextury()
        
    def updateTextury(self):
        im = self.metUpdateTex(self)
        self.images =  [pygame.transform.smoothscale(im,(int(im.get_width() * self.scaleRes* self.scale),int(im.get_height() * self.scaleRes * self.scale)))]
        self.image = self.images[0]
        
    def initFont(self,fontVelkost):
        pass
    def updateText(self):
        pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
