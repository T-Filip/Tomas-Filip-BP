'''
Created on 18. 3. 2017

@author: T.Filip
'''
import random
from Predmety.predmet import Predmet

'''
Zoznam metod pre vypocty tazenia
Metody drop sa vyuzivaju ako parametri pri vytvarani roznych objektov - je vala druhov objektov a kazdy z nich moze davat rozlisny drop v rozlisnych poctoch s inou nahodou a pod

'''



def vypocitajDlzkuTazenia(tazenyObjekt,nastroj,hrac):
    return 100






'''
vstup pole s prvkami poctu dropu 
kamen
zelezo
zlato

'''
def dropVelkyKamen(args,hrac):
    hrac.vlozPredmet(Predmet(2100,5)) 
    hrac.vlozPredmet(Predmet(2101,1)) 
    hrac.vlozPredmet(Predmet(2102,1))  
    