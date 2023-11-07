import random

def findRandomMove(validMoves):
    for i in range(len(validMoves)):
        if validMoves[i].pieceCaptured == "wQ":
            return validMoves[i]
        elif validMoves[i].pieceCaptured == "wR":
            return validMoves[i]
        elif validMoves[i].pieceCaptured == "wB" or validMoves[i].pieceCaptured == "wN":
            return validMoves[i]
        elif validMoves[i].pieceCaptured != "--":
            return validMoves[i]        
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove():
    pass
