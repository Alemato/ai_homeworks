import chess

from chessgame import StateChessGame

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # Il re ha un valore speciale
}

# Tabelle di pezzi
PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

BISHOP_TABLE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

ROOK_TABLE = [
    [0, 0, 0, 5, 5, 0, 0, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

QUEEN_TABLE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

KING_TABLE = [
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30]
]

# Pesi, Penalità e bonus
OPEN_FILE_PENALTY = -25
ADJACENT_PAWN_BONUS = 10
KING_SAFETY_WEIGHT = 0.5
MOBILITY_WEIGHT = 0.1
CENTER_CONTROL_WEIGHT = 0.5
CENTER_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]


class SoftBoardEvaluationChessGame:
    """
    Provides an evaluation of a chess board based on various criteria, helping
    to determine the quality of a board state for use in search algorithms.

    Methods:
        evaluate_board: Evaluates the overall quality of the board.
        material_evaluation: Evaluates the board based on the material present.
        piece_square_evaluation: Evaluates the board based on piece positions.
        mobility_evaluation: Evaluates the board based on piece mobility.
        king_safety_evaluation: Evaluates the board based on king safety.
        center_control_evaluation: Evaluates board control of center squares.
    """

    def h(self, state: StateChessGame):
        """
        Evaluates the overall quality of the board based on various criteria.
        :param state:The current state of the chess game.
        :return: The evaluation score of the board.
        """
        board = state.game_board.game_board
        h1 = state.game_over_eval()
        if h1 is not None:
            return h1
        else:
            total_evaluation = (
                    self.piece_material_evaluation(board) +
                    self.piece_position_evaluation(board) +
                    self.mobility_evaluation(board) +
                    self.king_safety_evaluation(board) +
                    self.center_control_evaluation(board)
            )
            return total_evaluation

    def piece_material_evaluation(self, board):
        """
        Evaluates the board based on the material (pieces) present.

        This function calculates a numerical evaluation score for a given chess board based on the material (pieces)
        present on the board. It assigns scores to pieces based on their type and color, and the final score reflects
        the material advantage or disadvantage of one side over the other.

        :param board: The current chess board (chess.Board object). :return: The evaluation score based on material.
        A positive score indicates an advantage for white, while a negative score indicates an advantage for black.
        """
        evaluation = 0.0
        # Iterate through all squares on the chess board and evaluate the material present on each square.
        for square, piece in board.piece_map().items():
            # Get the value of the chess piece based on its type (pawn, knight, bishop, rook, queen, king).
            piece_value = PIECE_VALUES[piece.piece_type]

            # Check if the piece is white (color is chess.WHITE) or black (color is chess.BLACK) and adjust the
            # evaluation score accordingly.
            if piece.color == chess.WHITE:
                evaluation += piece_value  # Add the piece value for white.
            else:
                evaluation -= piece_value  # Subtract the piece value for black.
        return evaluation

    def piece_position_evaluation(self, board):
        """
        Evaluates the board based on the positions of the pieces.

        This function calculates a numerical evaluation score for a given chess board based on the positions of the
        pieces. It assigns scores to pieces based on their positions using predefined tables.

        :param board: The current chess board (chess.Board object). :return: The evaluation score based on piece
        positions. A positive score indicates an advantage for white based on piece positions, while a negative score
        indicates an advantage for black.
        """
        evaluation = 0.0

        for square, piece in board.piece_map().items():
            # Determine which piece type (pawn, knight, bishop, rook, queen, king) is on the current square.
            if piece.piece_type == chess.PAWN:
                table = PAWN_TABLE
            elif piece.piece_type == chess.KNIGHT:
                table = KNIGHT_TABLE
            elif piece.piece_type == chess.BISHOP:
                table = BISHOP_TABLE
            elif piece.piece_type == chess.ROOK:
                table = ROOK_TABLE
            elif piece.piece_type == chess.QUEEN:
                table = QUEEN_TABLE
            elif piece.piece_type == chess.KING:
                table = KING_TABLE

            # Calculate the row and column of the square.
            row = square // 8
            col = square % 8

            # Check if the piece is white (color is chess.WHITE) or black (color is chess.BLACK) and adjust the
            # evaluation score accordingly.
            if piece.color == chess.WHITE:
                evaluation += table[row][col]  # Add the piece value for white.
            else:
                # Tables are made for white, so let's reverse for black
                evaluation -= table[7 - row][col]  # Subtract the piece value for black.

        return evaluation

    def mobility_evaluation(self, board):
        """
        Evaluates the board based on the mobility (legal moves) of the pieces. This function calculates a numerical
        evaluation score for a given chess board based on the mobility of the pieces.
        Mobility refers to the number of legal moves that can be made by each side (white and black) on the board.

        :param board: The current chess board (chess.Board object).
        :return: The evaluation score based on mobility. A positive score indicates an advantage for the side with more
                 mobility, while a negative score indicates an advantage for the side with less mobility.
        """
        evaluation = 0.0

        # Calculate mobility for white and black
        white_mobility = len(list(board.legal_moves))
        board.push(chess.Move.null())  # Perform a null move to change the turn
        black_mobility = len(list(board.legal_moves))
        board.pop()  # Go back to the original shift
        # Evaluate mobility based on weights
        evaluation += MOBILITY_WEIGHT * (white_mobility - black_mobility)

        return evaluation

    def king_safety_evaluation(self, board):
        """
        Evaluates the safety of kings on the board.

        This function calculates a numerical evaluation score for a given chess board based on the safety of both kings.
        It considers factors such as pawn protection and open files near the kings.

        :param board: The current chess board (chess.Board object).
        :return: The evaluation score based on king safety. A positive score indicates a safer position for the white
                 king, while a negative score indicates a safer position for the black king.
        """
        evaluation = 0.0

        # Find the positions of the white and black kings on the board
        white_king_square = list(board.pieces(chess.KING, chess.WHITE))[0]
        black_king_square = list(board.pieces(chess.KING, chess.BLACK))[0]

        # Evaluate the safety of the white king
        if board.attacks(white_king_square) & board.pieces(chess.PAWN, chess.BLACK):
            # If black pawns can attack the white king, penalize the evaluation (open file penalty).
            evaluation += OPEN_FILE_PENALTY
        # Check adjacent squares to the white king for friendly pawns and provide a bonus for pawn protection.
        for square in chess.SQUARES:
            if abs(square - white_king_square) in [1, 7, 8, 9] and board.piece_at(
                    square) == chess.PAWN and board.color_at(square) == chess.WHITE:
                evaluation += ADJACENT_PAWN_BONUS

        # Evaluate the safety of the black king
        if board.attacks(black_king_square) & board.pieces(chess.PAWN, chess.WHITE):
            # If white pawns can attack the black king, penalize the evaluation (open file penalty).
            evaluation -= OPEN_FILE_PENALTY
        # Check adjacent squares to the black king for friendly pawns and provide a bonus for pawn protection.
        for square in chess.SQUARES:
            if abs(square - black_king_square) in [1, 7, 8, 9] and board.piece_at(
                    square) == chess.PAWN and board.color_at(square) == chess.BLACK:
                evaluation -= ADJACENT_PAWN_BONUS

        return evaluation * KING_SAFETY_WEIGHT

    def center_control_evaluation(self, board):
        """
        Evaluates control of the center of the chessboard.

        This function calculates a numerical evaluation score for a given chess board based on control of the central squares
        of the board. It assigns scores to pieces occupying central squares and gives additional scores for pieces
        controlling central squares.

        :param board: The current chess board (chess.Board object).
        :return: The evaluation score based on control of the center. A positive score indicates better control of the center
                 by white, while a negative score indicates better control by black.
        """

        evaluation = 0.0

        for square in CENTER_SQUARES:
            # If a central square is occupied by a piece, assign a score based on the piece color.
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    evaluation += 1
                else:
                    evaluation -= 1

            # Assign additional scores based on the number of attackers to central squares by each side.
            attackers = board.attackers(chess.WHITE, square)
            evaluation += len(attackers)
            attackers = board.attackers(chess.BLACK, square)
            evaluation -= len(attackers)

        return evaluation * CENTER_CONTROL_WEIGHT
