import numpy as np

from chessgame import StateChessGame
from .EvaluateBoardWithoutKing import EvaluateBoardWithoutKing
from .EvaluateCentralControlScore import EvaluateCentralControlScore
from .EvaluateKingSafety import EvaluateKingSafety
from .EvaluatePiecePositions import EvaluatePiecePositions


class SoftBoardEvaluationChessGame:
    def __init__(self, balance_evaluation=True, print_evaluation=False):
        self.balance_evaluation = balance_evaluation
        self.print_evaluation = print_evaluation
        self.evaluate_board_without_king = EvaluateBoardWithoutKing(normalize_result=True)
        self.evaluate_central_control_score = EvaluateCentralControlScore(normalize_result=True)
        self.evaluate_king_safety = EvaluateKingSafety(normalize_result=True)
        self.evaluate_piece_positions = EvaluatePiecePositions(normalize_result=True)

    def h(self, state: StateChessGame):
        board = state.game_board
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
        else:
            board_without_king = self.evaluate_board_without_king.h(state)
            central_control_score = self.evaluate_central_control_score.h(state)
            king_safety = self.evaluate_king_safety.h(state)
            piece_positions = self.evaluate_piece_positions.h(state)
            if self.print_evaluation:
                print("Valutazione: ", board_without_king, central_control_score, king_safety, piece_positions)
            if self.balance_evaluation:
                return (
                        board_without_king * 0.35 +  # Bilancio del materiale
                        central_control_score * 0.20 +  # Controllo del centro
                        king_safety * 0.25 +  # Sicurezza del re
                        piece_positions * 0.20  # Posizione dei pezzi
                )
            return (
                    board_without_king +
                    central_control_score +
                    king_safety +
                    piece_positions
            )
