import pygame
import ObjektyMapa.objMapa as objMapa
import ObjektyMapa.scale as scale
import random



class Hrac(pygame.sprite.Sprite, scale.ObjScale):
    def __init__(self,hra,surPix):
        self.suradnice = [int(surPix[0]/64),int(surPix[1]/64)]
        self.hra = hra
        pygame.sprite.Sprite.__init__(self,self.hra.dajAktivBlitGroup())
        self.image = pygame.Surface((64,64))
        self.rect = self.image.get_rect()
        
        self.imageZaloha = pygame.Surface((64,64))
        self.imageZaloha.fill((200,100,0))
        self.rectTextOblastMapa = self.image.get_rect()
        self.rectTextOblastMapa.x = surPix[0]
        self.rectTextOblastMapa.y = surPix[1]
        self.topLeftScaleMap = [self.rect.x, self.rect.y]
        #self.rect.x = sur[0]#?
        #self.rect.y = sur [1]
        self.scale(1)#da sa aj lepsie
        #self.pixeloveUmiestnenieNaMape = sur # pixel ktory urcuje jeho polohu - stred hitboxu
       

    def update(self, *args):
        i = 6
        #self.hra.mapa.updatniPoziciu(self.topLeftScaleMap,self.rect)
        #print("hrac: " + str(self.rectTextOblastMapa))
        #self.rect.x = self.pixeloveUmiestnenieNaMape[0] - self.hra.mapa.lavoHorePixelKamera[0]-32
        #self.rect.y = self.pixeloveUmiestnenieNaMape[1] - self.hra.mapa.lavoHorePixelKamera[1]-32
        #print ("hrac suradnice pix: " + str(self.pixeloveUmiestnenieNaMape[0]) + " " + str(self.pixeloveUmiestnenieNaMape[1]))
        #print ("hrac vykreslovanie: " + str(self.rect.x) + " " + str(self.rect.y))
        

        
    def eventy(self):

        klavesy = self.hra.manazerOkien.klavesy
        if klavesy[pygame.K_UP] or klavesy[pygame.K_w]:

            #self.rectTextOblastMapa.y -= 1
            self.rectTextOblastMapa= self.rectTextOblastMapa.move(0,-2)
        if klavesy[pygame.K_DOWN] or klavesy[pygame.K_s]:

            #self.rectTextOblastMapa.y += 1
            self.rectTextOblastMapa= self.rectTextOblastMapa.move(0,2)
        if klavesy[pygame.K_LEFT] or klavesy[pygame.K_a]:

            #self.rectTextOblastMapa.x -= 1
            self.rectTextOblastMapa= self.rectTextOblastMapa.move(-2,0)
        if klavesy[pygame.K_RIGHT] or klavesy[pygame.K_d]:

            #self.rectTextOblastMapa.x += 1
            self.rectTextOblastMapa= self.rectTextOblastMapa.move(2,0)
            #print(str(self.pixeloveUmiestnenieNaMape[1]))
        self.topLeftScaleMap[0] = self.rectTextOblastMapa.x*self.hra.mapa.dajNas()
        self.topLeftScaleMap[1] = self.rectTextOblastMapa.y*self.hra.mapa.dajNas()
        self.hra.mapa.nacitajPolicka(self)
        self.hra.dajAktivBlitGroup().change_layer(self,self.rectTextOblastMapa.y+30)

        
        
        
        