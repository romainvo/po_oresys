import numpy as np
""" surface et nombre de piece réel issu du repertoire RPLS, Théorique issu de l'extraction d'information

def CalculScore(surfaceTheo, surfaceReel, nbpieceTheo, nbpieceReel):
    score = ((np.minimum(surfaceTheo/surfaceReel,surfaceReel/surfaceTheo)*np.minimum(surfaceReel/surfaceTheo,surfaceTheo/surfaceReel))/1.25)*100
    on impose un score minimum de 0.25 du fait de la proximité, les 0.75 restants etant calculés via la formule précédente
    score = 25+score
"""
def calculScore(scoreSurface,scoreNbPiece, scoreEtage):
    PoidsEtage=0.25
    PoidsProximite = 0.25
    PoidsSurface = 0.25
    PoidsNbPiece = 1-PoidsEtage-PoidsSurface-PoidsProximite

    """ score total borné entre 0 et 100. Si il est dans la zone de proximite, il est d'office egal à PoidsProximite*100"""
    scoreTotal=(PoidsProximite+PoidsEtage*scoreEtage+PoidsSurface*scoreSurface+PoidsNbPiece*scoreNbPiece)*100

