""" surface et nombre de piece réel issu du repertoire RPLS, Théorique issu de l'extraction d'information"""

def CalculScore(surfaceTheo, surfaceReel, nbpieceTheo, nbpieceReel):
    score = (min(surfaceTheo/surfaceReel,surfaceReel/surfaceTheo)*min(surfaceReel/surfaceTheo,surfaceTheo/surfaceReel))/1.25
    """ on impose un score minimum de 0.25 du fait de la proximité, les 0.75 restants etant calculés via la formule précédente"""
    score = 0.25+score

