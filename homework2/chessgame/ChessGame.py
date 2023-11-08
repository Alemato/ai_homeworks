from StateChessGame import StateChessGame


class ChessGame:
    """
    Represents a chess game that provides functionality to determine neighboring states.

    Methods:
        neighbors: Computes the neighboring states of a given chess game state.
    """
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
            neighbor = StateChessGame(game_representation=representation, state_parent=state,
                                      move=legal_move)
            neighbors.append(neighbor)
        return neighbors
