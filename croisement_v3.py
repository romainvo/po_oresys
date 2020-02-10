import pandas as pd
import geopandas as gpd
import numpy as np
from functools import partial
import time

start = time.time()

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

def func_apply(row, radius,nb_results, data_rpls=None):
    print(row.id_bnb)
    distances = haversine(data_rpls.longitude, data_rpls.latitude
                          , lon2=row.longitude, lat2=row.latitude)
    pd.Series.sort_values(distances)
    results = []
    count = 0
    for index,value in pd.Series.items(distances) :
        if value < radius and count < nb_results : # les nb_resultats les plus proches dans un rayon de radius
            results.append(index)                  
            results.append(value)
            count = count + 1
    # On remplit les tableaux avec des None pour avoir la même taille de results à chaque fois
    for i in range(nb_results*2-len(results)):
        results.append(None)
    return results
   
results = data_airbnb.apply(partial(func_apply,radius=100,nb_results=100,data_rpls=data_rpls)
, axis=1, result_type='expand')

columns_name = []
for i in range(len(results.columns)//2):
    columns_name.append('id_rpls'+str(i))
    columns_name.append('distance'+str(i))

results.columns = columns_name
results.index.rename('id_bnb', inplace=True)
results.to_csv('results_rd100_nb100.csv', header=True)

print("Temps d'éxécution : " + str(time.time()-start))

# Essai pour les résultats dans sur plusieurs lignes et non colonnes. NON FONCTIONNEL
"""
def func_apply(row, data_rpls=None, radius=50):
    print(row[1].id_bnb)
    distances = haversine(data_rpls.longitude, data_rpls.latitude
                          , lon2=row[1].longitude, lat2=row[1].latitude)
    results = pd.Series()
    for index,value in pd.Series.items(distances) :
        if value < radius:
            results.add(np.array([index, value]))
    return results

results_df = pd.DataFrame()
for row in data_airbnb.iterrows():
    results = func_apply(row, data_rpls)
    for element in pd.Series.items(results) :
        print(element)
        results_df.append(element)


results = data_airbnb.apply(partial(func_apply,data_rpls=data_rpls,radius=10)
, axis=1, result_type='expand')

results_df.columns = ['id_rpls', 'distance']
results_df.index.rename('id_bnb', inplace=True)
results_df.to_csv('results2.csv', header=True)

print(results_df.head())

"""
