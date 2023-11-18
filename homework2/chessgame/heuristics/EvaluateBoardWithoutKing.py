from chessgame import StateChessGame
from .constants import *


# 13 microsecondi
# min = -9999
# max = 9999
class EvaluateBoardWithoutKing:
    """
    Provides heuristic evaluation of a chess board state, focusing on piece values and game conditions.

    Attributes:
        evaluate_end_game_phase (bool): Flag to indicate whether to evaluate endgame phases differently.
        normalize_result (bool): Flag to indicate whether to normalize the evaluation result.
        h_max_value (int): Maximum heuristic value for normalization.
        h_min_value (int): Minimum heuristic value for normalization.
    """

    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        """
        Initializes the evaluator with options for endgame evaluation and result normalization.

        :param evaluate_end_game_phase: Set to True to evaluate endgame phases differently.
        :param normalize_result: Set to True to normalize the evaluation result.
        """
        self.evaluate_end_game_phase = evaluate_end_game_phase  # Flag to evaluate endgame phases.
        self.normalize_result = normalize_result  # Flag to normalize the evaluation result.
        self.h_max_value = 99  # Maximum heuristic value for normalization.
        self.h_min_value = -99  # Minimum heuristic value for normalization.

    def h(self, state: StateChessGame):
        """
        Evaluates the heuristic of a given game state.

        :param state: StateChessGame object representing the current state of the chess game.
        :return: The heuristic value of the state.
        """
        # Evaluates endgame phase or normalizes the result based on the flags set in the constructor.
        if self.evaluate_end_game_phase:
            return self.__h(state.game_board)
        elif self.normalize_result:
            raw_eval = self.__h(state.game_board)
            return self.__normalize(raw_eval)
        else:
            return self.__h(state.game_board)

    def h_piccolo(self, board):
        """
        Similar to h() but operates directly on a chess board and allows specifying normalization bounds.

        :param board: The chess board to evaluate.
        :return: The heuristic value of the board.
        """
        # Evaluates the endgame phase, normalizes the result, or provides raw evaluation.
        if self.evaluate_end_game_phase:
            return self.__h(board)
        elif self.normalize_result:
            raw_eval = self.__h(board)
            return self.__normalize(raw_eval, 10, -10)
        else:
            return self.__h(board)

    def __h(self, board):
        """
        Private method for raw heuristic evaluation of a board.

        :param board: The chess board to evaluate.
        :return: The raw heuristic value of the board.
        """
        # Special handling for endgame phase.
        if self.evaluate_end_game_phase:
            game_over_eval = None
            # Assign extreme values for checkmate situations.
            if board.is_checkmate():
                outcome = board.outcome()
                if outcome is not None:
                    game_over_eval = float("inf") if outcome.winner else float("-inf")
            # Assign zero for draw situations.
            if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                game_over_eval = 0

            if game_over_eval is not None:
                return game_over_eval

        # If the game is over, returns high positive or negative values for checkmate, and zero for other endings.
        if board.is_game_over():
            if board.is_checkmate():
                return -99 if board.turn else 99
            else:
                return 0  # Handles stalemate and insufficient material.

        # Piece-based evaluation, optimized.
        eval = sum(PIECE_VALUE[piece] * (len(board.pieces(piece, chess.WHITE)) - len(board.pieces(piece, chess.BLACK)))
                   for piece in PIECE_VALUE)
        # Slightly favors the player whose turn it is, as they might have the initiative.
        eval += 0.1 if board.turn else -0.1

        return eval

    def __normalize(self, value, maxv=100, minv=-100):
        """
        Normalizes the evaluation value within a specified range.

        :param value: The value to be normalized.
        :param maxv: The maximum value for normalization. Defaults to 100.
        :param minv: The minimum value for normalization. Defaults to -100.
        :return: The normalized value.
        """
        # Normalizes the value within the range from minv to maxv.
        if value >= 0:
            # Normalizes positive values.
            normalized = (value / self.h_max_value) * 100
        else:
            # Normalizes negative values.
            normalized = (value / abs(self.h_min_value)) * 100

        # Limits the normalized value between minv and maxv.
        normalized = max(min(normalized, maxv), minv)
        return normalized
