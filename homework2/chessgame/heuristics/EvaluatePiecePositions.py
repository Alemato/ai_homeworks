from chessgame import StateChessGame
from .constants import *


# 21 microsecondi
# min = -285 -275
# max = 420 395
class EvaluatePiecePositions:
    """
    This class evaluates the positions of pieces on a chessboard. It calculates a score based on the
    positioning of each piece type according to specific positional tables, especially considering different
    game phases (e.g., opening, endgame).

    Attributes:
        evaluate_end_game_phase (bool): If true, the evaluation changes for the endgame phase.
        normalize_result (bool): If true, normalizes the evaluation score within a specific range.
        h_max_value (float): Maximum value for normalization.
        h_min_value (float): Minimum value for normalization.
    """

    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        """
        Initializes the evaluator with options for endgame evaluation and normalization of results.

        :param evaluate_end_game_phase: Indicates whether to apply a different evaluation strategy for endgame.
        :param normalize_result: Indicates whether to normalize the evaluation score.
        """
        self.evaluate_end_game_phase = evaluate_end_game_phase  # Determines if endgame is evaluated differently.
        self.normalize_result = normalize_result  # Determines if score should be normalized.
        self.h_max_value = 505  # Maximum value for heuristic normalization.
        self.h_min_value = -420  # Minimum value for heuristic normalization.

    def h(self, state: StateChessGame):
        """
        Evaluates the piece positions for the given state of the chess game.

        :param state: The current state of the chess game.
        :return: A heuristic value representing the evaluation of piece positions.
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
        A variant of the h() method, working directly on a chess board. It allows for custom normalization bounds.

        :param board: The chess board to evaluate.
        :return: A heuristic value representing the piece positions.
        """
        # Handles endgame evaluation or normalization based on the board state.
        if self.evaluate_end_game_phase:
            return self.__h(board)
        elif self.normalize_result:
            raw_eval = self.__h(board)
            return self.__normalize(raw_eval, 10, -10)
        else:
            return self.__h(board)

    def __evaluate_piece_positions(self, board, piece_table, piece_type, color):
        """
        Evaluates the positions of a specific type of piece on the board based on a predefined table.

        :param board: The chess board to evaluate.
        :param piece_table: A table with positional values for each square of the board.
        :param piece_type: Type of the piece to evaluate.
        :param color: Color of the pieces to evaluate.
        :return: A score based on the positioning of the pieces.
        """
        score = 0
        pieces = board.pieces(piece_type, color)
        # Calculate the score for each piece based on its position.
        for square in pieces:
            piece_position_value = piece_table[square]
            # Adjust score based on the piece color.
            score += piece_position_value if color == chess.WHITE else -piece_position_value
        return score

    def __is_endgame(self, board):
        """
        Determines if the current board state is in the endgame phase.

        :param board: The chess board to evaluate.
        :return: True if it's the endgame phase, False otherwise.
        """
        # Regine
        white_queens = len(board.pieces(chess.QUEEN, chess.WHITE))
        black_queens = len(board.pieces(chess.QUEEN, chess.BLACK))

        # se entrambi i lati non hanno Regine -> endgame phase
        if white_queens == 0 and black_queens == 0:
            return True

        # Minorpieces
        white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))
        white_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
        black_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))
        white_minors = white_bishops + white_knights
        black_minors = black_bishops + black_knights

        white_rooks = len(board.pieces(chess.ROOK, chess.WHITE))
        black_rooks = len(board.pieces(chess.ROOK, chess.BLACK))

        # se ogni lato che ha una regina, non ha altri pezzi oppure ha
        # 1 Minorpiece al massimo -> endgame phase
        white_endgame_condition_with_queen = (
                white_queens == 1 and (white_rooks == 0 and white_minors <= 1)
        )
        black_endgame_condition_with_queen = (
                black_queens == 1 and (black_rooks == 0 and black_minors <= 1)
        )

        if (
                (white_endgame_condition_with_queen and black_queens == 0)
                or (black_endgame_condition_with_queen and white_queens == 0)
                or (
                white_endgame_condition_with_queen
                and black_endgame_condition_with_queen
        )
        ):
            return True

        return False

    def __h(self, board):
        """
        Calculates the total score based on the position of pieces on the board.

        :param board: The chess board to evaluate.
        :return: A score representing the overall evaluation of piece positions.
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
        total_score = 0
        if self.__is_endgame(board):
            king_table_to_use = KING_ENDGAME_TABLE
        else:
            king_table_to_use = KING_INITGAME_TABLE
        total_score += self.__evaluate_piece_positions(board, PAWN_TABLE, chess.PAWN, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, KNIGHT_TABLE, chess.KNIGHT, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, BISHOP_TABLE, chess.BISHOP, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, ROOK_TABLE, chess.ROOK, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, QUEEEN_TABLE, chess.QUEEN, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, king_table_to_use, chess.KING, chess.WHITE)

        total_score -= self.__evaluate_piece_positions(board, PAWN_TABLE, chess.PAWN, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, KNIGHT_TABLE, chess.KNIGHT, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, BISHOP_TABLE, chess.BISHOP, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, ROOK_TABLE, chess.ROOK, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, QUEEEN_TABLE, chess.QUEEN, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, king_table_to_use, chess.KING, chess.BLACK)

        return total_score

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
