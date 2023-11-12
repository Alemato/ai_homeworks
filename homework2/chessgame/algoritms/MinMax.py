import numpy as np

from chessgame import StateChessGame


class MinMax:
    """
    Implementation of the Minimax algorithm for game state evaluation and decision-making.

    Attributes:
        game: An instance of a game object which provides interface methods for the game state and its neighbors.
        heuristic: An instance of a heuristic object used to evaluate game states.
        max_depth: The maximum depth for the minimax search. Default is 1.
        eval_count: Count of the evaluations performed during the search.
        """

    def __init__(self, game, heuristic, max_depth=1):
        """
        Initializes an instance of the MinMax class.
        :param game: The game for which the search is performed.
        :param heuristic: The heuristic used to evaluate the game states.
        :param max_depth: The maximum depth of the search. Default is 1.
        """
        self.game = game
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.eval_count = 0

    def pick(self, states, parent_turn):
        if parent_turn:
            return max(states, key=lambda state: state.h)  # Select the state with the highest heuristic value.
        else:
            return min(states, key=lambda state: state.h)  # Select the state with the lowest heuristic value.

    def evaluate(self, states, parent_turn):
        for state in states:
            if state.game_board.can_claim_draw():
                state.h = 0.0  # Set the heuristic value to 0 if the game can be claimed as a draw.
            else:
                # Calculate heuristic value using Minimax.
                state.h = self.__minmax(state, self.max_depth - 1, not parent_turn)

    def __minmax(self, state, depth, turn):
        self.eval_count += 1  # Increment evaluation count.
        neighbors = self.game.neighbors(state)  # Get neighboring states from the current state.

        # Base cases: If the search depth is 0 or if the game is in an endgame state, return the heuristic value.
        if depth == 0 or state.game_board.is_game_over():
            return self.heuristic.h(state)

        if turn:
            value = -np.inf  # Initialize value for maximizing player to negative infinity.
            for child in neighbors:
                value = max(value, self.__minmax(child, depth - 1, False))  # Recursively maximize.
            return value
        else:
            value = np.inf  # Initialize value for minimizing player to positive infinity.
            for child in neighbors:
                value = min(value, self.__minmax(child, depth - 1, True))  # Recursively minimize.
            return value

    def search(self, state: StateChessGame):
        neighbors = self.game.neighbors(state)  # Get neighboring states from the current state.
        self.evaluate(neighbors, state.game_board.turn)  # Calculate heuristic values for the neighbors.
        return self.pick(neighbors, state.game_board.turn)  # Select the best next state using the Minimax algorithm.
