import chess

from StateChessGame import StateChessGame


class ChessGame:
    """
    Represents a chess game that provides functionality to determine neighboring states.

    Methods:
        neighbors: Computes the neighboring states of a given chess game state.
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
    def neighbors(self, state: StateChessGame):
        """
        Determines the neighboring states of the provided chess game state.
        :param state: The current state of the chess game.
        :return: A list of neighboring states for the given state.
        """
        neighbors = []

        # Iterate through all legal moves and compute the resulting game state
        for legal_move in state.game_representation.get_all_legal_moves():
            representation = state.game_representation.make_a_move(legal_move)
            neighbor = StateChessGame(game_board=representation, state_parent=state,
                                      move=legal_move)
            neighbors.append(neighbor)
        return neighbors
