import random
import StockfishEngine

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

def findBestMove(board):
    traslateToFEN(board)


def traslateToFEN(board):
    #print(board)
    result = ""
    for i in range(len(board)):
        empty = 0
        for j in range(len(board)):
            c = board[i][j][0]
            if c == 'w' or c == 'b':
                if empty > 0:
                    result += str(empty)
                    empty = 0
                if c == 'w':
                    result += board[i][j][1].upper()
                else:
                    result += board[i][j][1].lower()
            else:
                empty += 1
        if empty > 0:
            result += str(empty)
        if i < len(board) - 1:
          result += '/'
    result += ' w KQkq - 0 1'

    print(result)
    #print(StockfishEngine.notationValidation())
    
    return result
    