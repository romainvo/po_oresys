# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:31:12 2019

@author: romain
"""

import pandas as pd
import numpy as np

def converter_cp(string):
    try:
        return int(string)
    except:
        return 0    
    
data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
    
data_rpls = pd.read_csv("paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                        header='infer', index_col=0,
                        converters={'codepostal':converter_cp},
                        dtype={'longitude':'float', 'latitude':'float'})

results = pd.read_csv('results.csv', header='infer', index_col='id_bnb',
                      dtype={'id_rpls':'int', 'distance':'float'})

results.sort_values(by='distance', inplace=True)

check = results.iloc[0:15]

check_bnb = data_airbnb.loc[check.index,
                      ['name','space','description','access','host_location',
                       'host_neighbourhood','neighbourhood','city','zipcode',
                       'latitude','longitude','bathrooms','bedrooms']]

check_rpls = data_rpls.loc[check.id_rpls,
                           ['codepostal','numvoie','typvoie','nomvoie','nbpiece',
                            'numboite','etage','numapp','surfhab','longitude',
                            'latitude']]
check_rpls.index.rename('id_rpls', inplace=True)

results.to_csv('results_sorted.csv', header=True)
check_bnb.to_csv('check_bnb.csv', header=True)
check_rpls.to_csv('check_rpls.csv', header=True)

# =========================================================================== #
# =========================================================================== #


#mini = results.loc[results.distance.idxmin()]
#print(mini)
#
#
#idx_bnb = mini.name
#idx_rpls = int(mini.id_rpls)
#distance = mini.distance
#
#print(data_rpls.loc[idx_rpls, 
#                    ['codepostal','numvoie','typvoie','nomvoie','nbpiece',
#                     'numboite','etage','numapp','surfhab','longitude','latitude']])
#    
#print(data_airbnb.loc[idx_bnb,
#                      ['name','space','description','access','host_location',
#                       'host_neighbourhood','neighbourhood','city','zipcode',
#                       'latitude','longitude','bathrooms','bedrooms']])
    