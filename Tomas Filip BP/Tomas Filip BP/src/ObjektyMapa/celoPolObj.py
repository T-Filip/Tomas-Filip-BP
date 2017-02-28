'''
Created on 20. 2. 2017

@author: T.Filip
'''
  
import ObjektyMapa.infObjekty as infObjekty 
import ObjektyMapa.objMapa as objMapa  
import pygame 
import random
        
        


class CeloPolObj():
    def __init__(self,policko,id):
        self.random = random.Random(policko.noise)
        self.id = id
        self.policko = policko
        self.inf = infObjekty.INF_OBJ_MAPA[self.id]
        
        self.zoznamObj =pygame.sprite.Group() # drzi si vsetky ciastocne objekty
        
       
        
        
    def stage2(self,zoznamPolicok):
        
        
        self.zoznamPolicok = zoznamPolicok
        hlavneStrany = 0
        i = 0
        while i<7:
            if zoznamPolicok[i].dajIdCeloPol() == self.id:
                hlavneStrany += 1
            i += 2
                
        a = self.policko.suradnice
        if a[0] == 22 and a[1]== -30:
            i =5 
                
       #da sa lepsie
        indexyTvaru = 0
        if hlavneStrany == 4:
            indexyTvaru =self.h4()
        elif hlavneStrany == 3:
            indexyTvaru =self.h3()
        elif hlavneStrany == 2:
            indexyTvaru =self.h2()    
        elif hlavneStrany == 1:
            indexyTvaru =self.h1()
        else:
            indexyTvaru =self.h0()
            
        if indexyTvaru != None:
            #for x in range (4):
             #   print()
              #  for y in range (4):
               #     print(" " + str(indexyTvaru[y][x]),end='')
            self.vytvorObjekty(indexyTvaru)
        else:
           self.zmenStavPolicka()#policko je obklopene rovnakym typom celopol obj
           print("NONE")
           
    def zmenStavPolicka(self):
        #ak vsade dookola je rovnake celo polickove objekty tak sa len zmeni textura na hlboku vodu
        print("celoPolObj zmenStavPolicka doimplementovat")
                
                
    def h0(self):
        indexyTvaru = [[0 for x in range(4)] for y in range(4)]  # treba nastavit indexy tvaru na kazde policko potom sa vytvoria prislusne objekty
        indexyTvaru[0][0]=0
        indexyTvaru[0][1]=5
        indexyTvaru[0][2]=5
        indexyTvaru[0][3]=2
        
        indexyTvaru[1][0]=4
        indexyTvaru[1][1]=-1
        indexyTvaru[1][2]=-1
        indexyTvaru[1][3]=7#?
        
        indexyTvaru[2][0]=4
        indexyTvaru[2][1]=-1
        indexyTvaru[2][2]=-1
        indexyTvaru[2][3]=7#?
        
        indexyTvaru[3][0]=1
        indexyTvaru[3][1]=6
        indexyTvaru[3][2]=6
        indexyTvaru[3][3]=3
        return indexyTvaru
        
    def h1(self):
        indexyTvaru = self.h0()
        if self.zoznamPolicok[0].dajIdCeloPol() == self.id:
            indexyTvaru[3][0]=4
            indexyTvaru[3][1]=-1
            indexyTvaru[3][2]=-1
            indexyTvaru[3][3]=7
        if self.zoznamPolicok[2].dajIdCeloPol() == self.id:
            indexyTvaru[0][3]=5
            indexyTvaru[1][3]=-1
            indexyTvaru[2][3]=-1
            indexyTvaru[3][3]=6
        if self.zoznamPolicok[4].dajIdCeloPol() == self.id:
            indexyTvaru[0][0]=4
            indexyTvaru[0][1]=-1
            indexyTvaru[0][2]=-1
            indexyTvaru[0][3]=7
        if self.zoznamPolicok[6].dajIdCeloPol() == self.id:
            indexyTvaru[0][0]=5
            indexyTvaru[1][0]=-1
            indexyTvaru[2][0]=-1
            indexyTvaru[3][0]=6
        return indexyTvaru
    def h2(self):
        indexyTvaru = self.h1()
        #ceknutie rohu
        if self.zoznamPolicok[0].dajIdCeloPol() == self.id:
            if self.zoznamPolicok[6].dajIdCeloPol() == self.id:
                if self.zoznamPolicok[7].dajIdCeloPol() == self.id:
                    indexyTvaru[3][0]=-1
                else:
                    indexyTvaru[3][0]=10#2
            elif self.zoznamPolicok[2].dajIdCeloPol() == self.id:
                if self.zoznamPolicok[1].dajIdCeloPol() == self.id:
                    indexyTvaru[3][3]=-1
                else:
                    indexyTvaru[3][3]=8
        elif self.zoznamPolicok[4].dajIdCeloPol() == self.id:
            if self.zoznamPolicok[6].dajIdCeloPol() == self.id:
                if self.zoznamPolicok[5].dajIdCeloPol() == self.id:
                    indexyTvaru[0][0]=-1
                else:
                    indexyTvaru[0][0]=11
            elif self.zoznamPolicok[2].dajIdCeloPol() == self.id:
                if self.zoznamPolicok[3].dajIdCeloPol() == self.id:
                    indexyTvaru[0][3]=-1
                else:
                    indexyTvaru[0][3]=9
        return indexyTvaru
      
    def h3(self):
        indexyTvaru = self.h1()
        if self.zoznamPolicok[0].dajIdCeloPol() != self.id:
            indexyTvaru[3][0]=6
            indexyTvaru[3][3]=6
            if self.zoznamPolicok[5].dajIdCeloPol() == self.id:
                indexyTvaru[0][0]=-1
            else:
                indexyTvaru[0][0]=3
            if self.zoznamPolicok[3].dajIdCeloPol() == self.id:
                indexyTvaru[0][3]=-1
            else:
                indexyTvaru[0][3]=1
        if self.zoznamPolicok[2].dajIdCeloPol() != self.id:
            indexyTvaru[0][3]=7
            indexyTvaru[3][3]=7
            if self.zoznamPolicok[5].dajIdCeloPol() == self.id:
                indexyTvaru[0][0]=-1
            else:
                indexyTvaru[0][0]=3
            if self.zoznamPolicok[7].dajIdCeloPol() == self.id:
                indexyTvaru[3][0]=-1
            else:
                indexyTvaru[3][0]=2
        if self.zoznamPolicok[4].dajIdCeloPol() != self.id:
            indexyTvaru[0][0]=5
            indexyTvaru[0][3]=5
            if self.zoznamPolicok[7].dajIdCeloPol() == self.id:
                indexyTvaru[3][0]=-1
            else:
                indexyTvaru[3][0]=2
            if self.zoznamPolicok[1].dajIdCeloPol() == self.id:
                indexyTvaru[3][3]=-1
            else:
                indexyTvaru[3][3]=0
        if self.zoznamPolicok[6].dajIdCeloPol() != self.id:
            indexyTvaru[0][0]=4
            indexyTvaru[0][3]=4
            if self.zoznamPolicok[1].dajIdCeloPol() == self.id:
                indexyTvaru[3][3]=-1
            else:
                indexyTvaru[3][3]=0
            if self.zoznamPolicok[3].dajIdCeloPol() == self.id:
                indexyTvaru[0][3]=-1
            else:
                indexyTvaru[0][3]=1
        return indexyTvaru
    def h4(self):
        indexyTvaru = self.h1()
        rohy = 0
        if self.zoznamPolicok[1].dajIdCeloPol() == self.id:
            rohy +=1
            indexyTvaru[3][3]=-1
        else:
            indexyTvaru[3][3]=8
        if self.zoznamPolicok[3].dajIdCeloPol() == self.id:
            rohy +=1
            indexyTvaru[0][3]=-1
        else:
            indexyTvaru[0][3]=10
        if self.zoznamPolicok[5].dajIdCeloPol() == self.id:
            rohy +=1
            indexyTvaru[0][0]=-1
        else:
            indexyTvaru[0][0]=11
        if self.zoznamPolicok[7].dajIdCeloPol() == self.id:
            rohy +=1
            indexyTvaru[3][0]=-1
        else:
            indexyTvaru[3][0]=9
            
        if rohy == 0:
            return None
              
        return indexyTvaru
        
     
    #  0 1 2 3    
    #A
    #B
    #C
    #D   
    #indexy [1234][abcd]
    def vytvorObjekty(self,indexy):
        for x in range (0,4):
            for y in range (0,4):   
                obj = self.vytvorObjekt(x,y,indexy)
                obj.vlozDo(self.zoznamObj)
                    
                    
    def vytvorObjekt(self,x,y,indexy):

            index = self.random.randint(0,len(self.inf.infObjekty[indexy[x][y]])-1)
            print (index)
            print ("a")
            #index = 0
            if index > 0 :
                i=5
            return objMapa.ObjMapaVlastInf(self.policko, self.id,(x*16,y*16),self.inf.infObjekty[indexy[x][y]][index])
                
    
    def dajId(self):
        return self.id
        
        
   
        
        
        
        
        
        
        
        
        
