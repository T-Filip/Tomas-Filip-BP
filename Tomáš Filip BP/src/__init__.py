
import pygame
import uvodneNastavenia
import generator
from generator import SimplexNoiseOctava

'''
gen = generator.SimplexNoise(300,0.4,123)
print (gen.getNoise(1,1))
for i in range (-300,300):
    for j in range (-300,300):
        print (str(round(gen.getNoise(i,j),2)) + "  ",end='')
    print()

  '''  
uvod = uvodneNastavenia.UvodneNastavenia()
uvod.run()

print()