# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:42:59 2019

@author: romain
"""

import pandas as pd
import geopandas as gpd
import numpy as np
import multiprocessing
from functools import partial

def converter_cp(string):
    try:
        return int(string)
    except:
        return 0

def haversine(lon1, lat1, lon2=1.0, lat2=1.0):

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    r = 6371008 # Radius of earth in meters
    d = 2 * r * np.arcsin(np.sqrt(a)) 

    return d

def func(chunk_bnb, data_rpls=None):
    for idx, row in enumerate(chunk_bnb.itertuples()):
        print(row.id_bnb)
        distances = haversine(data_rpls.longitude, data_rpls.latitude
                              , lon2=row.longitude, lat2=row.latitude)
        chunk_bnb.at[idx, 'id_rpls'] = distances.idxmin()
        chunk_bnb.at[idx, 'dist'] = distances.min()
    
data_rpls = pd.read_csv("paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                        header='infer', 
                        usecols=['codepostal','longitude','latitude','id_geo-rpls'],
                        converters={'codepostal':converter_cp},
                        dtype={'longitude':'float', 'latitude':'float'})

data_airbnb = pd.read_csv("airbnb.csv", sep=',', header='infer',
                          usecols=['latitude','longitude'],
                          dtype={'longitude':'float', 'latitude':'float'})

data_airbnb.loc[:, 'id_bnb'] = data_airbnb.index.astype(int)

#-----------------------------------------------------------------------------#
#-------------------------- WITH DataFrame.apply -----------------------------#
#-----------------------------------------------------------------------------#


def func_apply(row, data_rpls=None):
    print(row.id_bnb)
    distances = haversine(data_rpls.longitude, data_rpls.latitude
                          , lon2=row.longitude, lat2=row.latitude)
    
    return [distances.idxmin(), distances.min()]

results = data_airbnb.apply(partial(func_apply,data_rpls=data_rpls)
, axis=1, result_type='expand')

results.columns = ['id_rpls', 'distance']
results.index.rename('id_bnb', inplace=True)
#results.to_csv('results.csv', header=True)

#-----------------------------------------------------------------------------#
#------------------------- WITH MULTIPROCESSING ------------------------------#
#-----------------------------------------------------------------------------#

#data_airbnb.loc[:,'id_rpls'] = -1
#data_airbnb.loc[:, 'dist'] = -1
#
#num_processes = multiprocessing.cpu_count()
#
## calculate the chunk size as an integer
#chunk_size = int(data_airbnb.shape[0]/num_processes)
#
#chunks = [data_airbnb.iloc[data_airbnb.index[i:i + chunk_size]] \
#          for i in range(0, data_airbnb.shape[0], chunk_size)]
#
## create our pool with `num_processes` processes
#pool = multiprocessing.Pool(processes=num_processes)
#
## apply our function to each chunk in the list
#result = pool.map(partial(func, data_rpls=data_rpls), chunks)
#
#for i in range(len(result)):
#   # since result[i] is just a dataframe
#   # we can reassign the original dataframe based on the index of each chunk
#   data_airbnb.iloc[result[i].index] = result[i]