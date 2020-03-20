import numpy as np 
import pandas as pd 
import po_oresys.api.decorators 
import po_oresys.api.data_loader as data_loader

class Comparateur:
    
    def __init__(self, airbnb_path=None, rpls_path=None, croisement_path=None
                 , scores_path=None
                 , poids_sous_scores={'croisement':0.2, 'surfhab':0.3
                                      , 'etage':0.3, 'nbpiece':0.2}
                 , surfhab_tokens=None, etage_tokens=None, nbpiece_tokens=None):

        self.data_airbnb = data_loader.import_data_airbnb(airbnb_path)
        self._validate_airbnb(self.data_airbnb)
    
        self.data_rpls = data_loader.import_data_rpls(rpls_path)
        self._validate_rpls(self.data_rpls)
            
        self.croisement = data_loader.import_croisement(croisement_path)
        self._validate_croisement(self, self.croisement)
        
        self.all_scores = data_loader.import_scores(scores_path)
        self._validate_all_scores(self, self.all_scores)
        
        self.weights = poids_sous_scores    
        
        if surfhab_tokens is not None:
            self.surfhab_tokens = surfhab_tokens
        if etage_tokens is not None:
            self.etage_tokens = etage_tokens
        if nbpiece_tokens is not None:
            self.nbpiece_tokens = nbpiece_tokens

    @staticmethod
    def _validate_airbnb(obj : pd.DataFrame):
        """ Vérifie si la DataFrame regroupe bien un ensemble d'annonces airbnb,
        utilisé au moment de "l'instanciation" du décorateur.
        
        Parameters:
            _obj (pd.DataFrame): DataFrame regroupant l'ensemble des annonces
            airbnb.
        
        Raise:
            AttributeError: si le format n'est pas respecté
        """     

        columns = {'name','summary','space','description','longitude','latitude'}
        if not columns.issubset(set(obj.columns)):
            raise AttributeError("Must have {}".format(list(columns)))

    @staticmethod
    def _validate_rpls(obj : pd.DataFrame):
        """ Vérifie si la DataFrame regroupe bien un ensemble de logements 
        sociaux. Utilisé au moment de "l'instanciation" du décorateur.
        
        Parameters:
            obj (pd.DataFrame): DataFrame regroupant l'ensemble des logements
            sociaux.
        
        Raise:
            AttributeError: si le format n'est pas respecté
        """     

        columns = {'libcom','numvoie','typvoie','nomvoie','surfhab', 'etage'
                   ,'nbpiece' ,'longitude','latitude'}
        if not columns.issubset(set(obj.columns)):
            raise AttributeError("Must have {}".format(list(columns)))

    @staticmethod
    def _validate_croisement(self, obj : pd.DataFrame):
        if not self.data_airbnb.index.equals(obj.index):
            raise ValueError("'croisement' ne correspond ne croise pas les annonces",
                             "airbnb contenu dans 'self.airbnb'")
    @staticmethod            
    def _validate_all_scores(self, obj : pd.DataFrame):
        if not self.data_airbnb.index.equals(obj.index):
            raise ValueError("'all_scores' ne correspond ne calcule pas les scores",
                             "des pairs 'AirBnB/logement social' résultat du produit",
                             "cartésien de self.airbnb.index par self.rpls.index")

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
            
            if not hasattr(self, 'surfhab_tokens'):
                print("...Text mining en cours - surfhab non extrait")
                self.surfhab_tokens \
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
            = pd.Series(self.surfhab_tokens).reindex(index=range(self.data_airbnb.shape[0]))

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
            
            if not hasattr(self, 'etage_tokens'):
                print("...Text mining en cours - etage non extrait")
                self.etage_tokens \
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
            = pd.Series(self.etage_tokens).reindex(index=range(self.data_airbnb.shape[0]))
            
            etage_scoring = etage_rpls.subtract(etage, axis=0)
            etage_scoring = etage_scoring.applymap(self._etage_score_filtering)
            etage_scoring.index.rename('id_bnb', inplace=True)
            self.etage_scoring = etage_scoring
            
        return self.etage_scoring

    @staticmethod
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
            
            if not hasattr(self, 'nbpiece_tokens'):
                print("...Text mining en cours - nombre de pièce non extrait")
                self.nbpiece_tokens \
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
            = pd.Series(self.nbpiece_tokens).reindex(index=range(self.data_airbnb.shape[0]))
            
            nbpiece_scoring = nbpiece_rpls.subtract(pieces, axis=0)
            nbpiece_scoring = nbpiece_scoring.applymap(self._nbpiece_score_filtering)
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
                if not pd.isna(self.croisement.iloc[idx, int(column_score_max[idx])]):
                    best_match[idx,0] \
                    = self.croisement.iloc[idx, int(column_score_max[idx])]
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
            self.best_match.sort_values(by='score', ascending=False, inplace=True)
        else:
            raise AttributeError("L'ensemble des scores n'a pas été calculé :",
                                 "exécutez la méthode 'calculer_all_scores")

