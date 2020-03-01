#________________________________________
import pandas as pd
import re, pprint
import numpy as np

data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
keep_cols = ["name", "summary", "space", "description"]
df = data_airbnb[keep_cols]
#df=df.head(200000)
df
name_airbnb=df.loc[:, 'name']
summary_airbnb = df.loc[:, 'summary']
space_airbnb = df.loc[:, 'space']
description_airbnb = df.loc[:, 'description'] 
# --------------------------------------------------------------------------- #
pattern_pieces = r"""(?x)
    (\d | \Aa | (?:\s)one | (?:\s)two | (?:\s)three)
    (?:
     (?:\s+bedroom|\-bedroom|bedroom|bedrm)
    |(?:\s?bdr|-?bdr|bdr)
    |\s?bed
    |(?:\s?br|-?br|br)
    |(?:\sroom|\srooms|room|rooms|r\s|\sr\s)
    |(?:\spi.ce|\spi.ces|pi.ce|pi.ces|p\s|\sp\s)
    #|(?:\s?pi.ces?|\s?pi.ce?|\(?p\)\s|p\s)
    |(?:\s?chambre|chbr?|\s?chambres?\s|chambre|chbr?|chambres?\s|-?chambre|-+chbr?|-?chambres?\s)
    )
    """
tokens_pieces = dict()
tokens_nombre = dict()

#Test Pattern pour l'affiner
#for idx in name_airbnb:
 #   test_string = idx.lower()
  #  result = re.findall(pattern_pieces, test_string)

    #print("\n")
    #print(test_string)
    #print(result)



#----------------------------------------------------------------------------#


#surfhab_tokens_feet = dict()
#surfhab_tokens_meter = dict()
#surfhab_tokens_surface = dict()
#name_airbnb=df.loc[:, 'name']
#summary_airbnb = df.loc[:, 'summary']
#space_airbnb = df.loc[:, 'space']
#description_airbnb = df.loc[:, 'description'] 

for idx, row in enumerate(name_airbnb):
    if row is not np.NaN:
        row = row.lower()
        print("____________________________")
        print(row)
        temp_pieces = re.findall(pattern_pieces, row) 


        if (temp_pieces == ('a') or ('one') or ('two') or ('three')):
            temp_pieces=[1 if (x=='a' or
             x=='one') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three') else x for x in temp_pieces]
        
        print('\n show temp' )
        print(temp_pieces)
            
        if temp_pieces:
            tokens_pieces[idx] = temp_pieces #poner elemento en el diccionario
        print("*******************")
        print(tokens_pieces)

            
for idx, row in enumerate(summary_airbnb):#recorrer todos elementos del array 
    if row is not np.NaN:
        row = row.lower() #Ponerlos en minuscula

        temp_pieces = re.findall(pattern_pieces, row) 
        if (temp_pieces == ('a') or ('one') or ('two') or ('three')):
            temp_pieces=[1 if (x=='a' or x=='one') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three') else x for x in temp_pieces]
            
        if temp_pieces:
            if idx not in tokens_pieces:
                tokens_pieces[idx] = temp_pieces
            else:
                tokens_pieces[idx] += temp_pieces

for idx, row in enumerate(space_airbnb):
    if row is not np.NaN:
        row = row.lower()

        temp_pieces = re.findall(pattern_pieces, row) 
        if (temp_pieces == ('a') or ('one') or ('two') or ('three')):
            temp_pieces=[1 if (x=='a' or x=='one') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three') else x for x in temp_pieces]
            
        if temp_pieces:
            if idx not in tokens_pieces:
                tokens_pieces[idx] = temp_pieces
            else:
                tokens_pieces[idx] += temp_pieces
            
for idx, row in enumerate(description_airbnb):
    if row is not np.NaN:
        row = row.lower()

        temp_pieces = re.findall(pattern_pieces, row) 
        if (temp_pieces == ('a') or ('one') or ('two') or ('three')):
            temp_pieces=[1 if (x=='a' or x=='one') else x for x in temp_pieces]
            temp_pieces=[2 if (x=='two') else x for x in temp_pieces]
            temp_pieces=[3 if (x=='three') else x for x in temp_pieces]
            
        if temp_pieces:
            if idx not in tokens_pieces:
                tokens_pieces[idx] = temp_pieces
            else:
                tokens_pieces[idx] += temp_pieces
    
#    if idx == 200:
#        break



for key, element in tokens_pieces.items():
    tokens_pieces[key] = list(map(float, tokens_pieces[key]))

print (len(tokens_pieces))





    

