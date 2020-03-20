# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 19:33:47 2020

@author: romain
"""

import re
import numpy as np
import pandas as pd

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

def extraire_surfhab(data_airbnb, id):    
    """Retourne la surface habitable (en mètres carrés) indiquée dans 
    l'annonce airbnb si présente.
    
    Parameters:
        data_airbnb (pd.DataFrame): DataFrame contenant un ensemble d'annonces
        airbnb.
        
        id (int or [int]): identifiant de l'annonce airbnb ou liste
        d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
        la DataFrame.
        
    Returns:
        surfhab (float or {id:surfhab}): surface habitable indiquée dans 
        l'annonce, np.nan si non détectée.
    """
    
    if not hasattr(id, '__iter__'):
        indexes = [id]
    else :
        indexes = id
        
    name_airbnb = data_airbnb.loc[indexes, 'name']
    summary_airbnb = data_airbnb.loc[indexes, 'summary']
    space_airbnb = data_airbnb.loc[indexes, 'space']
    description_airbnb = data_airbnb.loc[indexes, 'description'] 

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
    
    for idx, row in zip(indexes, description_airbnb.values):
        if not pd.isna(row):
            row = row.lower()
            temp_feet = re.findall(pattern_surfhab_feet, row) 
            temp_meter = re.findall(pattern_surfhab_meter, row)
                
            if temp_feet:
                surfhab_tokens_feet[idx] = list(temp_feet)
                
            if temp_meter:
                surfhab_tokens_meter[idx] = list(temp_meter)
    
    for idx, row in zip(indexes, name_airbnb):
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
                    surfhab_tokens_meter[idx] = list(temp_meter)  
                else:
                    surfhab_tokens_meter[idx] += temp_meter
    
    for idx, row in zip(indexes, summary_airbnb):
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
                    surfhab_tokens_meter[idx] = list(temp_meter)  
                else:
                    surfhab_tokens_meter[idx] += temp_meter
    
    for idx, row in zip(indexes, space_airbnb):
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
                    surfhab_tokens_meter[idx] = list(temp_meter)  
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
    
    if type(id) is int:
        if id in surfhab_tokens:
            return surfhab_tokens[id]
        else:
            return np.nan
    else:
        return surfhab_tokens
    
def extraire_etage(data_airbnb : pd.DataFrame, id):
    """Retourne le numéro de l'étage indiqué dans l'annonce airbnb si présente.
    
    Parameters:
        data_airbnb (pd.DataFrame): DataFrame contenant un ensemble d'annonces
        airbnb.
    
        id (int or [int]): identifiant de l'annonce airbnb ou liste
        d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
        la DataFrame.
        
    Returns:
        etage (int): numéro de l'étage indiqué dans l'annonce, np.nan si
        non-détecté.
    """
    
    if not hasattr(id, '__iter__'):
        indexes = [id]
    else :
        indexes = id
        
    name_airbnb = data_airbnb.loc[indexes, 'name']
    summary_airbnb = data_airbnb.loc[indexes, 'summary']
    space_airbnb = data_airbnb.loc[indexes, 'space']
    description_airbnb = data_airbnb.loc[indexes, 'description'] 
    
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
    
    letter_to_number \
    = {'first':1,'second':2,'third':3,'fourth':4,'fifth':5
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
    
    for idx, row in zip(indexes, description_airbnb.values):
        if not pd.isna(row):
            row = row.lower()
            temp_number = re.findall(pattern_etage_number, row) 
            temp_letter = re.findall(pattern_etage_letter, row)
                
            if temp_number:
                etage_tokens_number[idx] = list(temp_number)
                
            if temp_letter:
                etage_tokens_letter[idx] = temp_letter
                
    for idx, row in zip(indexes, name_airbnb.values):
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
                    
    for idx, row in zip(indexes, summary_airbnb.values):
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
    
    for idx, row in zip(indexes, space_airbnb.values):
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
            
    if type(id) is int:
        if id in etage_tokens:
            return etage_tokens[id]
        else:
            return np.nan
    else:
        return etage_tokens   

def extraire_nbpiece(data_airbnb : pd.DataFrame, id):
    """Retourne le nombre de pièces indiqué dans l'annonce airbnb si présente.
    
    Parameters:
        data_airbnb (pd.DataFrame): DataFrame contenant un ensemble d'annonces
        airbnb.
        
        id (int or [int]): identifiant de l'annonce airbnb ou liste
        d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
        la DataFrame.
        
    Returns:
        etage (int): nombre de pièce indiqué dans l'annonce, np.nan si
        non-détecté.
    """
    
    if not hasattr(id, '__iter__'):
        indexes = [id]
    else :
        indexes = id
        
    name_airbnb = data_airbnb.loc[indexes, 'name']
    summary_airbnb = data_airbnb.loc[indexes, 'summary']
    space_airbnb = data_airbnb.loc[indexes, 'space']
    description_airbnb = data_airbnb.loc[indexes, 'description'] 
    
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
        
    for idx, row in zip(indexes, name_airbnb.values):
        if not pd.isna(row):
            row = row.lower()
            temp_pieces = re.findall(pattern_pieces, row) 
            temp_pieces += re.findall('studio', row) 

            temp_pieces=[1 if (x=='studio' or x=='a' or x==' a' or x=='one' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x=='une' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two' or x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three' or x==' three' or x=='\tthree' or x=='\xa0three' or x==' trois' or x=='trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
            temp_pieces=[4 if (x=='four' or x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre'  or x=='quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
  
            if temp_pieces:
                tokens_pieces[idx] = list(temp_pieces)
            
    for idx, row in zip(indexes, summary_airbnb.values):
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

    for idx, row in zip(indexes, space_airbnb.values):
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
                
    for idx, row in zip(indexes, description_airbnb.values):
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

    if type(id) is int:
        if id in tokens_pieces:
            return tokens_pieces[id]
        else:
            return np.nan
    else:
        return tokens_pieces