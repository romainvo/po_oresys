import pandas as pd
import numpy as np
import re
from decorators import AirbnbAccessor, RPLSAccessor
from comparateur import Comparateur

def import_data_rpls(path : str):

    def converter_codepostal(string):
        try:
            return int(string)
        except:
            return 0   
        
    def converter_etage(string):
        try: 
            return float(string)
        except:
            if string == 'RC':
                return 0.0
            
            match_temp = re.search(r"[1-9][0-9]*", string)
            if match_temp != None:
                return float(match_temp.group())
            else:
                return np.nan
            
    data_rpls = pd.read_csv(path, sep=',',error_bad_lines=False, 
                    header='infer', index_col=0,
                    converters={'codepostal':converter_codepostal
                                , 'etage':converter_etage},
                    dtype={'longitude':'float', 'latitude':'float'})
    
    data_rpls.index.rename('id_rpls', inplace=True)

    return data_rpls

def import_data_airbnb(path : str):
    
    data_airbnb = pd.read_csv(path, sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
    
    data_airbnb.index.rename('id_bnb', inplace=True)

    return data_airbnb

def import_croisement(path : str):
    
    keep_columns = ['id_bnb']
    for i in range(250):
        keep_columns.append('id_rpls{}'.format(i))
    croisement= pd.read_csv(path, header='infer', usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype())   
    
    return croisement

class API:
    
    def __init__(self, path_airbnb='csv/airbnb.csv', path_rpls='csv/paris_rpls_2017'
                 , path_croisement='csv/results_rd155_nb250', score=''):
        
        self.data_airbnb = import_data_airbnb(path_airbnb)
        self.data_rpls = import_data_rpls(path_rpls)
        self.croisement = import_croisement(path_croisement)
        self.comparateur = Comparateur(self.data_airbnb, self.data_rpls
                                       , self.croisement)

