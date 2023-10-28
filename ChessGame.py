import chess
import numpy as np

from State import State


class ChessGame:
    def __init__(self, game_board=None):
        # Initialize the chessboard. If no board is provided, create a new standard board.
        if game_board is None:
            self.game_board_init = chess.Board()
        else:
            self.game_board_init = game_board

    # Define equality comparison for ChessBoard objects based on the board state.
    def __eq__(self, other):
        if not isinstance(other, ChessGame):
            return False
        return str(self.game_board_init) == str(other.game_board_init)

    # Define inequality comparison.
    def __ne__(self, other):
        return not self.__eq__(other)

    # Define a hash function based on the board state for hashable collections.
    def __hash__(self):
        return hash(str(self.game_board_init))

    # Return a string representation of the board.
    def __str__(self):
        return str(self.game_board_init)

    def make_move(self, move, game_board):
        if move in game_board.legal_moves:
            new_board = game_board.copy()
            new_board.push(move)
            return State(game_board=new_board, move=move.__repr__())
        return None

    def neighbors(self, state: State):
        neighbors_state = []

        for legal_move in state.game_board.legal_moves:
            new_state = self.make_move(move=legal_move, game_board=state.game_board)
            new_state.parent_state = state
            neighbors_state.append(new_state)

        return neighbors_state

    def is_endgame(self, game_board):
        return game_board.is_game_over()

    def ask_draw(self, game_board):
        return game_board.can_claim_draw()

    def name_player_win(self, game_board):
        if game_board.is_checkmate():
            outcome = game_board.outcome()
            if outcome is not None:
                return "White" if outcome.winner else "Black"
        return None

    def is_patta(self, game_board):
        return ChessGame.patta(game_board)

    @staticmethod
    def is_in_endgame_phase(game_board):
        # Count the number of queens for each player.
        white_queens = len(game_board.pieces(chess.QUEEN, chess.WHITE))
        black_queens = len(game_board.pieces(chess.QUEEN, chess.BLACK))

        # If both players have no queens, it's considered an endgame phase.
        if white_queens == 0 and black_queens == 0:
            return True

        # Count rooks for each player.
        white_rooks = len(game_board.pieces(chess.ROOK, chess.WHITE))
        black_rooks = len(game_board.pieces(chess.ROOK, chess.BLACK))

        # Count the number of bishops
        white_bishops = len(game_board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(game_board.pieces(chess.BISHOP, chess.BLACK))

        # Count the number of knights
        white_knights = len(game_board.pieces(chess.KNIGHT, chess.WHITE))
        black_knights = len(game_board.pieces(chess.KNIGHT, chess.BLACK))

        # Count total minor pieces for each player.
        white_minors = white_bishops + white_knights
        black_minors = black_bishops + black_knights

        white_endgame_condition_with_queen = (
                white_queens == 1 and (white_rooks == 0 and white_minors <= 1)
        )

        black_endgame_condition_with_queen = (
                black_queens == 1 and (black_rooks == 0 and black_minors <= 1)
        )

        if (
                (white_endgame_condition_with_queen and black_queens == 0)
                or (black_endgame_condition_with_queen and white_queens == 0)
                or (white_endgame_condition_with_queen and black_endgame_condition_with_queen)
        ):
            return True
        return False

    @staticmethod
    def winner(game_board):
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

    @staticmethod
    def game_over_eval(game_board):
        if game_board.is_checkmate():
            if ChessGame.winner(game_board):
                return np.inf
            else:
                return -np.inf
        if ChessGame.patta(game_board):
            return 0
        return None
