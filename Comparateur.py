import scoring
import numpy as np 
import pandas as pd 

class Comparateur:
    
    def __init__(self,data_rpls='paris_rpls_2017.csv',data_airbnb='airbnb.csv',croisemnt='result_rd155_nb250.csv',scorng='scoring'):
        self.data_airbnb = data_airbnb
        self.data_rpls = data_rpls
        self.croisement = pd.read_csv(croisemnt, sep=',',header='infer')
        self.scoring=pd.read_csv(scorng, sep=',',header='infer')
    