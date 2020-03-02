import scoring
import numpy as np 
import pandas as pd 

class Comparateur:
    def __init__(self,data_rpls,data_airbnb,data_croisement):
            self.data_airbnb = data_rpls
            self.data_rpls = data_airbnb
            self.data_rpls = data_croisement