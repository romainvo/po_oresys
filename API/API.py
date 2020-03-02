import pandas as pd
import numpy as np
import re
import Airbnb,Comparateur,Rpls
class API:
    def __init__(self,airbnb,rpls,croisement,score):
        self.airbnb = Airbnb.Airbnb(self.airbnb)
        self.rpls = Rpls.Rpls(self.rpls)
        self.comparateur = Comparateur.Comparateur(self.airbnb,self.rpls,self.data_croisement,self.data_scoring)

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
