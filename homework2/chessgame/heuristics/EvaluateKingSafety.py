import chess

from chessgame import StateChessGame


# 12.1 microsecondi
# min = -7.5 -8.5
# max = 7.5 8.5
class EvaluateKingSafety:
    """
    A class to evaluate the safety of the king in a chess game. It assesses the level of threat or safety
    for both kings based on the game board configuration.

    Attributes:
        evaluate_end_game_phase (bool): Flag to indicate if endgame phases should be evaluated differently.
        normalize_result (bool): Flag to determine if the evaluation result should be normalized.
        h_max_value (float): Maximum heuristic value for normalization purposes.
        h_min_value (float): Minimum heuristic value for normalization purposes.
    """
    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        """
        Initializes the evaluator with options for endgame evaluation and result normalization.

        :param evaluate_end_game_phase: Set to True to apply special evaluations in endgame phases.
        :param normalize_result: Set to True to normalize the evaluation score within a specific range.
        """
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.normalize_result = normalize_result
        self.h_max_value = 9.5  # Max heuristic value for normalization.
        self.h_min_value = -9.5  # Min heuristic value for normalization

    def h(self, state: StateChessGame):
        """
        Evaluates the safety of the king based on the current game state.

        :param state: StateChessGame object representing the current state of the chess game.
        :return: The heuristic value representing the king's safety.
        """
        # Applies special endgame evaluation or normalization as per the initialization flags.
        if self.evaluate_end_game_phase:
            return self.__h(state.game_board)
        elif self.normalize_result:
            raw_eval = self.__h(state.game_board)
            return self.__normalize(raw_eval)
        else:
            return self.__h(state.game_board)

    def h_piccolo(self, board):
        """
        A variant of the h() method, working directly on a chess board.

        :param board: The chess board to evaluate.
        :return: The heuristic value representing the king's safety.
        """
        # Handles endgame phase evaluation or normalization as specified.
        if self.evaluate_end_game_phase:
            return self.__h(board)
        elif self.normalize_result:
            raw_eval = self.__h(board)
            return self.__normalize(raw_eval, 10, -10)
        else:
            return self.__h(board)

    def __h(self, board):
        """
        Private method for raw heuristic evaluation of the king's safety on the board.

        :param board: The chess board to evaluate.
        :return: The raw heuristic value representing the king's safety.
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
        score = 0
        pawn_cover_score = 0.5
        attacked_square_score = -0.75

        # Bit masks for black and white pedestrians
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        # Calculation for the white king
        white_king_square = board.king(chess.WHITE)
        white_king_attacks = board.attacks(white_king_square)
        white_king_zone = white_pawns & white_king_attacks
        score += pawn_cover_score * bin(white_king_zone).count('1')

        # Controlla le caselle attaccate dai neri nella zona del re bianco
        for square in white_king_attacks:
            if board.is_attacked_by(chess.BLACK, square):
                score += attacked_square_score

        # Check the squares attacked by blacks in the white king's area
        black_king_square = board.king(chess.BLACK)
        black_king_attacks = board.attacks(black_king_square)
        black_king_zone = black_pawns & black_king_attacks
        score -= pawn_cover_score * bin(black_king_zone).count('1')

        # Check the squares attacked by whites in the black king's area
        for square in black_king_attacks:
            if board.is_attacked_by(chess.WHITE, square):
                score -= attacked_square_score

        return score

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
