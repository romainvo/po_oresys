import nltk 
nltk.data.path.append("D:\\Users\\romai\\nltk_data")
import pandas as pd
import re, pprint
import numpy as numpy
                
from nltk.book import * 

data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})

print((data_airbnb.is_location_exact == 't').sum())
          
#Colonnes à analyser dans les données airbnb
# summary / space / description / neighorhood_overview / street / neighbourhood
# neighbourhoud_cleansed / neighbourhood_group_cleansed / city / 
# room_type / bathrooms / bedrooms / beds / square_feet / property_type
# longitude / latitude

# nltk object 
desc = nltk.Text(nltk.word_tokenize(data_airbnb.iloc[638].description, language='english'))

#part_of_speech tagging
# nltk.help.upenn_tagset('VBP') : meaning of tag 
pos_desc = nltk.pos_tag(desc)

#Now we’ll implement noun phrase chunking to identify named entities using a
# regular expression consisting of rules that indicate how sentences should be chunked.
#Our chunk pattern consists of one rule, that a noun phrase, NP, should be 
#formed whenever the chunker finds an optional determiner, DT, followed by any 
#number of adjectives, JJ, and then a noun, NN.
pattern = 'SFHAB: {<CD>+<NNS>+<JJ>+}'

pattern = 'SFHAB: {"<CD>+\s+(?:mètres)\s+"}'

cp = nltk.RegexpParser(pattern)

result = cp.parse(pos_desc) 
print(result)