import chess
import numpy as np

from State import State


class HChessGame:
    def __init__(self):
        self.c1 = 0.35
        self.c2 = 0.3
        self.c3 = 0.2
        self.c4 = 0.2
        self.c5 = 0.5
        self.c6 = 0.15
        self.c7 = 0.15
        self.c8 = 0.2
        self.c9 = 0.15
        self.c10 = 0.2
        self.c11 = 0.35
        self.c12 = 0.40
        self.c13 = 0.80

    PIECE_VALUES = {
        'p': 100,
        'n': 320,
        'b': 330,
        'r': 500,
        'q': 900,
        'k': 20000,
    }

    PAWN_TABLE = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    PIECE_SQUARE_TABLES = {
        'P': [0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25,
              10, 5, 5, 0, 0, 0, 20, 20, 0, 0, 0, 5, -5, -10, 0, 0, -10, -5, 5, 5, 10, 10, -20, -20, 10, 10, 5, 0, 0,
              0, 0, 0, 0, 0, 0],
        'N': [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 0, 0, 0, -20, -40, -30, 0, 10, 15, 15, 10, 0, -30,
              -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 10, 15, 15, 10, 5, -30, -40, -20,
              0, 5, 5, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50],
        'B': [-20, -10, -10, -10, -10, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 5,
              5, 10, 10, 5, 5, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 5, 0, 0, 0,
              0, 5, -10, -20, -10, -10, -10, -10, -10, -10, -20],
        'R': [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 5, 5, 0, 0, 0],
        'Q': [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 5, 5, 5, 0, -10, -5, 0, 5,
              5, 5, 5, 0, -5, 0, 0, 5, 5, 5, 5, 0, -5, -10, 5, 5, 5, 5, 5, 0, -10, -10, 0, 5, 0, 0, 0, 0, -10, -20,
              -10, -10, -5, -5, -10, -10, -20],
        'K': {
            'early': [-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40,
                      -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -20, -30, -30, -40, -40, -30,
                      -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0,
                      10, 30, 20],
            'end': [-50, -40, -30, -20, -20, -30, -40, -50, -30, -20, -10, 0, 0, -10, -20, -30, -30, -10, 20, 30, 30,
                    20, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 20,
                    30, 30, 20, -10, -30, -30, -30, 0, 0, 0, 0, -30, -30, -50, -30, -30, -30, -30, -30, -30, -50]
        }
    }

    PIECE_SQUARE_TABLES['p'] = [row for row in reversed(PIECE_SQUARE_TABLES['P'])]
    PIECE_SQUARE_TABLES['n'] = [row for row in reversed(PIECE_SQUARE_TABLES['N'])]
    PIECE_SQUARE_TABLES['b'] = [row for row in reversed(PIECE_SQUARE_TABLES['B'])]
    PIECE_SQUARE_TABLES['r'] = [row for row in reversed(PIECE_SQUARE_TABLES['R'])]
    PIECE_SQUARE_TABLES['q'] = [row for row in reversed(PIECE_SQUARE_TABLES['Q'])]
    PIECE_SQUARE_TABLES['k'] = {"early": [row for row in reversed(PIECE_SQUARE_TABLES['K']['early'])],
                                "end": [row for row in reversed(PIECE_SQUARE_TABLES['K']["end"])]}

    @staticmethod
    def is_in_endgame_phase(game_board):
        # Regine
        white_queens = len(game_board.pieces(chess.QUEEN, chess.WHITE))
        black_queens = len(game_board.pieces(chess.QUEEN, chess.BLACK))

        # se entrambi i lati non hanno Regine -> endgame phase
        if white_queens == 0 and black_queens == 0:
            return True

        # Pezzi minori
        white_bishops = len(game_board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(game_board.pieces(chess.BISHOP, chess.BLACK))
        white_knights = len(game_board.pieces(chess.KNIGHT, chess.WHITE))
        black_knights = len(game_board.pieces(chess.KNIGHT, chess.BLACK))
        white_minors = white_bishops + white_knights
        black_minors = black_bishops + black_knights

        white_rooks = len(game_board.pieces(chess.ROOK, chess.WHITE))
        black_rooks = len(game_board.pieces(chess.ROOK, chess.BLACK))

        # se ogni lato che ha una regina, non ha altri pezzi oppure ha
        # 1 pezzo minore al massimo -> endgame phase
        # fmt: off
        white_endgame_condition_with_queen = (
                white_queens == 1 and (white_rooks == 0 and white_minors <= 1)
        )
        black_endgame_condition_with_queen = (
                black_queens == 1 and (black_rooks == 0 and black_minors <= 1)
        )
        # fmt: on

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

    def material_value(self, state: State):
        """Compute the material advantage of a State."""
        game_board = state.game_board
        value = 0
        for square, piece in game_board.piece_map().items():
            piece_symbol = piece.symbol()
            if piece_symbol.isupper():
                value += HChessGame.PIECE_VALUES.get(piece_symbol, 0)
            elif piece_symbol.islower():
                value -= HChessGame.PIECE_VALUES.get(piece_symbol.upper(), 0)
        return value

    def piece_position_value(self, state: State):
        game_board = state.game_board
        value = 0
        for square, piece in game_board.piece_map().items():
            y, x = divmod(square, 8)
            piece_symbol = piece.symbol()
            if piece_symbol == 'P':
                value += HChessGame.PAWN_TABLE[y][x]
            elif piece_symbol == 'p':
                value -= HChessGame.PAWN_TABLE[y][x]
        return value

    def center_control(self, state: State):
        game_board = state.game_board
        center_squares = [chess.D3, chess.E3, chess.D4, chess.E4]
        value = 0
        for square in center_squares:
            piece = game_board.piece_at(square)
            if piece:
                if piece.symbol().isupper():
                    value += 10
                else:
                    value -= 10
        return value

    def mobility(self, state: State):
        game_board = state.game_board
        value = 0
        for piece in game_board.piece_map().values():
            if piece.symbol().isupper():
                value += 1
            else:
                value -= 1
        return value

    def king_safety(self, state: State):
        game_board = state.game_board
        value = 0
        king_positions = {'K': game_board.king(chess.WHITE), 'k': game_board.king(chess.BLACK)}
        rook_positions = {'R': list(game_board.pieces(chess.ROOK, chess.WHITE)),
                          'r': list(game_board.pieces(chess.ROOK, chess.BLACK))}

        for rook_pos in rook_positions['r']:
            if king_positions['K'] and (
                    rook_pos // 8 == king_positions['K'] // 8 or rook_pos % 8 == king_positions['K'] % 8):
                value -= 50

        for rook_pos in rook_positions['R']:
            if king_positions['k'] and (
                    rook_pos // 8 == king_positions['k'] // 8 or rook_pos % 8 == king_positions['k'] % 8):
                value += 50

        return value

    def pawn_structure(self, state: State):
        game_board = state.game_board
        value = 0
        for square, piece in game_board.piece_map().items():
            y, x = divmod(square, 8)
            if piece.symbol() in ['P', 'p']:
                is_isolated = True
                left_square = (y, x - 1) if x - 1 >= 0 else None
                right_square = (y, x + 1) if x + 1 <= 7 else None
                if left_square and game_board.piece_at(8 * left_square[0] + left_square[1]) == piece.symbol():
                    is_isolated = False
                if right_square and game_board.piece_at(8 * right_square[0] + right_square[1]) == piece.symbol():
                    is_isolated = False
                if is_isolated:
                    value -= 10 if piece.symbol() == 'P' else 10
        return value

    def rooks_on_open_files(self, state: State):
        game_board = state.game_board
        value = 0
        for x in range(8):
            has_rook = False
            open_file = True
            rook_color = None
            for y in range(8):
                piece = game_board.piece_at(8 * y + x)
                if piece and piece.symbol() in ['P', 'p']:
                    open_file = False
                if piece and piece.symbol() in ['R', 'r']:
                    has_rook = True
                    rook_color = piece.color
            if open_file and has_rook:
                if rook_color == chess.WHITE:
                    value += 25
                else:
                    value -= 25
        return value

    @staticmethod
    def is_victory(game_board):
        if game_board.is_checkmate():
            if HChessGame.mario(game_board):
                return np.inf
            else:
                return -np.inf
        if HChessGame.patta(game_board):
            return 0
        return None

    @staticmethod
    def mario(game_board):
        if game_board.is_checkmate():
            outcome = game_board.outcome()
            if outcome is not None:
                return outcome.winner
        return None

    @staticmethod
    def patta(game_board):
        return (
                game_board.is_fivefold_repetition()
                or game_board.is_seventyfive_moves()
                or game_board.is_insufficient_material()
                or game_board.is_stalemate()
        )

    def check_forks(self, state: State):
        game_board = state.game_board
        forks_value = 0

        for move in game_board.legal_moves:
            game_board.push(move)
            attacks_after_move = game_board.attackers(game_board.turn, move.to_square)
            if len(attacks_after_move) > 1:  # More than one attacker implies a fork
                forks_value += 10
            game_board.pop()

        return forks_value

    def check_pins(self, state: State):
        game_board = state.game_board
        pins_value = 0
        opponent_color = not game_board.turn

        # Check for each piece of the current player if it's pinned
        for square in chess.SQUARES:
            piece = game_board.piece_at(square)
            if piece and piece.color == game_board.turn:
                attackers = game_board.attackers(opponent_color, square)
                for attacker_square in attackers:
                    attacker_piece = game_board.piece_at(attacker_square)
                    if game_board.is_pinned(game_board.turn, attacker_square):
                        pins_value -= 10

        return pins_value

    def check_discovered_attacks(self, state: State):
        game_board = state.game_board
        discovered_value = 0

        # Check for each piece of the current player if moving it would create a discovered attack
        for square in chess.SQUARES:
            piece = game_board.piece_at(square)
            if piece and piece.color == game_board.turn:
                for move in game_board.legal_moves:
                    if move.from_square == square:
                        game_board.push(move)
                        if game_board.is_check():
                            discovered_value += 10
                        game_board.pop()

        return discovered_value

    CENTER_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]

    def piece_development(self, state: State):
        game_board = state.game_board
        value = 0

        # Penalize knights and bishops that haven't moved from their starting positions
        knight_bishop_initial_positions = [chess.B1, chess.G1, chess.B8, chess.G8,
                                           chess.C1, chess.F1, chess.C8, chess.F8]

        for square in knight_bishop_initial_positions:
            piece = game_board.piece_at(square)
            if piece and (piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP):
                value -= 10  # Decrease value for undeveloped piece

        # Reward pieces that control the center
        for square in HChessGame.CENTER_SQUARES:  # assuming HChessGame.CENTER_SQUARES is defined
            if game_board.is_attacked_by(game_board.turn, square):
                value += 5  # Increase value for controlling the center

        # Check if the king has castled
        if game_board.turn == chess.WHITE:
            if not game_board.has_kingside_castling_rights(
                    chess.WHITE) and not game_board.has_queenside_castling_rights(
                chess.WHITE):
                value += 20  # Assuming the white king has castled if it has no castling rights left
        else:
            if not game_board.has_kingside_castling_rights(
                    chess.BLACK) and not game_board.has_queenside_castling_rights(
                chess.BLACK):
                value += 20  # Assuming the black king has castled if it has no castling rights left

        return value

    def attack_value(self, state: State):
        game_board = state.game_board
        value = 0

        for square in chess.SQUARES:
            piece = game_board.piece_at(square)
            if piece:
                attacked_value = HChessGame.PIECE_VALUES.get(piece.symbol(), 0)
                attackers_of_square = game_board.attackers(not game_board.turn, square)

                if piece.color == game_board.turn:
                    value -= len(attackers_of_square) * attacked_value

                else:
                    value += len(attackers_of_square) * attacked_value

        if game_board.is_check():
            value += 20

        return value

    def all_piece_values_and_piece_square_tables(self, state: State):
        total = 0
        endgame = HChessGame.is_in_endgame_phase(state.game_board)
        for square, piece in state.game_board.piece_map().items():
            piece_str = str(piece)
            piece_type = piece_str.lower()
            piece_value = 0
            if piece.piece_type == chess.KING:
                if not endgame:
                    piece_value = (
                            self.PIECE_VALUES[piece_type]
                            + self.PIECE_SQUARE_TABLES[piece_str]["early"][square]  # Access using two indices
                    )
                else:
                    piece_value = (
                            self.PIECE_VALUES[piece_type]
                            + self.PIECE_SQUARE_TABLES[piece_str]["end"][square]  # Access using two indices
                    )
            else:
                piece_value = (
                        self.PIECE_VALUES[piece_type] + self.PIECE_SQUARE_TABLES[piece_str][square]
                )
            total += piece_value if piece.color == chess.WHITE else -piece_value
        return total

    def h(self, state: State):
        h1 = HChessGame.is_victory(state.game_board)
        if h1 is not None:
            return h1
        else:
            return (
                    self.c3 * self.center_control(state) +
                    self.c4 * self.mobility(state) +
                    self.c5 * self.king_safety(state) +
                    self.c6 * self.pawn_structure(state) +
                    self.c7 * self.rooks_on_open_files(state) +
                    self.c8 * self.check_forks(state) +
                    self.c9 * self.check_pins(state) +
                    self.c10 * self.check_discovered_attacks(state) +
                    self.c13 * self.all_piece_values_and_piece_square_tables(state)
            )
