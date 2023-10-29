import numpy as np

from ChessRepresentation import ChessRepresentation


class StateChessGame:
    def __init__(self, game_representation=None, state_parent=None, move=None):
        self.game_representation = game_representation
        self.parent_state = state_parent
        self.move = move
        self.h = None

        if self.game_representation is None:
            self.game_representation = ChessRepresentation()

    def is_endgame(self):
        return self.game_representation.is_game_over()

    def is_victory(self):
        return self.game_representation.is_victory()

    def is_draw(self):
        return self.game_representation.is_draw()

    def can_claim_draw(self):
        return self.game_representation.can_claim_draw()

    def winner(self):
        return self.game_representation.winner()

    def turn(self):
        return self.game_representation.turn()

    def game_over_eval(self):
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
