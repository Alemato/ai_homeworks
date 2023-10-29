import numpy as np

from ChessRepresentation import ChessRepresentation


class StateChessGame:
    """
    Represents a specific state of a chess game, encapsulating details about the game
    at this state, its parent state, and the move that led to this state.

    Attributes:
        game_representation (ChessRepresentation): The chess board state at this specific state.
        parent_state (StateChessGame): The preceding state from which this state was derived.
        move (chess.Move): The move that led to this state.
        h (float or None): A heuristic value, likely used for evaluation in search algorithms.
    """

    def __init__(self, game_representation=None, state_parent=None, move=None):
        """
        Initializes the chess game state.
        :param game_representation: The chess board state.
                Defaults to a new chess board state if not provided.
        :param state_parent: The preceding state. Defaults to None.
        :param move: The move leading to this state. Defaults to None.
        """
        self.game_representation = game_representation
        self.parent_state = state_parent
        self.move = move
        self.h = None

        if self.game_representation is None:
            self.game_representation = ChessRepresentation()

    def is_endgame(self):
        """
        Checks if the game is over.
        :return: True if the game is over, False otherwise.
        """
        return self.game_representation.is_game_over()

    def is_victory(self):
        """
        Checks if the current state is a checkmate.
        :return: True if it's checkmate, False otherwise.
        """
        return self.game_representation.is_victory()

    def is_draw(self):
        """
        Checks if the game is a draw.
        :return: True if the game is a draw, False otherwise.
        """
        return self.game_representation.is_draw()

    def can_claim_draw(self):
        """
        Checks if a draw can be claimed based on the current state.
        :return: True if a draw can be claimed, False otherwise.
        """
        return self.game_representation.can_claim_draw()

    def winner(self):
        """
        Determines the winner of the game.
        :return: True if White is the winner, False if Black is the winner,
                None if no winner.
        """
        return self.game_representation.winner()

    def turn(self):
        """
        Returns the current player's turn.
        :return: True if it's White's turn, False if it's Black's turn.
        """
        return self.game_representation.turn()

    def game_over_eval(self):
        """
        Evaluates the game if it's over.
        :return: Positive infinity if White wins, negative infinity if Black wins,
                0 if it's a draw, None if the game is not over.
        """
        if self.is_victory():
            return np.inf if self.winner() else -np.inf
        if self.is_draw():
            return 0
        return None

    def __eq__(self, other):
        if not isinstance(other, StateChessGame):
            return False
        return self.game_representation == other.game_representation

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.game_representation))
