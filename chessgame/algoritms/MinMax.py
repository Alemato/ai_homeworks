import numpy as np


class MinMax:
    """
    Implementation of the Minimax algorithm for game state evaluation and decision-making.

    Attributes:
        game: An instance of a game object which provides interface methods for the game state and its neighbors.
        heuristic: An instance of a heuristic object used to evaluate game states.
        max_depth: The maximum depth for the minimax search. Default is 1.
        prune_count: Count of the times pruning occurred during the search
                    (not actively used in this class but reserved for possible extensions).
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
        self.prune_count = 0
        self.eval_count = 0

    @staticmethod
    def pick(states, parent_turn):
        """
        Picks the best state based on the heuristic values.

        This static method selects the best game state from a list of states based on their heuristic values.
        The selection is determined by whether it's the maximizing player's turn or the minimizing player's turn.

        :param states: List of game states to pick from.
        :param parent_turn: Indicates whose turn it is: True for the player trying to maximize and False for
                            the player trying to minimize.
        :return: The best state based on the heuristic value.
        """
        if parent_turn:
            return max(states, key=lambda state: state.h)  # Select the state with the highest heuristic value.
        else:
            return min(states, key=lambda state: state.h)  # Select the state with the lowest heuristic value.

    def evaluate(self, states, parent_turn):
        """
        Evaluates a list of game states using the Minimax algorithm.

        This method evaluates a list of game states using the Minimax algorithm, which is a decision-making algorithm in
        game theory for minimizing the possible loss for a worst-case scenario. It assigns heuristic values to
        each state based on the algorithm's calculations.

        :param states: List of game states to evaluate.
        :param parent_turn: Indicates whose turn it is: True for the player trying to maximize and False
                            for the player trying to minimize.
        """
        for state in states:
            if state.can_claim_draw():
                state.h = 0.0  # Set the heuristic value to 0 if the game can be claimed as a draw.
            else:
                # Calculate heuristic value using Minimax.
                state.h = self.__minmax(state, self.max_depth - 1, not parent_turn)

    def __minmax(self, state, depth, turn):
        """
        Recursive helper method to perform the Minimax search.

        This private method performs a recursive Minimax search on a game tree to determine the heuristic
        value of a given game state.

        :param state: The current game state.
        :param depth: The current depth in the search.
        :param turn: Indicates whose turn it is: True for the player trying to maximize and False for the player
                    trying to minimize.
        :return: Heuristic value of the provided game state.
        """
        self.eval_count += 1  # Increment evaluation count.
        neighbors = self.game.neighbors(state)  # Get neighboring states from the current state.

        # Base cases: If the search depth is 0 or if the game is in an endgame state, return the heuristic value.
        if depth == 0 or self.game.is_endgame(state.game_board):
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

    def search(self, state):
        """
        Initiates the Minimax search for a given game state.

        This method initializes the Minimax search process for a given game state.
        It calculates the heuristic values for the neighboring states and selects the best next state based
        on the Minimax algorithm.

        :param state: The game state to start the search from.
        :return:  Best next game state based on the Minimax algorithm.
        """
        neighbors = self.game.neighbors(state)  # Get neighboring states from the current state.
        self.evaluate(neighbors, state.turn())  # Calculate heuristic values for the neighbors.
        return self.pick(neighbors, state.turn())  # Select the best next state using the Minimax algorithm.
