'''
Created on 11. 3. 2017

@author: T.Filip
'''
from Textury import textury
from Nastavenia import nastavenia
import Menu.menuOkno as menuOkno
import Menu.objMenu as objMenu

class MenuOknoVlastnosti(menuOkno.MenuOknoHra):
    def __init__(self,manazerOkien,scale, sirkaCast = 0.5,vyskaCast = 0.55):
        super().__init__(manazerOkien, scale, sirkaCast, vyskaCast)
         
    def reinit(self, hrac):
        menuOkno.MenuOknoHra.reinit(self, hrac)

        x= self.topLeftXPredScale + 80
        y= self.topLeftYPredScale + 50
        zvKonst = 50
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[0],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[1],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[2],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)
        y+=zvKonst
        objMenu.TlacidloIncDecValLock(self,[textury.TPlus,textury.TPlusOznacene,textury.TPlusLock],"",16,x,y,True,False,self.hrac.dajVlastnosti()[3],self.hrac.dajVolneVlastnosti(),[0,10],self.scaleRes)
        
        
    def close(self):
        self.allSprites.empty()
        self.hrac.reinitVlastnosti()
        
        
    
        
        
    def vykresliVlastnosti(self,screen):
        
        font = textury.dajFont(int(25*self.scaleRes))  
        vlastnosti = nastavenia.VLASTNOSTI_POSTAVY # text
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
        
    def vykresliLevel(self,screen):
        font = textury.dajFont(int(20*self.scaleRes))
        text = "Level: " + str(self.hrac.dajLevel()) + "    Skusenosti: " + str(self.hrac.dajSkusenosti()) + "/" + str(self.hrac.dajDalsiLevelNaSkusenostiach())                                  
        textSurf = font.render(text,1, nastavenia.BLACK)
        x= int(self.rect.x + (self.rect.width - textSurf.get_width())/2)
        y= self.rect.y + self.rect.height - int(70*self.scaleRes)
        screen.blit(textSurf,(x,y))
               
    def draw(self, screen):
        menuOkno.MenuOknoHra.draw(self, screen)
        self.vykresliNadpis(screen,"vlastnosti")
        self.vykresliVlastnosti(screen)
        self.vykresliVolneVlastnosti(screen)
        self.vykresliLevel(screen)
                
                
                
                
                
                
                
                
                
                
                
                
                
                