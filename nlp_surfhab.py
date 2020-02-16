import pandas as pd
import re, pprint
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
data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})

name_airbnb = data_airbnb.loc[:, 'name']
summary_airbnb = data_airbnb.loc[:, 'summary']
space_airbnb = data_airbnb.loc[:, 'space']
description_airbnb = data_airbnb.loc[:, 'description'] 
#for i in range(200):
#    print(i, description_airbnb.iloc[i])
#
#Recherche de pattern dans 'description' jusqu'à l'index 202

#print((data_airbnb.is_location_exact == 't').sum(), 'b')
          
#Colonnes à analyser dans les données airbnb
# summary / space / description / neighorhood_overview / street / neighbourhood
# neighbourhoud_cleansed / neighbourhood_group_cleansed / city / 
# room_type / bathrooms / bedrooms / beds / square_feet / property_type
# longitude / latitude

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
#surfhab_tokens_nltk = dict()

#pattern_surfhab_nltk = r"""(?x)
#    <.*><m.tre.><carre.*>
#    |<.*m2>
#    |<.*> <m2>
#    """
#        description_tokens = nltk.word_tokenize(row, language='english')
#        description_nltk = nltk.Text(description_tokens)
        
#        temp_nltk = TokenSearcher(description_nltk).findall(pattern_surfhab_nltk)
#
#        if temp_nltk:
#            surfhab_tokens_nltk[idx] = temp_nltk
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
    
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

#pattern_surfhab_feet = r"""(?x)
#     (\d+\.?,?\d*)\s?square.?\s?(?:feet|ft|foot)
#    |(\d+\.?,?\d*)\s?feet²
#    |(\d+\.?,?\d*)\s?sq\.?\s?(?:f.{0,2}t|\.\s?ft|f|/ft)
#    """

#pattern_surfhab_re = r"""(?x)
#     \d+\.?,?\d*\s+m.tre.\s+carre.
#    |\d+\.?,?\d*\s?m2
#    |\d+\.?,?\d*\s?sqm
#    |\d+\.?,?\d*m?\s?m?²
#    |\d+\.?,?\d*\s?square.?\s?(?:met...?)?(?:feet)?(?:ft)?(?:foot)?
#    |\d+\.?,?\d*\s?feet²
#    |\d+\.?,?\d*\s?sq\.?\s?(?:f.{0,2}t)?(?:\.mts)?(?:meter.?)?(?:\.\s?m)?(?:\.\s?ft)?
#    |\d+\.?,?\d*\s?sq\sm
#    |\d+\.?,?\d*\s?sq\.?f
#    """  

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

# --------------------------------------------------------------------------- #
# ------------------------- TEST SCORE SURFHAB ------------------------------ #
# --------------------------------------------------------------------------- #

def converter_cp(string):
    try:
        return int(string)
    except:
        return 0    
    
data_rpls = pd.read_csv("paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                        header='infer', index_col=0,
                        converters={'codepostal':converter_cp},
                        dtype={'longitude':'float', 'latitude':'float'})

keep_columns = ['id_bnb']
for i in range(100):
    keep_columns.append('id_rpls'+str(i))
dtype = {key:'int64' for key in keep_columns}

results = pd.read_csv('results_rd150_nb100_score.csv', header='infer'
                      , usecols=keep_columns
                      , index_col='id_bnb'
                      , dtype=pd.Int64Dtype())

#re.sub("[^0-9]", "","ldkfljzg55f2cv")
surfhab_rpls = pd.DataFrame()
for i in range(100):
    surfhab_rpls.loc[:, 'surfhab_{}'.format(i)] = \
        data_rpls.surfhab.reindex(results['id_rpls{}'.format(i)]).values

#surfhab contient les surface extraites pour les airbnb, avec en index l'id 
#du airbnb (le numéro de la ligne dans data_airbnb)
surfhab = pd.Series(surfhab_tokens).reindex(index=range(data_airbnb.shape[0]))

surfhab_scoring = surfhab_rpls.div(surfhab, axis=0)
surfhab_scoring = surfhab_scoring.applymap(lambda x: 1/x if x > 1 else x)

#nombre de airbnb avec au moins 1 match exact: 
# ((surfhab_scoring == 1).sum(axis=1) != 0).sum()

"""for i in range(110):
    j=np.random.randint(250,60000)
    print(name_airbnb[j],"\n",space_airbnb[j],"\n",description_airbnb[j],"\n",summary_airbnb[j])
    if (surfhab[j]==np.NaN):
        print("pas de resultats")
    print(surfhab[j])
"""
#Résultats avec un echantillon random de 110 annonces :  38% de réussite, 2,7% d'erreur, et 59.3% d'annonces où la taille n'est pas indiquée.

