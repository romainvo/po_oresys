import pandas as pd
import numpy as np
import re
from decorators import AirbnbAccessor, RPLSAccessor

class API:
    def __init__(self,airbnb='airbnb.csv',rpls='paris_rpls_2017',croisement='results_rd155_nb250',score=''):
        self.airbnb = Airbnb.Airbnb(airbnb)
        self.rpls = Rpls.Rpls(rpls)
        #self.comparateur = Comparateur.Comparateur(airbnb,rpls,croisement,score)

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
