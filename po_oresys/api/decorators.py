import pandas as pd
import re
import numpy as np

@pd.api.extensions.register_dataframe_accessor("rpls")
class RPLSAccessor:
    """ Instancie un décorateur python permettant de manipuler les dataframe
    instanciant des rpls (répertoire des logements sociaux) plus facilement.
    
    Parameters:
        _obj (pd.DataFrame): DataFrame regroupant l'ensemble des logements
        sociaux.
    """
    
    def __init__(self, pandas_obj : pd.DataFrame):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj : pd.DataFrame):
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

    def coordonnees(self, id : int):
        return (self._obj.loc[id,'latitude'], self._obj.loc[id,'longitude'])

    def complete_description(self, id : int, pprint=True, rreturn=False):
        """Print l'ensemble des champs textuels pertinents pour le logement
        social d'iditifiant 'id'
        
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
            
        Keyword arguments:
            pprint (boolean): True si on affiche la description complète

            rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        
        Returns:
            (pd.Series): en index les noms des champs textuels retournés, en 
            élements les string des champs textuels pertinents.
        """
        
        columns = ['libcom','numvoie','typvoie','nomvoie','surfhab', 'etage'
                   ,'nbpiece']
        print("Champs affichés : {}".format(columns[0]), end=" ")
        for elt in columns[1:]:
            print(",",elt, end="")
        print(" - coordonnées gps = {}".format(self.coordonnees(id), "\n"))
        print()
        
        if pprint:
            for elt in columns :
                print("{} :".format(elt), end=" ")
                print(self._obj.loc[id, elt])
            print()
        
        if rreturn:
            return self._obj.loc[id, columns]  
        
    """ renvoie la surface habitable du rpls caractérisé par l'id id
    Parameters:
        id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
    Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
    Return:
        valeur de la surface habitable du rpls id dans le dataframe.(float)
    """
    def surface_habitable(self,id,pprint = True,rreturn = False):
        if(pprint):
            print(self._obj.loc[id,'surfhab'])
        
        if(rreturn):
            return self._obj.loc[id,'surfhab']
 
    
    def nombre_piece(self,id,pprint = True,rreturn = False):
        """ renvoie le nombre de piece du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        valeur du nombre de piece du rpls id dans le dataframe.(float)
        """
        if(pprint):
            print(self._obj.loc[id,'nbpiece'])
        
        if(rreturn):
            return self._obj.loc[id,'nbpiece']
 

    def arrondissement(self,id,pprint = True,rreturn = False):
        """ renvoie l'arrondissement' du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        arrondissement du rpls id dans le dataframe (string).
        """
        if(pprint):
            print(self._obj.loc[id,'libcom'])
        
        if(rreturn):
            return self._obj.loc[id,'libcom']

    def etage(self,id,pprint = True,rreturn = False):
        """ renvoie l'etage' du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        etage du rpls id dans le dataframe (float).
        """
        if(pprint):
            print(self._obj.loc[id,'etage'])
        
        if(rreturn):
            return self._obj.loc[id,'etage']

    def adresse(self,id,pprint = True,rreturn = False):
        """ renvoie l'adresse du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        adresse du rpls id dans le dataframe (string).
        """
        S = self._obj.loc[id,'numvoie']+" "
        if(self._obj.loc[id,'indrep']!=np.nan):
            S=S+self._obj.loc[id,'indrep']
        S=S+self._obj.loc[id,'typvoie']+" "+self._obj.loc[id,'nomvoie']
        if(self._obj.loc[id,'bat']!=np.nan):
            S=S+", batiment "+self.batiment(id,pprint=False,rreturn=True)
        if(self._obj.loc[id,'numappt']!=np.nan):
            S=S+", appartement "+self.numero_appartement(id,pprint=False,rreturn=True)
        if(pprint):
            print(S)
        if(rreturn):
            return S
    
    def batiment(self,id,pprint = True,rreturn = False):
        """ renvoie le batiment du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        batiment du rpls id dans le dataframe (float).
        """

        if(pprint):
            print(self._obj.loc[id,'bat'])
        
        if(rreturn):
            return self._obj.loc[id,'bat']
    
    def numero_appartement(self,id,pprint = True,rreturn = False):
        """ renvoie le numero d'appartement du rpls caractérisé par l'id id
        Parameters:
            id (int): identifiant du logement social. Index de la ligne dans 
            la DataFrame.
        Key arguments:
        pprint (boolean): True si on affiche la description complète

        rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        Return:
        numero d'appartement du rpls id dans le dataframe (float).
        """
        if(pprint):
            print(self._obj.loc[id,'numappt'])
        if(rreturn):
            return self._obj.loc[id,'numappt']

