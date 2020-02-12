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

for i in range(200):
    print(i, description_airbnb.iloc[i])

pattern_surfhab_meter = r"""(?x)
    (\d+\.?,?\d*)
    (?:
     \s+m.tre.\s+carre.
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
    if row is not np.NaN:
        row = row.lower()

        temp_feet = re.findall(pattern_surfhab_feet, row) 
        temp_meter = re.findall(pattern_surfhab_meter, row)
            
        if temp_feet:
            surfhab_tokens_feet[idx] = temp_feet
            
        if temp_meter:
            surfhab_tokens_meter[idx] = temp_meter
    
#    if idx == 200:
#        break