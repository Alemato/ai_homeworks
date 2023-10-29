from StateChessGame import StateChessGame


class ChessGame:
    def neighbors(self, state: StateChessGame):
        neighbors = []

        for legal_move in state.game_representation.get_all_legal_moves():
            representation = state.game_representation.make_a_move(legal_move)
            neighbor = StateChessGame(game_representation=representation, state_parent=state,
                                      move=None)
            neighbors.append(neighbor)
        return neighbors
