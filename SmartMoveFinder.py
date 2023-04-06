import random




def findRandomMove(validMoves):
 #   for i in range(len(validMoves)):
        #if validMoves[i].pieceCaptured != "--":
        #    return validMoves[i]        
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove():
    pass
