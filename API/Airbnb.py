import pandas as pd
class Airbnb(pd.DataFrame): 
     def __init__(self,data):
        data_airbnb = pd.read_csv(data, sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
        self.data_airbnb.loc[:, 'id_bnb'] = self.data_airbnb.index.astype(int)
        self =  data_airbnb.copy(deep=True)


    @property
    def _constructor(self):
        return Airbnb

    