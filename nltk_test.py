import nltk 
nltk.data.path.append("D:\\Users\\romai\\nltk_data")
import pandas as pd
import re, pprint
import numpy as np
                
from nltk.book import * 
from nltk.text import TokenSearcher

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


summary_airbnb = data_airbnb.loc[:, 'description']
description_airbnb = data_airbnb.loc[:, 'description'] 
#Recherche de pattern dans 'description' jusqu'à l'index 202

print((data_airbnb.is_location_exact == 't').sum(), 'b')
          
#Colonnes à analyser dans les données airbnb
# summary / space / description / neighorhood_overview / street / neighbourhood
# neighbourhoud_cleansed / neighbourhood_group_cleansed / city / 
# room_type / bathrooms / bedrooms / beds / square_feet / property_type
# longitude / latitude

surfhab_tokens_re = dict()
surfhab_tokens_nltk = dict()

pattern_surfhab_nltk = r"""(?x)
    <.*><m.tre.><carre.*>
    |<.*m2>
    |<.*> <m2>
    """
pattern_surfhab_re = r"""(?x)
     \d+\.?,?\d*\s+m.tre.\s+carre.
    |\d+\.?,?\d*\s?m2
    |\d+\.?,?\d*\s?sqm
    |\d+\.?,?\d*m?\s?m?²
    |\d+\.?,?\d*\s?square.?\s?(?:met...?)?(?:feet)?(?:ft.?)?(?:foot)?
    |\d+\.?,?\d*\s?feet(?:²)?
    |\d+\.?,?\d*\s?sq\.?\s?(?:f.{0,2}t)?(?:\.mts)?(?:meter.?)?(?:\.\s?m)?(?:\.\s?ft)?
    |\d+\.?,?\d*\s?sq\sm
    |\d+\.?,?\d*\s?sq\.?f
    """

for idx, row in enumerate(description_airbnb):
    
    if row is not np.NaN:
        row = row.lower()
        description_tokens = nltk.word_tokenize(row, language='english')
        description_nltk = nltk.Text(description_tokens)
        
        temp_nltk = TokenSearcher(description_nltk).findall(pattern_surfhab_nltk)
        temp_re = re.findall(pattern_surfhab_re, row)
        
        if temp_re:
            surfhab_tokens_re[idx] = temp_re
        
        if temp_nltk:
            surfhab_tokens_nltk[idx] = temp_nltk

    
#for idx,row in enumerate(description_airbnb[100:]):
#    print((100+idx))    
#    print(row)
#    print('')