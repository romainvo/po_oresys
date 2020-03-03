import pandas as pd
import numpy as np
import re
from decorators import AirbnbAccessor, RPLSAccessor

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

class API:
    
    def __init__(self, airbnb='csv/airbnb.csv', rpls='csv/paris_rpls_2017'
                 , croisement='csv/results_rd155_nb250', score=''):
        
        self.airbnb = import_data_airbnb(airbnb)
        self.rpls = import_data_rpls(rpls)
        #self.comparateur = Comparateur.Comparateur(airbnb,rpls,croisement,score)

