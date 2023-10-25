import chess


class ChessGame:
    def __init__(self, game_board=None):
        if game_board is not None:
            self.game_board = chess.Board()
        else:
            self.game_board = game_board

    def legal_moves(self):
        return self.game_board.legal_moves

    def winner_player_is(self):
        if self.is_victory():
            outcome = self.board.outcome()
            if outcome is not None:
                return "White" if outcome.winner else "Black"
        return None

    def is_victory(self):
        return self.game_board.is_checkmate()

    def is_endgame(self):
        return self.game_board.is_game_over()

    def is_pareggio(self):
        return (
                self.game_board.is_fivefold_repetition()
                or self.game_board.is_seventyfive_moves()
                or self.game_board.is_insufficient_material()
                or self.game_board.is_stalemate()
        )

    def is_the_turn_of(self):
        return self.game_board.turn
