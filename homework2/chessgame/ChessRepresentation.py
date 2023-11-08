import chess


class ChessRepresentation:
    """
    Represents a chess game's board state and provides various utility methods
    to interact with and evaluate the state of the board.

    Attributes:
        game_board (chess.Board): The current state of the chess board.
    """

    def __init__(self, game_board=None):
        """
        Initializes the chess representation with an optional game board.
        :param game_board: The initial state of the chess board.
                Defaults to a new chess board if not provided.
        """
        self.game_board = game_board

        if game_board is None:
            self.game_board = chess.Board()

    def is_victory(self):
        """
        Checks if the current state is a checkmate.
        :return: True if it's checkmate, False otherwise.
        """
        return self.game_board.is_checkmate()

    def winner(self):
        """
        Determines the winner of the game.
        :return:True if White is the winner, False if Black is the winner,
                None if no winner.
        """
        if self.is_victory():
            outcome = self.game_board.outcome()
            if outcome is not None:
                return outcome.winner
        return None

    def get_name_winner_player(self):
        """
        Returns the name ("White" or "Black") of the winner.
        :return: "White" if White is the winner, "Black" if Black is the winner,
                None if no winner.
        """
        if self.is_victory():
            outcome = self.game_board.outcome()
            if outcome is not None:
                return "White" if outcome.winner else "Black"
        return None

    def is_in_endgame_phase(self):
        """
        Checks if the game is in the endgame phase based on certain conditions.
        :return: True if the game is in the endgame phase, False otherwise.
        """
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
        """
        Checks if the game is a draw based on various conditions.
        :return: True if the game is a draw, False otherwise.
        """
        return (
                self.game_board.is_stalemate()
                or self.game_board.is_insufficient_material()
                or self.game_board.is_seventyfive_moves()
                or self.game_board.is_fivefold_repetition()
        )

    def turn(self):
        """
        Returns the current player's turn.
        :return: True if it's White's turn, False if it's Black's turn.
        """
        return self.game_board.turn

    def can_claim_draw(self):
        """
        Checks if a draw can be claimed based on the current state.
        :return: True if a draw can be claimed, False otherwise.
        """
        return self.game_board.can_claim_draw()

    def is_game_over(self):
        """
        Checks if the game is over based on various conditions.
        :return: True if the game is over, False otherwise.
        """
        return self.game_board.is_game_over()

    def piece_map(self):
        """
        Returns a mapping of the pieces on the board.
        :return: A dictionary mapping from square numbers to chess pieces.
        """
        return self.game_board.piece_map()

    def get_all_legal_moves(self):
        """
        Returns all legal moves for the current position.
        :return: A generator of all legal moves.
        """
        return self.game_board.legal_moves

    def make_a_move(self, move):
        """
        Makes a move and returns a new chess representation if the move is legal.
        :param move: The move to be made.
        :return: A new chess representation after making the move.
                None if the move is not legal.
        """
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
