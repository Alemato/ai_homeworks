import chess

from chessgame import StateChessGame

# Dictionary defining the intrinsic values for each chess piece.
piece_values = {
    "p": 100,  # Value of a Pawn
    "n": 320,  # Value of a Knight
    "b": 330,  # Value of a Bishop
    "r": 500,  # Value of a Rook
    "q": 900,  # Value of a Queen
    "k": 20000,  # Value of a King (set very high to represent its critical importance)
}

# Piece-square table for the white pawn, defining values based on pawn's position on the board.
pawn_white_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]

# The black pawn's piece-square table is just a reversed version of the white pawn's table.
pawn_black_table = list(reversed(pawn_white_table))

# Piece-square table for the white knight.
knight_white_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

# The black knight's table is a reversed version of the white knight's table.
knight_black_table = list(reversed(knight_white_table))

# Piece-square table for the white bishop.
bishop_white_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

# The black bishop's table is a reversed version of the white bishop's table.
bishop_black_table = list(reversed(bishop_white_table))

# Piece-square table for the white rook.
rook_white_table = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

# The black rook's table is a reversed version of the white rook's table.
rook_black_table = list(reversed(rook_white_table))

# Piece-square table for the white queen.
queen_white_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

# The black queen's table is a reversed version of the white queen's table.
queen_black_table = list(reversed(queen_white_table))

# Piece-square table for the white king during the middle game.
king_white_table = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

# The black king's table is a reversed version of the white king's table.
king_black_table = list(reversed(king_white_table))

# Piece-square table for the white king during the endgame.
king_white_table_endgame = [
    -50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]

# The black king's endgame table is a reversed version of the white king's endgame table.
king_black_table_endgame = list(reversed(king_white_table_endgame))

# A comprehensive dictionary containing piece-square tables for each piece and color.
# The tables indicate the value of placing a piece on a specific square.
piece_square_tables = {
    "p": pawn_black_table,  # Black pawn
    "n": knight_black_table,  # Black knight
    "b": bishop_black_table,  # Black bishop
    "r": rook_black_table,  # Black rook
    "q": queen_black_table,  # Black queen
    "k": {"early": king_black_table, "end": king_black_table_endgame},  # Black king (both middle game and endgame)

    "P": pawn_white_table,  # White pawn
    "N": knight_white_table,  # White knight
    "B": bishop_white_table,  # White bishop
    "R": rook_white_table,  # White rook
    "Q": queen_white_table,  # White queen
    "K": {"early": king_white_table, "end": king_white_table_endgame},  # White king (both middle game and endgame)
}


