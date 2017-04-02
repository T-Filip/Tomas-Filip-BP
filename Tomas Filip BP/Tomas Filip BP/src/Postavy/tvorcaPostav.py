'''
Created on 9. 3. 2017

@author: T.Filip
'''

from Textury import textury
import pygame
import nastavenia as nastavenia
import random

'''
    //Abstraktna trieda// ktorej ulohou je vytvaranie textur pre vsetky postavy v hre na zaklade parametrov.

'''
def vytvorPostavu(jeToHrac, paSmerPostavy,farbaTela,typPostavy,cisloTvare,cisloVlasov,cisloOci,cisloPohlavia):
    postavy = textury.POSTAVY
    tvare = textury.TVARE
    
    #postava = pygame.Surface((64,64),pygame.SRCALPHA)
    
    smerPostavy = paSmerPostavy
    if smerPostavy==4:
        smerPostavy = 2
    #telo
    postavaMala = pygame.Surface((64,64),pygame.SRCALPHA)
    postavaMala.blit(postavy,(0,0),(int(64*smerPostavy),int(64*typPostavy),64,64))
    #farbatela
    farbaPostavy = pygame.Surface((64,64),pygame.SRCALPHA)
    farbaPostavy.blit(postavy,(0,0),(int(64*smerPostavy+256),int(64*typPostavy),64,64))
    farbaPostavy.fill(farbaTela, None, pygame.BLEND_RGBA_MULT)
    
    postavaMala.blit(farbaPostavy,(0,0))
    
    #HLAVA
    hlava = pygame.Surface((32,32),pygame.SRCALPHA)
    hlava.blit(tvare,(0,0),(64*cisloTvare,0,32,32))
    
    #farbaHlavy
    farbaHlavy = pygame.Surface((32,32),pygame.SRCALPHA)
    farbaHlavy.blit(tvare,(0,0),(32+ 64*cisloTvare,0,32,32))
    farbaHlavy.fill(farbaTela, None, pygame.BLEND_RGBA_MULT)

    
    hlava.blit(farbaHlavy,(0,0))
    
    #oci
    hlava.blit(tvare,(0,0),(int(32*smerPostavy+256*cisloPohlavia),int(32+32*cisloOci),32,32))
    #vlasy
    hlava.blit(tvare,(0,0),(int(32*smerPostavy+128+256*cisloPohlavia),int(32+32*cisloVlasov),32,32))

    
    if smerPostavy==2:
        posHlava = (12,4)
    else:
        posHlava = (16,4)
        
    postavaMala.blit(hlava,posHlava)
    
    if paSmerPostavy == 4:
        postavaMala = pygame.transform.flip(postavaMala, True, False)
    
    
    
    #pygame.transform.scale(postavaMala,(64,64),postava)
    #pygame.transform.scale2x(postavaMala,postava)
    
    
    return postavaMala


        
def vytvorPostavuRandom(jeToHrac,postava):
    
    if jeToHrac:
        cap = random.randint(0,len(nastavenia.FARBA_TELA)-1)
        farbaTela = nastavenia.FARBA_TELA[cap]
    else:
        cap = random.randint(0,len(nastavenia.FARBA_TELA_NPC)-1)
        print(cap)
        farbaTela = nastavenia.FARBA_TELA_NPC[cap]
        
    cap = nastavenia.CAP_TYP_POSTAVY
    typPostavy = random.randint(cap[0],cap[1])
    vlastnosti = nastavenia.VLASTNOSTI_POSTAVY_TYP_POSTAVY[typPostavy].copy()
    
    postava.setTypPostavy(typPostavy)
    cap = nastavenia.CAP_POHLAVIE
    pohlavie = random.randint(cap[0],cap[1])
    vlpoh = nastavenia.VLASTNOSTI_POSTAVY_POHLAVIE[pohlavie]
    cap = nastavenia.CAP_TVAR[pohlavie]
    tvar = random.randint(cap[0],cap[1])
    cap = nastavenia.CAP_VLASY[pohlavie]
    vlasy = random.randint(cap[0],cap[1])
    cap = nastavenia.CAP_HLAVA
    hlava = random.randint(cap[0],cap[1])
    
    vlastnostiNovejPostavy = [[vlastnosti[0] + vlpoh[0]],[vlastnosti[1] + vlpoh[1]],[vlastnosti[2] + vlpoh[2]],[vlastnosti[3] + vlpoh[3]]]
    postava.setVlastnosti(vlastnostiNovejPostavy)

    imageZaloha = [vytvorPostavu(False, 0, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                        ,vytvorPostavu(False, 1, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                        ,vytvorPostavu(False, 2, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                        ,vytvorPostavu(False, 3, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)
                        ,vytvorPostavu(False, 4, farbaTela, typPostavy, hlava, vlasy, tvar, pohlavie)]
    return imageZaloha
        



''' 
(self.args[0],self.menu.farbaTela[self.menu.indexFarbyTela[0]],self.menu.typPostavy[0],self.menu.cisloTvare[0],self.menu.cisloVlasov[0],self.menu.cisloOci[0],self.menu.cisloPohlavia[0])

   postavy = textury.POSTAVY
    tvare = textury.TVARE
    
    #postava = pygame.Surface((64,64),pygame.SRCALPHA)
    
    smerPostavy = self.args[0]
    if smerPostavy==4:
        smerPostavy = 2
    #telo
    postavaMala = pygame.Surface((64,64),pygame.SRCALPHA)
    postavaMala.blit(postavy,(0,0),(int(64*smerPostavy),int(64*self.menu.typPostavy[0]),64,64))
    #farbatela
    farbaPostavy = pygame.Surface((64,64),pygame.SRCALPHA)
    farbaPostavy.blit(postavy,(0,0),(int(64*smerPostavy+256),int(64*self.menu.typPostavy[0]),64,64))
    farbaPostavy.fill(self.menu.farbaTela[self.menu.indexFarbyTela[0]], None, pygame.BLEND_RGBA_MULT)
    
    postavaMala.blit(farbaPostavy,(0,0))
    
    #HLAVA
    hlava = pygame.Surface((32,32),pygame.SRCALPHA)
    hlava.blit(tvare,(0,0),(64*self.menu.cisloTvare[0],0,32,32))
    
    #farbaHlavy
    farbaHlavy = pygame.Surface((32,32),pygame.SRCALPHA)
    farbaHlavy.blit(tvare,(0,0),(32+ 64*self.menu.cisloTvare[0],0,32,32))
    farbaHlavy.fill(self.menu.farbaTela[self.menu.indexFarbyTela[0]], None, pygame.BLEND_RGBA_MULT)

    
    hlava.blit(farbaHlavy,(0,0))
    
    #oci
    hlava.blit(tvare,(0,0),(int(32*smerPostavy+256*self.menu.cisloPohlavia[0]),int(32+32*self.menu.cisloOci[0]),32,32))
    #vlasy
    hlava.blit(tvare,(0,0),(int(32*smerPostavy+128+256*self.menu.cisloPohlavia[0]),int(32+32*self.menu.cisloVlasov[0]),32,32))

    
    if smerPostavy==2:
        posHlava = (12,4)
    else:
        posHlava = (16,4)
        
    postavaMala.blit(hlava,posHlava)
    
    if self.args[0] == 4:
        postavaMala = pygame.transform.flip(postavaMala, True, False)
    
    self.menu.postavyHrac[self.args[0]] = postavaMala
    '''