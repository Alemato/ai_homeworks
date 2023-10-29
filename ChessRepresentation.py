import chess


class ChessRepresentation:
    def __init__(self, game_board=None):
        self.game_board = game_board

        if game_board is None:
            self.game_board = chess.Board()

    def is_victory(self):
        return self.game_board.is_checkmate()

    def winner(self):
        if self.is_victory():
            outcome = self.game_board.outcome()
            if outcome is not None:
                return outcome.winner
        return None

    def get_name_winner_player(self):
        if self.is_victory():
            outcome = self.game_board.outcome()
            if outcome is not None:
                return "White" if outcome.winner else "Black"
        return None

    def is_in_endgame_phase(self):
        # Count the number of queens for each player.
        white_queens = len(self.game_board.pieces(chess.QUEEN, chess.WHITE))
        black_queens = len(self.game_board.pieces(chess.QUEEN, chess.BLACK))

        # If both players have no queens, it's considered an endgame phase.
        if white_queens == 0 and black_queens == 0: return True

        # Count the number of rooks for each player.
        white_rooks = len(self.game_board.pieces(chess.ROOK, chess.WHITE))
        black_rooks = len(self.game_board.pieces(chess.ROOK, chess.BLACK))

        # Count the number of bishops for each player.
        white_bishops = len(self.game_board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(self.game_board.pieces(chess.BISHOP, chess.BLACK))

        # Count the number of knights for each player.
        white_knights = len(self.game_board.pieces(chess.KNIGHT, chess.WHITE))
        black_knights = len(self.game_board.pieces(chess.KNIGHT, chess.BLACK))

        # Count minor pieces for each player.
        white_minors = white_bishops + white_knights
        black_minors = black_bishops + black_knights

        white_endgame_condition_with_queen = (
                white_queens == 1 and (white_rooks == 0 and white_minors <= 1)
        )
        black_endgame_condition_with_queen = (
                black_queens == 1 and (black_rooks == 0 and black_minors <= 1)
        )

        if ((white_endgame_condition_with_queen and black_queens == 0) or (
                black_endgame_condition_with_queen and white_queens == 0) or (
                white_endgame_condition_with_queen and black_endgame_condition_with_queen)): return True

        return False

    def is_draw(self):
        return (
                self.game_board.is_stalemate()
                or self.game_board.is_insufficient_material()
                or self.game_board.is_seventyfive_moves()
                or self.game_board.is_fivefold_repetition()
        )

    def turn(self):
        return self.game_board.turn

    def can_claim_draw(self):
        return self.game_board.can_claim_draw()

    def is_game_over(self):
        return self.game_board.is_game_over()

    def piece_map(self):
        return self.game_board.piece_map()

    def get_all_legal_moves(self):
        return self.game_board.legal_moves

    def make_a_move(self, move):
        if move in self.get_all_legal_moves():
            new_game_board = self.game_board.copy()
            new_game_board.push(move)
            return ChessRepresentation(game_board=new_game_board)
        return None

    def __eq__(self, other):
        if not isinstance(other, ChessRepresentation):
            return False
        return str(self.game_board) == str(other.game_board)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.game_board))

    def __str__(self):
        return str(self.game_board)
