# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:55:32 2020

@author: romain
"""

import re
import pandas as pd
import numpy as np

def import_data_rpls(rpls_path=None):
    
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
    

    if rpls_path is None:
        path = "po_oresys/csv/paris_rpls_2017.csv"
    else:
        path = rpls_path
    
    data_rpls = pd.read_csv(path, sep=',',error_bad_lines=False, 
                    header='infer', index_col=0,
                    converters={'codepostal':converter_codepostal
                                , 'etage':converter_etage},
                    dtype={'longitude':'float', 'latitude':'float'})
    
    data_rpls.index.rename('id_rpls', inplace=True)

    return data_rpls

def import_data_airbnb(airbnb_path=None):
    
    if airbnb_path is None:
        path = "po_oresys/csv/airbnb.csv"
    else:
        path = airbnb_path
    data_airbnb = pd.read_csv(path, sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
    
    data_airbnb.index.rename('id_bnb', inplace=True)

    return data_airbnb

def import_croisement(croisement_path=None):
    
    
    if croisement_path is None:
        path = 'po_oresys/csv/results_rd155_nb250.csv'
    else:
        path = croisement_path
        
    keep_columns = ['id_bnb']
    for i in range(250):
        keep_columns.append('id_rpls{}'.format(i))
#    dtype = {key:'int64' for key in keep_columns}
    
    croisement_v3 = pd.read_csv(path, header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype()) 
    
    return croisement_v3
 
def import_scores(scores_path=None):
    
    if scores_path is None:
        path = 'po_oresys/csv/all_scores_090320.csv'
    else:
        path = scores_path
    
    all_scores = pd.read_csv(path, header='infer', index_col='id_bnb') 
    
    return all_scores
