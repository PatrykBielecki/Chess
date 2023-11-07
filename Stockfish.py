from stockfish import Stockfish

stockfish = Stockfish("StockfishSrc/stockfish-windows-x86-64-avx2.exe")

print(stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))