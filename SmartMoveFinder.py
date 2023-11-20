import random
import chess
import chess.engine

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


def findBestMove(game_state, validMoves):
    if (game_state.whiteToMove): 
        bestMove = getLc0Move(traslateToFEN(game_state))
    else: 
        bestMove = getStockfishMove(traslateToFEN(game_state))
    startCol = ord(bestMove[0]) - ord('a')
    startRow = ((int(bestMove[1]) - 1) - 7) * -1
    endCol = ord(bestMove[2]) - ord('a')
    endRow = ((int(bestMove[3]) - 1) - 7) * -1
    index_found = None
    for i, obj in enumerate(validMoves):
        if (
            obj.startRow == startRow and
            obj.startCol == startCol and
            obj.endRow == endRow and
            obj.endCol == endCol
        ):
            index_found = i
            break

    if index_found is not None:
        return validMoves[index_found]
    else:
        print("Object not found, tried: ", startCol, startRow, endCol, endRow)
        print(traslateToFEN(game_state))
        for i in range(len(validMoves)):
            print(validMoves[i].startCol, validMoves[i].startRow, validMoves[i].endCol, validMoves[i].endRow)
        print("---------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------")
        return findRandomMove(validMoves)
    


def traslateToFEN(game_state):
    result = ""
    for i in range(len(game_state.board)):
        empty = 0
        for j in range(len(game_state.board)):
            c = game_state.board[i][j][0]
            if c == 'w' or c == 'b':
                if empty > 0:
                    result += str(empty)
                    empty = 0
                if c == 'w':
                    result += game_state.board[i][j][1].upper()
                else:
                    result += game_state.board[i][j][1].lower()
            else:
                empty += 1
        if empty > 0:
            result += str(empty)
        if i < len(game_state.board) - 1:
          result += '/'

    if (game_state.whiteToMove): 
        result += ' w '
    else:
        result += ' b '

    castlingRights = game_state.currentCastlingRight

    #castle rights in FEN notation
    if not (castlingRights.wks or castlingRights.wqs or castlingRights.bks or castlingRights.bqs):
        result += ' - '
    if (castlingRights.wks):
        result += 'K'
    if (castlingRights.wqs):
        result += 'Q'
    if (castlingRights.bks):
        result += 'k'
    if (castlingRights.bqs):
        result += 'q'

    result += ' '

    if(game_state.enPassantPossible): # enpasant
        enPassantCol = chr(game_state.enPassantPossible[1] + ord('a'))
        enPassantRow = ((int(game_state.enPassantPossible[0]) - 1) - 7) * -1
        result += enPassantCol + str(enPassantRow)
    else:
        result += '-' 

    result += ' '

    if(game_state.fiftyMoveRuleCounter > 0):   
        result += str(int(game_state.fiftyMoveRuleCounter)) #fifty-move rule
    else:
        result += str(game_state.fiftyMoveRuleCounter)
    
    result += ' '

    result += str(game_state.moveNumber) 
    
    return result



def getStockfishMove(fen, depth=3):
    # Set the path to your Stockfish executable
    stockfish_path = "StockfishSrc/stockfish-windows-x86-64-avx2.exe"

    # Create a chess.Board object from the FEN string
    board = chess.Board(fen)

    # Create a Stockfish engine
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        # Set the position on the board
        result = engine.play(board, chess.engine.Limit(random.uniform(0.1, 2.0)))

        # Get the best move
        best_move = result.move

    #print(best_move.uci())
    return best_move.uci()
    
def getLc0Move(fen, depth=3):
    # Set the path to your Lc0 executable
    lc0_path = "Lc0Src\lc0.exe"

    # Create a chess.Board object from the FEN string
    board = chess.Board(fen)

    # Create a Lc0 engine
    with chess.engine.SimpleEngine.popen_uci(lc0_path) as engine:
        # Set the position on the board
        result = engine.play(board, chess.engine.Limit(random.uniform(0.1, 2.0)))

        # Get the best move
        best_move = result.move

    #print(best_move.uci())
    return best_move.uci()
    