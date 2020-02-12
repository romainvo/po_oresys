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

summary_airbnb = data_airbnb.loc[:, 'summary']
space_airbnb = data_airbnb.loc[:, 'space']
description_airbnb = data_airbnb.loc[:, 'description'] 

#for i in range(200):
#    print(i, description_airbnb.iloc[i])

pattern_etage_number = r"""(?x)
    (\d+\.?,?\d*)
    (?:
     \s*(?:th|d|nd|rd|st|e|.me|°)\s*(?:floor|.tage)
    |\s*(?:th|d|nd|rd|st|e|.me|°).*(?:floor|.tage)
    |\s*(?:floor|.tage)
    )
    """
    
pattern_etage_letter = r"""(?x)
    (first|second|third|[a-z]+th|[a-z]+)
    (?:
     \s*(?:floor|.tage)
    |.*(?:floor|.tage)
    )
    """
    
etage_tokens_number = dict()
etage_tokens_letter = dict()

for idx, row in enumerate(description_airbnb):
    if row is not np.NaN:
        row = row.lower()

        temp_number = re.findall(pattern_etage_number, row) 
        temp_letter = re.findall(pattern_etage_letter, row)
            
        if temp_number:
            etage_tokens_number[idx] = temp_number
            
        if temp_letter:
            etage_tokens_letter[idx] = temp_letter
    
#    if idx == 200:
#        break