import pandas as pd
import re
import numpy as np


def extraction_pieces(data_airbnb):
    data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
<<<<<<< HEAD
    keep_cols = ["name", "summary", "space", "description"]
    df = data_airbnb[keep_cols]
    #df=df.head(200000)
    df

    name_airbnb=df.loc[:, 'name']
    summary_airbnb = df.loc[:, 'summary']
    space_airbnb = df.loc[:, 'space']
    description_airbnb = df.loc[:, 'description'] 
    
    
    pattern_pieces = r"""(?x)
=======
keep_cols = ["name", "summary", "space", "description"]
df = data_airbnb[keep_cols]
#df=df.head(200000)
df
name_airbnb=df.loc[:, 'name']
summary_airbnb = df.loc[:, 'summary']
space_airbnb = df.loc[:, 'space']
description_airbnb = df.loc[:, 'description'] 

# --------------------------------------------------------------------------- #

pattern_pieces = r"""(?x)
>>>>>>> 1341188af98e865f15051281e24e9b8140fcc8ac
    (\d | (?:\s)a | (?:\s)one | (?:\s)two | (?:\s)three)
    (?:
     (?:\s+bedroom|\-bedroom|bedroom|bedrm)
    |(?:\s?bdr|-?bdr|bdr)
    |\s?bed
    |(?:\s?br|-?br|br)
    |(?:\sroom|\srooms|room|rooms|r\s|\sr\s)
    |(?:\spi.ce|\spi.ces|pi.ce|pi.ces|p\s|\sp\s)
    #|(?:\s?pi.ces?|\s?pi.ce?|\(?p\)\s|p\s)
    |(?:\s?chambre|chbr?|\s?chambres?\s|chambre|chbr?|chambres?\s|-?chambre|-+chbr?|-?chambres?\s)
    )
    """
<<<<<<< HEAD
    tokens_pieces = dict()
    pieces_tokens = dict()
        
    for idx, row in enumerate(name_airbnb):
        if row is not np.NaN:
            row = row.lower()
            #print("____________________________")
            #print(row)
            temp_pieces = re.findall(pattern_pieces, row) 
=======
    
tokens_pieces = dict()
tokens_nombre = dict()
>>>>>>> 1341188af98e865f15051281e24e9b8140fcc8ac


            if (temp_pieces == (' a') or (' one') or (' two') or (' three')):
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three') else x for x in temp_pieces]
            
            #print('\n show temp' )
            #print(temp_pieces)
                
            if temp_pieces:
                tokens_pieces[idx] = temp_pieces  #poner elemento en el diccionario
            #print("*******************")
            #print(tokens_pieces)

<<<<<<< HEAD
            
    for idx, row in enumerate(summary_airbnb):#recorrer todos elementos del array 
        if row is not np.NaN:
            row = row.lower() #Ponerlos en minuscula

            temp_pieces = re.findall(pattern_pieces, row) 
            if (temp_pieces == (' a') or (' one') or (' two') or (' three')):
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three') else x for x in temp_pieces]
                
            if temp_pieces:
                if idx not in tokens_pieces:
                    tokens_pieces[idx] = temp_pieces 
                else:
                    tokens_pieces[idx] += temp_pieces 

    for idx, row in enumerate(space_airbnb):
        if row is not np.NaN:
            row = row.lower()

            temp_pieces = re.findall(pattern_pieces, row) 
            if (temp_pieces == (' a') or (' one') or (' two') or (' three')):
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three') else x for x in temp_pieces]
                
            if temp_pieces:
                if idx not in tokens_pieces:
                    tokens_pieces[idx] = temp_pieces 
                else:
                    tokens_pieces[idx] += temp_pieces 
                
    for idx, row in enumerate(description_airbnb):
        if row is not np.NaN:
            row = row.lower()

            temp_pieces = re.findall(pattern_pieces, row) 
            if (temp_pieces == (' a') or (' one') or (' two') or (' three')):
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three') else x for x in temp_pieces]
                
            if temp_pieces:
                if idx not in tokens_pieces:
                    tokens_pieces[idx] = temp_pieces 
                else:
                    tokens_pieces[idx] += temp_pieces 
=======
#----------------------------------------------------------------------------#

#surfhab_tokens_feet = dict()
#surfhab_tokens_meter = dict()
#surfhab_tokens_surface = dict()
#name_airbnb=df.loc[:, 'name']
#summary_airbnb = df.loc[:, 'summary']
#space_airbnb = df.loc[:, 'space']
#description_airbnb = df.loc[:, 'description'] 
>>>>>>> 1341188af98e865f15051281e24e9b8140fcc8ac

    # for key in set(list(tokens_pieces.keys())):

    #         tokens_pieces[key] \
    #         = max(tokens_pieces[key])
    
    for key, element in tokens_pieces.items():
        tokens_pieces[key] = list(map(float, tokens_pieces[key]))

    
    for key in set(list(tokens_pieces.keys())):

        pieces_tokens[key] \
        = max(tokens_pieces[key])
        pieces_tokens[key] \
        = pieces_tokens[key]+1

    print (len(pieces_tokens))
    
    return pieces_tokens
                    
                    

    
def pieces_score_filtering(x):
    if x == 0:
        return 1
    elif abs(x) == 1:
        return 0.50
    elif abs(x) == 2:
        return 0.20
    elif not pd.isna(x):
        return 0
    else:
        return np.NaN
    
def score_etage(data_airbnb, croisement_v3, pieces_tokens):
    
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
        
    nb_col_croisement_v3 = croisement_v3.shape[1]
    
    data_rpls = pd.read_csv("paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                            header='infer', index_col=0,
                            converters={'codepostal':converter_cp
                                        , 'etage':converter_etage},
                            dtype={'longitude':'float', 'latitude':'float'})
    
    #re.sub("[^0-9]", "","ldkfljzg55f2cv")
    pieces_rpls = pd.DataFrame()    
    for i in range(nb_col_croisement_v3):
        pieces_rpls.loc[:, 'nbpiece_{}'.format(i)] = \
            data_rpls.nbpiece.reindex(croisement_v3['id_rpls{}'.format(i)]).values
    
    #etage contient les surface extraites pour les airbnb, avec en index l'id 
    #du airbnb (le numéro de la ligne dans data_airbnb)
    pieces = pd.Series(pieces_tokens).reindex(index=range(data_airbnb.shape[0]))
    
    pieces_scoring = pieces_rpls.subtract(pieces, axis=0)
    
    pieces_scoring = pieces_scoring.applymap(pieces_score_filtering)
    
    pieces_scoring.index.rename('id_bnb', inplace=True)
    
    return pieces_scoring

if __name__ == '__main__':

    keep_columns = ['id_bnb']
    for i in range(250):
        keep_columns.append('id_rpls{}'.format(i))
#    dtype = {key:'int64' for key in keep_columns}
    
    croisement_v3 = pd.read_csv('results_rd155_nb250.csv', header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype())    
    
    data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                              dtype={'longitude':'float', 'latitude':'float'})
    
    pieces_tokens = extraction_pieces(data_airbnb)

# -------- Évaluation des performances de l'algorithme de détection --------- # 

#    nombre de détections : 25059
#    len(etage_tokens)

    name_airbnb = data_airbnb.loc[:, 'name']
    summary_airbnb = data_airbnb.loc[:, 'summary']
    space_airbnb = data_airbnb.loc[:, 'space']
    description_airbnb = data_airbnb.loc[:, 'description'] 

    for i in range(110):
        j = np.random.randint(250,60000)
        print(name_airbnb[j]
            ,"\n"
            ,space_airbnb[j]
            ,"\n"   
            ,description_airbnb[j]
            ,"\n"
            ,summary_airbnb[j]
            ,"\n")
        if j not in pieces_tokens:
            print("pas de resultats \n")
        else:    
            print(pieces_tokens[j])

#    
#    Résultats avec un echantillon random de 110 annonces :  39.09% de réussite, 
#    1.82% de détection avec 1 étage de différence, 3.64% d'erreur, et 55.45% 
#    d'annonces où la taille n'est pas indiquée.

# --------------------- Évaluation du scoring avec rpls --------------------- # 

    etage_scoring = score_etage(data_airbnb, croisement_v3, pieces_tokens)
    
#    nombre de airbnb avec au moins 1 match exact dans rpls: 19625
#    ((etage_scoring == 1).sum(axis=1) != 0).sum()
    
#    nombre de airbnb avec seulement des match 1 étage de différence 
#    dans rpls: 1020
#    (((etage_scoring == 0.2).sum(axis=1) != 0)
#        & ((etage_scoring == 1).sum(axis=1) == 0)).sum()
    
#    nombre de airbnb avec 0 match : 1084
#    (((etage_scoring == 0).sum(axis=1) != 0) 
#        & ((etage_scoring == 0.2).sum(axis=1) == 0)
#        & ((etage_scoring == 1).sum(axis=1) == 0)).sum()
        
#    nombre de airbnb avec que des nan = 0 prédictions ou 0 rpls dans le
#    rayon d'anonymisation : 43241
#    ((~etage_scoring.isna()).sum(axis=1) == 0).sum()
    
    
    #INUTILE DE RÉALISER UNE ANALYSE DES PERF PAR TRANCHE CAR LA REPARTITION DU
    #SCORE EST DISCRETE
    
#    rename_col = {'etage_{}'.format(i) : i for i in range(etage_scoring.shape[1])} 
#    etage_scoring.rename(columns=rename_col, inplace=True)
#    
#    #On récupère le numéro des colonnes avec le score maximal
#    column_score_max = etage_scoring.idxmax(axis=1).values
#    score_max = etage_scoring.max(axis=1).values
#    
#    best_match = -1 * np.ones((croisement_v3.shape[0],2)) 
#    for idx in range(croisement_v3.shape[0]):
#        if not pd.isna(column_score_max[idx]):
#            best_match[idx,0] = croisement_v3.iloc[idx, int(column_score_max[idx])]
#            best_match[idx,1] = score_max[idx]
#            
#    best_match = pd.DataFrame(best_match)
#    
#    best_match.index.rename('id_bnb', inplace=True)
#    best_match.rename(columns={0:'id_rpls', 1:'score'}, inplace=True)
#    best_match = best_match.astype({'id_rpls':'int64'})
#
#    best_match.replace(to_replace={'score':-1.0}, value={'score':0.0}
#    , inplace=True)
#    
#    tranche_score = [0,1,30,40,50,60,62.5,65,70,75,80,90,95,97.5,98.5,99.5,100]
#    
#    somme_cumulee = 0
#    for i, tranche in enumerate(tranche_score):
#        if tranche == 100:
#            break
#        elif i == (len(tranche_score) - 2):
#            nb_temp = best_match.loc[(best_match.score >= tranche/100)
#                    & (best_match.score <= tranche_score[i+1]/100)].shape[0]
#            
#            somme_cumulee += nb_temp           
#        else:            
#            nb_temp = best_match.loc[(best_match.score >= tranche/100)
#                        & (best_match.score < tranche_score[i+1]/100)].shape[0]
#            
#            somme_cumulee += nb_temp
#        
#        print("Détections avec une suspicion entre {}% et {}% : {} -- somme cumulée : {}"
#              .format(tranche, tranche_score[i+1], nb_temp, somme_cumulee))