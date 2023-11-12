import numpy as np

from chessgame import StateChessGame


class MinMaxAlphaBetaPruning:
    """
    Implementation of Minimax algorithm with Alpha-Beta pruning.

    Attributes:
        game: An instance of a game object that provides interface methods for the game state and its neighbors.
        heuristic: An instance of a heuristic object used to evaluate game states.
        max_depth: Maximum depth for the minimax search. Default is 1.
        prune_count: Count of the times pruning occurred during the search.
        eval_count: Count of the evaluations performed during the search.
    """

    def __init__(self, game, heuristic, max_depth=1):
        """
        Initializes an instance of the MinMaxAlphaBetaPruning class.
        :param game: The game for which the search is performed.
        :param heuristic: The heuristic to evaluate the game states.
        :param max_depth: Maximum depth of the search. Default is 1.
        """
        self.game = game
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.prune_count = 0
        self.eval_count = 0

    def pick(self, states, parent_turn):
        if parent_turn:
            # If it's the maximizing player's turn, select the state with the highest heuristic value.
            return max(states, key=lambda state: state.h)
        else:
            # If it's the minimizing player's turn, select the state with the lowest heuristic value.
            return min(states, key=lambda state: state.h)

    def evaluate(self, states, parent_turn):
        for state in states:
            if state.game_board.can_claim_draw():
                # If the state can claim a draw, assign a heuristic value of 0.
                state.h = 0.0
            else:
                # Otherwise, use the Minimax algorithm with Alpha-Beta pruning to assign a heuristic value.
                state.h = self.__minmax_alpha_beta(state, self.max_depth - 1, -np.inf, np.inf, not parent_turn)

    def __minmax_alpha_beta(self, state, depth, alpha, beta, turn):
        self.eval_count += 1  # Count the number of state evaluations.
        neighbors = self.game.neighbors(state)  # Generate possible successor states.

        if depth == 0 or state.game_board.is_game_over():
            # Base case: If the maximum depth is reached or the state represents an endgame, return the heuristic value.
            return self.heuristic.h(state)

        if turn:  # Maximizing player
            value = -np.inf
            for neighbor in neighbors:
                value = max(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)  # Update alpha with the maximum value found so far.
                if alpha >= beta:  # Alpha-Beta pruning: Stop evaluating if alpha is greater than or equal to beta.
                    self.prune_count += 1  # Count pruned branches.
                    break
            return value
        else:  # Minimizing player
            value = np.inf
            for neighbor in neighbors:
                value = min(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, True))
                beta = min(beta, value)  # Update beta with the minimum value found so far.
                if beta <= alpha:  # Alpha-Beta pruning: Stop evaluating if beta is less than or equal to alpha.
                    self.prune_count += 1  # Count pruned branches.
                    break
            return value

    def search(self, state: StateChessGame):
        neighbors = self.game.neighbors(state)  # Generate possible successor states.
        self.evaluate(neighbors, state.game_board.turn)  # Evaluate the neighboring states using Minimax.
        return self.pick(neighbors, state.game_board.turn)  # Choose and return the best next game state.
