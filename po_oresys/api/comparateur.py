import numpy as np 
import pandas as pd 
import re
import po_oresys.api.decorators 

class Comparateur:
    
    def __init__(self, data_airbnb, data_rpls, croisement
                 , poids_sous_scores={'croisement':0.2, 'surfhab':0.3
                                      , 'etage':0.3, 'nbpiece':0.2}
                 , surfhab_tokens=None, etage_tokens=None, nbpiece_tokens=None
                 , all_scores=None):

        self.data_airbnb = data_airbnb
        self.data_rpls = data_rpls
        self.croisement = croisement
        self.weights = poids_sous_scores
        
        if surfhab_tokens is not None:
            self.surfhab_tokens = surfhab_tokens
        if etage_tokens is not None:
            self.etage_tokens = etage_tokens
        if nbpiece_tokens is not None:
            self.nbpiece_tokens = nbpiece_tokens
        if all_scores is not None:
            self.all_scores = all_scores
 
    def voisinage_rpls(self, id_airbnb : int):
        #renvoie la liste des rpls présens dans le rayon d'anonymisation
        return self.croisement.loc[id_airbnb]
        
    def correspondance_distance(self, id_airbnb : int, id_rpls : int):
#       renvoie true si le airbnb et le rpls sontà moins de 150m l'un de l'autre
        
        return id_rpls in self.croisement.loc[id_airbnb].values

    def comparer(self, id_airbnb : int, id_rpls : int):
        
        self.data_airbnb.bnb.complete_description(id_airbnb)
        print("---------------------------------------------------------------"
              , "\n")
        self.data_rpls.rpls.complete_description(id_rpls)
        print("---------------------------------------------------------------"
              , "\n")        
        self.data_airbnb.bnb.all_extractions(id_airbnb, pprint=True, rreturn=False)
        print()
        
    def sous_score_surfhab(self, id_airbnb : int, id_rpls : int):
        surfhab_airbnb = self.data_airbnb.bnb.extraire_surfhab(id_airbnb)
        surfhab_rpls = self.data_rpls.loc[id_rpls, 'surfhab']
        
        if pd.isna(surfhab_airbnb) or pd.isna(surfhab_rpls):
            print("surfhab : score nul car aucune détection")
            return 0
        elif surfhab_airbnb < surfhab_rpls:
            return surfhab_airbnb / surfhab_rpls
        else:
            return surfhab_rpls / surfhab_airbnb
        
    def sous_score_etage(self, id_airbnb : int, id_rpls : int):
        etage_airbnb = self.data_airbnb.bnb.extraire_etage(id_airbnb)
        etage_rpls = self.data_rpls.loc[id_rpls, 'etage']
        
        if pd.isna(etage_airbnb) or pd.isna(etage_rpls):
            print("etage : score nul car aucune détection")
            return 0
        elif abs(etage_airbnb - etage_rpls) == 0:
            return 1
        elif abs(etage_airbnb - etage_rpls) == 1:
            return 0.2
        else:
            return 0
        
    def sous_score_nbpiece(self, id_airbnb : int, id_rpls : int):
        nbpiece_airbnb = self.data_airbnb.bnb.extraire_nbpiece(id_airbnb)
        nbpiece_rpls = self.data_rpls.loc[id_rpls, 'nbpiece']
        
        if pd.isna(nbpiece_airbnb) or pd.isna(nbpiece_rpls):
            print("nbpiece : score nul car aucune détection")
            return 0
        elif abs(nbpiece_airbnb - nbpiece_rpls) == 0:
            return 1
        elif abs(nbpiece_airbnb - nbpiece_rpls) == 1:
            return 0.5
        elif abs(nbpiece_airbnb - nbpiece_rpls) == 2:
            return 0.2
        else:
            return 0
        
    def calculer_score(self, id_airbnb : int, id_rpls : int, descriptif=False):   
        sous_scores = {key:np.nan for key in self.weights}

        if self.correspondance_distance(id_airbnb, id_rpls):
            sous_scores['croisement'] = 1
            
            score = self.weights['croisement'] * sous_scores['croisement']
            
            if 'surfhab' in self.weights:
                sous_scores['surfhab'] = self.sous_score_surfhab(id_airbnb, id_rpls)
                score += self.weights['surfhab'] * sous_scores['surfhab']
                
            if 'etage' in self.weights:
                sous_scores['etage'] = self.sous_score_etage(id_airbnb, id_rpls)
                score += self.weights['etage'] * sous_scores['etage'] 
                        
            if 'nbpiece' in self.weights:
                sous_scores['nbpiece'] = self.sous_score_nbpiece(id_airbnb, id_rpls)
                score += self.weights['nbpiece'] * sous_scores['nbpiece'] 
            
            if descriptif:
                print()
                print("Descriptif des sous-scores :")
                print("Poids des sous scores - {}".format(self.weights))
                for key in sous_scores:
                    print("Score {} : {}".format(key, sous_scores[key]))
                print()
                self.comparer(id_airbnb, id_rpls)
            return score
            
        else:
            if descriptif:
                print()
                print("Descriptif des sous-scores :")
                print("Poids des sous scores - {}".format(self.weights))
                for key in sous_scores:
                    print("Score {} : {}".format(key, sous_scores[key]))
                print()   
                self.comparer(id_airbnb, id_rpls)
            return 0
        
    def calculer_surfhab_scoring(self):
        if hasattr(self, 'surfhab_scoring'):
            print("Les sous_scores de surface habitable de chaque airbnb et"
                  ,"leur logement sociaux respectifs sont déjà calculés")
        
        else:  
            print("Calcul des sous_scores de surface habitable")
            
            if hasattr(self, 'surfhab_tokens'):
                surfhab_tokens = self.surfhab_tokens
            else:
                print("Text mining en cours - surfhab non extrait")
                surfhab_tokens \
                = self.data_airbnb.bnb.extraire_surfhab(self.data_airbnb.index.values)
            
            nb_col_croisement = self.croisement.shape[1]
            surfhab_rpls = pd.DataFrame()
            
            for i in range(nb_col_croisement):
                surfhab_rpls.loc[:, 'surfhab_{}'.format(i)] = \
                self.data_rpls.surfhab.reindex(
                         self.croisement['id_rpls{}'.format(i)]).values
            
            #surfhab contient les surface extraites pour les airbnb, avec 
            #en index l'id du airbnb (le numéro de la ligne dans data_airbnb)
            surfhab \
            = pd.Series(surfhab_tokens).reindex(index=range(data_airbnb.shape[0]))

            surfhab_scoring = surfhab_rpls.div(surfhab, axis=0)
            surfhab_scoring = surfhab_scoring.applymap(lambda x: 1/x if x > 1 else x)
            surfhab_scoring.index.rename('id_bnb', inplace=True)
            self.surfhab_scoring = surfhab_scoring
            
        return self.surfhab_scoring

    @staticmethod
    def _etage_score_filtering(x):
        if x == 0:
            return 1
        elif abs(x) == 1:
            return 0.20
        elif not pd.isna(x):
            return 0
        else:
            return np.NaN
    
    def calculer_etage_scoring(self):
        if hasattr(self, 'etage_scoring'):
            print("Les sous_scores d'étage de chaque airbnb et"
                  ,"leur logement sociaux respectifs sont déjà calculés")
        
        else:
            print("Calcul des sous_scores d'étage")
            
            if hasattr(self, 'etage_tokens'):
                etage_tokens = self.etage_tokens
            else:
                print("Text mining - etage non extrait")
                etage_tokens \
                = self.data_airbnb.bnb.extraire_etage(self.data_airbnb.index.values)
          
            nb_col_croisement = self.croisement.shape[1]
            etage_rpls = pd.DataFrame()
            
            for i in range(nb_col_croisement):
                etage_rpls.loc[:, 'etage_{}'.format(i)] = \
                    self.data_rpls.etage.reindex(
                            self.croisement['id_rpls{}'.format(i)]).values
            
            #etage contient les surface extraites pour les airbnb, avec en 
            #index l'id du airbnb (le numéro de la ligne dans data_airbnb)
            etage \
            = pd.Series(etage_tokens).reindex(index=range(data_airbnb.shape[0]))
            
            etage_scoring = etage_rpls.subtract(etage, axis=0)
            etage_scoring = etage_scoring.applymap(Comparateur._etage_score_filtering)
            etage_scoring.index.rename('id_bnb', inplace=True)
            self.etage_scoring = etage_scoring
            
        return self.etage_scoring

    def _nbpiece_score_filtering(x):
        if x == 0:
            return 1
        elif abs(x) == 1:
            return 0.50
        elif abs(x) == 2:
            return 0.20
        elif not pd.isna(x):
            return 0
        else:
            return np.NaN

    def calculer_nbpiece_scoring(self):
        if hasattr(self, 'nbpiece_scoring'):
            print("Les sous_scores de nombre de pièces de chaque airbnb et"
                  ,"leur logement sociaux respectifs sont déjà calculés")
        
        else:
            print("Calcul des sous_scores du nombre de pièce")
            
            if hasattr(self, 'nbpiece_tokens'):
                nbpiece_tokens = self.nbpiece_tokens
            else:
                nbpiece_tokens \
                = self.data_airbnb.bnb.extraire_nbpiece(self.data_airbnb.index.values)
        
            nb_col_croisement = self.croisement.shape[1]
            nbpiece_rpls = pd.DataFrame()    
            for i in range(nb_col_croisement): #pour chaque col
                nbpiece_rpls.loc[:, 'nbpiece_{}'.format(i)] = \
                    self.data_rpls.nbpiece.reindex(
                            self.croisement['id_rpls{}'.format(i)]).values
            
            #etage contient les surface extraites pour les airbnb, avec en index l'id 
            #du airbnb (le numéro de la ligne dans data_airbnb)
            pieces \
            = pd.Series(nbpiece_tokens).reindex(index=range(data_airbnb.shape[0]))
            
            nbpiece_scoring = nbpiece_rpls.subtract(pieces, axis=0)
            nbpiece_scoring = nbpiece_scoring.applymap(Comparateur._nbpiece_score_filtering)
            nbpiece_scoring.index.rename('id_bnb', inplace=True)
            self.nbpiece_scoring = nbpiece_scoring
        
        return self.nbpiece_scoring
    
    def calculer_all_scores(self):
        
        if hasattr(self, 'all_scores'):
            print("Les scores de chaque airbnb et leur logement sociaux"
                  ,"respectifs sont déjà calculés")
        
        else:  
            #Un par un on calcule ou récupère les sous_scores correspondant aux 
            #champs textuels analysés par l'algorithme.
            
            scores = (~self.croisement.isna()).values * self.weights['croisement']
                
            if 'surfhab' in self.weights and hasattr(self, 'surfhab_scoring'):
                scores += \
                self.surfhab_scoring.fillna(0).values * self.weights['surfhab']
            elif 'surfhab' in self.weights:
                self.calculer_surfhab_scoring()
                scores += \
                self.surfhab_scoring.fillna(0).values * self.weights['surfhab']
                
            if 'etage' in self.weights and hasattr(self, 'etage_scoring'):
                scores += \
                self.etage_scoring.fillna(0).values * self.weights['etage']
            elif 'etage' in self.weights:
                self.calculer_etage_scoring()
                scores += \
                self.etage_scoring.fillna(0).values * self.weights['etage']                

            if 'nbpiece' in self.weights and hasattr(self, 'nbpiece_scoring'):
                scores += \
                self.nbpiece_scoring.fillna(0).values * self.weights['nbpiece']
            elif 'nbpiece' in self.weights:
                self.calculer_nbpiece_scoring()
                scores += \
                self.nbpiece_scoring.fillna(0).values * self.weights['nbpiece']  
        
            scores = pd.DataFrame(scores)
            scores.index.rename('id_bnb', inplace=True)
            self.all_scores = scores
            
        return self.all_scores

    def extract_best_match(self):
        
        if hasattr(self, 'all_scores'):
            #On récupère le numéro des colonnes avec le score maximal
            column_score_max = self.all_scores.idxmax(axis=1).values
            score_max = self.all_scores.max(axis=1).values
            
            best_match = -1 * np.ones((self.croisement.shape[0],2)) 
            for idx in range(self.croisement.shape[0]):
                if not pd.isna(self.croisement.iloc[idx, column_score_max[idx]]):
                    best_match[idx,0] \
                    = self.croisement.iloc[idx, column_score_max[idx]]
                    best_match[idx,1] = score_max[idx]
                    
            best_match = pd.DataFrame(best_match)
            best_match.index.rename('id_bnb', inplace=True)
            best_match.rename(columns={0:'id_rpls', 1:'score'}, inplace=True)
            best_match = best_match.astype({'id_rpls':'int64'})
            best_match.replace(to_replace={'score':-1.0}, value={'score':0.0}
            , inplace=True)
        
            self.best_match = best_match
            return best_match   
        
        else:
            self.calculer_all_scores()
            return self.extract_best_match()
        
    def sort_best_match(self):
        if hasattr(self, 'best_match'):
            self.best_match.sort_values(by='score', ascending=False)
        else:
            raise AttributeError("L'ensemble des scores n'a pas été calculé :",
                                 "exécutez la méthode 'calculer_all_scores")

if __name__ == '__main__':

    data_airbnb = pd.read_csv("po_oresys/csv/airbnb.csv", sep=',', header='infer',
                          dtype={'longitude':'float', 'latitude':'float'})
    
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
            
    data_rpls = pd.read_csv("po_oresys/csv/paris_rpls_2017.csv", sep=',',error_bad_lines=False, 
                    header='infer', index_col=0,
                    converters={'codepostal':converter_codepostal
                                , 'etage':converter_etage},
                    dtype={'longitude':'float', 'latitude':'float'})
    
    data_rpls.index.rename('id_rpls', inplace=True)
    
    keep_columns = ['id_bnb']
    for i in range(250):
        keep_columns.append('id_rpls{}'.format(i))
#    dtype = {key:'int64' for key in keep_columns}
    
    croisement_v3 = pd.read_csv('po_oresys/csv/results_rd155_nb250.csv', header='infer'
                          , usecols=keep_columns
                          , index_col='id_bnb'
                          , dtype=pd.Int64Dtype()) 
    
    comparateur = Comparateur(data_airbnb, data_rpls, croisement_v3)
    
    all_scores = comparateur.calculer_all_scores()