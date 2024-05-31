INSTALLED = True

import requests
import struct
import numpy as np
if INSTALLED:
    from pycanum.httpdata import HttpData
else:
    from httpdata import HttpData
import matplotlib.pyplot as plt
import time
import scipy.signal
import os
import subprocess


ENTREE_CHRONO = 16



if INSTALLED:
    PATH = os.path.dirname(__file__)+"\\"
else:
    PATH = "../build/Debug/"


class Sysam:
    def __init__(self,nom='SP5'):
        try:
            #os.system('start /B ../build/Debug/sysamhttp.exe "http://127.0.0.1:5000/"')
            os.system('start /B '+PATH+'sysamhttp.exe "http://127.0.0.1:5000/"')
        except:
            pass
        time.sleep(0.1)
        self.http = HttpData("http://127.0.0.1:5000/")
        self.http.sendRequest("ouvrir")
        self.ecrire(1,0.0,2,0.0)

    def fermer(self):
        self.http.initData()
        self.http.sendRequest("fermer")
        self.http.initData()
        self.http.sendRequest("terminate")

    def config_entrees(self,voies,calibres,diff=[]):
        self.http.initData()
        self.http.writeInt8(len(voies))
        for v in voies:
            self.http.writeInt8(v)
        self.http.writeInt8(len(calibres))
        for c in calibres:
            self.http.writeFloat(c)
        self.http.writeInt8(len(diff))
        for d in diff:
            self.http.writeInt8(d)
        self.http.sendRequest("config_entrees")

    def activer_lecture(self,voies):
        self.http.initData()
        self.http.writeInt8(len(voies))
        for v in voies:
            self.http.writeInt8(v)
        self.http.writeInt8(0)
        self.http.sendRequest("activer_lecture")

    def desactiver_lecture(self):
        self.http.sendRequest("desactiver_lecture")

    def config_echantillon(self,techant,nbpoints):
        self.http.initData()
        self.http.writeDouble(techant)
        self.http.writeInt32(nbpoints,signed=False)
        self.http.sendRequest("config_echantillon")

    def config_echantillon_permanent(self,techant,nbpoints):
        self.http.initData()
        self.http.writeDouble(techant)
        self.http.writeInt32(nbpoints,signed=False)
        self.http.sendRequest("config_echantillon_permanent")

    def config_trigger(self,voie,seuil,montant=1,pretrigger=1,pretriggerSouple=0,hysteresis=0):
        self.http.initData()
        self.http.writeInt8(0)
        self.http.writeInt8(voie)
        self.http.writeDouble(seuil)
        self.http.writeInt8(montant)
        self.http.writeInt32(pretrigger)
        self.http.writeInt8(pretriggerSouple)
        self.http.writeInt32(hysteresis,signed=False)
        self.http.sendRequest("config_trigger")

    
    def config_trigger_externe(self,pretrigger=1,pretriggerSouple=0):
        self.http.initData()
        self.http.writeInt8(1)
        self.http.writeInt8(0)
        self.http.writeDouble(0)
        self.http.writeInt8(1)
        self.http.writeInt32(pretrigger,signed=False)
        self.http.writeInt8(pretriggerSouple)
        self.http.writeInt32(0)
        self.http.sendRequest("config_trigger")

    def config_quantification(self,quantification):
        self.http.initData()
        self.http.writeInt8(quantification)
        self.http.sendRequest("config_quantification")


    def envoyer_signal(self,nsortie,valeurs):
        self.http.initData()
        N = len(valeurs)
        self.http.writeInt8(nsortie)
        self.http.writeInt32(N,signed=False)
        self.http.sendRequest("config_longueur_signal")
        i = 0
        size = 1000
        while i < N:
            self.http.initData()
            self.http.writeInt8(nsortie)
            i2 = min(i+size,N)
            self.http.writeInt32(i2-i)
            self.http.writeDoubleArray(valeurs[i:i2])
            i += size
            self.http.sendRequest("ajout_signal")
        
        

    def config_sortie(self,nsortie,techant,valeurs,repetition=0):
        self.envoyer_signal(nsortie,valeurs)
        self.http.initData()
        self.http.writeInt32(len(valeurs),signed=False)
        self.http.writeInt32(0,signed=False)
        self.http.sendRequest("config_longueur_signal")
        self.http.initData()
        self.http.writeInt8(nsortie)
        self.http.writeDouble(techant)
        self.http.writeInt8(repetition,signed=True)
        self.http.sendRequest("config_sortie")
        

    def acquerir(self):
        self.http.initData()
        self.http.sendRequest("acquerir")

    def acquerir_permanent(self):
        self.http.initData()
        self.http.sendRequest("acquerir_permanent")

    def lancer(self):
        self.http.initData()
        self.http.sendRequest("lancer")

    def lancer_permanent(self,repetition):
        self.http.initData()
        self.http.writeInt8(repetition)
        self.http.sendRequest("lancer_permanent")

    def acquerir_avec_sorties(self,valeurs1,valeurs2):
        self.envoyer_signal(1,valeurs1)
        self.envoyer_signal(2,valeurs2)
        self.http.initData()
        self.http.sendRequest("acquerir_avec_sorties")

    def lancer_avec_sorties(self,valeurs1,valeurs2):
        self.envoyer_signal(1,valeurs1)
        self.envoyer_signal(2,valeurs2)
        self.http.initData()
        self.http.sendRequest("lancer_avec_sorties")

    def stopper_acquisition(self):
        self.http.initData()
        self.http.sendRequest("stopper_acquisition")
    

    def entrees(self,reduction=1):
        self.http.initData()
        self.http.writeInt32(reduction,signed=False)
        self.http.sendRequest("entrees")
        nombreEA = self.http.readInt8(signed=False)
        nbpoints = self.http.readInt32(signed=False)
        tensions = np.zeros((nombreEA,nbpoints),dtype=np.float64)
        for v in range(nombreEA):
            tensions[v] = self.http.readDoubleNdArray(nbpoints)
        return tensions

    def entrees_filtrees(self,reduction=1):
        self.http.initData()
        self.http.writeInt32(reduction,signed=False)
        self.http.sendRequest("entrees_filtrees")
        nombreEA = self.http.readInt8(signed=False)
        nbpoints = self.http.readInt32(signed=False)
        tensions = np.zeros((nombreEA,nbpoints),dtype=np.float64)
        for v in range(nombreEA):
            tensions[v] = self.http.readDoubleNdArray(nbpoints)
        return tensions

    def temps(self,reduction=1):
        self.http.initData()
        self.http.writeInt32(reduction,signed=False)
        self.http.sendRequest("temps")
        nombreEA = self.http.readInt8(signed=False)
        nbpoints = self.http.readInt32(signed=False)
        temps = np.zeros((nombreEA,nbpoints),dtype=np.float64)
        for v in range(nombreEA):
            temps[v] = self.http.readDoubleNdArray(nbpoints)
        return temps

    def paquet(self,premier,reduction=1):
        self.http.initData()
        if premier>=0:
            self.http.writeInt32(premier,signed=False)
            self.http.writeInt32(reduction,signed=False)
            self.http.sendRequest("paquet")
        else:
            self.http.writeInt32(reduction,signed=False)
            self.http.sendRequest("paquet_circulaire")
        
        nombreEA = self.http.readInt8(signed=False)
        nbpoints = self.http.readInt32(signed=False)
        paquet = np.zeros((nombreEA*3,nbpoints),dtype=np.float64)
        for v in range(nombreEA*3):
            paquet[v] = self.http.readDoubleNdArray(nbpoints)
        return paquet

    def paquet_filtrees(self,premier,reduction=1):
        self.http.initData()
        if premier>=0:
            self.http.writeInt32(premier,signed=False)
            self.http.writeInt32(reduction,signed=False)
            self.http.sendRequest("paquet_filtrees")
        else:
            self.http.writeInt32(reduction,signed=False)
            self.http.sendRequest("paquet_circulaire_filtrees")
        
        nombreEA = self.http.readInt8(signed=False)
        nbpoints = self.http.readInt32(signed=False)
        paquet = np.zeros((nombreEA*2,nbpoints),dtype=np.float64)
        for v in range(nombreEA*2):
            paquet[v] = self.http.readDoubleNdArray(nbpoints)
        return paquet

    def lire(self):
        self.http.initData()
        self.http.sendRequest("lire")
        nombreEA = self.http.readInt8(signed=False)
        return self.http.readDoubleNdArray(nombreEA)
        
        

    def declencher_sorties(self,ns1,ns2):
        self.http.initData()
        self.http.writeInt8(ns1)
        self.http.writeInt8(ns2)
        self.http.sendRequest("declencher_sorties")

    def stopper_sorties(self,ns1,ns2):
        self.http.initData()
        self.http.writeInt8(ns1)
        self.http.writeInt8(ns2)
        self.http.sendRequest("stopper_sorties")

    def ecrire(self,ns1,valeur1,ns2,valeur2):
        self.http.initData()
        self.http.writeInt8(ns1)
        self.http.writeDouble(valeur1)
        self.http.writeInt8(ns2)
        self.http.writeDouble(valeur2)
        self.http.sendRequest("ecrire")

    def config_filtre(self,listeA,listeB):
        self.envoyer_signal(1,np.array(listeA,dtype=np.float64))
        self.envoyer_signal(2,np.array(listeB,dtype=np.float64))
        self.http.initData()
        self.http.sendRequest("config_filtre")

    def portB_config(self,bits,etat):
        self.http.initData()
        self.http.writeInt8(bits)
        self.http.writeInt8(etat)
        self.http.sendRequest("portB_config")

    def portC_config(self,bits,etat):
        self.http.initData()
        self.http.writeInt8(bits)
        self.http.writeInt8(etat)
        self.http.sendRequest("portC_config")

    def portB_ecrire(self,bit,etat):
        self.http.initData()
        self.http.writeInt8(bit)
        self.http.writeInt8(etat)
        self.http.sendRequest("portB_ecrire")

    def portC_ecrire(self,bit,etat):
        self.http.initData()
        self.http.writeInt8(bit)
        self.http.writeInt8(etat)
        self.http.sendRequest("portC_ecrire")

    def portB_lire(self,bit):
        self.http.initData()
        self.http.writeInt8(bit)
        self.http.sendRequest("portB_lire")
        return self.http.readInt8(signed=False)

    def portC_lire(self,bit):
        self.http.initData()
        self.http.writeInt8(bit)
        self.http.sendRequest("portC_lire")
        return self.http.readInt8(signed=False)

    def config_compteur(self,entree,front_montant,front_descend,hysteresis,duree):
        self.http.initData()
        self.http.writeInt8(entree)
        self.http.writeInt8(front_montant)
        self.http.writeInt8(front_descend)
        self.http.writeDouble(hysteresis)
        self.http.writeDouble(duree)
        self.http.sendRequest("config_compteur")

    def compteur(self):
        self.http.initData()
        self.http.sendRequest("compteur")

    def lire_compteur(self):
        self.http.initData()
        self.http.sendRequest("lire_compteur")
        high = self.http.readInt32(signed=False)
        low = self.http.readInt32(signed=False)
        return np.uint64(np.left_shift(high,32)+low)

    def config_chrono(self,entree,front_montant,front_descend,hysteresis):
        self.http.initData()
        self.http.writeInt8(entree)
        self.http.writeInt8(front_montant)
        self.http.writeInt8(front_descend)
        self.http.writeDouble(hysteresis)
        self.http.sendRequest("config_chrono")

    def chrono(self):
        self.http.initData()
        self.http.sendRequest("chrono")

    def lire_chrono(self):
        self.http.initData()
        self.http.sendRequest("lire_chrono")
        high = self.http.readInt32(signed=False)
        low = self.http.readInt32(signed=False)
        return np.uint64(np.left_shift(high,32)+low)

