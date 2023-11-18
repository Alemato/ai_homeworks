import chess

from chessgame import StateChessGame


# 32 microsecondi
# min 0
# max 84
class EvaluateMobility:
    """
    This class evaluates the mobility of pieces in a chess game. It calculates a score based on
    the number of legal moves available for white and black, representing the degree of freedom
    and potential for offensive or defensive actions in the game.

    Attributes:
        evaluate_end_game_phase (bool): Indicates if the endgame should be evaluated differently.
        normalize_result (bool): Determines if the evaluation score should be normalized.
        h_max_value (float): The upper limit for normalization of the heuristic score.
        h_min_value (float): The lower limit for normalization of the heuristic score.
    """

    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        """
        Initializes the evaluator with options for endgame evaluation and result normalization.

        :param evaluate_end_game_phase: Set to True for specialized evaluations in endgame phases.
        :param normalize_result: Set to True to normalize the evaluation score within a range.
        """
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.normalize_result = normalize_result
        self.h_max_value = 90  # Max heuristic value for normalization.
        self.h_min_value = -10  # Min heuristic value for normalization.

    def h(self, state: StateChessGame):
        """
        Evaluates the mobility based on the current game state. Determines if special handling
        for the endgame or normalization of results is required.

        :param state: StateChessGame object representing the current state of the chess game.
        :return: A heuristic value representing the mobility balance.
        """
        # Applies endgame evaluation or normalization based on the initialization flags.
        if self.evaluate_end_game_phase:
            return self.__h(state.game_board)
        elif self.normalize_result:
            raw_eval = self.__h(state.game_board)
            return self.__normalize(raw_eval)
        else:
            return self.__h(state.game_board)

    def h_piccolo(self, board):
        """
        A similar function to h(), but operates directly on a chess board and allows for custom
        normalization bounds.

        :param board: The chess board to evaluate.
        :return: A heuristic value representing the mobility balance.
        """
        # Handles endgame evaluation or normalization based on the board state.
        if self.evaluate_end_game_phase:
            return self.__h(board)
        elif self.normalize_result:
            raw_eval = self.__h(board)
            return self.__normalize(raw_eval, 10, -10)
        else:
            return self.__h(board)

    def __h(self, board):
        """
        Private method for the raw heuristic evaluation of mobility on the board. It calculates
        the difference in the number of legal moves available to each player.

        :param board: The chess board to evaluate.
        :return: The raw heuristic value representing the mobility balance.
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
        white_mobility = 0
        black_mobility = 0

        # Calculate the mobility for both white and black pieces.
        for move in board.legal_moves:
            if board.color_at(move.from_square) == chess.WHITE:
                white_mobility += 1
            else:
                black_mobility += 1

        mobility_balance = white_mobility - black_mobility
        # Return the mobility balance, adjusted for the current player's turn.
        return mobility_balance if board.turn == chess.WHITE else -mobility_balance

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
