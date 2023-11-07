from stockfish import Stockfish

stockfish = Stockfish("StockfishSrc/stockfish-windows-x86-64-avx2.exe")

def notationValidation(FEN):
    return stockfish.is_fen_valid(FEN)