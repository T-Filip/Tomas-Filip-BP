
import pygame
import random
import time
import nastavenia
import mapa
from Postavy import hrac
import ObjektyMapa.infObjekty as infObjekty
import logging
import Menu.oknoInventar as oknoInventar
import Menu.enumOknaHra as enumOknaHra
import Textury.textury as textury
from generator import Generator
import math
from Textury import enumTextura







class Hra:
    def __init__(self,manazerOkien, screen, textury,vlastnosti,typP):
        self.manazerOkien = manazerOkien
        scale = nastavenia.ROZLISENIA_X[nastavenia.vybrateRozlisenie]/1280
        self.screen = screen
        #nacitat mapu a tak
        self.timeUP = time.time()+1
        
        self.pocetFPS = 0
        self.fpsCount = 0
        
        self.pocetTPS = 0
        self.tpsCount = 0
        
        self.pocetTickov = 0
    
        self.allSprites = pygame.sprite.Group()
        self.aktivBlitObjMapa = pygame.sprite.LayeredUpdates()
        self.postavyGroup = pygame.sprite.Group()
        self.mobky = pygame.sprite.Group()
        self.polickaSprites = pygame.sprite.RenderPlain()
        

        
        
        
        
        self.hrac = hrac.Hrac(self,[0,0],typP,textury,vlastnosti,48,48)
        
        logging.info("Vytvorenie mapy")
        self.mapa = mapa.Mapa(self)
        
        self.hrac.linkMapa(self.mapa)
        
        
        
        logging.info("inicializacia mapy")
        self.hrac.update()
        
        self.initInformacieOHracovi(scale)
        self.invOknoRychlyPristup.reinit(self.hrac.dajInventarRychlyPristup())
        self.manazerOkien.dajOknoHra(enumOknaHra.EnumOknaHra.INVENTAR).vlozOkno(self.invOknoRychlyPristup)
        
        '''
        self.polickaSpritesTEST = pygame.sprite.RenderPlain()
        for i in range (0,10000):
            test(self,50,50)
        '''

        self.casovanieModulo = 0
        
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
        self.updateHluku()
        pygame.display.flip()
        
        self.casNextUpdateStavNpc = 0

            
        self.initTime = time.time()
        
    def dajPostavyGroup(self):
        return self.postavyGroup
        
    def dajManazerOkien(self):
        return self.manazerOkien
        
    def dajPocetTickov(self):
        return self.pocetTickov

    def dajHraca(self):
        return self.hrac
        
    def dajOknoInventarRychlyPristup(self):
        return self.invOknoRychlyPristup
    
    def dajGroupPreMobky(self):
        return self.mobky

       
    def initInformacieOHracovi(self,scale):
        width= int(640*scale)
        posX = int(320*scale)
        posY = int(630*scale)
        height = int(80*scale)
        self.invOknoRychlyPristup = oknoInventar.OknoInventar(pygame.Rect(posX,posY,width,height),64)
        posX = int(390*scale)
        posY = int(610*scale)
        sirka= int(500*scale)
        vyska = int(20*scale)
        self.healthBar = textury.dajTexturu(enumTextura.EnumTextura.HEALTH_BAR, sirka, vyska)
        self.sirkaHpBaru = sirka
        self.sirkaUkazovatelaZdravia = sirka
        self.updateUkazovatelZdravia()
        
    def skontrolujAktualnostZdravia(self):
        #koli efektu - taktiez uz nebude nutne updatovat zdravie hracovi toto to skontroluje
        #vzhladom na to ze ide o destinne cila tak porovnavam vzdialenosti 2 bodov od realneho a ktory je na tom lepsie ten sa stane novym
        nas = self.hrac.dajHp()/self.hrac.dajMaxHp()
        nasGraf = self.sirkaUkazovatelaZdravia/self.sirkaHpBaru
        if nas<nasGraf:
            nasGrafNew = self.sirkaUkazovatelaZdravia - 1/self.sirkaHpBaru
            prip = -1
        else:
            nasGrafNew = self.sirkaUkazovatelaZdravia + 1/self.sirkaHpBaru
            prip = 1
              
        vzdialenostStary = math.fabs(nas-nasGraf)
        vzdialenostNovy = math.fabs(nas-nasGrafNew)
        if vzdialenostNovy < vzdialenostStary:
            self.sirkaUkazovatelaZdravia += prip
            self.updateUkazovatelZdravia()
        else:
            return # vsetko ostava po starom

            
            
        
       
    def updateUkazovatelZdravia(self):
        print("UPDATE")
        scale = self.mapa.dajScaleNas()
        nas = self.hrac.dajHp()/self.hrac.dajMaxHp()
        #sirka= int(500*scale*nas)
        vyska = int(20*scale)
        posX = int(390*scale)
        posY = int(610*scale)
        self.umiestnenieHp = [[posX+1,posY+1],[posX+1,posY+vyska-1],[posX+self.sirkaUkazovatelaZdravia-1,posY+vyska-1],[posX+self.sirkaUkazovatelaZdravia-1,posY+1]]
        
        
    def addAktivBlit(self,sprite):
        self.aktivBlitObjMapa.add(sprite)
        
    def dajAktivBlitGroup(self):
        return self.aktivBlitObjMapa


    
    
    def vykresliHru(self):
        #self.screen.fill(nastavenia.BLACK)
        
        #gc.collect()
        '''
        if self.fpsCount == 1:
            print("-------")
            print("all sprites: " + str(len(self.allSprites)))
            print(self.hrac.suradnice)
        '''

        
        self.fpsCount +=  1
        #print(len(self.polickaSprites))
        
        
        
        
        
       #iba ak sa hrac pohne? 
        self.mapa.updateKamera(self.hrac)
        #self.hrac.updateScreenPosition(self.mapa)

        if self.mapa.menilSaZoom:
            #print(self.mapa.zoom)
            nas = self.mapa.scaleNasobitel
            self.mapa.menilSaZoom = False
            for policko in self.polickaSprites:
                policko.updatePozicie(self.mapa)
                policko.scale(nas)
                policko.updateScreenPosition(self.mapa)


            
            for postava in self.postavyGroup:
                postava.scale(nas)
                postava.updateScreenPosition(self.mapa)
                try:
                    postava.updateLayer()
                except ValueError:
                    pass
                
            
            #poscaluje textury
            for infObj in infObjekty.infObjScalovanie:
                if len(infObj.sprites) > 0:
                    infObj.scale(nas)
            
            for obj in infObjekty.objMapaScalovanie:
                obj.scale(nas)
                obj.updateScreenPosition(self.mapa)
        else:
            for policko in self.polickaSprites:
                policko.updatePozicie(self.mapa)
                policko.updateScreenPosition(self.mapa)
            
            for obj in infObjekty.objMapaScalovanie:
                obj.updateScreenPosition(self.mapa)

            for postava in self.postavyGroup:
                postava.updateTopLeft(self.mapa.dajNas())
                postava.updateScreenPosition(self.mapa)
                try:
                    postava.updateLayer()
                except ValueError:
                    '''
                    Pri update pozicie sa postavy mozu zmazat ak sa ocitnu mimo nacitanej oblasti
                    Ak sa tak stane uz nie je mozne menit layer kedze tato postava bola z groupy uz odstranena.
                    Pri buducom iterovani cez self.postavyGroup uz tento problem nebude kedze sa tato postava odstrani aj z tohto zoznamu
                    '''
                    pass 
            
                
                

        
        #for sprite in self.aktivBlitObjMapa:
        #    try:
        #        sprite.dorobit(self.mapa)
        #    except:
        #        pass
                

            

        
        
        self.polickaSprites.draw(self.screen)
        self.aktivBlitObjMapa.draw(self.screen)
        #self.polickaSpritesTEST.draw(self.screen)
        '''
        if self.fpsCount == 20:
            print("---------------")
            print (len(self.polickaSprites))
            print (len(self.aktivBlitObjMapa))
        '''
        if not self.manazerOkien.jeVykresleneNejakeMenu():
                self.hrac.vykresliOznacenyPredmet(self.screen)
        self.invOknoRychlyPristup.draw(self.screen)
        self.vykresliHpBar(self.screen)
        
    def vykresliHpBar(self,screen):
        pygame.draw.polygon(screen,nastavenia.RED,self.umiestnenieHp)
        screen.blit(self.healthBar,(self.umiestnenieHp[0][0],self.umiestnenieHp[0][1]))

        
        
    def dajMapu(self):
        return self.mapa
        
    def klikButton1(self):
        self.hrac.klikButton1()
    def klikButton2(self):
        self.hrac.klikButton2()
    def klikButton3(self):
        self.hrac.klikButton3()
    def klikButton4(self):
        self.hrac.klikButton4()
    def klikButton5(self):
        self.hrac.klikButton5()
        
    def vykresliInfoRoh(self):
        font = textury.dajFont(16)
        
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
        self.casovanieModulo +=1
        self.pocetTickov += 1 
        
        
        zlozitostVKroku = time.time()
        modulo10 = self.casovanieModulo % 10
        modulo100 = self.casovanieModulo % 100
        
        self.tpsCount += 1
        if time.time() > self.timeUP:
            self.timeUP = time.time()+1
            self.pocetFPS = self.fpsCount
            self.pocetTPS = self.tpsCount
            self.tpsCount = 0
            self.fpsCount = 0
            
        self.postavyGroup.update([modulo100])#tu uz je aj hrac
        
        if modulo10 == 0: 
            self.mapa.updateZoom()
            
        self.riadMobky(modulo100,modulo10)
        
            
            

        #print(time.time()-zlozitostVKroku)


            
            
            
        
        logging.info("hrac-eventy")
        self.hrac.eventy()
        self.skontrolujAktualnostZdravia()
        
        #iba raz za cas napr raz za 2 sec mozno viac
    def updateHluku(self):
        self.hlukoveCentra = {}
        self.hodnotyHlukovychCentier = {}
        id = 0
        for postava in self.postavyGroup:
            esteTrebaUlozit = True
            for hlukCentrum in self.hlukoveCentra.values():
                vzdialenost = hlukCentrum[0].dajVzdialenostOdPostavy(postava)
                if vzdialenost < 200:
                    hlukCentrum[postava] = postava
                    self.hodnotyHlukovychCentier[hlukCentrum[0]] += postava.dajHodnotuHluku()
                    esteTrebaUlozit = False
                    break
            if esteTrebaUlozit:
                self.hlukoveCentra[postava] = {0:postava}#nove hlukove centrum
                self.hodnotyHlukovychCentier[postava] = postava.dajHodnotuHluku()#leader ako kluc do dic pre hodnoty
                 
        #self.pocetHlukovychCentrier = id-1
        
    def dajHlukoveCentra(self):
        return self.hlukoveCentra
    def dajHodnotyHlukovychCentier(self):
        return self.hodnotyHlukovychCentier

    def riadMobky(self,modulo100,modulo10):
        poc = math.ceil(len(self.mobky)/10)
        
        if poc == 0:
            return
        
        if modulo100 == 75:
            self.updateHluku()


        if modulo10 == 7:
            if self.casNextUpdateStavNpc < time.time():
                self.casNextUpdateStavNpc = time.time() + 1/len(self.mobky)
                samp = random.sample(list(self.mobky),poc)
                for mob in samp:
                    mob.updateZmenStav()
                
        
                
        elif modulo10 == 4: # ak je 0 vykonava sa zoom co je operacia zlozita na vypocet preto mu nebudeme pridavat 1 do istoty aby sa tam spravil frame
            samp = random.sample(list(self.mobky),poc)
            for mob in samp:
                mob.updateCinnostStavu()
        
    def stlacena0(self):
        self.hrac.stlacena0()
        
    def stlacena1(self):
        self.hrac.stlacena1()
        
    def stlacena2(self):
        self.hrac.stlacena2()
        
    def stlacena3(self):
        self.hrac.stlacena3()
        
    def stlacena4(self):
        self.hrac.stlacena4()
        
    def stlacena5(self):
        self.hrac.stlacena5()
        
    def stlacena6(self):
        self.hrac.stlacena6()
        
    def stlacena7(self):
        self.hrac.stlacena7()
        
    def stlacena8(self):
        self.hrac.stlacena8()
        
    def stlacena9(self):
        self.hrac.stlacena9()
        
    def stlaceneR(self):
        self.hrac.stlaceneR()
    
    
    
    
        
        
class test(pygame.sprite.Sprite):
    def __init__(self, hra,xPos,yPos):
        self.hra = hra
        pygame.sprite.Sprite.__init__(self, self.hra.polickaSpritesTEST)
        self.image = pygame.Surface((64,64))
        #self.image.set_colorkey((255,0,255))
        #self.image = image
        #self.image.convert()
        self.image.fill((255,0,255))
        #self.image.blit(image,(0,0))

        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos
        
        
        
class test2(pygame.sprite.Sprite):
    def __init__(self, hra,xPos,yPos):
        self.hra = hra
        pygame.sprite.Sprite.__init__(self, self.hra.layeredSprites)
        #self.image = pygame.Surface((64,64), pygame.SRCALPHA )
        #self.image.set_colorkey((255,0,255))
        #self.zdroj = image
        self.image = pygame.Surface((64,64), pygame.SRCALPHA)
        #self.image.blit(self.zdroj,(0,0))                         
        #self.image.convert()
        self.image.fill((255,0,255))
        #self.image.blit(image,(0,0))

        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos
        
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
