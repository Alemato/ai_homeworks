import chess


class StateChessGame:
    """
    Represents a specific state of a chess game, encapsulating details about the game
    at this state, its parent state, and the move that led to this state.

    Attributes:
        game_representation (ChessGame): The chess board state at this specific state.
        parent_state (StateChessGame): The preceding state from which this state was derived.
        move (chess.Move): The move that led to this state.
        h (float or None): A heuristic value, likely used for evaluation in search algorithms.
    """

    def __init__(self, game_board=None, state_parent=None, move=None):
        """
        Initializes the chess game state.
        :param game_board: The chess board state.
                Defaults to a new chess board state if not provided.
        :param state_parent: The preceding state. Defaults to None.
        :param move: The move leading to this state. Defaults to None.
        """
        self.game_board = game_board
        self.parent_state = state_parent
        self.move = move
        self.h = None
        self.h0 = None
        self.hl = None

        if self.game_board is None:
            self.game_board = chess.Board()

    def __eq__(self, other):
        if not isinstance(other, StateChessGame):
            return False
        return self.game_board == other.game_board

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.game_board))
