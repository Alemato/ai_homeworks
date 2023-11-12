import chess
import numpy as np

from chessgame import StateChessGame


# 32 microsecondi
# min 0
# max 84
class EvaluateMobility:
    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.normalize_result = normalize_result
        self.h_max_value = 168
        self.h_min_value = -168

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
                        game_over_eval = np.inf
                    else:
                        game_over_eval = -np.inf
            if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                game_over_eval = 0

            if game_over_eval is not None:
                return game_over_eval
        white_mobility = 0
        black_mobility = 0

        # Calculate mobility in one pass over the legal moves
        for move in board.legal_moves:
            if board.color_at(move.from_square) == chess.WHITE:
                white_mobility += 1
            else:
                black_mobility += 1

        mobility_balance = white_mobility - black_mobility
        return mobility_balance if board.turn == chess.WHITE else -mobility_balance

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
