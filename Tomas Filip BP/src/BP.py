
import pygame
from Nastavenia import uvodneNastavenia
from Menu import manazerOkien
from ObjektyMapa import generator as generator
import time 
import itertools
import logging
import ObjektyMapa.infObjekty as infObjekty
import random




'''
import os
cur_path = os.getcwd()
ignore_set = set(["__init__.py", "count_sourcelines.py"])

loclist = []

for pydir, _, pyfiles in os.walk(cur_path):
    for pyfile in pyfiles:
        if pyfile.endswith(".py") and pyfile not in ignore_set:
            totalpath = os.path.join(pydir, pyfile)
            loclist.append( ( len(open(totalpath, "r").read().splitlines()),
                               totalpath.split(cur_path)[1]) )

for linenumbercount, filename in loclist: 
    #print ("%05d lines in %s" % (linenumbercount, filename))

print ("\nTotal: %s lines (%s)" %(sum([x[0] for x in loclist]), cur_path))
'''



'''

pygame.init()
screen = pygame.display.set_mode((500,500 ),pygame.NOFRAME,24)
screen.fill((255,0,0))

tex = pygame.image.load('img/Test8.png')
#tex2 = pygame.image.load('img/Test8.png').convert()
print(tex.get_bitsize())
tim = time.time()
#screen.blit(tex,(0,0))
#screen.blit(tex2,(60,0))
for i in range (10000):
    screen.blit(tex,(0,0))
    #pygame.display.flip()
    
print(time.time() - tim)
pygame.display.flip()
time.sleep(3)

'''

'''

gen = generator.SimplexNoise(300,0.4,123)
print (gen.getNoise(1,1))
for i in range (-300,300):
    for j in range (-300,300):
        #print (str(round(gen.getNoise(i,j),2)) + "  ",end='')
    #print()

'''  

'''
funcdict = {
  1: mypackage.mymodule.myfunction,

}

funcdict[myvar](parameter1, parameter2)
'''
'''
i = [1,2,3]
try:
    #print(str(i[3]))
except IndexError:
    #print("indexErr")
     
''' 

'''
pocetTrafiliSa = 0
for i in range (1000000):
    a = False
    aC = random.randint(0,99)
    b = False
    bC = random.randint(0,99)
    for j in range(10):
        c = random.randint(0,99)
        if c == aC:
            a = True
        if c == bC:
            b = True
    if a and b:
        pocetTrafiliSa+=1
        
print(pocetTrafiliSa)
print("percenta: " + str(pocetTrafiliSa/1000000))
'''       
    

'''
generatorPreMobky = generator.Generator(14,150,0.95)
pocet = 0
for i in range (0,40):
    #print()
    for j in range (0,200):
        n = generatorPreMobky.noise(i,j)
        if n > 1 or n<0:
            #print("A",end='')
            pocet += 1
        else:
            #print(" ",end='')
        #print("%.2f" % round(n,2),end='  ')
        
        
print("aaaaa")
print(pocet)
'''
        

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='log.txt',
                    filemode='w')



 
logging.info("--- Uvodne menu ---")

uvodneNastavenia.UvodneNastavenia().run()

logging.info("nacitanie inf obj")
infObjekty.nacitajTexturyObjMapa()
logging.info("--- Hra ---")
manazer = manazerOkien.ManazerOkien()
manazer.run()






