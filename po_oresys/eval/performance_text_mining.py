# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 09:48:02 2020

@author: romain
"""

#import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
import numpy as np
import po_oresys.api.data_loader as data_loader
import po_oresys.api.decorators

if __name__ == '__main__':

    data_airbnb = data_loader.import_data_airbnb()
    
    analyse_surfhab = True
    analyse_etage = True
    analyse_nbpiece = True
        
#---------- Évaluation des performances des algorithme de détection -----------# 

    if analyse_surfhab:
        print("Nombre de détection - {} : {}".format(
            'surfhab', len(data_airbnb.bnb.extraire_surfhab(data_airbnb.index))))
        print()
    
    if analyse_etage:
        print("Nombre de détection - {} : {}".format(
            'etage', len(data_airbnb.bnb.extraire_etage(data_airbnb.index))))
        print()
        
    if analyse_nbpiece:
        print("Nombre de détection - {} : {}".format(
            'nbpiece', len(data_airbnb.bnb.extraire_nbpiece(data_airbnb.index))))
        print() 
        
    for i in range(110):
        
        j = np.random.randint(250,60000)
        
        print()
        print("id_airbnb : {}".format(j))
        data_airbnb.bnb.complete_description(j)
        data_airbnb.bnb.all_extractions(j, pprint=True, rreturn=False)
        print("---------------------------------------------------------------")
        
        if i == 2:
            break
    
