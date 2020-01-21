import nltk 
nltk.data.path.append("D:\\Users\\romai\\nltk_data")
import pandas as pd
import numpy as numpy

data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
          
#Colonnes à analyser dans les données airbnb
# summary / space / description / neighorhood_overview / street / neighbourhood
# neighbourhoud_cleansed / neighbourhood_group_cleansed / city / 
                
from nltk.book import * 

#Words in context
text1.concordance("monstruous")
text2.concordance("affection")

#What other words appear in a similar range of contexts
text2.similar("affection")

#Examine the contextes that are shared by two or more words
text2.common_contexts(["affection","very"])

#positional information can be displayed using 
#a dispersion plot. Each stripe represents an 
#instance of a word and each row represents the 
#entire text
text4.dispersion_plot(
        ["citizens", "democracy", "freedom", "duties", "America"])

def lexical_diversity(text):
    return len(set(text)) / len(text)

def percentage(count, total):
    return 100 * count / total
