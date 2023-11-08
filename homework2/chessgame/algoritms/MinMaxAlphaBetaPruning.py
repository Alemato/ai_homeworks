import numpy as np


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

    @staticmethod
    def pick(states, parent_turn):
        """
        Picks the best state based on the heuristic values.

        This function evaluates a list of game states and selects the state that optimizes
        the current player's position.
        If it is the maximizing player's turn (parent_turn is True), the state with the highest heuristic
        value is chosen.
        Otherwise, if it is the minimizing player's turn (parent_turn is False), the state with the lowest heuristic
        value is chosen.

        :param states: List of game states to pick from.
        :param parent_turn: Indicates whose turn it is: True for maximizing player and False for minimizing player.
        :return: The best state based on the heuristic value.
        """
        if parent_turn:
            # If it's the maximizing player's turn, select the state with the highest heuristic value.
            return max(states, key=lambda state: state.h)
        else:
            # If it's the minimizing player's turn, select the state with the lowest heuristic value.
            return min(states, key=lambda state: state.h)

    def evaluate(self, states, parent_turn):
        """
        Evaluates a list of game states using the Minimax algorithm with Alpha-Beta pruning.

        This function evaluates a list of game states using the Minimax algorithm with Alpha-Beta pruning.
        It assigns a heuristic value to each state based on its evaluation at a specified depth in the game tree.
        The depth of the evaluation is determined by the 'max_depth' attribute of the object.

        :param states: List of game states to evaluate.
        :param parent_turn: Indicates whose turn it is: True for maximizing player and False for minimizing player.
        """
        for state in states:
            if state.can_claim_draw():
                # If the state can claim a draw, assign a heuristic value of 0.
                state.h = 0.0
            else:
                # Otherwise, use the Minimax algorithm with Alpha-Beta pruning to assign a heuristic value.
                state.h = self.__minmax_alpha_beta(state, self.max_depth - 1, -np.inf, np.inf, not parent_turn)

    def __minmax_alpha_beta(self, state, depth, alpha, beta, turn):
        """
        Recursive helper method to perform Minimax search with Alpha-Beta pruning.

        This private method performs a recursive Minimax search with Alpha-Beta pruning to find the optimal move
        in the game tree.
        It evaluates the provided game state and returns a heuristic value based on the current player's turn.

        :param state: Current game state.
        :param depth: Current depth in the search.
        :param alpha: Best already explored option for the maximizer.
        :param beta: Best already explored option for the minimizer.
        :param turn: Indicates whose turn it is: True for maximizing player and False for minimizing player.
        :return: Heuristic value of the provided game state.
        """
        self.eval_count += 1  # Count the number of state evaluations.
        neighbors = self.game.neighbors(state)  # Generate possible successor states.

        if depth == 0 or state.is_endgame():
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

    def search(self, state):
        """
        Initiates the Minimax search with Alpha-Beta pruning for a given game state.

        This method initializes the Minimax search with Alpha-Beta pruning to find the best next game state based on the
        current game state.
        It evaluates the neighboring states, chooses the best move, and returns the resulting game state.

        :param state: The game state to search from.
        :return: Best next game state based on the Minimax algorithm with Alpha-Beta pruning.
        """
        neighbors = self.game.neighbors(state)  # Generate possible successor states.
        self.evaluate(neighbors, state.turn())  # Evaluate the neighboring states using Minimax.
        return self.pick(neighbors, state.turn())  # Choose and return the best next game state.