@pd.api.extensions.register_dataframe_accessor("bnb")
class AirbnbAccessor:
    """ Instancie un décorateur python permettant de manipuler les dataframe
    regroupant des annonces airbnb plus facilement.
    
    Parameters:
        _obj (pd.DataFrame): DataFrame regroupant l'ensemble des annonces
        airbnb.
    """
    
    def __init__(self, pandas_obj : pd.DataFrame):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj : pd.DataFrame):
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
   
    def complete_description(self, id : int, pprint=True, rreturn=False):
        """Print l'ensemble des champs textuels pertinents pour l'annonce 
        airbnb d'iditifiant 'id'
        
        Parameters:
            id (int): identifiant de l'annonce airbnb. Index de la ligne dans 
            la DataFrame.
            
        Keyword arguments:
            pprint (boolean): True si on affiche la description complète

            rreturn (boolean): True si on retourne la description complète de 
            l'annonce spécifié sous forme de Series.
        
        Returns:
            (pd.Series): en index les noms des champs textuels retournés, en 
            élements les string des champs textuels pertinents.
        """
        
        columns = ['name', 'summary', 'space', 'description']
        print("Champs affichés : {}".format(columns[0]), end=" ")
        for elt in columns[1:]:
            print(",",elt, end="")
        print(" - coordonnées gps = {}".format(self.coordonnees(id), "\n"))
        print()
        
        if pprint:
            for elt in columns :
                print("{} :".format(elt))
                print(self._obj.loc[id, elt], "\n")
        
        if rreturn:
            return self._obj.loc[id, columns]  
  
    def coordonnees(self, id : int):
        return (self._obj.loc[id,'latitude'], self._obj.loc[id,'longitude'])
    
    def name(self, id : int):
        return self._obj.loc[id, 'name']
    
    def summary(self, id : int):
        return self._obj.loc[id, 'summary']
    
    def description(self, id : int):
        return self._obj.loc[id, 'description']
    
    def all_extractions(self, id : int, pprint=False, rreturn=True):
        extractions = dict()
        extractions['surfhab'] = self.extraire_surfhab(id)
        extractions['etage'] = self.extraire_etage(id)
        extractions['nbpiece'] = self.extraire_nbpiece(id)
        
        if pprint:
            print("Ensemble des champs textuels extraits :")
            print(extractions)
            
        if rreturn:
            return extractions

    def extraire_surfhab(self, id):    
        """Retourne la surface habitable (en mètres carrés) indiquée dans 
        l'annonce airbnb si présente.
        
        Parameters:
            id (int or [int]): identifiant de l'annonce airbnb ou liste
            d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            surfhab (float or {id:surfhab}): surface habitable indiquée dans 
            l'annonce, np.nan si non détectée.
        """
        
        if not hasattr(id, '__iter__'):
            indexes = [id]
        else :
            indexes = id
            
        name_airbnb = self._obj.loc[indexes, 'name']
        summary_airbnb = self._obj.loc[indexes, 'summary']
        space_airbnb = self._obj.loc[indexes, 'space']
        description_airbnb = self._obj.loc[indexes, 'description'] 
    
        pattern_surfhab_meter = r"""(?x)
            (\d+\.?,?\d*)
            (?:
             \s+m.tre.\s+carr.*
            |\s?m2
            |\s?sqm
            |(?:m\s|\sm|m)²
            |\s?square.?\s?met...?
            |\s?sq\.?\s?(?:\.mts|meter.?|\.\s?m)
            |\s?sq\sm
            )
            """
        pattern_surfhab_feet = r"""(?x)
            (\d+\.?,?\d*)
            (?:
             \s?square.?\s?(?:feet|ft|foot)
            |\s?feet²
            |\s?sq\.?\s?(?:f.{0,2}t|\.\s?ft|f|/ft)
            )
            """
        
        surfhab_tokens_feet = dict()
        surfhab_tokens_meter = dict()
        surfhab_tokens = dict()
        
        for idx, row in zip(indexes, description_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    surfhab_tokens_feet[idx] = list(temp_feet)
                    
                if temp_meter:
                    surfhab_tokens_meter[idx] = list(temp_meter)
        
        for idx, row in zip(indexes, name_airbnb):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    if idx not in surfhab_tokens_feet:
                        surfhab_tokens_feet[idx] = list(temp_feet)
                    else:
                        surfhab_tokens_feet[idx] += temp_feet
                    
                if temp_meter:
                    if idx not in surfhab_tokens_meter:
                        surfhab_tokens_meter[idx] = list(temp_meter)  
                    else:
                        surfhab_tokens_meter[idx] += temp_meter
        
        for idx, row in zip(indexes, summary_airbnb):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    if idx not in surfhab_tokens_feet:
                        surfhab_tokens_feet[idx] = list(temp_feet)
                    else:
                        surfhab_tokens_feet[idx] += temp_feet
                    
                if temp_meter:
                    if idx not in surfhab_tokens_meter:
                        surfhab_tokens_meter[idx] = list(temp_meter)  
                    else:
                        surfhab_tokens_meter[idx] += temp_meter
        
        for idx, row in zip(indexes, space_airbnb):
            if not pd.isna(row):
                row = row.lower()
                temp_feet = re.findall(pattern_surfhab_feet, row) 
                temp_meter = re.findall(pattern_surfhab_meter, row)
                    
                if temp_feet:
                    if idx not in surfhab_tokens_feet:
                        surfhab_tokens_feet[idx] = list(temp_feet)
                    else:
                        surfhab_tokens_feet[idx] += temp_feet
                    
                if temp_meter:
                    if idx not in surfhab_tokens_meter:
                        surfhab_tokens_meter[idx] = list(temp_meter)  
                    else:
                        surfhab_tokens_meter[idx] += temp_meter
        
        for key, element in surfhab_tokens_meter.items():
            surfhab_tokens_meter[key] = list(map(lambda x: x.replace(',','.'), element))
            surfhab_tokens_meter[key] = list(map(float, surfhab_tokens_meter[key]))
            surfhab_tokens_meter[key] = max(surfhab_tokens_meter[key])
        
        for key, element in surfhab_tokens_feet.items():
            surfhab_tokens_feet[key] = list(map(lambda x: x.replace(',','.'), element))
            surfhab_tokens_feet[key] = list(map(float, surfhab_tokens_feet[key]))
            surfhab_tokens_feet[key] = max(surfhab_tokens_feet[key])
            surfhab_tokens_feet[key] = surfhab_tokens_feet[key] / 10.764 #1m² = 10.764 feet²
            
        for key in set(list(surfhab_tokens_meter.keys())+list(surfhab_tokens_feet.keys())):
            if (key not in surfhab_tokens_meter) and (key in surfhab_tokens_feet):
                surfhab_tokens[key] = surfhab_tokens_feet[key]
            elif (key in surfhab_tokens_meter) and (key not in surfhab_tokens_feet):
                surfhab_tokens[key] = surfhab_tokens_meter[key]
            elif (key in surfhab_tokens_meter) and (key in surfhab_tokens_feet):
                surfhab_tokens[key] \
                = max(surfhab_tokens_feet[key], surfhab_tokens_meter[key])
        
        if type(id) is int:
            if id in surfhab_tokens:
                return surfhab_tokens[id]
            else:
                return np.nan
        else:
            return surfhab_tokens
        
    def extraire_etage(self, id : int):
        """Retourne le numéro de l'étage indiqué dans l'annonce airbnb si présente.
        
        Parameters:
            id (int or [int]): identifiant de l'annonce airbnb ou liste
            d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            etage (int): numéro de l'étage indiqué dans l'annonce, np.nan si
            non-détecté.
        """
        
        if not hasattr(id, '__iter__'):
            indexes = [id]
        else :
            indexes = id
            
        name_airbnb = self._obj.loc[indexes, 'name']
        summary_airbnb = self._obj.loc[indexes, 'summary']
        space_airbnb = self._obj.loc[indexes, 'space']
        description_airbnb = self._obj.loc[indexes, 'description'] 
        
        pattern_etage_number = r"""(?x)
            (\d+(?:\.\d+)?)
            (?:
             \s*(?:th|d|nd|rd|st|e|.me|°)\s*(?:floor|.tage)
            |\s*(?:th|d|nd|rd|st|e|.me|°)[a-z\s]{0,20}(?:floor|.tage)
            |\s*(?:floor|.tage)
            )
            """
        pattern_etage_letter = r"""(?x)
            (first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|nineth|tenth
            |eleventh|twelveth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth
            |eighteenth|nineteenth|twentieth|ground|rez.de.chauss[a-z]{1,2}
            |premier|deuxi.me|troisi.me[a-z]?|quatri.me[a-z]?|cinqui.me[a-z]?
            |sixi.me[a-z]?|septi.me[a-z]?|huiti.me[a-z]?|neuvi.me[a-z]?|dizi.me[a-z]?
            |onzi.me[a-z]?|douzi.me[a-z]?|treizi.me[a-z]?|quatorzi.me[a-z]?|quinzi.me[a-z]?
            |seizi.me[a-z]?|dix.?septi.me[a-z]?|dix.huiti.me[a-z]?|dix.neuvi.me[a-z]?
            |vingti.me[a-z]?)
            (?:
             \s*(?:floor|.tage)
            |[a-z\s]{0,20}(?:floor|.tage)
            )
            """
        
        letter_to_number \
        = {'first':1,'second':2,'third':3,'fourth':4,'fifth':5
            ,'sixth':6,'seventh':7,'eighth':8,'ninth':9,'nineth':9
            ,'tenth':10,'eleventh':11,'twelveth':12,'thirteenth':13
            ,'fourteenth':14,'fifteenth':15,'sixteenth':16
            ,'seventeenth':17,'eighteenth':18,'nineteenth':19
            ,'twentieth':20,'ground':0,'premier':1,'deuxieme':2
            ,'deuxième':2,'troisieme':3,'troisième':3,'quatrieme':4
            ,'quatrième':4,'cinquieme':5,'cinquième':5,'sixieme':6
            ,'sixième':6,'septieme':7,'septième':7,'huitieme':8
            ,'huitième':8,'neuvieme':9,'neuvième':9,'dixieme':10
            ,'dixième':10,'onzieme':11,'onzième':11,'douzieme':12
            ,'douzième':12,'treizieme':13,'treizième':13,'quatorzieme':14
            ,'quatorzième':14,'quinzieme':15,'quinzième':15
            ,'seizieme':16,'seizième':16,'dix-septieme':17
            ,'dix-septième':17,'dix-huitieme':18,'dix-huitième':18
            ,'dix-neuvieme':19,'dix-neuvième':19,'vingtieme':20
            ,'vingtième':20,'rez-de-chaussée':0,'rez-de-chausee':0
            ,'rez-de-chaussé':0,'rez-de-chausse':0,'rez de chaussée':0
            ,'rez de chaussé':0, 'rez de chaussez':0} 
           
        etage_tokens_number = dict()
        etage_tokens_letter = dict()
        etage_tokens = dict()
        
        for idx, row in zip(indexes, description_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    etage_tokens_number[idx] = list(temp_number)
                    
                if temp_letter:
                    etage_tokens_letter[idx] = temp_letter
                    
        for idx, row in zip(indexes, name_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    if idx not in etage_tokens_number:
                        etage_tokens_number[idx] = list(temp_number)
                    else:
                        etage_tokens_number[idx] += temp_number
        
                if temp_letter:
                    if idx not in etage_tokens_letter:
                        etage_tokens_letter[idx] = list(temp_letter)
                    else:
                        etage_tokens_letter[idx] += temp_letter
                        
        for idx, row in zip(indexes, summary_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    if idx not in etage_tokens_number:
                        etage_tokens_number[idx] = list(temp_number)
                    else:
                        etage_tokens_number[idx] += temp_number
        
                if temp_letter:
                    if idx not in etage_tokens_letter:
                        etage_tokens_letter[idx] = list(temp_letter)
                    else:
                        etage_tokens_letter[idx] += temp_letter
        
        for idx, row in zip(indexes, space_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_number = re.findall(pattern_etage_number, row) 
                temp_letter = re.findall(pattern_etage_letter, row)
                    
                if temp_number:
                    if idx not in etage_tokens_number:
                        etage_tokens_number[idx] = list(temp_number)
                    else:
                        etage_tokens_number[idx] += temp_number
        
                if temp_letter:
                    if idx not in etage_tokens_letter:
                        etage_tokens_letter[idx] = list(temp_letter)
                    else:
                        etage_tokens_letter[idx] += temp_letter
                              
        for key, element in etage_tokens_number.items():
            etage_tokens_number[key] = list(map(float, element))
            etage_tokens_number[key] = min(etage_tokens_number[key])
        
        for key, element in etage_tokens_letter.items():
            etage_tokens_letter[key] \
            = list(map(lambda x: letter_to_number[x], element))
            etage_tokens_letter[key] = min(etage_tokens_letter[key])
            
        for key in set(list(etage_tokens_number.keys())+list(etage_tokens_letter.keys())):
            if (key not in etage_tokens_number) and (key in etage_tokens_letter):
                etage_tokens[key] = etage_tokens_letter[key]
            elif (key not in etage_tokens_letter) and (key in etage_tokens_number):
                etage_tokens[key] = etage_tokens_number[key]
            elif (key in etage_tokens_number) and (key in etage_tokens_letter):
                etage_tokens[key] \
                = min(etage_tokens_number[key], etage_tokens_letter[key])
                
        if type(id) is int:
            if id in etage_tokens:
                return etage_tokens[id]
            else:
                return np.nan
        else:
            return etage_tokens
          
    def extraire_nbpiece(self, id : int):
        """Retourne le nombre de pièces indiqué dans l'annonce airbnb si présente.
        
        Parameters:
            id (int or [int]): identifiant de l'annonce airbnb ou liste
            d'identifiants des annonces airbnb à traiter. Index de la ligne dans 
            la DataFrame.
            
        Returns:
            etage (int): nombre de pièce indiqué dans l'annonce, np.nan si
            non-détecté.
        """
        
        if not hasattr(id, '__iter__'):
            indexes = [id]
        else :
            indexes = id
            
        name_airbnb = self._obj.loc[indexes, 'name']
        summary_airbnb = self._obj.loc[indexes, 'summary']
        space_airbnb = self._obj.loc[indexes, 'space']
        description_airbnb = self._obj.loc[indexes, 'description'] 
        
        pattern_pieces = r"""(?x)
        (\d | (?:\s)a | (?:\s)one | (?:\s)two | (?:\s)three | (?:\s)four 
        | (?:\s)une | (?:\s)deux | (?:\s)trois | (?:\s)quatre )
        (?:
         (?:\s+bedroom\s|\-bedroom\s|bedroom\s|bedrm\s)
        |(?:\s?bdr\s|-?bdr\s|bdr\s)
        |(?:\s?studio\s)
        |\s?bed\s
        |(?:\s?br\s|-?br\s|br\s)
        |(?:\sroom\s|\srooms\s|room\s|rooms\s|r\s|\sr\s)
        |(?:\spi.ce\s|\spi.ces\s|pi.ce\s|pi.ces\s|p\s|\sp\s)
        |(?:\s?chambre|chbr?|\s?chambres?\s|chambre|chbr?|chambres?\s|-?chambre|-+chbr?|-?chambres?\s)
        )
        """
    
        tokens_pieces = dict()
            
        for idx, row in zip(indexes, name_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_pieces = re.findall(pattern_pieces, row) 
    
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three'  or x==' trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
                temp_pieces=[4 if (x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
  
                if temp_pieces:
                    tokens_pieces[idx] = list(temp_pieces)
                
        for idx, row in zip(indexes, summary_airbnb.values):
            if not pd.isna(row):
                row = row.lower() 
                temp_pieces = re.findall(pattern_pieces, row) 
                
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three'  or x==' trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
                temp_pieces=[4 if (x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
                      
                if temp_pieces:
                    if idx not in tokens_pieces:
                        tokens_pieces[idx] = list(temp_pieces) 
                    else:
                        tokens_pieces[idx] += temp_pieces 
    
        for idx, row in zip(indexes, space_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_pieces = re.findall(pattern_pieces, row) 
                
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three'  or x==' trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
                temp_pieces=[4 if (x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
                      
                if temp_pieces:
                    if idx not in tokens_pieces:
                        tokens_pieces[idx] = list(temp_pieces) 
                    else:
                        tokens_pieces[idx] += temp_pieces 
                    
        for idx, row in zip(indexes, description_airbnb.values):
            if not pd.isna(row):
                row = row.lower()
                temp_pieces = re.findall(pattern_pieces, row) 
                
                temp_pieces=[1 if (x==' a' or x==' one' or x=='\ta' or x=='\tone' or x=='\xa0one' or x=='\xa0a' or x==' une' or x=='\tune' or x=='\xa0une') else x for x in temp_pieces]
                temp_pieces=[2 if (x==' two' or x=='\ttwo' or x=='\xa0two' or x==' deux' or x=='\tdeux' or x=='\xa0deux') else x for x in temp_pieces]
                temp_pieces=[3 if (x==' three' or x=='\tthree' or x=='\xa0three'  or x==' trois' or x=='\ttrois' or x=='\xa0trois') else x for x in temp_pieces]
                temp_pieces=[4 if (x==' four' or x=='\tfour' or x=='\xa0four'  or x==' quatre' or x=='\tquatre' or x=='\xa0quatre') else x for x in temp_pieces]
                      
                if temp_pieces:
                    if idx not in tokens_pieces:
                        tokens_pieces[idx] = list(temp_pieces) 
                    else:
                        tokens_pieces[idx] += temp_pieces 
        
        for key, element in tokens_pieces.items():
            tokens_pieces[key] = list(map(float, element))
        
        for key, element in tokens_pieces.items():
            tokens_pieces[key] = max(element)
            tokens_pieces[key] = tokens_pieces[key] + 1

        if type(id) is int:
            if id in tokens_pieces:
                return tokens_pieces[id]
            else:
                return np.nan
        else:
            return tokens_pieces
        
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