def test1():
    sys = Sysam()
    sys.config_entrees([0,1],[10,10])
    sys.config_echantillon(10,10000)
    #sys.config_trigger(0,1.0)
    sys.config_quantification(12)
    sys.acquerir()
    u = sys.entrees()
    t = sys.temps()
    print(len(u[0]))
    plt.figure()
    plt.plot(t[0],u[0])
    plt.plot(t[1],u[1])
    plt.grid()
    plt.show()
    sys.fermer()

def test2():
    sys = Sysam()
    sys.config_entrees([0,1],[10,10])
    sys.config_echantillon(100,20000)
    x = np.linspace(0,10,20000)
    s1 = 3.0*np.sin(2*np.pi*x)
    s2 = 2.0*np.sin(2*np.pi*x+np.pi/2)
    sys.acquerir_avec_sorties(s1,s2)
    u = sys.entrees()
    t = sys.temps()
    plt.figure()
    plt.plot(t[0],u[0])
    plt.plot(t[1],u[1])
    plt.grid()
    plt.show()
    sys.fermer()

def test3():
    sys = Sysam()
    x = np.linspace(0,1,50000)
    s1 = 3.0*np.sin(2*np.pi*x)
    s2 = 2.0*np.sin(2*np.pi*x+np.pi/2)
    te = 10
    sys.config_sortie(1,te,s1,-1)
    sys.config_sortie(2,te,s2,-1)
    sys.declencher_sorties(1,1)
    plt.figure()
    plt.plot(s1)
    plt.grid()
    plt.show()
    sys.stopper_sorties(1,1)
    sys.fermer()

