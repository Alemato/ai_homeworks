import chess


class StateChessGame:
    """
    Represents a state in a chess game, including the board configuration and various heuristic evaluations.

    Attributes:
        game_board (chess.Board): The current chess board configuration.
        parent_state (StateChessGame): The parent state from which this state is derived.
        move (chess.Move): The move that led to this state.
        h (float): General heuristic value for the state.
        h0 (float): Heuristic value used for h0 cutoff.
        hl (float): Heuristic value used for hl cutoff.
        hr (float): Heuristic value for the cut of the nonlinear regressor.
    """

    def __init__(self, game_board=None, state_parent=None, move=None):
        """
        Initializes a new game state.

        :param game_board: The current chess board configuration. If None, initializes a new chess board.
        :param state_parent: The parent state from which this state is derived.
        :param move: The move that led to this state.
        """
        self.game_board = game_board  # The current chess board (chess.Board object).
        self.parent_state = state_parent  # The parent state from which this state is derived.
        self.move = move  # The move that led to this state.
        self.h = None  # General heuristic value for the state.
        self.h0 = None  # Heuristic value used for h0 cutoff.
        self.hl = None  # Heuristic value used for hl cutoff.
        self.hr = None  # Heuristic value used for nonlinear regressor cutoff.

        # If no game board is provided, initialize a new chess board.
        if self.game_board is None:
            self.game_board = chess.Board()

    def __eq__(self, other):
        """
        Checks if this state is equal to another state. States are considered equal if they have the same game
        board configuration.

        :param other: The other StateChessGame object to compare with.
        :return: True if the states are equal, False otherwise.
        """
        if not isinstance(other, StateChessGame):
            return False
        return self.game_board == other.game_board

    def __ne__(self, other):
        """
        Checks if this state is not equal to another state. It relies on the __eq__ method.

        :param other: The other StateChessGame object to compare with.
        :return: True if the states are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Generates a hash for the state. This is based on the string representation of the game board, allowing the state
        to be used in hash tables or sets.

        :return: The hash of the state.
        """
        return hash(str(self.game_board))
