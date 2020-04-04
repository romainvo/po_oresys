# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 23:45:40 2020

@author: romain
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle
from po_oresys.api.comparateur import Comparateur

if __name__ == '__main__':
    
    analyse_discriminante = True
    
    analyse_meilleurs_scores = False
    
#------------------------------------------------------------------------------# 
#------------------------ INITIALISATION DU COMPARATEUR -----------------------# 
#------------------------------------------------------------------------------# 
    
    with open('po_oresys/resources/surfhab_tokens.pickle', 'rb') as fileIn:
        surfhab_tokens = pickle.load(fileIn)

    with open('po_oresys/resources/etage_tokens.pickle', 'rb') as fileIn:
        etage_tokens = pickle.load(fileIn)

    with open('po_oresys/resources/nbpiece_tokens.pickle', 'rb') as fileIn:
        nbpiece_tokens = pickle.load(fileIn)       

    comparateur = Comparateur(surfhab_tokens=surfhab_tokens,
                              etage_tokens=etage_tokens, 
                              nbpiece_tokens=nbpiece_tokens)
        
    surfhab_scoring = comparateur.calculer_surfhab_scoring()
    etage_scoring = comparateur.calculer_etage_scoring()
    nbpiece_scoring = comparateur.calculer_nbpiece_scoring()  
    
    scoring = {'surfhab':surfhab_scoring, 
               'etage':etage_scoring, 
               'nbpiece':nbpiece_scoring}
    
#------------------------------------------------------------------------------# 
#------ EVALUATION DU CARACTERE DISCRIMINANT DE CHAQUE LEVIER DE DECISION -----# 
#------------------------------------------------------------------------------# 

    if analyse_discriminante:
        
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update({'font.size':12})
#        plt.rcParams["figure.figsize"] = (50,40)
        fig, ax = plt.subplots(nrows=3, sharex=True, sharey=True)
#        fig.tight_layout()
        title = """Distributions cumulées inversées du pourcentage de logements sociaux autour 
        de chaque annonce airbnb ayant un match exact selon chaque levier de suspicion"""
        fig.suptitle(title)
        plt.xlabel("Pourcentage de logements sociaux avec un match exact selon le levier de détection")
        fig.text(0.05,0.5, "Somme cumulée du nombre d'annonces airbnb concernées",
                 ha="center", va="center", rotation=90)
        color_palette = sns.color_palette("muted")
     
        for idx,levier in enumerate({'surfhab','etage','nbpiece'}):
            if levier != 'surfhab':
                sns.distplot((scoring[levier] == 1)
                    .sum(axis=1)
                        .divide((~comparateur.croisement.isna()).sum(axis=1))
                            , bins=150
                            , kde=False
                            , hist_kws={'cumulative':-1, 'alpha':0.5,
                                        'edgecolor':'w'}
                            , ax=ax[idx]
                            , label=levier
                            , color=color_palette[idx])
            else:
                sns.distplot((scoring[levier] >= 0.95)
                    .sum(axis=1)
                        .divide((~comparateur.croisement.isna()).sum(axis=1))
                            , bins=150
                            , kde=False
                            , hist_kws={'cumulative':-1, 'alpha':0.5,
                                        'edgecolor':'w'}
                            , ax=ax[idx]
                            , label=levier
                            , color=color_palette[idx])
                
            ax[idx].legend()
    
