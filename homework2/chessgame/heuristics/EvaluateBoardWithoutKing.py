from chessgame import StateChessGame
from .constants import *


# 13 microsecondi
# min = -9999
# max = 9999
class EvaluateBoardWithoutKing:
    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.normalize_result = normalize_result
        self.h_max_value = 99
        self.h_min_value = -99

    def h(self, state: StateChessGame):
        if self.evaluate_end_game_phase:
            return self.__h(state.game_board)
        elif self.normalize_result:
            raw_eval = self.__h(state.game_board)
            return self.__normalize(raw_eval)
        else:
            return self.__h(state.game_board)

    def __h(self, board):
        if self.evaluate_end_game_phase:
            game_over_eval = None
            if board.is_checkmate():
                outcome = board.outcome()
                if outcome is not None:
                    if outcome.winner:
                        game_over_eval = float("inf")
                    else:
                        game_over_eval = float("-inf")
            if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                game_over_eval = 0

            if game_over_eval is not None:
                return game_over_eval
        # Se la partita è finita, restituisce un valore molto alto o molto basso
        if board.is_game_over():
            if board.is_checkmate():
                return -99 if board.turn else 99
            else:
                return 0  # Gestisce stallo e materiale insufficiente

        # Valutazione basata sui soli pezzi, ottimizzata
        eval = sum(PIECE_VALUE[piece] * (len(board.pieces(piece, chess.WHITE)) - len(board.pieces(piece, chess.BLACK)))
                   for piece in PIECE_VALUE)

        # Aggiungi qui altre euristiche, come la posizione dei pezzi, la mobilità, ecc.

        # Preferisce chi ha il turno di gioco, dato che potrebbe avere l'iniziativa
        eval += 0.1 if board.turn else -0.1

        return eval

    def __normalize(self, value):
        # Normalizza il valore in un range da -100 a +100
        if value >= 0:
            # Normalizzazione per valori positivi
            normalized = (value / self.h_max_value) * 100
        else:
            # Normalizzazione per valori negativi
            normalized = (value / abs(self.h_min_value)) * 100

        # Limita il valore normalizzato tra -100 e +100
        normalized = max(min(normalized, 100), -100)
        return normalized
