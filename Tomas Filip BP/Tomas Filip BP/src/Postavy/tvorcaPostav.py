'''
Created on 9. 3. 2017

@author: T.Filip
'''

import textury
import pygame

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