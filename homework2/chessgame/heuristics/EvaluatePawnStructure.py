import chess

from chessgame import StateChessGame


# 60 microsecondi
# min = -420
# max = 420
class EvaluatePawnStructure:
    """
    This class evaluates the pawn structure in a chess game. It analyzes various factors like isolated,
    doubled, backward, and passed pawns, computing a score to represent the strategic and positional strength
    of the pawn structure.

    Attributes:
        evaluate_end_game_phase (bool): Indicates if the endgame should be evaluated differently.
        file_bb (list): Bitboards representing each file on the chessboard.
        rank_bb (list): Bitboards representing each rank on the chessboard.
        advance_shifts (dict): Dict for calculating the square index after advancing a pawn.
        normalize_result (bool): Determines if the evaluation score should be normalized.
        h_max_value (float): The upper limit for normalization of the heuristic score.
        h_min_value (float): The lower limit for normalization of the heuristic score.
    """

    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        """
        Initializes the evaluator with options for endgame evaluation, pawn advancement, and result normalization.

        :param evaluate_end_game_phase: Set to True for specialized evaluations in endgame phases.
        :param normalize_result: Set to True to normalize the evaluation score within a range.
        """
        self.evaluate_end_game_phase = evaluate_end_game_phase  # Flag to adjust evaluation in endgame phases.
        self.file_bb = [chess.BB_FILES[f] for f in range(8)]  # Bitboards for each file (column) of the chessboard.
        self.rank_bb = [chess.BB_RANKS[r] for r in range(8)]  # Bitboards for each rank (row) of the chessboard.
        self.advance_shifts = {chess.WHITE: 8, chess.BLACK: -8}  # Square shift for pawn advancement based on color.
        self.normalize_result = normalize_result  # Flag to normalize the evaluation score.
        self.h_max_value = 430  # Max heuristic value for normalization.
        self.h_min_value = -430  # Min heuristic value for normalization.

    def h(self, state: StateChessGame):
        """
        Evaluates the pawn structure based on the current game state. Determines if special handling
        for the endgame or normalization of results is required.

        :param state: StateChessGame object representing the current state of the chess game.
        :return: A heuristic value representing the pawn structure.
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
        :return: A heuristic value representing the pawn structure.
        """
        # Handles endgame evaluation or normalization based on the board state.
        if self.evaluate_end_game_phase:
            return self.__h(board)
        elif self.normalize_result:
            raw_eval = self.__h(board)
            return self.__normalize(raw_eval, 10, -10)
        else:
            return self.__h(board)

    def __pawn_structure_score(self, pawns, color, board):
        score = 0
        our_pawns_bb = int(pawns)  # Convert to integer bitboard if it's not already
        all_pawns_bb = int(board.pieces(chess.PAWN, chess.WHITE)) | int(board.pieces(chess.PAWN, chess.BLACK))

        # Precompute pawn presence for files using bitwise operations
        pawns_on_file = [bool(our_pawns_bb & self.file_bb[f]) for f in range(8)]

        for square in chess.SquareSet(our_pawns_bb):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            # Isolated pawns
            if not (pawns_on_file[file - 1] if file > 0 else False) and \
                    not (pawns_on_file[file + 1] if file < 7 else False):
                score -= 20

            # Doubled pawns
            if bin(our_pawns_bb & self.file_bb[file]).count('1') > 1:
                score -= 10

            # Backward pawns
            supported = False
            advance_square = square + self.advance_shifts[color]
            support_squares = [square - 1, square + 1] + \
                              [advance_square - 1, advance_square + 1]

            # Check if the pawn is supported by our other pawns
            for support_sq in support_squares:
                if 0 <= support_sq < 64 and (all_pawns_bb & (1 << support_sq)):
                    supported = True
                    break
            if not supported and 0 <= advance_square < 64 and board.piece_at(advance_square) is None:
                score -= 15

        return score

    def __passed_pawn_score(self, our_pawns, their_pawns, color):
        """
        Calculates a score based on the structure of the pawns for a given color. It considers factors such
        as isolated, doubled, and backward pawns.

        :param color: The color of the pawns to be evaluated (chess.WHITE or chess.BLACK).
        :return: An integer score representing the structural strengths and weaknesses of the pawns.
        """
        score = 0
        their_pawns_bb = int(their_pawns)  # Assicurati che sia un bitboard intero
        for our_pawn in our_pawns:
            file = chess.square_file(our_pawn)
            rank = chess.square_rank(our_pawn)
            passed = True
            if color == chess.WHITE:
                for r in range(rank + 1, 8):
                    if self.file_bb[file] & self.rank_bb[r] & their_pawns_bb:  # Utilizzo bitboard intero
                        passed = False
                        break
            else:
                for r in range(rank - 1, -1, -1):
                    if self.file_bb[file] & self.rank_bb[r] & their_pawns_bb:  # Utilizzo bitboard intero
                        passed = False
                        break
            if passed:
                score += 50

        return score

    def __h(self, board):
        """
        Private method for the raw heuristic evaluation of the pawn structure on the board. It considers
        the overall structure, including both white and black pawns, and computes a combined score.

        :param board: The chess board to evaluate.
        :return: The raw heuristic value representing the overall pawn structure.
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
        # Get the positions of white and black pawns.
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        # Get the positions of white and black pawns.
        score += self.__pawn_structure_score(white_pawns, chess.WHITE, board)
        score -= self.__pawn_structure_score(black_pawns, chess.BLACK, board)

        # Evaluate passed pawn score for both sides.
        score += self.__passed_pawn_score(white_pawns, black_pawns, chess.WHITE)
        score -= self.__passed_pawn_score(black_pawns, white_pawns, chess.BLACK)

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
