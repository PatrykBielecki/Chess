import random
import chess
import chess.engine

def useEngine(game_state, validMoves, engineWhite, engineBlack):
    translatedFEN = traslateToFEN(game_state)
    bestMove = ''
    if (game_state.whiteToMove): 
        if (engineWhite == 'MINMAX'):       return findMinmaxMove(validMoves)
        elif (engineWhite == 'NEGAMAX'):    return getNegaMaxMove(game_state, validMoves)
        elif (engineWhite == 'LC0'):        bestMove = getLc0Move(translatedFEN)
        elif (engineWhite == 'FATFRITZ2'):  bestMove = getFatFritz2Move(translatedFEN)
        elif (engineWhite == 'STOCKFISH'):  bestMove = getStockfishMove(translatedFEN)
    else:
        if (engineBlack == 'MINMAX'):       return findMinmaxMove(validMoves)
        elif (engineBlack == 'NEGAMAX'):    return getNegaMaxMove(game_state, validMoves)
        elif (engineBlack == 'LC0'):        bestMove = getLc0Move(translatedFEN)
        elif (engineBlack == 'FATFRITZ2'):  bestMove = getFatFritz2Move(translatedFEN)
        elif (engineBlack == 'STOCKFISH'):  bestMove = getStockfishMove(translatedFEN)

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
        return findMinmaxMove(validMoves)

def findMinmaxMove(validMoves):
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
        result = engine.play(board, chess.engine.Limit(time = random.uniform(0.5, 2)))

        # Get the best move
        best_move = result.move

    #print(best_move.uci())
    return best_move.uci()
    
def getFatFritz2Move(fen, depth=3):
    # Set the path to your Lc0 executable
    fatFritz2_path = 'FatFritz2\FatFritz2.exe'

    # Create a chess.Board object from the FEN string
    board = chess.Board(fen)

    # Create a Lc0 engine
    with chess.engine.SimpleEngine.popen_uci(fatFritz2_path) as engine:
        # Set the position on the board
        result = engine.play(board, chess.engine.Limit(time = random.uniform(0.5, 2)))

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
        result = engine.play(board, chess.engine.Limit(time = random.uniform(0.5, 2)))

        # Get the best move
        best_move = result.move

    #print(best_move.uci())
    return best_move.uci()





piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def getNegaMaxMove(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.whiteToMove else -1)
    traslateToFEN(game_state)
    return next_move


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score