def test4():
    sys = Sysam()
    sys.config_entrees([0,1],[10,10])
    sys.config_echantillon(100,10000)
    x = np.linspace(0,10,10000)
    s1 = 3.0*np.sin(2*np.pi*x)
    s2 = 2.0*np.sin(2*np.pi*x+np.pi/2)
    sys.config_filtre([1,0],[0.5])
    sys.lancer_avec_sorties(s1,s2)
    premier = 0
    for i in range(10):
        time.sleep(0.1)
        paquet = sys.paquet(premier)
        premier = len(paquet[0])
        print(paquet.shape)
    paquet = sys.paquet(0)
    print(paquet.shape)
    t0 = paquet[0]
    t1 = paquet[1]
    u0 = paquet[2]
    u1 = paquet[3]
    uf0 = paquet[4]
    uf1 = paquet[5]
    plt.figure()
    plt.plot(t0,u0,"r-")
    plt.plot(t1,u1,"b-")
    plt.plot(t0,uf0,"r--")
    plt.plot(t1,uf1,"b--")
    plt.grid()
    plt.show()
    sys.fermer()

def test5():
    sys = Sysam()
    sys.config_entrees([0,1],[10,10])
    sys.config_echantillon_permanent(10,1000000)
    sys.acquerir_permanent()
    u = sys.entrees()
    t = sys.temps()
    print(len(u[0]))
    plt.figure()
    plt.plot(t[0],u[0])
    plt.plot(t[1],u[1])
    plt.grid()
    plt.show()
    sys.fermer()

