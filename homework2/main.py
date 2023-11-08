import os
from timeit import timeit

import chess
from itertools import islice

# Assegna un valore ai pezzi secondo il principio comune
piece_value = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # Il valore del re è gestito separatamente
}


# Valuta la scacchiera
def evaluate_board(board):
    # Se la partita è finita, restituisce un valore molto alto o molto basso
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Valutazione basata sui soli pezzi
    eval = 0
    for piece_type in piece_value.keys():
        eval += len(board.pieces(piece_type, chess.WHITE)) * piece_value[piece_type]
        eval -= len(board.pieces(piece_type, chess.BLACK)) * piece_value[piece_type]

    # Aggiungi qui altre euristiche, come la posizione dei pezzi, la mobilità, ecc.

    # Preferisce chi ha il turno di gioco, dato che potrebbe avere l'iniziativa
    eval += 0.1 if board.turn == chess.WHITE else -0.1

    return eval


# if __name__ == '__main__':
#     board = chess.Board()
#     moves = board.legal_moves
#     move = next(islice(moves, 19, 20), None)
#     print(board)
#     board.push(move)
#     print(board)
#     print(evaluate_board(board))
#     print(os.cpu_count())

if __name__ == '__main__':
      board = chess.Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
      moves = board.legal_moves
      evaluation = EvaluatePawnStructure()
      print(board)
      print()
      print(evaluation.h(board))
      move = next(islice(moves, 10, 11), None)
      board.push(move)
      print(board)
      print(evaluation.h(board))

