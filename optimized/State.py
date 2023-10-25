import numpy as np


class State:
    def __init__(self, game_board, move=None, parent_state=None):
        self.game_board = np.array(game_board)
        self.parent_state = parent_state
        self.move = move
        self.h = None
        self.f = None
        self.g = None

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return np.array_equal(self.game_board, other.game_board)

    def __hash__(self):
        return hash(self.game_board.tobytes())

    def __str__(self):
        return "\n".join("\t".join(map(str, row)) for row in self.game_board)
