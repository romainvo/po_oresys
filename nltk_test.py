import nltk 
nltk.data.path.append("D:\\Users\\romai\\nltk_data")
import pandas as pd
import re, pprint
import numpy as np
                
from nltk.book import * 
from nltk.text import TokenSearcher

data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})

summary_airbnb = data_airbnb.loc[:, 'description']
description_airbnb = data_airbnb.loc[:, 'description']

print((data_airbnb.is_location_exact == 't').sum(), 'b')
          
#Colonnes à analyser dans les données airbnb
# summary / space / description / neighorhood_overview / street / neighbourhood
# neighbourhoud_cleansed / neighbourhood_group_cleansed / city / 
# room_type / bathrooms / bedrooms / beds / square_feet / property_type
# longitude / latitude

# nltk object 
description_tokens = nltk.word_tokenize(description_airbnb.iloc[653], language='english')
description_nltk = nltk.Text(description_tokens)

pattern_surfhab = r"<.*><m.tre.><carre.*>|<..m2>"
    
TokenSearcher(description_nltk).findall(pattern_surfhab)