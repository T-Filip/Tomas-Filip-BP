'''
Created on 11. 3. 2017

@author: T.Filip
'''
from Textury import textury
import nastavenia
import Menu.menuOkno as menuOkno
import Menu.objMenu as objMenu

class MenuOknoVlastnosti(menuOkno.MenuOknoHra):
    def __init__(self,manazerOkien,scale, sirkaCast = 0.5,vyskaCast = 0.5):
        super().__init__(manazerOkien, scale, sirkaCast, vyskaCast)
        
        
        
    def reinit(self, hrac):
        menuOkno.MenuOknoHra.reinit(self, hrac)
        #x= int((self.rect.x + 80)*self.scaleRes)
        #y= int((self.rect.y + 80)*self.scaleRes)
        x= self.topLeftXPredScale + 80
        y= self.topLeftYPredScale + 50
        zvKonst = 50
        #def __init__(self,Menu,imgs,text,font,sirka,vyska,zvysovatHore,cykliSa,hodnota,hodnotaLock, cap, scale = 1,kontrola = None):
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[0],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[1],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[2],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[3],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)

        
        
    def close(self):
        self.hrac.reinitVlastnosti()
        
        
        
        
    def vykresliVlastnosti(self,screen):
        
        font = textury.dajFont(int(25*self.scaleRes))  
        vlastnosti = nastavenia.VLASTNOSTI_POSTAVY # text
        pocetVlastnosti = 4
        x= (self.topLeftXPredScale + 150)*self.scaleRes
        y= (self.topLeftYPredScale + 55)*self.scaleRes
        zvKonst = (50*self.scaleRes)

        vlastnostiHraca = self.hrac.dajVlastnosti()
        for i in range (len(vlastnostiHraca)):   
            text = vlastnosti[i] + ": " + str(vlastnostiHraca[i])                                  
            textSurf = font.render(text,1, nastavenia.BLACK)
            screen.blit(textSurf,(x,y))
            y += zvKonst
            

    def vykresliVolneVlastnosti(self,screen):
        font = textury.dajFont(int(25*self.scaleRes))
        text = "Volne vlastnosti: " + str(self.hrac.dajVolneVlastnosti()[0])                                 
        textSurf = font.render(text,1, nastavenia.BLACK)
        x= int(self.rect.x + (self.rect.width - textSurf.get_width())/2)
        y= self.rect.y + self.rect.height - int(45*self.scaleRes)
        screen.blit(textSurf,(x,y))

                
                
    def draw(self, screen):
        menuOkno.MenuOknoHra.draw(self, screen)
        self.vykresliNadpis(screen,"vlastnosti")
        self.vykresliVlastnosti(screen)
        self.vykresliVolneVlastnosti(screen)
                
                
                
                
                
                
                
                
                
                
                
                
                
                