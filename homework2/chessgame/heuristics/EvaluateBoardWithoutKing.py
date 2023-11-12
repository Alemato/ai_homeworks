import numpy as np

from constants import *


# 13 microsecondi
# min = -9999
# max = 9999
class EvaluateBoardWithoutKing:
    def __init__(self, evaluate_end_game_phase=False):
        self.evaluate_end_game_phase = evaluate_end_game_phase

    def h(self, board):
        if self.evaluate_end_game_phase:
            game_over_eval = None
            if board.is_checkmate():
                outcome = board.outcome()
                if outcome is not None:
                    if outcome.winner:
                        game_over_eval = np.inf
                    else:
                        game_over_eval = -np.inf
            if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                game_over_eval = 0

            if game_over_eval is not None:
                return game_over_eval
        # Se la partita è finita, restituisce un valore molto alto o molto basso
        if board.is_game_over():
            if board.is_checkmate():
                return -9999 if board.turn else 9999
            else:
                return 0  # Gestisce stallo e materiale insufficiente

        # Valutazione basata sui soli pezzi, ottimizzata
        eval = sum(PIECE_VALUE[piece] * (len(board.pieces(piece, chess.WHITE)) - len(board.pieces(piece, chess.BLACK)))
                   for piece in PIECE_VALUE)

        # Aggiungi qui altre euristiche, come la posizione dei pezzi, la mobilità, ecc.

        # Preferisce chi ha il turno di gioco, dato che potrebbe avere l'iniziativa
        eval += 0.1 if board.turn else -0.1

        return eval
