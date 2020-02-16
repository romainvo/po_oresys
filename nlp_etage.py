# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 09:34:57 2020

@author: romain
"""

import pandas as pd
import re, pprint
import numpy as np

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

pattern_etage_number = r"""(?x)
    (\d+(?:\.\d+)?)
    (?:
     \s*(?:th|d|nd|rd|st|e|.me|°)\s*(?:floor|.tage)
    |\s*(?:th|d|nd|rd|st|e|.me|°)[a-z\s]{0,20}(?:floor|.tage)
    |\s*(?:floor|.tage)
    )
    """
    
pattern_etage_letter = r"""(?x)
    (first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|nineth|tenth
    |eleventh|twelveth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth
    |eighteenth|nineteenth|twentieth|ground|rez.de.chauss[a-z]{1,2}
    |premier|deuxi.me|troisi.me[a-z]?|quatri.me[a-z]?|cinqui.me[a-z]?
    |sixi.me[a-z]?|septi.me[a-z]?|huiti.me[a-z]?|neuvi.me[a-z]?|dizi.me[a-z]?
    |onzi.me[a-z]?|douzi.me[a-z]?|treizi.me[a-z]?|quatorzi.me[a-z]?|quinzi.me[a-z]?
    |seizi.me[a-z]?|dix.?septi.me[a-z]?|dix.huiti.me[a-z]?|dix.neuvi.me[a-z]?
    |vingti.me[a-z]?)
    (?:
     \s*(?:floor|.tage)
    |[a-z\s]{0,20}(?:floor|.tage)
    )
    """

letter_to_number = {'first':1,'second':2,'third':3,'fourth':4,'fifth':5
                    ,'sixth':6,'seventh':7,'eighth':8,'ninth':9,'nineth':9
                    ,'tenth':10,'eleventh':11,'twelveth':12,'thirteenth':13
                    ,'fourteenth':14,'fifteenth':15,'sixteenth':16
                    ,'seventeenth':17,'eighteenth':18,'nineteenth':19
                    ,'twentieth':20,'ground':0,'premier':1,'deuxieme':2
                    ,'deuxième':2,'troisieme':3,'troisième':3,'quatrieme':4
                    ,'quatrième':4,'cinquieme':5,'cinquième':5,'sixieme':6
                    ,'sixième':6,'septieme':7,'septième':7,'huitieme':8
                    ,'huitième':8,'neuvieme':9,'neuvième':9,'dixieme':10
                    ,'dixième':10,'onzieme':11,'onzième':11,'douzieme':12
                    ,'douzième':12,'treizieme':13,'treizième':13,'quatorzieme':14
                    ,'quatorzième':14,'quinzieme':15,'quinzième':15
                    ,'seizieme':16,'seizième':16,'dix-septieme':17
                    ,'dix-septième':17,'dix-huitieme':18,'dix-huitième':18
                    ,'dix-neuvieme':19,'dix-neuvième':19,'vingtieme':20
                    ,'vingtième':20,'rez-de-chaussée':0,'rez-de-chausee':0
                    ,'rez-de-chaussé':0,'rez-de-chausse':0,'rez de chaussée':0
                    ,'rez de chaussé':0, 'rez de chaussez':0} 
   
etage_tokens_number = dict()
etage_tokens_letter = dict()
etage_tokens = dict()

for idx, row in enumerate(description_airbnb):
    if not pd.isna(row):
        row = row.lower()

        temp_number = re.findall(pattern_etage_number, row) 
        temp_letter = re.findall(pattern_etage_letter, row)
            
        if temp_number:
            etage_tokens_number[idx] = temp_number
            
        if temp_letter:
            etage_tokens_letter[idx] = temp_letter
    
#    if idx == 200:
#        break
            
for idx, row in enumerate(name_airbnb):
    if not pd.isna(row):
        row = row.lower()

        temp_number = re.findall(pattern_etage_number, row) 
        temp_letter = re.findall(pattern_etage_letter, row)
            
        if temp_number:
            if idx not in etage_tokens_number:
                etage_tokens_number[idx] = list(temp_number)
            else:
                etage_tokens_number[idx] += temp_number

        if temp_letter:
            if idx not in etage_tokens_letter:
                etage_tokens_letter[idx] = list(temp_letter)
            else:
                etage_tokens_letter[idx] += temp_letter
                
for idx, row in enumerate(summary_airbnb):
    if not pd.isna(row):
        row = row.lower()

        temp_number = re.findall(pattern_etage_number, row) 
        temp_letter = re.findall(pattern_etage_letter, row)
            
        if temp_number:
            if idx not in etage_tokens_number:
                etage_tokens_number[idx] = list(temp_number)
            else:
                etage_tokens_number[idx] += temp_number

        if temp_letter:
            if idx not in etage_tokens_letter:
                etage_tokens_letter[idx] = list(temp_letter)
            else:
                etage_tokens_letter[idx] += temp_letter

for idx, row in enumerate(space_airbnb):
    if not pd.isna(row):
        row = row.lower()

        temp_number = re.findall(pattern_etage_number, row) 
        temp_letter = re.findall(pattern_etage_letter, row)
            
        if temp_number:
            if idx not in etage_tokens_number:
                etage_tokens_number[idx] = list(temp_number)
            else:
                etage_tokens_number[idx] += temp_number

        if temp_letter:
            if idx not in etage_tokens_letter:
                etage_tokens_letter[idx] = list(temp_letter)
            else:
                etage_tokens_letter[idx] += temp_letter
                
                
for key, element in etage_tokens_number.items():
    etage_tokens_number[key] = list(map(float, element))
    etage_tokens_number[key] = min(etage_tokens_number[key])

for key, element in etage_tokens_letter.items():
    etage_tokens_letter[key] \
    = list(map(lambda x: letter_to_number[x], element))
    etage_tokens_letter[key] = min(etage_tokens_letter[key])
    
for key in set(list(etage_tokens_number.keys())+list(etage_tokens_letter.keys())):
    if (key not in etage_tokens_number) and (key in etage_tokens_letter):
        etage_tokens[key] = etage_tokens_letter[key]
    elif (key not in etage_tokens_letter) and (key in etage_tokens_number):
        etage_tokens[key] = etage_tokens_number[key]
    elif (key in etage_tokens_number) and (key in etage_tokens_letter):
        etage_tokens[key] \
        = min(etage_tokens_number[key], etage_tokens_letter[key])

# --------------------------------------------------------------------------- #
# ------------------------- TEST SCORE SURFHAB ------------------------------ #
# --------------------------------------------------------------------------- #

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
    
data_rpls = pd.read_csv("paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                        header='infer', index_col=0,
                        converters={'codepostal':converter_cp
                                    , 'etage':converter_etage},
                        dtype={'longitude':'float', 'latitude':'float'})

keep_columns = ['id_bnb']
for i in range(100):
    keep_columns.append('id_rpls{}'.format(i))
dtype = {key:'int64' for key in keep_columns}

results = pd.read_csv('results_rd150_nb100_score.csv', header='infer'
                      , usecols=keep_columns
                      , index_col='id_bnb'
                      , dtype=pd.Int64Dtype())

#re.sub("[^0-9]", "","ldkfljzg55f2cv")
etage_rpls = pd.DataFrame()
for i in range(100):
    etage_rpls.loc[:, 'etage_{}'.format(i)] = \
        data_rpls.etage.reindex(results['id_rpls{}'.format(i)]).values

#etage contient les surface extraites pour les airbnb, avec en index l'id 
#du airbnb (le numéro de la ligne dans data_airbnb)
etage = pd.Series(etage_tokens).reindex(index=range(data_airbnb.shape[0]))

etage_scoring = etage_rpls.subtract(etage, axis=0)

def etage_score_filtering(x):
    if x == 0:
        return 1
    elif abs(x) == 1:
        return 0.20
    elif not pd.isna(x):
        return 0
    else:
        return np.NaN

etage_scoring = etage_scoring.applymap(etage_score_filtering)

#nombre de airbnb avec au moins 1 match exact: 
# ((etage_scoring == 1).sum(axis=1) != 0).sum()