#------------------------------------------------------------------------------# 
#-------------- AFFICHAGE DE LA DISTRIBUTION DES MEILLEURS SCORES -------------# 
#------------------------------------------------------------------------------# 

    if analyse_meilleurs_scores:
            
        rename_col= dict()
        column_score_max = dict()
        score_max = dict()
        best_match = dict()
        tranche_score = dict()
        tranche_index = dict()
        tranche_nombre = dict()
       
        for levier in {'surfhab','etage','nbpiece'}:
            rename_col[levier] \
            = {'{}_{}'.format(levier, i) : 
                i for i in range(comparateur.croisement.shape[1])} 
            
            scoring[levier].rename(columns=rename_col[levier], 
                                   inplace=True)
            
            column_score_max[levier] = scoring[levier].idxmax(axis=1).values
            score_max[levier] = scoring[levier].max(axis=1).values
            
            best_match[levier] = -1 * np.ones((comparateur.croisement.shape[0],2))
            for idx in range(comparateur.croisement.shape[0]):
                if not pd.isna(column_score_max[levier][idx]):
                    best_match[levier][idx,0] \
                    = comparateur.croisement.iloc[
                            idx, 
                            int(column_score_max[levier][idx])]
                    
                    best_match[levier][idx,1] = score_max[levier][idx]
                    
            best_match[levier] = pd.DataFrame(best_match[levier])
            
            best_match[levier].index.rename('id_bnb', inplace=True)
            best_match[levier].rename(columns={0:'id_rpls', 1:'score'}, 
                                      inplace=True)
            best_match[levier] = best_match[levier].astype({'id_rpls':'int64'})        
    
    #    best_match.replace(to_replace={'score':-1.0}, value={'score':0.0}
    #    , inplace=True)
    
        plt.style.use('seaborn-darkgrid')
        plt.rcParams.update({'font.size':7.5})
        fig_d, ax_d = plt.subplots(nrows=3)
            
        tranche_score \
        = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
        
        tranche_index['etage'] = ["no detection", "0%", "20%", "100%"]
        tranche_index['nbpiece'] = ["no detection", "0%", "20%", "50%", "100%"]
    
        for idx,levier in enumerate({'surfhab','etage','nbpiece'}):
        
            if levier == 'surfhab':
                n = best_match[levier].shape[0]
                somme_cumulee = 0
                for i, tranche in enumerate(tranche_score):
                    if tranche == 100:
                        break
                    elif i == (len(tranche_score) - 2):
                        nb_temp \
                        = best_match[levier].loc[
                                (best_match[levier].score >= tranche/100)
                                & 
                                (best_match[levier].score <= tranche_score[i+1]/100)
                                ].shape[0]
                        
                        somme_cumulee += nb_temp  
                        
                    else:            
                        nb_temp \
                        = best_match[levier].loc[
                                (best_match[levier].score >= tranche/100)
                                & 
                                (best_match[levier].score < tranche_score[i+1]/100)
                                ].shape[0]
                        
                        somme_cumulee += nb_temp
                    
                    if i == 0:
                        tranche_nombre[levier] = [nb_temp]
                        tranche_index[levier] \
                        = ["{}% - {}%".format(tranche, tranche_score[i+1])]
                    else:
                        tranche_nombre[levier].append(nb_temp)
                        tranche_index[levier].append("{}% - {}%".format(
                                tranche, tranche_score[i+1]))
                        
                    print("Détections avec une suspicion entre {}% et {}% : {} -- somme cumulée : {}"
                          .format(tranche, 
                                  tranche_score[i+1], 
                                  nb_temp, 
                                  somme_cumulee/n))
                
                tranche_index[levier][0] = "no detection"
            
            elif levier == 'etage':                   
                tranche_nombre[levier] = [0]
                tranche_nombre[levier].append((best_match[levier].score == 0).sum())
                tranche_nombre[levier].append((best_match[levier].score == 0.2).sum())
                tranche_nombre[levier].append((best_match[levier].score == 1).sum())
                tranche_nombre[levier][0] \
                = best_match[levier].shape[0] - np.sum(tranche_nombre[levier][1:])    
               
            else:
                tranche_nombre[levier] = [0]
                tranche_nombre[levier].append((best_match[levier].score == 0).sum())
                tranche_nombre[levier].append((best_match[levier].score == 0.5).sum())
                tranche_nombre[levier].append((best_match[levier].score == 0.2).sum())
                tranche_nombre[levier].append((best_match[levier].score == 1).sum())
                tranche_nombre[levier][0] \
                = best_match[levier].shape[0] - np.sum(tranche_nombre[levier][1:])    
                 
                
            ax_d[idx].set_title("Distribution des scores - {}".format(levier))
            sns.barplot(y=tranche_nombre[levier], x=tranche_index[levier]
                        , orient='v', ax=ax_d[idx], edgecolor='white')