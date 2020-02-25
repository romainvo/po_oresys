import numpy as np
import pandas as pd
import re

""" surface et nombre de piece réel issu du repertoire RPLS, Théorique issu de l'extraction d'information

def CalculScore(surfaceTheo, surfaceReel, nbpieceTheo, nbpieceReel):
    score = ((np.minimum(surfaceTheo/surfaceReel,surfaceReel/surfaceTheo)*np.minimum(surfaceReel/surfaceTheo,surfaceTheo/surfaceReel))/1.25)*100
    on impose un score minimum de 0.25 du fait de la proximité, les 0.75 restants etant calculés via la formule précédente
    score = 25+score
"""

def calculScore(scoreSurface,scoreNbPiece, scoreEtage):
    PoidsEtage=0.25
    PoidsProximite = 0.25
    PoidsSurface = 0.25
    PoidsNbPiece = 1-PoidsEtage-PoidsSurface-PoidsProximite

    """ score total borné entre 0 et 100. Si il est dans la zone de proximite, il est d'office egal à PoidsProximite*100"""
    scoreTotal=(PoidsProximite+PoidsEtage*scoreEtage+PoidsSurface*scoreSurface+PoidsNbPiece*scoreNbPiece)*100

def converter_cp(string):
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

from nlp_surfhab import extraction_surfhab, score_surfhab
from nlp_etage import extraction_etage, score_etage

if __name__ == '__main__':

    data_rpls = pd.read_csv("paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                        header='infer', index_col=0,
                        converters={'codepostal':converter_cp
                                    , 'etage':converter_etage},
                        dtype={'longitude':'float', 'latitude':'float'})
    
    keep_columns = ['id_bnb']
    for i in range(100):
        keep_columns.append('id_rpls{}'.format(i))
#    dtype = {key:'int64' for key in keep_columns}
    
    croisement_v3 = pd.read_csv('results_rd150_nb100_score.csv', header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype())    
    
    data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                              dtype={'longitude':'float', 'latitude':'float'})
    
    etage_tokens = extraction_etage(data_airbnb)

    etage_scoring = score_etage(data_airbnb, croisement_v3, etage_tokens)    
    
    #Score total
    
    surfhab_tokens = extraction_surfhab(data_airbnb)
    surfhab_scoring = score_surfhab(data_airbnb, croisement_v3, surfhab_tokens)
    
    score_total = pd.DataFrame(croisement_v3.isna().values*0.2 + 
                               surfhab_scoring.fillna(0).values * 0.4 + 
                               etage_scoring.fillna(0).values * 0.4)
    
    #On récupère les index des colonnes avec le score maximal
    index_score_max = score_total.idxmax(axis=1).values
    
    best_match = -1 * np.ones(croisement_v3.shape[0]) 
    for idx in range(croisement_v3.shape[0]):
        if not pd.isna(croisement_v3.iloc[idx, index_score_max[idx]]):
            best_match[idx] = croisement_v3.iloc[idx, index_score_max[idx]]
            
    best_match = pd.Series(best_match, dtype='int64')
    best_match.index.rename('id_bnb', inplace=True)
    best_match.rename('id_rpls', inplace=True)
    
    name_airbnb = data_airbnb.loc[:, 'name']
    summary_airbnb = data_airbnb.loc[:, 'summary']
    space_airbnb = data_airbnb.loc[:, 'space']
    description_airbnb = data_airbnb.loc[:, 'description'] 
    
    def print_result(id_bnb, id_rpls):
        print(name_airbnb[id_bnb]
            ,"\n"
            ,space_airbnb[id_bnb]
            ,"\n"
            ,description_airbnb[id_bnb]
            ,"\n"
            ,summary_airbnb[id_bnb]
            ,"\n"
            ,"\n"
            ,data_airbnb.loc[id_bnb, 'longitude']
            ,"\n"
            ,data_airbnb.loc[id_bnb, 'latitude']
            )
        print()
        print("Detection etage : {}".format(etage_tokens[id_bnb]))
        print()
        print("Detection surface habitable : {}".format())
        print(data_rpls.loc[id_rpls
                            , ['numvoie','typvoie','nomvoie','surfhab'
                               , 'etage','nbpiece','longitude','latitude']])
