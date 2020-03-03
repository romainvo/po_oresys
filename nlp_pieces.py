#________________________________________
import pandas as pd
import re, pprint
import numpy as np

data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
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
    
tokens_pieces = dict()
tokens_nombre = dict()

#Test Pattern pour l'affiner
#for idx in name_airbnb:
 #   test_string = idx.lower()
  #  result = re.findall(pattern_pieces, test_string)

    #print("\n")
    #print(test_string)
    #print(result)

#----------------------------------------------------------------------------#

#surfhab_tokens_feet = dict()
#surfhab_tokens_meter = dict()
#surfhab_tokens_surface = dict()
#name_airbnb=df.loc[:, 'name']
#summary_airbnb = df.loc[:, 'summary']
#space_airbnb = df.loc[:, 'space']
#description_airbnb = df.loc[:, 'description'] 

for idx, row in enumerate(name_airbnb):
    if row is not np.NaN:
        row = row.lower()
        #print("____________________________")
        #print(row)
        temp_pieces = re.findall(pattern_pieces, row) 


        if (temp_pieces == (' a') or (' one') or (' two') or (' three')):
            temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a') else x for x in temp_pieces]
            temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two') else x for x in temp_pieces]
            temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three') else x for x in temp_pieces]
        
        #print('\n show temp' )
        #print(temp_pieces)
            
        if temp_pieces:
            tokens_pieces[idx] = temp_pieces #poner elemento en el diccionario
        #print("*******************")
        #print(tokens_pieces)

            
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
    
#    if idx == 200:
#        break



for key, element in tokens_pieces.items():
    tokens_pieces[key] = list(map(float, tokens_pieces[key]))

print (len(tokens_pieces))

# -------- Évaluation des performances de l'algorithme de détection --------- # 

#    nombre de détections : 24723
#    len(tokens_pieces)

   
#    name_airbnb = data_airbnb.loc[:, 'name']
#    summary_airbnb = data_airbnb.loc[:, 'summary']
#    space_airbnb = data_airbnb.loc[:, 'space']
#    description_airbnb = data_airbnb.loc[:, 'description'] 
    
    for i in range(110):
        j = np.random.randint(250,60000)
        print(name_airbnb[j]
            ,"\n"
            ,space_airbnb[j]
            ,"\n"
            ,description_airbnb[j]
            ,"\n"
            ,summary_airbnb[j]
            ,"\n"
        )
        if j not in surfhab_tokens:
            print("pas de resultats")
        else:    
           print(etage[j])
    
#    Résultats avec un echantillon random de 110 annonces :
#    38% de réussite, 2,7% d'erreur, et 59.3% d'annonces où la taille n'est 
#    pas indiquée.

# --------------------- Évaluation du scoring avec rpls --------------------- # 

 #   surfhab_scoring = score_surfhab(data_airbnb, croisement_v3, surfhab_tokens)
    
#    nombre de airbnb avec au moins 1 match exact dans le rpls: 9046
#    ((surfhab_scoring == 1).sum(axis=1) != 0).sum()
    
#    nombre de airbnb avec seulement des match non exacts dans rpls: 18109
#    (((surfhab_scoring > 0).sum(axis=1) != 0) 
#        & ((surfhab_scoring == 1).sum(axis=1) == 0)).sum()
#    
#    nombre de airbnb avec 0 match : 1
#    (((surfhab_scoring == 0).sum(axis=1) != 0) 
#        & ((surfhab_scoring > 0).sum(axis=1) == 0)).sum()
        
#    nombre de airbnb avec que des nan = 0 prédictions ou 0 rpls dans le
#    rayon d'anonymisation : 37814
##    ((~surfhab_scoring.isna()).sum(axis=1) == 0).sum() 
#    
# 
#    
#    rename_col = {'surfhab_{}'.format(i) : i for i in range(surfhab_scoring.shape[1])} 
#    surfhab_scoring.rename(columns=rename_col, inplace=True)
#    
#    #On récupère le numéro des colonnes avec le score maximal
#    column_score_max = surfhab_scoring.idxmax(axis=1).values
#    score_max = surfhab_scoring.max(axis=1).values
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



    

