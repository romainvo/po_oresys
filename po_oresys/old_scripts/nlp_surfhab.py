import pandas as pd
import re
import numpy as np

#import nltk 
#nltk.data.path.append("D:\\Users\\romai\\nltk_data")               
#from nltk.book import * 
#from nltk.text import TokenSearcher

#. 	Wildcard, matches any character
#^abc 	Matches some pattern abc at the start of a string
#abc$ 	Matches some pattern abc at the end of a string
#[abc] 	Matches one of a set of characters
#[A-Z0-9] 	Matches one of a range of characters
#ed|ing|s 	Matches one of the specified strings (disjunction)
#* 	Zero or more of previous item, e.g. a*, [a-z]* (also known as Kleene Closure)
#+ 	One or more of previous item, e.g. a+, [a-z]+
#? 	Zero or one of the previous item (i.e. optional), e.g. a?, [a-z]?
#{n} 	Exactly n repeats where n is a non-negative integer
#{n,} 	At least n repeats
#{,n} 	No more than n repeats
#{m,n} 	At least m and no more than n repeats
#a(b|c)+ 	Parentheses that indicate the scope of the operators

#\b 	Word boundary (zero width)
#\d 	Any decimal digit (equivalent to [0-9])
#\D 	Any non-digit character (equivalent to [^0-9])
#\s 	Any whitespace character (equivalent to [ \t\n\r\f\v])
#\S 	Any non-whitespace character (equivalent to [^ \t\n\r\f\v])
#\w 	Any alphanumeric character (equivalent to [a-zA-Z0-9_])
#\W 	Any non-alphanumeric character (equivalent to [^a-zA-Z0-9_])
#\t 	The tab character
#\n 	The newline character

#Colonnes à analyser dans les données airbnb
# summary / space / description / neighorhood_overview / street / neighbourhood
# neighbourhoud_cleansed / neighbourhood_group_cleansed / city / 
# room_type / bathrooms / bedrooms / beds / square_feet / property_type
# longitude / latitude

#Recherche de règles/structures à détecter de l'indice 0 à 200 puis au feeling

def extraction_surfhab(data_airbnb):
    
    name_airbnb = data_airbnb.loc[:, 'name']
    summary_airbnb = data_airbnb.loc[:, 'summary']
    space_airbnb = data_airbnb.loc[:, 'space']
    description_airbnb = data_airbnb.loc[:, 'description'] 

    pattern_surfhab_meter = r"""(?x)
        (\d+\.?,?\d*)
        (?:
         \s+m.tre.\s+carr.*
        |\s?m2
        |\s?sqm
        |(?:m\s|\sm|m)²
        |\s?square.?\s?met...?
        |\s?sq\.?\s?(?:\.mts|meter.?|\.\s?m)
        |\s?sq\sm
        )
        """
    
    pattern_surfhab_feet = r"""(?x)
        (\d+\.?,?\d*)
        (?:
         \s?square.?\s?(?:feet|ft|foot)
        |\s?feet²
        |\s?sq\.?\s?(?:f.{0,2}t|\.\s?ft|f|/ft)
        )
        """
    
    surfhab_tokens_feet = dict()
    surfhab_tokens_meter = dict()
    surfhab_tokens = dict()
    
    for idx, row in enumerate(description_airbnb):
        if not pd.isna(row):
            row = row.lower()
    
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                surfhab_tokens_feet[idx] = temp_feet
                
            if temp_meter:
                surfhab_tokens_meter[idx] = temp_meter
        
    #    if idx == 200:
    #        break
    
    for idx, row in enumerate(name_airbnb):
        if not pd.isna(row):
            row = row.lower()
    
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                if idx not in surfhab_tokens_feet:
                    surfhab_tokens_feet[idx] = list(temp_feet)
                else:
                    surfhab_tokens_feet[idx] += temp_feet
                
            if temp_meter:
                if idx not in surfhab_tokens_meter:
                    surfhab_tokens_meter[idx] = temp_meter  
                else:
                    surfhab_tokens_meter[idx] += temp_meter
    
    for idx, row in enumerate(summary_airbnb):
        if not pd.isna(row):
            row = row.lower()
    
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                if idx not in surfhab_tokens_feet:
                    surfhab_tokens_feet[idx] = list(temp_feet)
                else:
                    surfhab_tokens_feet[idx] += temp_feet
                
            if temp_meter:
                if idx not in surfhab_tokens_meter:
                    surfhab_tokens_meter[idx] = temp_meter  
                else:
                    surfhab_tokens_meter[idx] += temp_meter
    
    for idx, row in enumerate(space_airbnb):
        if not pd.isna(row):
            row = row.lower()
    
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                if idx not in surfhab_tokens_feet:
                    surfhab_tokens_feet[idx] = temp_feet
                else:
                    surfhab_tokens_feet[idx] += temp_feet
                
            if temp_meter:
                if idx not in surfhab_tokens_meter:
                    surfhab_tokens_meter[idx] = temp_meter  
                else:
                    surfhab_tokens_meter[idx] += temp_meter
    
    for key, element in surfhab_tokens_meter.items():
        surfhab_tokens_meter[key] = list(map(lambda x: x.replace(',','.'), element))
        surfhab_tokens_meter[key] = list(map(float, surfhab_tokens_meter[key]))
        surfhab_tokens_meter[key] = max(surfhab_tokens_meter[key])
    
    for key, element in surfhab_tokens_feet.items():
        surfhab_tokens_feet[key] = list(map(lambda x: x.replace(',','.'), element))
        surfhab_tokens_feet[key] = list(map(float, surfhab_tokens_feet[key]))
        surfhab_tokens_feet[key] = max(surfhab_tokens_feet[key])
        surfhab_tokens_feet[key] = surfhab_tokens_feet[key] / 10.764 #1m² = 10.764 feet²
        
    for key in set(list(surfhab_tokens_meter.keys())+list(surfhab_tokens_feet.keys())):
        if (key not in surfhab_tokens_meter) and (key in surfhab_tokens_feet):
            surfhab_tokens[key] = surfhab_tokens_feet[key]
        elif (key in surfhab_tokens_meter) and (key not in surfhab_tokens_feet):
            surfhab_tokens[key] = surfhab_tokens_meter[key]
        elif (key in surfhab_tokens_meter) and (key in surfhab_tokens_feet):
            surfhab_tokens[key] \
            = max(surfhab_tokens_feet[key], surfhab_tokens_meter[key])
        
    return surfhab_tokens

