
import pygame
import uvodneNastavenia
import manazerOkien
import generator as generator
import time 
import itertools
import logging
import ObjektyMapa.infObjekty as infObjekty
import random






'''
gen = generator.SimplexNoise(300,0.4,123)
print (gen.getNoise(1,1))
for i in range (-300,300):
    for j in range (-300,300):
        print (str(round(gen.getNoise(i,j),2)) + "  ",end='')
    print()

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
    print(str(i[3]))
except IndexError:
    print("indexErr")
     
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
    print()
    for j in range (0,200):
        n = generatorPreMobky.noise(i,j)
        if n > 1 or n<0:
            print("A",end='')
            pocet += 1
        else:
            print(" ",end='')
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






