import numpy as np

from chessgame import StateChessGame
from chessgame.heuristics.EvaluateBoardWithoutKing import EvaluateBoardWithoutKing
from chessgame.heuristics.EvaluateCentralControlScore import EvaluateCentralControlScore
from chessgame.heuristics.EvaluateKingSafety import EvaluateKingSafety
from chessgame.heuristics.EvaluateMobility import EvaluateMobility
from chessgame.heuristics.EvaluatePawnStructure import EvaluatePawnStructure
from chessgame.heuristics.EvaluatePiecePositions import EvaluatePiecePositions


class HardBoardEvaluationChessGame:
    def __init__(self):
        self.evaluate_board_without_king = EvaluateBoardWithoutKing(normalize_result=True)
        self.evaluate_central_control_score = EvaluateCentralControlScore(normalize_result=True)
        self.evaluate_king_safety = EvaluateKingSafety(normalize_result=True)
        self.evaluate_mobility = EvaluateMobility(normalize_result=True)
        self.evaluate_pawn_structure = EvaluatePawnStructure(normalize_result=True)
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
            return (
                    self.evaluate_board_without_king.h(state) +
                    self.evaluate_central_control_score.h(state) +
                    self.evaluate_king_safety.h(state) +
                    self.evaluate_mobility.h(state) +
                    self.evaluate_pawn_structure.h(state) +
                    self.evaluate_piece_positions.h(state)
            )
