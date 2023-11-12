import chess
import numpy as np


# 32 microsecondi
# min 0
# max 84
class EvaluateMobility:
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
