
import pygame
import random
from random import randint
import time
import nastavenia
import mapa
import postavy
import ObjektyMapa.infObjekty as infObjekty






class Hra:
    def __init__(self,manazerOkien, screen):
        self.manazerOkien = manazerOkien
        
        self.screen = screen
        #nacitat mapu a tak
        b=4
        self.timeUP = time.time()+1
        
        self.pocetFPS = 0
        self.fpsCount = 0
        
        self.pocetTPS = 0
        self.tpsCount = 0
        
    

        self.aktivBlitObjMapa = pygame.sprite.LayeredUpdates()
        self.polickaSprites = pygame.sprite.RenderPlain()
        
        
        self.hrac = postavy.Hrac(self,[2200,-2400],pygame.Rect(16,48,16,16))
        self.mapa = mapa.Mapa(self)
        self.hrac.initMapu()
        self.hrac.update()

        
        
        self.imagee = pygame.Surface((64,64))
        #self.imagee.fill((100,200,120))
        
        self.Test = pygame.image.load('img\\Test32.png')
        self.img = pygame.Surface((64,64))
        self.img.blit(self.Test,(0,0))
        self.img.convert()
        self.img2 = pygame.Surface((64,64), pygame.SRCALPHA)
        self.img2.blit(self.Test,(0,0))
        self.img.convert_alpha()
        
        '''
        for i in range (1,1000):
            col = (randint(0,255),randint(0,255),randint(0,255))
            test(self,randint(0,1000),randint(0,1000),self.img,col)
            
            
        for i in range (1,30):
            col = (randint(0,255),randint(0,255),randint(0,255))
            test2(self,randint(0,1000),randint(0,1000),self.img2,col)
            '''
            
        self.aktivBlitObjMapa.draw(self.screen)
        pygame.display.flip()
        

            
        self.initTime = time.time()

        
        
        
    def addAktivBlit(self,sprite):
        self.aktivBlitObjMapa.add(sprite)
        
    def dajAktivBlitGroup(self):
        return self.aktivBlitObjMapa

    
    def vykresliHru(self):
        #self.screen.fill(nastavenia.BLACK)
        
        self.fpsCount +=  1
        
        for policko in self.polickaSprites:
            policko.updatePozicie(self.mapa)
        
        



        if self.mapa.menilSaZoom:
            #print(self.mapa.zoom)
            nas = self.mapa.scaleNasobitel
            self.mapa.menilSaZoom = False
            for policko in self.polickaSprites:
                policko.scale(nas)

            
            self.hrac.scale(nas)
            
            #poscaluje textury
            for infObj in infObjekty.infObjScalovanie:
                if len(infObj.sprites) > 0:
                    infObj.scale(nas)
            
            for obj in infObjekty.objMapaScalovanie:
                obj.scale(nas)
                
                
       #iba ak sa hrac pohne? 
        self.mapa.updateKamera(self.hrac)
        self.hrac.updateScreenPosition(self.mapa)
        
        for sprite in self.aktivBlitObjMapa:
            try:
                sprite.dorobit(self.mapa)
            except:
                pass
                
        for sprite in self.polickaSprites:
            sprite.updateScreenPosition(self.mapa)
            
        for obj in infObjekty.objMapaScalovanie:
                obj.updateScreenPosition(self.mapa)
        
        
        self.polickaSprites.draw(self.screen)
        self.aktivBlitObjMapa.draw(self.screen)
        
        font = nastavenia.FONT_1_16
        
        text = str("x: " + str(self.hrac.suradnice[0]) + "   y: " + str(self.hrac.suradnice[1]))
        textSurf = font.render(text, 10, (255,255,0))#ERROR zero width? rychle spustenie do prava
        self.screen.blit(textSurf, (10, 10))
        
        text = "FPS: " + str(self.pocetFPS)
        textSurf = font.render(text, 10, (255,255,0))
        self.screen.blit(textSurf, (10, 30))
        
        text = "TPS: " + str(self.pocetTPS)
        textSurf = font.render(text, 10, (255,255,0))
        self.screen.blit(textSurf, (10, 50))
        


           
            
        #self.hracKocka = pygame.Surface((64,64))
        #self.hracKocka.fill((255,0,0))
        #self.screen.blit(self.hracKocka,(self.hrac.rect.topleft))
        pygame.display.flip()  
        
        
    def update(self):
        
        self.tpsCount += 1
        
        if time.time() > self.timeUP:
            self.timeUP = time.time()+1
            self.pocetFPS = self.fpsCount
            self.pocetTPS = self.tpsCount
            self.tpsCount = 0
            self.fpsCount = 0
        
        #pos = pygame.mouse.get_pos()
        #sprites_pod_myskou = [s for s in self.layeredSprites if s.rect.collidepoint(pos)]
        #print(len(sprites_pod_myskou))
        
        
        
        self.hrac.eventy()
        
        #nah = randint(0,99)
        #if nah<20:
        #    self.layeredSprites.update()
        
        
        
        #self.polickaSprites.update(self.mapa) # nic tam nie je 
        
        
        
            
            
        





class test(pygame.sprite.Sprite):
    def __init__(self, hra,sirka,vyska,image,col):
        self.hra = hra
        pygame.sprite.Sprite.__init__(self, self.hra.polickaSprites)
        self.image = pygame.Surface((64,64))
        #self.image.set_colorkey((255,0,255))
        #self.image = image
        #self.image.convert()
        #self.image.fill((255,0,255))
        self.image.blit(image,(0,0))

        self.rect = self.image.get_rect()
        self.rect.x = sirka
        self.rect.y = vyska
        
        
        
class test2(pygame.sprite.Sprite):
    def __init__(self, hra,sirka,vyska,image,col):
        self.hra = hra
        pygame.sprite.Sprite.__init__(self, self.hra.layeredSprites)
        #self.image = pygame.Surface((64,64), pygame.SRCALPHA )
        #self.image.set_colorkey((255,0,255))
        self.zdroj = image
        self.image = pygame.Surface((64,64), pygame.SRCALPHA)
        self.image.blit(self.zdroj,(0,0))                         
        #self.image.convert()
        #self.image.fill((255,0,255))
        #self.image.blit(image,(0,0))

        self.rect = self.image.get_rect()
        self.rect.x = sirka
        self.rect.y = vyska
        
    def update(self):
        self.rect = self.rect.inflate(1,1)
        self.image = pygame.transform.scale(self.zdroj,(self.rect.width,self.rect.height))
        


'''
class Hra:
    # The Game object will initialize the game, run the game loop,
    # and display start/end screens

    def __init__(self):

        pg.init()
        # initialize sound - uncomment if you're using sound
        # pygame.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # start the clock
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True

    def new(self):
        # initialize all your variables and do all the setup for a new game
        self.run()

    def load_data(self):
        # load all your assets (sounds, images, etc.)
        pass

    def run(self):
        # The Game loop - set self.running to False to end the game
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # the update part of the game loop
        pass

    def draw(self):
        # draw everything to the screen
        self.screen.fill(BGCOLOR)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            # this one checks for the window being closed
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # add any other events here (keys, mouse, etc.)

    def show_start_screen(self):
        # show the start screen
        pass

    def show_go_screen(self):
        # show the game over screen
        pass

# create the game object
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
'''
