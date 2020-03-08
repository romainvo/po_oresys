import numpy as np
import pandas as pd
import re
from nlp_surfhab import extraction_surfhab, score_surfhab
from nlp_etage import extraction_etage, score_etage

def import_data_rpls():

    def converter_codepostal(string):
        try:
            return int(string)
        except:
            return 0   
        
    def converter_etage(string):
        try: 
            return float(string)
        except:
            if string == 'RC':
                return 0.0
            
            match_temp = re.search(r"[1-9][0-9]*", string)
            if match_temp != None:
                return float(match_temp.group())
            else:
                return np.nan
            
    data_rpls = pd.read_csv("csv/paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                    header='infer', index_col=0,
                    converters={'codepostal':converter_codepostal
                                , 'etage':converter_etage},
                    dtype={'longitude':'float', 'latitude':'float'})
    
    data_rpls.index.rename('id_rpls', inplace=True)

    return data_rpls

def import_data_airbnb():
    
    data_airbnb = pd.read_csv("csv/airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
    
    data_airbnb.index.rename('id_bnb', inplace=True)

    return data_airbnb

def score_total(weights, croisement, surfhab=None
                , etage=None, pieces=None):
    
    score = (~croisement.isna()).values * weights['croisement']
    
    if surfhab is not None:
        score += surfhab.fillna(0).values * weights['surfhab']
        
    if etage is not None:
        score += etage.fillna(0).values * weights['etage']

    if pieces is not None:
        score += pieces.fillna(0).values * weights['pieces']

    score = pd.DataFrame(score)
    score.index.rename('id_bnb', inplace=True)

    return score

def print_result(id_bnb, id_rpls, data_airbnb, etage=None
                 , surfhab=None, pieces=None):
    print(data_airbnb.loc[id_bnb, 'name']
        ,"\n"
        ,data_airbnb.loc[id_bnb, 'space']
        ,"\n"
        ,data_airbnb.loc[id_bnb, 'description']
        ,"\n"
        ,data_airbnb.loc[id_bnb, 'summary']
        ,"\n"
        ,"\n"
        ,data_airbnb.loc[id_bnb, 'longitude']
        ,"\n"
        ,data_airbnb.loc[id_bnb, 'latitude']
        )
    print()
    if etage is not None and id_bnb in etage:
        print("Detection etage : {}".format(etage[id_bnb]))
    if surfhab is not None and id_bnb in surfhab:
        print("Detection surface habitable : {}".format(surfhab[id_bnb]))
    if pieces is not None and id_bnb in pieces:
        print("Detection nombre de pièces: {}".format(pieces[id_bnb]))
    print()
    print(data_rpls.loc[id_rpls
                        , ['numvoie','typvoie','nomvoie','surfhab'
                           , 'etage','nbpiece','longitude','latitude']])    

def extract_best_match(scores, croisement):
    
    #On récupère le numéro des colonnes avec le score maximal
    column_score_max = scores.idxmax(axis=1).values
    score_max = scores.max(axis=1).values
    
    best_match = -1 * np.ones((croisement_v3.shape[0],2)) 
    for idx in range(croisement_v3.shape[0]):
        if not pd.isna(croisement_v3.iloc[idx, column_score_max[idx]]):
            best_match[idx,0] = croisement_v3.iloc[idx, column_score_max[idx]]
            best_match[idx,1] = score_max[idx]
            
    best_match = pd.DataFrame(best_match)
    
    best_match.index.rename('id_bnb', inplace=True)
    best_match.rename(columns={0:'id_rpls', 1:'score'}, inplace=True)
    best_match = best_match.astype({'id_rpls':'int64'})

    best_match.replace(to_replace={'score':-1.0}, value={'score':0.0}
    , inplace=True)

    return best_match    

if __name__ == '__main__':

    data_rpls = import_data_rpls()
    
    data_airbnb = import_data_airbnb()
    
    keep_columns = ['id_bnb']
    for i in range(250):
        keep_columns.append('id_rpls{}'.format(i))
#    dtype = {key:'int64' for key in keep_columns}
    
    croisement_v3 = pd.read_csv('csv/results_rd155_nb250.csv', header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype())    
    
    etage_tokens = extraction_etage(data_airbnb)
    etage_scoring = score_etage(data_airbnb, croisement_v3, etage_tokens)    
        
    surfhab_tokens = extraction_surfhab(data_airbnb)
    surfhab_scoring = score_surfhab(data_airbnb, croisement_v3, surfhab_tokens)
    
    # --------------------------- SCORE TOTAL ------------------------------- #
    
    weights = {'croisement':0.2, 'surfhab':0.4, 'etage':0.4}
    scores = score_total(weights, croisement=croisement_v3
                         , surfhab=surfhab_scoring, etage=etage_scoring)
    
    best_match = extract_best_match(scores, croisement_v3)
    
    # ---------------------- AFFICHER LES RÉSULTATS ------------------------- #

    print(best_match)
    print_result(0, 84622, data_airbnb, surfhab=surfhab_tokens
                 , etage=etage_tokens)

    # ----------------------- EVALUER LE SCORING ---------------------------- #

    #Nombre de airbnb avec 0 rpls dans le rayon d'anonymisation de 150m
    #((~croisement_v3.isna()).sum(axis=1) == 0).sum()
    #Statistique nombre de croisements : 
    #(~croisement_v3.isna()).sum(axis=1).describe()

    tranche_score = [0,5,10,15,20,22.5,25,30,40,50,60,62.5,65,70,75,80,90,95
                     ,97.5,100]
    tranche_index = []
    tranche_nombre = []
    
    somme_cumulee = 0
    for i, tranche in enumerate(tranche_score):
        if tranche == 100:
            break
        elif i == (len(tranche_score) - 2):
            nb_temp = best_match.loc[(best_match.score >= tranche/100)
                    & (best_match.score <= tranche_score[i+1]/100)].shape[0]
            
            somme_cumulee += nb_temp           
        else:            
            nb_temp = best_match.loc[(best_match.score >= tranche/100)
                        & (best_match.score < tranche_score[i+1]/100)].shape[0]
            
            somme_cumulee += nb_temp
        
        tranche_nombre.append(nb_temp)
        tranche_index.append("{}% - {}%".format(tranche, tranche_score[i+1]))
        print("Détections avec une suspicion entre {}% et {}% : {} -- somme cumulée : {}"
              .format(tranche, tranche_score[i+1], nb_temp, somme_cumulee))
      
    print("\n","Moyenne des score : {}".format(best_match.score.mean()))
    print("Ecart-type : {}".format(best_match.score.std()))
    print("On affiche les différents déciles", "\n")          
    for i in [0,5,10,15,40,50,60,80,82.5,85,87.5,90,95,97.5,100]:
        print("Quantile {}% : {}".format(i, best_match.score.quantile(i/100)))           


    tranche_index[0] = "no detection"
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.style.use('seaborn-darkgrid')
#    plt.rcParams.update({'font.size':35})
#    plt.rcParams["figure.figsize"] = (50,40)
    
    fig, ax = plt.subplots()
    ax.set_title("Nombre de suspicions par tranche de score")
    sns.barplot(y=tranche_nombre, x=tranche_index
                , orient='v', ax=ax, edgecolor='white')          