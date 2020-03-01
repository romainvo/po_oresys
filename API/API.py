import pandas as pd
import numpy as np
import re
import Airbnb,Comparateur,Rpls
class API:
    def __init__(self,airbnb,rpls,croisement):
        self.data_rpls = pd.read_csv(rpls, sep=',',error_bad_lines=False, 
                                header='infer', index_col=0,
                                converters={'codepostal':self.converter_cp
                                            , 'etage':self.converter_etage},
                                dtype={'longitude':'float', 'latitude':'float'})
        self.data_airbnb = pd.read_csv(airbnb, sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
        self.data_airbnb.loc[:, 'id_bnb'] = self.data_airbnb.index.astype(int)
        self.data_croisement = pd.read_csv(croisement, sep=',',header='infer')
        self.airbnb = Airbnb.Airbnb(self.data_airbnb)
        self.rpls = Rpls.Rpls(self.data_rpls)
        self.comparateur = Comparateur.Comparateur(self.data_airbnb,self.data_rpls,self.data_croisement)
    
    def converter_cp(self,string):
        try:
            return int(string)
        except:
            return 0   
        
    def converter_etage(self,string):
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