class CeloPolObjPoz(CeloPolObj):
    def __init__(self,policko,id):
        super().__init__(policko, id)
        
        
        
    def vytvorObjekt(self,x,y,indexy):
        if indexy[x][y]< 0:
            surf = pygame.Surface(self.inf.infObjekty[0][0].img.get_size(), pygame.SRCALPHA)
            rect = pygame.Rect(0,0,surf.get_width(),surf.get_height())
            infobj = infObjekty.InfObj(surf,rect,0.4)
            return objMapa.ObjMapaVlastInfPozadie(self.policko, self.id,(x*16,y*16),infobj,self.inf.pozadie)#pozadie sa nedava - kreslene v plnej velkosti ako default
        else:
            #podobne ako v rodicovy akurat sa vytvara potomok ObjMapy s fukciou pre kreslenie pozadia
            index = self.random.randint(0,len(self.inf.infObjekty[indexy[x][y]])-1)
            return objMapa.ObjMapaVlastInfPozadie(self.policko,   self.id,   (x*16,y*16),
                                                      self.inf.infObjekty[indexy[x][y]][index],
                                                          self.inf.pozadie,
                                                             self.inf.rectPozadia[indexy[x][y]][index])# rectPozadia predstavuje pole viacerych rect 

    
    
    
    
    
    
    
    