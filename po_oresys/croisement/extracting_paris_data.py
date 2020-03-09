import pandas as pd

def converter_cp(string):
    try:
        return int(string)
    except:
        return 0

#Extraction des index correspondant à la ville de Paris dans geo-rpls2017.csv
#geo-rpls2017.csv contient répertorie l'ensemble des logements sociaux en France métropolitaine
reader = pd.read_csv("geo-rpls2017.csv", sep=',',error_bad_lines=False,
                     header='infer', usecols=['codepostal'],
                     converters={'codepostal':converter_cp})
                     
data_rpls = reader.loc[(reader['codepostal'] >= 75000) & (reader['codepostal'] < 76000)]
data_rpls.loc[:, 'id_geo-rpls'] = data_rpls.index.values
data_rpls.reset_index(drop=True, inplace=True)

#Création du geo-rpls2017_paris.csv (avec toutes les columns)
reader = pd.read_csv('geo-rpls2017.csv', iterator=True, chunksize=200000,
                     header='infer', converters={'codepostal':converter_cp})

paris_rpls = pd.concat([chunk.loc[chunk.index.isin(data_rpls['id_geo-rpls'].values)] \
                                  for chunk in reader])

#on mémorise dans la colonne 'id_geo-rpls' l'index initial du logement social dans le fichier 'geo-rpls2017'
paris_rpls.loc[:, 'id_geo-rpls'] = data_rpls['id_geo-rpls'].values

paris_rpls.reset_index(drop=True, inplace=True)
paris_rpls.to_csv('paris_rpls_2017.csv', header=True)