def test6():
    sys = Sysam()
    sys.config_entrees([0,1],[10,10])
    sys.config_echantillon_permanent(10,1000000)
    sys.lancer_permanent(0)
    premier = 0
    for i in range(10):
        time.sleep(1)
        paquet = sys.paquet(premier)
        premier = len(paquet[0])
        print(paquet.shape)
    paquet = sys.paquet(0)
    print(paquet.shape)
    t0 = paquet[0]
    t1 = paquet[1]
    u0 = paquet[2]
    u1 = paquet[3]
    uf0 = paquet[4]
    uf1 = paquet[5]
    plt.figure()
    plt.plot(t0,u0,"r-")
    plt.plot(t1,u1,"b-")
    plt.plot(t0,uf0,"r--")
    plt.plot(t1,uf1,"b--")
    plt.grid()
    plt.show()
    sys.fermer()

def test7():
    sys = Sysam()
    sys.config_entrees([0,1],[10,10])
    fe = 10000
    te = 1.0/fe
    sys.config_echantillon(te*1e6,10000)
    fc = fe/2*0.8 # fréquence de coupure
    b = scipy.signal.firwin(numtaps=40,cutoff=[fc/fe],fs=1,window='hann')
    sys.config_filtre([1],b)
    sys.acquerir()
    u = sys.entrees_filtrees()
    t = sys.temps()
    print(len(u[0]))
    plt.figure()
    plt.plot(t[0],u[0])
    plt.plot(t[1],u[1])
    plt.grid()
    plt.show()
    sys.fermer()
    
def test8():
    sys = Sysam()
    sys.config_entrees([0,1],[10.0,10.0])
    sys.activer_lecture([0,1])
    for k in range(10):
        print(sys.lire())
    sys.desactiver_lecture()
    sys.fermer()

def test9():
    sys = Sysam()
    sys.portB_config(0,0)
    for b in range(4):
        print(sys.portB_lire(b))
    sys.portB_config(0,1)
    sys.portB_ecrire(0,1)
    sys.fermer()

def test10():
    sys = Sysam()
    sys.config_compteur(ENTREE_CHRONO,0,1,100,1000000)
    # le comptage des fronts montants donne un résultat faux.
    sys.compteur()
    print(sys.lire_compteur())
    sys.fermer()

def test11():
    sys = Sysam()
    sys.config_chrono(ENTREE_CHRONO,1,0,100)
    sys.chrono()
    print(sys.lire_chrono())
    sys.fermer()

#test1()
