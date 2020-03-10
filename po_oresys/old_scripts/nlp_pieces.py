import pandas as pd
import re
import numpy as np


def extraction_nbpiece(data_airbnb):

    name_airbnb = data_airbnb.loc[:, 'name']
    summary_airbnb = data_airbnb.loc[:, 'summary']
    space_airbnb = data_airbnb.loc[:, 'space']
    description_airbnb = data_airbnb.loc[:, 'description'] 
    
    pattern_pieces = r"""(?x)
    (\d | (?:\s|\A)a | (?:\s|\A)one | (?:\s|\A)two | (?:\s|\A)three | (?:\s|\A)four | (?:\s|\A)une | (?:\s|\A)deux | (?:\s|\A)trois | (?:\s|\A)quatre )
    (?:
     (?:(?:\s|\-)bedroom(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/)|bedroom(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/))
    |(?:(?:\s|\-)bedrm(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/)|bedrm(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/))
    |(?:(?:\s|\-)bdr(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/)|bdr(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/))
    |(?:(?:\s|\-)bed(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|\/)|bed(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|\/))
    |(?:(?:\s|\-)br(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s\s|\/)|br(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s\s|\/))
    |(?:(?:\s|\-)room(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/)|room(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/))
    |(?:(?:\s|\-)r(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|\/)|r(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|\/))
    |(?:(?:\s|\-)pi.ce(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/)|pi.ce(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/))
    |(?:(?:\s|\-)p(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|\/)|p(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|\/))
    |(?:(?:\s|\-)chambre(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/)|chambre(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/))
    |(?:(?:\s|\-)chbr(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/)|chbr(?:\,\s|\.\s|\)\s|\:\s|\;\s|\s|s|s\s|\/))
    )
    """

    tokens_pieces = dict()
        
    for idx, row in enumerate(name_airbnb):
        if not pd.isna(row):
            row = row.lower()
            #print("____________________________")
            #print(row)
            temp_pieces = re.findall(pattern_pieces, row) 
            temp_pieces += re.findall('studio', row) 

            temp_pieces=[1 if (x=='studio' or x=='a' or x==' a' or x=='one' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x=='une' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two' or x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three' or x==' three' or x=='\tthree' or x=='\xa0three' or x==' trois' or x=='trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
            temp_pieces=[4 if (x=='four' or x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre'  or x=='quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]


            #print('\n show temp' )
            #print(temp_pieces)
                
            if temp_pieces:
                tokens_pieces[idx] = list(temp_pieces)  #poner elemento en el diccionario
            #print("*******************")
            #print(tokens_pieces)
            
    for idx, row in enumerate(summary_airbnb):#recorrer todos elementos del array 
        if not pd.isna(row):
            row = row.lower() #Ponerlos en minuscula

            temp_pieces = re.findall(pattern_pieces, row) 
            temp_pieces += re.findall('studio', row) 

            temp_pieces=[1 if (x=='studio' or x=='a' or x==' a' or x=='one' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x=='une' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two' or x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three' or x==' three' or x=='\tthree' or x=='\xa0three' or x==' trois' or x=='trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
            temp_pieces=[4 if (x=='four' or x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre'  or x=='quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
            
            if temp_pieces:
                if idx not in tokens_pieces:
                    tokens_pieces[idx] = list(temp_pieces) 
                else:
                    tokens_pieces[idx] += temp_pieces 

    for idx, row in enumerate(space_airbnb):
        if not pd.isna(row):
            row = row.lower()

            temp_pieces = re.findall(pattern_pieces, row) 
            temp_pieces += re.findall('studio', row) 

            temp_pieces=[1 if (x=='studio' or x=='a' or x==' a' or x=='one' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x=='une' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two' or x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three' or x==' three' or x=='\tthree' or x=='\xa0three' or x==' trois' or x=='trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
            temp_pieces=[4 if (x=='four' or x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre'  or x=='quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
            
            if temp_pieces:
                if idx not in tokens_pieces:
                    tokens_pieces[idx] = list(temp_pieces) 
                else:
                    tokens_pieces[idx] += temp_pieces 
                
    for idx, row in enumerate(description_airbnb):
        if not pd.isna(row):
            row = row.lower()

            temp_pieces = re.findall(pattern_pieces, row) 
            temp_pieces += re.findall('studio', row) 

            temp_pieces=[1 if (x=='studio' or x=='a' or x==' a' or x=='one' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x=='une' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two' or x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three' or x==' three' or x=='\tthree' or x=='\xa0three' or x==' trois' or x=='trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
            temp_pieces=[4 if (x=='four' or x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre'  or x=='quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
           
            if temp_pieces:
                if idx not in tokens_pieces:
                    tokens_pieces[idx] = list(temp_pieces) 
                else:
                    tokens_pieces[idx] += temp_pieces 
    
    for key, element in tokens_pieces.items():
        tokens_pieces[key] = list(map(float, element))
    
    for key, element in tokens_pieces.items():

        tokens_pieces[key] = max(element)
        tokens_pieces[key] = tokens_pieces[key] + 1
    
    return tokens_pieces
    
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
    
def score_pieces(data_airbnb, croisement_v3, pieces_tokens):
    
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
    
    data_rpls = pd.read_csv("../csv/paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                            header='infer', index_col=0,
                            converters={'codepostal':converter_cp
                                        , 'etage':converter_etage},
                            dtype={'longitude':'float', 'latitude':'float'})
    
    #re.sub("[^0-9]", "","ldkfljzg55f2cv")
    nbpiece_rpls = pd.DataFrame()    
    for i in range(nb_col_croisement_v3): #pour chaque col
        nbpiece_rpls.loc[:, 'nbpiece_{}'.format(i)] = \
        data_rpls.nbpiece.reindex(croisement_v3['id_rpls{}'.format(i)]).values
    
    #etage contient les surface extraites pour les airbnb, avec en index l'id 
    #du airbnb (le numéro de la ligne dans data_airbnb)
    pieces = pd.Series(pieces_tokens).reindex(index=range(data_airbnb.shape[0]))
    
    pieces_scoring = nbpiece_rpls.subtract(pieces, axis=0)
    
    pieces_scoring = pieces_scoring.applymap(pieces_score_filtering)
    
    pieces_scoring.index.rename('id_bnb', inplace=True)
    
    return pieces_scoring

if __name__ == '__main__':

    keep_columns = ['id_bnb']
    for i in range(250):
        keep_columns.append('id_rpls{}'.format(i))
#    dtype = {key:'int64' for key in keep_columns}
    
    croisement_v3 = pd.read_csv('../csv/results_rd155_nb250.csv', header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype())    
    
    data_airbnb = pd.read_csv("../csv/airbnb.csv", sep=',', header='infer',
                              dtype={'longitude':'float', 'latitude':'float'})
    
    nbpiece_tokens = extraction_nbpiece(data_airbnb)

# -------- Évaluation des performances de l'algorithme de détection --------- # 

#    nombre de détections :  40534
    len(nbpiece_tokens)

    name_airbnb = data_airbnb.loc[:, 'name']
    summary_airbnb = data_airbnb.loc[:, 'summary']
    space_airbnb = data_airbnb.loc[:, 'space']
    description_airbnb = data_airbnb.loc[:, 'description'] 

#    for i in range(110):
#        j = np.random.randint(250,60000)
#        print("_______name________", "\n", name_airbnb[j]
#            ,"\n"
#            ,"_______Space________", "\n",space_airbnb[j]
#            ,"\n"   
#            ,"_______Description________", "\n",description_airbnb[j]
#            ,"\n"
#            ,"_______Summary________", "\n",summary_airbnb[j]
#            ,"\n")
#        if j not in nbpiece_tokens:
#            print("pas de resultats \n")
#            print('******************************************************')
#        else:    
#            print(nbpiece_tokens[j])
#            print('******************************************************')


#    Résultats avec un echantillon random de 110 annonces :
#    31,8% de réussite, 17,2% d'erreur, et 56.3% d'annonces où le nombre de pieces  
#    n'est pas indiquée.

# --------------------- Évaluation du scoring avec rpls --------------------- # 

    pieces_scoring = score_pieces(data_airbnb, croisement_v3, nbpiece_tokens)

    #INUTILE DE RÉALISER UNE ANALYSE DES PERF PAR TRANCHE CAR LA REPARTITION DU
    #SCORE EST DISCRETE
    
    rename_col = {'nbpiece_{}'.format(i) : i for i in range(pieces_scoring.shape[1])} 
    pieces_scoring.rename(columns=rename_col, inplace=True)
    
    #On récupère le numéro des colonnes avec le score maximal
    column_score_max = pieces_scoring.idxmax(axis=1).values
    score_max = pieces_scoring.max(axis=1).values
    
    best_match = -1 * np.ones((croisement_v3.shape[0],2)) 
    for idx in range(croisement_v3.shape[0]):
        if not pd.isna(column_score_max[idx]):
            best_match[idx,0] = croisement_v3.iloc[idx, int(column_score_max[idx])]
            best_match[idx,1] = score_max[idx]
            
    best_match = pd.DataFrame(best_match)
    
    best_match.index.rename('id_bnb', inplace=True)
    best_match.rename(columns={0:'id_rpls', 1:'score'}, inplace=True)
    best_match = best_match.astype({'id_rpls':'int64'})

    import matplotlib.pyplot as plt
    import seaborn as sns

#    best_match.replace(to_replace={'score':-1.0}, value={'score':0.0}
#    , inplace=True)
    
    tranche_index = ["no detection", "0%", "20%", "50%", "100%"]
    tranche_nombre = [0]
    tranche_nombre.append((best_match.score == 0).sum())
    tranche_nombre.append((best_match.score == 0.2).sum())
    tranche_nombre.append((best_match.score == 0.5).sum())
    tranche_nombre.append((best_match.score == 1).sum())
    tranche_nombre[0] = best_match.shape[0] - np.sum(tranche_nombre[1:])

    plt.style.use('seaborn-darkgrid')
    plt.rcParams.update({'font.size':15})
#    plt.rcParams["figure.figsize"] = (50,40)    
    fig, ax = plt.subplots()
    ax.set_title("Distribution des scores - nombre de pièces")
    sns.barplot(y=tranche_nombre, x=tranche_index
                , orient='v', ax=ax, edgecolor='white')
    
    #Distribution du nombre de logements sociaux autour de chaque airbnb ayant
    #le même nombre de pièces
    #sns.distplot((pieces_scoring == 1).sum(axis=1))
    
    #en pourcentage cumulé
    #sns.distplot((etage_scoring == 1).sum(axis=1).divide((~croisement_v3.isna()).sum(axis=1)),
    #kde=False, hist_kws={'cumulative':-1})