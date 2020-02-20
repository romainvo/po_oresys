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



from nlp_surfhab import extraction_surfhab, score_surfhab
from nlp_etage import extraction_etage, score_etage

if __name__ == '__main__':

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