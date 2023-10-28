import numpy as np

from State import State


class MinMaxAlphaBetaPruning:
    def __init__(self, game, heuristic, max_depth=1):
        self.game = game
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.prune_count = 0
        self.eval_count = 0

    @staticmethod
    def pick(states, parent_turn):
        if parent_turn:
            return max(states, key=lambda state: state.h)
        else:
            return min(states, key=lambda state: state.h)

    def evaluate(self, states, parent_turn):
        for state in states:
            if self.game.ask_draw(state.game_board):
                state.h = 0.0
                state.f = state.h
            else:
                state.h = self.__minmax_alpha_beta(state, self.max_depth - 1, -np.inf, np.inf, not parent_turn)
                state.f = state.h

    def __minmax_alpha_beta(self, state, depth, alpha, beta, turn):
        self.eval_count += 1
        neighbors = self.game.neighbors(state)

        if depth == 0 or self.game.is_endgame(state.game_board):
            return self.heuristic.h(state)

        if turn:  # Maximizing player
            value = -np.inf
            for neighbor in neighbors:
                value = max(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:  # Pruning
                    self.prune_count += 1
                    break
            return value
        else:  # Minimizing player
            value = np.inf
            for neighbor in neighbors:
                value = min(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:  # Pruning
                    self.prune_count += 1
                    break
            return value

    def search(self, state: State):
        neighbors = self.game.neighbors(state)
        self.evaluate(neighbors, state.game_board.turn)
        return self.pick(neighbors, state.game_board.turn)