if __name__ == '__main__':

    comparateur = Comparateur()
    comparateur.extract_best_match()
    comparateur.sort_best_match()
    best_match = comparateur.best_match
    
    #comparateur.comparer(id_airbnb, id_rpls)

#    # ----------------------- EVALUER LE SCORING ---------------------------- #
#
#    #Nombre de airbnb avec 0 rpls dans le rayon d'anonymisation de 150m
#    #((~croisement_v3.isna()).sum(axis=1) == 0).sum()
#    #Statistique nombre de croisements : 
#    #(~croisement_v3.isna()).sum(axis=1).describe()
#
#    tranche_score = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
#    tranche_index = []
#    tranche_nombre = []
#    quantiles = []
#    
#    somme_cumulee = 0
#    for i, tranche in enumerate(tranche_score):
#        if tranche == 100:
#            break
#        elif i == (len(tranche_score) - 2):
#            nb_temp = best_match.loc[(best_match.score >= tranche/100)
#                    & (best_match.score <= tranche_score[i+1]/100)].shape[0]
#            
#            somme_cumulee += nb_temp           
#        else:            
#            nb_temp = best_match.loc[(best_match.score >= tranche/100)
#                        & (best_match.score < tranche_score[i+1]/100)].shape[0]
#            
#            somme_cumulee += nb_temp
#        
#        tranche_nombre.append(nb_temp)
#        tranche_index.append("{}% - {}%".format(tranche, tranche_score[i+1]))
#        print("Détections avec une suspicion entre {}% et {}% : {} -- somme cumulée : {}"
#              .format(tranche, tranche_score[i+1], nb_temp, somme_cumulee))
#    
#    tranche_index[0] = "no detection"
#    print("\n","Moyenne des score : {}".format(best_match.score.mean()))
#    print("Ecart-type : {}".format(best_match.score.std()))
#    print("On affiche les différents déciles", "\n")      
#    
#    for i, score in enumerate(tranche_score):
#        quantiles.append(best_match.score.quantile(score/100))
#        print("Quantile {}% : {}".format(i, quantiles[i]))           
#    
#    import matplotlib.pyplot as plt
#    import seaborn as sns
#    
#    plt.style.use('seaborn-darkgrid')
##    plt.rcParams.update({'font.size':15})
##    plt.rcParams["figure.figsize"] = (50,40)
#    
#    fig, ax = plt.subplots()
#    ax.set_title("Distribution des scores")
#    sns.barplot(y=tranche_nombre, x=tranche_index
#                , orient='v', ax=ax, edgecolor='white')  
#    
#    fig_q, ax_q = plt.subplots()
#    ax_q.set_title("Quantiles des scores")
#    sns.barplot(y=quantiles, x=tranche_score
#                , orient='v', ax=ax_q, edgecolor='white')  