def score_surfhab(data_airbnb, croisement_v3, surfhab_tokens):

    def converter_cp(string):
        try:
            return int(string)
        except:
            return 0    

    nb_col_croisement_v3 = croisement_v3.shape[1]
        
    data_rpls = pd.read_csv("../csv/paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                            header='infer', index_col=0,
                            converters={'codepostal':converter_cp},
                            dtype={'longitude':'float', 'latitude':'float'})
    
    #re.sub("[^0-9]", "","ldkfljzg55f2cv")
    surfhab_rpls = pd.DataFrame()
    for i in range(nb_col_croisement_v3):
        surfhab_rpls.loc[:, 'surfhab_{}'.format(i)] = \
        data_rpls.surfhab.reindex(croisement_v3['id_rpls{}'.format(i)]).values
    
    #surfhab contient les surface extraites pour les airbnb, avec en index l'id 
    #du airbnb (le numéro de la ligne dans data_airbnb)
    surfhab = pd.Series(surfhab_tokens).reindex(index=range(data_airbnb.shape[0]))
    
    surfhab_scoring = surfhab_rpls.div(surfhab, axis=0)
    surfhab_scoring = surfhab_scoring.applymap(lambda x: 1/x if x > 1 else x)
    
    surfhab_scoring.index.rename('id_bnb', inplace=True)

    return surfhab_scoring

if __name__ == '__main__':
    
    keep_columns = ['id_bnb']
    for i in range(250):
        keep_columns.append('id_rpls'+str(i))
#    dtype = {key:'int64' for key in keep_columns}
    
    croisement_v3 = pd.read_csv('../csv/results_rd155_nb250.csv', header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype())    
    
    data_airbnb = pd.read_csv("../csv/airbnb.csv", sep=',', header='infer',
                              dtype={'longitude':'float', 'latitude':'float'})

    surfhab_tokens = extraction_surfhab(data_airbnb)

# -------- Évaluation des performances de l'algorithme de détection --------- # 

#    nombre de détections : 30337
#    len(surfhab_tokens)
   
#    name_airbnb = data_airbnb.loc[:, 'name']
#    summary_airbnb = data_airbnb.loc[:, 'summary']
#    space_airbnb = data_airbnb.loc[:, 'space']
#    description_airbnb = data_airbnb.loc[:, 'description'] 
    
#    for i in range(110):
#        j = np.random.randint(250,60000)
#        print(name_airbnb[j]
#            ,"\n"
#            ,space_airbnb[j]
#            ,"\n"
#            ,description_airbnb[j]
#            ,"\n"
#            ,summary_airbnb[j]
#            ,"\n"
#        )
#        if j not in surfhab_tokens:
#            print("pas de resultats")
#        else:    
#           print(etage[j])
#    
#    Résultats avec un echantillon random de 110 annonces :
#    38% de réussite, 2,7% d'erreur, et 59.3% d'annonces où la taille n'est 
#    pas indiquée.

# --------------------- Évaluation du scoring avec rpls --------------------- # 

    surfhab_scoring = score_surfhab(data_airbnb, croisement_v3, surfhab_tokens)
   
    rename_col = {'surfhab_{}'.format(i) : i for i in range(surfhab_scoring.shape[1])} 
    surfhab_scoring.rename(columns=rename_col, inplace=True)
    
    #On récupère le numéro des colonnes avec le score maximal
    column_score_max = surfhab_scoring.idxmax(axis=1).values
    score_max = surfhab_scoring.max(axis=1).values
    
    best_match = -1 * np.ones((croisement_v3.shape[0],2)) 
    for idx in range(croisement_v3.shape[0]):
        if not pd.isna(column_score_max[idx]):
            best_match[idx,0] = croisement_v3.iloc[idx, int(column_score_max[idx])]
            best_match[idx,1] = score_max[idx]
            
    best_match = pd.DataFrame(best_match)
    
    best_match.index.rename('id_bnb', inplace=True)
    best_match.rename(columns={0:'id_rpls', 1:'score'}, inplace=True)
    best_match = best_match.astype({'id_rpls':'int64'})

    best_match.replace(to_replace={'score':-1.0}, value={'score':0.0}
    , inplace=True)
    
    tranche_score = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
    tranche_index = []
    tranche_nombre = []
    
    n = best_match.shape[0]
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
              .format(tranche, tranche_score[i+1], nb_temp, somme_cumulee/n))
    
    tranche_index[0] = "no detection"
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.style.use('seaborn-darkgrid')

    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size':15})
#    plt.rcParams["figure.figsize"] = (50,40)
    ax.set_title("Nombre de suspicions par tranche de score - surface habitable")
    sns.barplot(x=tranche_nombre, y=tranche_index
                , orient='h', ax=ax, edgecolor='white')