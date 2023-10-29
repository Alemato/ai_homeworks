import chess
import numpy as np

from StateChessGame import StateChessGame
from ValuesDefinistions import *


# Definition of the ChessHeuristics class.
class ChessHeuristics:
    # Constructor for the ChessHeuristics class with specified weights for different heuristic components.
    def __init__(self):
        # Coefficients for weighting various aspects of the game state.
        self.c1 = 0.4  # Weight for center control.
        self.c2 = 0.6  # Weight for mobility.
        self.c3 = 0.8  # Default weight for king safety (not passed as an argument).
        self.c4 = 0.8  # Weight for rooks on open files.
        self.c5 = 0.4  # Weight for check forks.
        self.c6 = 0.6  # Weight for check pins.
        self.c7 = 1  # Default weight for all piece values and piece square tables (constant value).
        self.c8 = 0.4  # Weight for attack value.

    # Static method to calculate the control of the center of the board.
    @staticmethod
    def center_control(state: StateChessGame):
        board = state.game_representation.game_board  # Access the chess board from the game state.
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
    def mobility(state: StateChessGame):
        board = state.game_representation.game_board
        mobility_value = 0

        # Iterate through all squares on the board.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Calculate the number of legal moves for the piece at the given square.
                legal_moves = board.attacks(square)
                num_moves = len(legal_moves)

                # Assign a mobility score based on the type of the piece.
                score = num_moves * ChessHeuristics.get_piece_mobility_value(piece)
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
    def king_safety(state: StateChessGame):
        board = state.game_representation.game_board
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
    def rooks_on_open_files(state: StateChessGame):
        board = state.game_representation.game_board
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
    def check_forks(state: StateChessGame):
        board = state.game_representation.game_board
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
    def check_pins(state: StateChessGame):
        board = state.game_representation.game_board
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
    def attack_value(state: StateChessGame):
        board = state.game_representation.game_board
        value = 0

        # Iterate through all squares on the board.
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Calculate the value of the piece being attacked.
                attacked_value = piece_values[piece.symbol().lower()]
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
    def all_piece_values_and_piece_square_tables(state: StateChessGame):
        total = 0
        endgame = state.game_representation.is_in_endgame_phase()
        # Iterate through each piece on the board.
        for square, piece in state.game_representation.piece_map().items():
            piece_str = str(piece)
            piece_type = piece_str.lower()
            piece_value = 0
            # Calculate the piece value based on its type and position.
            if piece.piece_type == chess.KING:
                # Use different tables based on whether the game is in the endgame phase.
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
            # Adjust the total value based on the color of the piece.
            total += piece_value if piece.color == chess.WHITE else -piece_value
        return total

    # Method to estimate the value of a given chess state.
    def h(self, state: StateChessGame):
        # First, check if the game is over (win, loss, or draw).
        h1 = self.get_game_over_evaluation(state)
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


"""
Risultato: Termination.CHECKMATE
Vincitore: White
Tempo: 12281.008005142212
Tempo medio mossa: 101.40227680363931
Numero Mosse: 121
Stati valutati        (agente 1): 38844
Potature effettuate   (agente 1): 0

Stati valutati        (agente 2): 23503
Potature effettuate   (agente 2): 6


Risultato: Termination.CHECKMATE
Vincitore: White
Tempo: 6291.694641113281
Tempo medio mossa: 118.62042714964669
Numero Mosse: 53
Stati valutati        (agente 1): 20270
Potature effettuate   (agente 1): 0

Stati valutati        (agente 2): 16609
Potature effettuate   (agente 2): 15



dept3 tutti par a 1:

Risultato: Termination.CHECKMATE
Vincitore: Black
Tempo: 100752.11811065674
Tempo medio mossa: 2963.2121324539185
Numero Mosse: 34
Stati valutati        (agente 1): 117227
Potature effettuate   (agente 1): 12527

Stati valutati        (agente 2): 371405
Potature effettuate   (agente 2): 14028



        self.c3 * self.center_control(state) +
        self.c4 * self.mobility(state) +
        self.c5 * self.king_safety(state) +
        self.c7 * self.rooks_on_open_files(state) +
        self.c8 * self.check_forks(state) +
        self.c9 * self.check_pins(state) +
        self.c11 * self.all_piece_values_and_piece_square_tables(state) +
        self.c13 * self.attack_value(state)
        self.c3 = 0.6
        self.c4 = 0.6
        self.c5 = 0.8
        self.c7 = 0.2
        self.c8 = 0.2
        self.c9 = 0.2
        self.c11 = 1
        self.c13 = 0.8

Risultato: Termination.CHECKMATE
Vincitore: Black
Tempo: 197453.36413383484
Tempo medio mossa: 5807.360614047331
Numero Mosse: 34
Stati valutati        (agente 1): 117810
Potature effettuate   (agente 1): 12519

Stati valutati        (agente 2): 370659
Potature effettuate   (agente 2): 14044



        self.c3 * self.center_control(state) +
        self.c4 * self.mobility(state) +
        self.c5 * self.king_safety(state) +
        self.c7 * self.rooks_on_open_files(state) +
        self.c8 * self.check_forks(state) +
        self.c9 * self.check_pins(state) +
        self.c11 * self.all_piece_values_and_piece_square_tables(state) +
        self.c13 * self.attack_value(state)
        TUTTE A 1

Risultato: Termination.CHECKMATE
Vincitore: Black
Tempo: 192443.1357383728
Tempo medio mossa: 5660.007028018727
Numero Mosse: 34
Stati valutati        (agente 1): 116614
Potature effettuate   (agente 1): 12569

Stati valutati        (agente 2): 370579
Potature effettuate   (agente 2): 14039
"""