class HardBoardEvaluationChessGame:
    """
    Provides an evaluation of a chess board based on various criteria, helping
    to determine the quality of a board state for use in search algorithms.

    Methods:
        king_safety: Evaluates the board based on king safety.
        all_piece_values_and_piece_square_tables: Evaluates the overall quality of the board.
        center_control: Evaluate control of the central squares on the chessboard.
        mobility: Evaluate the mobility of pieces on the chessboard.
        attack_value: Evaluate the value of piece attacks on the chessboard.
        rooks_on_open_files: Evaluate the presence of rooks on open files in the chessboard.
        check_forks: Evaluate the presence of fork opportunities in the chess position.
        check_pins: Evaluate the presence of pinned pieces in the chess position.
    """

    def h(self, state: StateChessGame):
        """
        Evaluates the overall quality of the board based on various criteria.
        :param state:The current state of the chess game.
        :return: The evaluation score of the board.
        """
        h1 = state.game_over_eval()
        if h1 is not None:
            return h1
        else:
            return (
                    self.king_safety(state) +
                    self.all_piece_values_and_piece_square_tables(state) +
                    self.center_control(state) +
                    self.mobility(state) +
                    self.attack_value(state) +
                    self.rooks_on_open_files(state) +
                    self.check_forks(state) +
                    self.check_pins(state)
            )

    def king_safety(self, state: StateChessGame):
        """
        Evaluates king safety for both sides.

        This function calculates the king safety evaluation based on the positions of kings and rooks. It penalizes the
        side if its king is on an open file with an opposing rook.

        :param state: The current state of the chess game (StateChessGame object).
        :return: The evaluation score for king safety. Positive score indicates safer kings for white, and negative score
                 indicates safer kings for black.
        """
        board = state.game_representation.game_board
        value = 0
        king_positions = {'K': board.king(chess.WHITE), 'k': board.king(chess.BLACK)}
        rook_positions = {'R': list(board.pieces(chess.ROOK, chess.WHITE)),
                          'r': list(board.pieces(chess.ROOK, chess.BLACK))}
        for rook_pos in rook_positions['r']:
            if king_positions['K'] and (
                    rook_pos // 8 == king_positions['K'] // 8 or rook_pos % 8 == king_positions['K'] % 8):
                value -= 50

        for rook_pos in rook_positions['R']:
            if king_positions['k'] and (
                    rook_pos // 8 == king_positions['k'] // 8 or rook_pos % 8 == king_positions['k'] % 8):
                value += 50

        return value * 0.8

    def all_piece_values_and_piece_square_tables(self, state: StateChessGame):
        """
        Calculate the combined value of all pieces on the chessboard.

        This function computes the total value of all pieces on the chessboard, considering their intrinsic values and
        positional advantages or disadvantages based on piece-square tables. It accounts for both the middle game and endgame
        scenarios.

        :param state: The current state of the chess game (StateChessGame object).
        :return: The combined evaluation score for all pieces on the board. A positive score indicates an advantage for white,
                 and a negative score indicates an advantage for black.
        """
        total = 0
        endgame = state.game_representation.is_in_endgame_phase()
        # Iterate through all squares on the chessboard and evaluate the value of pieces on each square.
        for square, piece in state.game_representation.game_board.piece_map().items():
            piece_str = str(piece)
            piece_type = piece_str.lower()
            piece_value = 0
            if piece.piece_type == chess.KING:
                if not endgame:
                    piece_value = (
                            piece_values[piece_type]
                            + piece_square_tables[piece_str]["early"][square]
                    )
                else:
                    piece_value = (
                            piece_values[piece_type]
                            + piece_square_tables[piece_str]["end"][square]
                    )
            else:
                piece_value = (
                        piece_values[piece_type] + piece_square_tables[piece_str][square]
                )
            # Add or subtract the piece value based on its color (white or black).
            total += piece_value if piece.color == chess.WHITE else -piece_value
        return total

    def center_control(self, state: StateChessGame):
        """
        Evaluate control of the central squares on the chessboard.

        This function calculates an evaluation score based on the control of central squares on the chessboard. It awards
        points for pieces occupying or influencing central squares, with a bonus for pieces controlled by the player (white)
        and a penalty for pieces controlled by the opponent (black).

        :param state: The current state of the chess game (StateChessGame object).
        :return: The evaluation score for central control. A positive score indicates an advantage for white, and a negative
                 score indicates an advantage for black.
        """
        board = state.game_representation.game_board  # Access the chess board from the game state.
        center_squares = [chess.D3, chess.E3, chess.D4, chess.E4]
        value = 0
        for square in center_squares:
            piece = board.piece_at(square)
            if piece:
                value += 10 if piece.symbol().isupper() else -10
        return value * 0.4

    def mobility(self, state: StateChessGame):
        """
        Evaluate the mobility of pieces on the chessboard.

        This function calculates an evaluation score based on the mobility of pieces on the chessboard. It assesses
        the number of legal moves available to each piece, considering their types (pawn, knight, bishop, rook,
        queen, king) and assigns scores accordingly. Mobility is a key factor in evaluating a position's strength.

        :param state: The current state of the chess game (StateChessGame object). :return: The evaluation score for
                piece mobility. A positive score indicates an advantage for white, and a negative score indicates an
                advantage for black.
        """
        # Define piece mobility values, specifying the importance of mobility for each piece type.
        piece_mobility_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 2,
            chess.QUEEN: 1,
            chess.KING: 1
        }

        board = state.game_representation.game_board
        mobility_value = 0

        # Iterate through all squares on the chessboard.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Calculate the legal moves for the current piece.
                legal_moves = board.attacks(square)
                num_moves = len(legal_moves)
                # Calculate a score based on the number of legal moves and the piece's type.
                score = num_moves * piece_mobility_values.get(piece.piece_type, 0)
                # Add or subtract the score based on the piece's color (white or black).
                mobility_value += score if piece.color == board.turn else -score

        return mobility_value * 0.6

    def attack_value(self, state: StateChessGame):
        """
        Evaluate the value of piece attacks on the chessboard.

        This function calculates an evaluation score based on the value of piece attacks on the chessboard. It assesses the
        value of pieces that are attacking or defending squares and considers whether a check is present in the position.

        :param state: The current state of the chess game (StateChessGame object).
        :return: The evaluation score for attack value. A positive score indicates an advantage for white, and a negative
                 score indicates an advantage for black.
        """
        board = state.game_representation.game_board
        value = 0
        # Iterate through all squares on the chessboard.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Determine the value of the piece on the current square.
                attacked_value = piece_values[piece.symbol().lower()]
                # Find attackers of the square from the opponent's side.
                attackers_of_square = board.attackers(not board.turn, square)
                if piece.color == board.turn:
                    # Subtract the value of attackers if the piece belongs to the player (white).
                    value -= len(attackers_of_square) * attacked_value
                else:
                    # Add the value of attackers if the piece belongs to the opponent (black).
                    value += len(attackers_of_square) * attacked_value
        # Add a bonus if the position is in check.
        if board.is_check():
            value += 20
        return value * 0.8

    def rooks_on_open_files(self, state: StateChessGame):
        """
        Evaluate the presence of rooks on open files in the chessboard.

        This function calculates an evaluation score based on the presence of rooks on open files in the chessboard. It assesses
        each column (file) to check if it is open (no pawns blocking) and whether there is at least one rook present. A bonus
        or penalty is assigned depending on the color of the rook (white or black) and whether the file is open or not.

        :param state: The current state of the chess game (StateChessGame object).
        :return: The evaluation score for rooks on open files. A positive score indicates an advantage for white, and a negative
                 score indicates an advantage for black.
        """
        board = state.game_representation.game_board
        value = 0
        # Iterate through each column (file) on the chessboard.
        for x in range(8):
            has_rook = False
            open_file = True
            rook_color = None
            # Iterate through each row (rank) in the current column.
            for y in range(8):
                piece = board.piece_at(8 * y + x)
                if piece and piece.symbol() in ['P', 'p']:
                    # If a pawn is found, the file is not open.
                    open_file = False
                if piece and piece.symbol() in ['R', 'r']:
                    # If a rook is found, mark that a rook is present on this file.
                    has_rook = True
                    rook_color = piece.color
            # Check if the file is open and there is at least one rook present.
            if open_file and has_rook:
                # Assign a bonus or penalty based on the color of the rook.
                value += 25 if rook_color == chess.WHITE else -25
        return value * 0.4

    def check_forks(self, state: StateChessGame):
        """
        Evaluate the presence of fork opportunities in the chess position.

        This function calculates an evaluation score based on the presence of fork opportunities in the chess
        position. It considers legal moves for the current player and checks whether each move results in multiple
        attackers on a single square, potentially creating a fork. A bonus is assigned for each detected fork
        opportunity.

        :param state: The current state of the chess game (StateChessGame object).
        :return: The evaluation score for fork opportunities. A positive score indicates an advantage for white,
                and a negative score indicates an advantage for black.
        """
        board = state.game_representation.game_board
        forks_value = 0
        # Iterate through all legal moves for the current player.
        for move in board.legal_moves:
            # Make the move on the board temporarily.
            board.push(move)
            # Find attackers after the move to the destination square.
            attacks_after_move = board.attackers(board.turn, move.to_square)
            # Check if multiple attackers are present on the same square, indicating a fork opportunity.
            if len(attacks_after_move) > 1:
                forks_value += 10
            # Undo the move to explore other moves.
            board.pop()
        return forks_value * 0.6

    def check_pins(self, state: StateChessGame):
        """
        Evaluate the presence of pinned pieces in the chess position.

        This function calculates an evaluation score based on the presence of pinned pieces in the chess position. It
        checks each square on the chessboard to identify pieces that belong to the current player (not opponent) and
        determines if any of those pieces are pinned by an opponent's piece. A penalty is assigned for each detected
        pinned piece.

        :param state: The current state of the chess game (StateChessGame object).
        :return: The evaluation score for pinned pieces. A positive score indicates an advantage for white,
                and a negative score indicates an advantage for black.
        """
        board = state.game_representation.game_board
        pins_value = 0
        opponent_color = not board.turn
        # Iterate through all squares on the chessboard.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            # Check if there is a piece on the square, and if it belongs to the current player.
            if piece and piece.color == board.turn:
                # Find attackers of the square by the opponent.
                attackers = board.attackers(opponent_color, square)
                for attacker_square in attackers:
                    # Check if the piece on the square is pinned.
                    attacker_piece = board.piece_at(attacker_square)
                    if board.is_pinned(board.turn, attacker_square):
                        # If pinned, assign a penalty to the evaluation score.
                        pins_value -= 10

        return pins_value * 0.4
