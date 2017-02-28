
import pygame
import uvodneNastavenia
import generator
import manazerOkien
from generator import SimplexNoiseOctava
import time 
import itertools


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


  
  
uvodneNastavenia.UvodneNastavenia().run()
manazer = manazerOkien.ManazerOkien().run()






