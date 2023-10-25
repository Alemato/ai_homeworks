import cairosvg
import chess
import chess.svg
from IPython.core.display import Image, display

from State import State


class ChessGame:
    def __init__(self, game_board=None):
        if game_board is not None:
            self.game_board = chess.Board()
        else:
            self.game_board = game_board

    @staticmethod
    def legal_moves(game_board):
        return game_board.legal_moves

    @staticmethod
    def is_the_turn_of(game_board):
        return game_board.turn

    def make_a_move(self, move, game_board):
        if move in self.legal_moves(game_board):
            new_board = game_board.copy()
            new_board.push(move)
            return State(game_board=new_board, move=move.__repr__())
        return None

    @staticmethod
    def ask_draw(game_board):
        return game_board.can_claim_draw()

    @staticmethod
    def piece_map(game_board):
        return game_board.piece_map()

    @staticmethod
    def get_last_move(game_board):
        if len(game_board.move_stack) > 0:
            return game_board.move_stack[-1]
        else:
            return None

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

    @staticmethod
    def is_endgame(game_board):
        return game_board.is_game_over()

    def game_termination(self, game_board):
        if self.is_endgame(game_board):
            outcome = game_board.outcome()
            if outcome is not None:
                return outcome.termination
        return None

    def winner_player_is(self, game_board):
        if self.is_victory(game_board):
            outcome = game_board.outcome()
            if outcome is not None:
                return "White" if outcome.winner else "Black"
        return None

    def white_is_winner(self, game_board):
        if self.is_victory(game_board):
            outcome = game_board.outcome()
            if outcome is not None:
                return outcome.winner
        return None

    @staticmethod
    def is_victory(game_board):
        return game_board.is_checkmate()

    @staticmethod
    def is_pareggio(game_board):
        return (
                game_board.is_fivefold_repetition()
                or game_board.is_seventyfive_moves()
                or game_board.is_insufficient_material()
                or game_board.is_stalemate()
        )

    @staticmethod
    def print_board(state: State):
        return state.game_board

    @staticmethod
    def print_img_board(state: State):
        svg_board = chess.svg.board(board=state.game_board, size=300)
        svg_bytes = cairosvg.svg2png(svg_board)
        if svg_bytes is not None:
            display(Image(svg_bytes, width=300))

    def neighbors(self, state: State):
        neighbors_state = []

        for legal_move in self.legal_moves(state.game_board):
            new_state = self.make_a_move(move=legal_move, game_board=state.game_board)
            new_state.parent_state = state
            neighbors_state.append(new_state)

        return neighbors_state
