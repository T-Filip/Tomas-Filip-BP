# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import math
import random
import nastavenia
from random import seed


class SimplexNoise:
    def __init__ (self, najHod, stal, seed):
        self.seed = seed
        self.stal = stal
        self.pocetOktav = math.ceil(math.log(najHod,2))
        self.listOktav = [None]*self.pocetOktav
        self.poleFrekvencii = [0]*self.pocetOktav
        self.poleAmplitud = [0]*self.pocetOktav
        random.seed(self.seed)
        for i in range(0,self.pocetOktav):
            #self.listOktav.insert(i,SimplexNoiseOctave(self.seed))
            self.listOktav[i] = SimplexNoiseOctava(self.seed);
            self.poleFrekvencii[i] = math.pow(2,i)
            self.poleAmplitud[i] = math.pow(self.stal, len(self.listOktav)-i)
            
    def getNoise(self,x,y):
        vysledok=0
        for i in range (0,self.pocetOktav):
            vysledok += self.listOktav[i].noise(x/self.poleFrekvencii[i],y/self.poleFrekvencii[i])*self.poleAmplitud[i]
        return vysledok
      
      
      
      
      
class SimplexNoiseOctava:
    def __init__(self,seed):
        self.seed = seed
        self.Gradienty = [[1,1],[-1,1],[1,-1],[-1,-1],[1,0],[0,1],[-1,0],[0,-1]]
        self.pocetSwapov = 500;
        #self.p = []*len(nastavenia.P_SUPPLY)
        self.p = list(nastavenia.P_SUPPLY)
        self.rand = random.Random()
        self.rand.seed(self.seed)
        self.poprehadzuj()
        self.perm = [0]*512
        self.permMod8 = [0]*512
        for i in range (0,512):
            self.perm[i] = self.p[i&255]
            self.permMod8[i] = self.p[i&255]%8
        
    def Floor(self, c):
        return int(c)
        
    def poprehadzuj(self):
        for i in range (1,self.pocetSwapov):
            nah1 = self.rand.randint(0, 255)
            nah2 = self.rand.randint(0, 255)
            #print(str(nah1))
            #print(str(nah2))
            pom = self.p[nah1]
            self.p[nah1] = self.p[nah2]
            self.p[nah2] = pom
            
    def dot(self,gradient,a,b):
        return gradient[0]*a+gradient[1]*b
        
    def noise(self, x , y):
        s=nastavenia.F2*(x+y)
        bod0X=self.Floor(s+x)
        bod0Y=self.Floor(s+y)
        t = (bod0X+bod0Y)*nastavenia.G2
        vzdialenost0X = x-(bod0X-t)
        vzdialenost0Y = y-(bod0Y-t)# vzdialenosti od zakladneho bodu trojuholnika
        #umiestnenie neznameho rohu trojuholnika
        if (vzdialenost0X > vzdialenost0Y):
            bod1X = 1#spodny trojuholnik
            bod1Y = 0
        else:
            bod1X = 0#horny trojuholnik
            bod1Y = 1
            
        offset1X = vzdialenost0X - bod0X + nastavenia.G2
        offset1Y = vzdialenost0Y - bod0Y + nastavenia.G2
        
        offset2X = vzdialenost0X-1+2*nastavenia.G2
        offset2Y = vzdialenost0Y-1+2*nastavenia.G2
        
        #hashovanie
        ii = bod0X & 255
        jj = bod0Y & 255
        indexGradientu0 = self.permMod8[ii+self.perm[jj]]
        indexGradientu1 = self.permMod8[ii+bod1X+self.perm[jj+bod1Y]]
        indexGradientu2 = self.permMod8[ii+1+self.perm[jj+1]]
        
        
        
        roh0 = 0.5 - vzdialenost0X*vzdialenost0X - vzdialenost0Y*vzdialenost0Y
        if (roh0<0):
            roh0 = 0
        else:
            roh0 = math.pow(roh0,4) * self.dot(self.Gradienty[indexGradientu0],vzdialenost0X,vzdialenost0Y)
            
        roh1 = 0.5 - offset1X*offset1X - offset1Y*offset1Y
        if (roh1<0):
            roh1 = 0
        else:
            roh1 = math.pow(roh1,4) * self.dot(self.Gradienty[indexGradientu1],offset1X,offset1Y)
            
        roh2 = 0.5 - offset2X*offset2X - offset2Y*offset2Y
        if (roh2<0):
            roh2 = 0
        else:
            roh2 = math.pow(roh2,4) * self.dot(self.Gradienty[indexGradientu2],offset2X,offset2Y)
            
            
            #print ("Rohy: " + str(roh0) + "  " + str(roh1) + "  "  + str(roh2) )
        return 70*(roh0+roh1+roh2)
        
            
            
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        