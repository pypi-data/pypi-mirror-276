INSTALLED = True

import requests
import struct
import numpy as np

if INSTALLED:
    from pycanum.httpdata import HttpData
else:
    from httpdata import HttpData

import time
import os
import subprocess


if INSTALLED:
    PATH = os.path.dirname(__file__)+"\\"
else:
    PATH = "../build/Debug/"

ENTREE_CHRONO = 16
SIGNAL_MAX_SIZE = 200000


class Sysam:
    def __init__(self,nom='SP5'):
        os.system('start /B '+PATH+'sysamhttp.exe "http://127.0.0.1:5000/"')
        time.sleep(0.1)
        self.http = HttpData("http://127.0.0.1:5000/")
        self.http.sendRequest("ouvrir")
        self.ecrire(1,0.0,2,0.0)

    def fermer(self):
        self.http.initData()
        self.http.sendRequest("fermer")
        self.http.initData()
        self.http.sendRequest("terminate")

    def afficher_calibrage(self):
        self.http.initData()
        self.http.sendRequest("afficher_calibrage")

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
        if len(valeurs) > SIGNAL_MAX_SIZE:
            valeurs = valeurs[0:SIGNAL_MAX_SIZE]
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

    def lancer_permanent(self,repetition=0):
        self.http.initData()
        self.http.writeInt8(repetition)
        self.http.sendRequest("lancer_permanent")

    def acquerir_avec_sorties(self,valeurs1,valeurs2):
        if type(valeurs1)!=np.ndarray:
            valeurs1 = np.zeros(0)
        if type(valeurs2)!=np.ndarray:
            valeurs2 = np.zeros(0)
        self.envoyer_signal(1,valeurs1)
        self.envoyer_signal(2,valeurs2)
        self.http.initData()
        self.http.sendRequest("acquerir_avec_sorties")

    def lancer_avec_sorties(self,valeurs1,valeurs2):
        if type(valeurs1)!=np.ndarray:
            valeurs1 = np.zeros(0)
        if type(valeurs2)!=np.ndarray:
            valeurs2 = np.zeros(0)
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

    def nombre_echant(self):
        self.http.initData()
        self.http.sendRequest("nombre_echant")
        nbpoints = self.http.readInt32(signed=False)
        return nbpoints

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

