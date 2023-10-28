import chess
import numpy as np

from ChessGame import ChessGame
from State import State


class HChessGame:
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

    # Constructor for the HChessGame class with specified weights for different heuristic components.
    def __init__(self, c1=0.4, c2=0.6, c8=0.8, c4=0.4, c5=0.6, c6=0.4):
        # Coefficients for weighting various aspects of the game state.
        self.c1 = c1  # Weight for center control.
        self.c2 = c2  # Weight for mobility.
        self.c3 = 0.8  # Default weight for king safety (not passed as an argument).
        self.c4 = c4  # Weight for rooks on open files.
        self.c5 = c5  # Weight for check forks.
        self.c6 = c6  # Weight for check pins.
        self.c7 = 1  # Default weight for all piece values and piece square tables (constant value).
        self.c8 = c8  # Weight for attack value.

    # Static method to calculate the control of the center of the board.
    @staticmethod
    def center_control(state: State):
        board = state.game_board  # Access the chess board from the game state.
        center_squares = [chess.D3, chess.E3, chess.D4, chess.E4]  # Define central squares on the chess board.
        value = 0
        # Iterate through central squares and calculate control value.
        for square in center_squares:
            piece = board.piece_at(square)
            # Assign points based on the color of the piece occupying the center squares.
            if piece:
                value += 10 if piece.symbol().isupper() else -10
        return value

    # Static method to calculate the mobility of pieces on the board.
    @staticmethod
    def mobility(state: State):
        board = state.game_board
        mobility_value = 0

        # Iterate through all squares on the board.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Calculate the number of legal moves for the piece at the given square.
                legal_moves = board.attacks(square)
                num_moves = len(legal_moves)

                # Assign a mobility score based on the type of the piece.
                score = num_moves * HChessGame.get_piece_mobility_value(piece)
                # Adjust the mobility value based on the color of the piece.
                mobility_value += score if piece.color == board.turn else -score

        return mobility_value

    # Static method to assign mobility values to different types of chess pieces.
    @staticmethod
    def get_piece_mobility_value(piece):
        # Define mobility values for each piece type.
        piece_mobility_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 2,
            chess.QUEEN: 1,
            chess.KING: 1
        }
        # Return the mobility value for the given piece type.
        return piece_mobility_values.get(piece.piece_type, 0)

    # Static method to evaluate the safety of the king.
    @staticmethod
    def king_safety(state: State):
        board = state.game_board
        value = 0
        # Identify the positions of the kings and rooks for both colors.
        king_positions = {'K': board.king(chess.WHITE), 'k': board.king(chess.BLACK)}
        rook_positions = {'R': list(board.pieces(chess.ROOK, chess.WHITE)),
                          'r': list(board.pieces(chess.ROOK, chess.BLACK))}

        # Calculate the king safety value based on the proximity of opposing rooks.
        for rook_pos in rook_positions['r']:
            if king_positions['K'] and (
                    rook_pos // 8 == king_positions['K'] // 8 or rook_pos % 8 == king_positions['K'] % 8):
                value -= 50

        for rook_pos in rook_positions['R']:
            if king_positions['k'] and (
                    rook_pos // 8 == king_positions['k'] // 8 or rook_pos % 8 == king_positions['k'] % 8):
                value += 50

        return value

    # Static method to evaluate the positioning of rooks on open files.
    @staticmethod
    def rooks_on_open_files(state: State):
        board = state.game_board
        value = 0
        # Iterate through each file (column) on the chess board.
        for x in range(8):
            has_rook = False
            open_file = True
            rook_color = None
            # Check each square in the file.
            for y in range(8):
                piece = board.piece_at(8 * y + x)
                # Determine if the file is open (no pawns) and if there is a rook.
                if piece and piece.symbol() in ['P', 'p']:
                    open_file = False
                if piece and piece.symbol() in ['R', 'r']:
                    has_rook = True
                    rook_color = piece.color
            # Assign value based on the presence of a rook on an open file.
            if open_file and has_rook:
                value += 25 if rook_color == chess.WHITE else -25
        return value

    # Static method to evaluate the game state for a win, loss, or draw.
    @staticmethod
    def get_game_over_evaluation(state):
        if state.is_victory():
            # Assign a very high/low value for a victory/defeat.
            return np.inf if state.winner() else -np.inf

        if state.is_draw():
            # Assign a neutral value for a draw.
            return 0

        return None

    # Static method to evaluate the potential for forks in the game state.
    @staticmethod
    def check_forks(state: State):
        board = state.game_board
        forks_value = 0

        # Iterate through all legal moves.
        for move in board.legal_moves:
            board.push(move)  # Make the move on the board.
            # Check if the move results in a fork (more than one piece under attack).
            attacks_after_move = board.attackers(board.turn, move.to_square)
            if len(attacks_after_move) > 1:
                forks_value += 10
            board.pop()  # Revert the move.

        return forks_value

    # Static method to evaluate the potential for pins in the game state.
    @staticmethod
    def check_pins(state: State):
        board = state.game_board
        pins_value = 0
        opponent_color = not board.turn

        # Check each piece of the current player to see if it's pinned.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                attackers = board.attackers(opponent_color, square)
                for attacker_square in attackers:
                    attacker_piece = board.piece_at(attacker_square)
                    # Deduct points for each pinned piece.
                    if board.is_pinned(board.turn, attacker_square):
                        pins_value -= 10

        return pins_value

    # Static method to calculate the value of attacks on the board.
    @staticmethod
    def attack_value(state: State):
        board = state.game_board
        value = 0

        # Iterate through all squares on the board.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Calculate the value of the piece being attacked.
                attacked_value = HChessGame.piece_values[piece.symbol().lower()]
                attackers_of_square = board.attackers(not board.turn, square)

                # Adjust the value based on the number and type of attackers.
                if piece.color == board.turn:
                    value -= len(attackers_of_square) * attacked_value
                else:
                    value += len(attackers_of_square) * attacked_value

        # Add extra value if the opponent is in check.
        if board.is_check():
            value += 20

        return value

    # Static method to evaluate all remaining pieces on the board using piece values and piece square tables.
    @staticmethod
    def all_piece_values_and_piece_square_tables(state: State):
        total = 0
        endgame = ChessGame.is_in_endgame_phase(state.game_board)
        # Iterate through each piece on the board.
        for square, piece in state.game_board.piece_map().items():
            piece_str = str(piece)
            piece_type = piece_str.lower()
            piece_value = 0
            # Calculate the piece value based on its type and position.
            if piece.piece_type == chess.KING:
                # Use different tables based on whether the game is in the endgame phase.
                if not endgame:
                    piece_value = (
                            HChessGame.piece_values[piece_type]
                            + HChessGame.piece_square_tables[piece_str]["early"][square]
                    )
                else:
                    piece_value = (
                            HChessGame.piece_values[piece_type]
                            + HChessGame.piece_square_tables[piece_str]["end"][square]
                    )
            else:
                piece_value = (
                        HChessGame.piece_values[piece_type] + HChessGame.piece_square_tables[piece_str][square]
                )
            # Adjust the total value based on the color of the piece.
            total += piece_value if piece.color == chess.WHITE else -piece_value
        return total

    # Method to estimate the value of a given chess state.
    def h(self, state: State):
        # First, check if the game is over (win, loss, or draw).
        h1 = ChessGame.game_over_eval(state.game_board)
        if h1 is not None:
            return h1
        else:
            # Combine different heuristic components, weighted by their respective coefficients.
            return (
                    self.c1 * self.center_control(state) +
                    self.c2 * self.mobility(state) +
                    self.c3 * self.king_safety(state) +
                    self.c4 * self.rooks_on_open_files(state) +
                    self.c5 * self.check_forks(state) +
                    self.c6 * self.check_pins(state) +
                    self.c7 * self.all_piece_values_and_piece_square_tables(state) +
                    self.c8 * self.attack_value(state)
            )
