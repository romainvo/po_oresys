# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 09:48:02 2020

@author: romain
"""

import numpy as np
import po_oresys.api.data_loader as data_loader
import po_oresys.api.decorators
import sys, getopt

def main(argv):
    
    surfhab = False
    etage = False
    nbpiece = False
    
    try:
        opts, args = getopt.getopt(argv,"hs:e:nb:",["surfhab=","etage=","nbpiece"])
    except getopt.GetoptError:
        print('-m po_oresys.performance_text_mining -s <True/False> -e <True/False> -nb <True/False>')
        sys.exit(2)
    for opt, arg in opts:
       
        if opt == '-h':
            print('-m po_oresys.performance_text_mining -s <True/False> -e <True/False> -nb <True/False>')
            sys.exit()
        elif opt in ("-s", "--surfhab"):
            surfhab = arg == 'True'
           
        elif opt in ("-e", "--etage"):
            etage = arg == 'True'
            
        elif opt in ("-nb", "--nbpiece"):
            nbpiece = arg == 'True'
    
    print()
    print("Calcul du nombre de détection sur les champs suivants : \n",
          " - surfhab : {} \n".format(surfhab),
          " - etage : {} \n".format(etage),
          " - nbpiece : {} \n".format(nbpiece))         
        
    return surfhab, etage, nbpiece

def run():
    
    analyse_surfhab, analyse_etage, analyse_nbpiece = main(sys.argv[1:])
    
    data_airbnb = data_loader.import_data_airbnb()
        
#---------- Évaluation des performances des algorithme de détection -----------# 

    print()
    print("---------------------------------------------------------------")
    print()

    if analyse_surfhab:
        print("Nombre de détection - {} : {}".format(
            'surfhab', len(data_airbnb.bnb.extraire_surfhab(data_airbnb.index))))
        
    if analyse_etage:
        print("Nombre de détection - {} : {}".format(
            'etage', len(data_airbnb.bnb.extraire_etage(data_airbnb.index))))
        
    if analyse_nbpiece:
        print("Nombre de détection - {} : {}".format(
            'nbpiece', len(data_airbnb.bnb.extraire_nbpiece(data_airbnb.index))))

    print()
    print("---------------------------------------------------------------")    
    print("Vérification manuel des performances des algorithmes de text mining :")
    print("---------------------------------------------------------------")    
    print()
    
    for i in range(110):
        
        j = np.random.randint(250,60000)
        
        print("id_airbnb : {}".format(j))
        data_airbnb.bnb.complete_description(j)
        data_airbnb.bnb.all_extractions(j, pprint=True, rreturn=False)
        print()
        print("---------------------------------------------------------------")
        
        inpt = input("Press enter to continue or q to quit... \n")
        if inpt == 'q':
            sys.exit(1)
            
if __name__ == '__main__':
    run()
    
    
