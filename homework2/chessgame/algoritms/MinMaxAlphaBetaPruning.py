from chessgame import StateChessGame


class MinMaxAlphaBetaPruning:
    """
    Implements the Minimax algorithm with Alpha-Beta pruning for a chess game.

    Attributes:
        game (StateChessGame): The current state of the chess game.
        heuristic (function): Heuristic function used to evaluate game states.
        max_depth (int): Maximum depth for the Minimax search.
        prune_count (int): Count of the number of pruned branches.
        eval_count (int): Count of the number of evaluations performed.
    """

    def __init__(self, game, heuristic, max_depth=1):
        """
        Initializes the MinMaxAlphaBetaPruning class with a game, heuristic function, and maximum search depth.
        :param game: The current state of the chess game.
        :param heuristic: Heuristic function used for evaluating game states.
        :param max_depth: Maximum depth for the Minimax search. Defaults to 1.
        """
        self.game = game  # The current state of the chess game.
        self.heuristic = heuristic  # Heuristic function used to evaluate game states.
        self.max_depth = max_depth  # Maximum depth for the Minimax search.
        self.prune_count = 0  # Count of the number of pruned branches.
        self.eval_count = 0  # Count of the number of evaluations performed.

    def pick(self, states, parent_turn):
        """
        Selects the best state from a list of states based on the player's turn.

        :param states: A list of game states to evaluate.
        :param parent_turn: A flag indicating if it's the parent player's turn.
        :return: The state with the maximum (or minimum) heuristic value based on the player's turn.
        """
        # If it's the parent's turn, choose the state with the maximum heuristic value.
        if parent_turn:
            return max(states, key=lambda state: state.h)
        # If it's the opponent's turn, choose the state with the minimum heuristic value.
        else:
            return min(states, key=lambda state: state.h)

    def evaluate(self, states, parent_turn):
        """
        Evaluates a list of states and updates their heuristic values.

        :param states: A list of game states to evaluate.
        :param parent_turn: A flag indicating if it's the parent player's turn.
        """
        for state in states:
            # If a draw can be claimed in the current state, set heuristic value to 0.0.
            if state.game_board.can_claim_draw():
                state.h = 0.0
            else:
                # Otherwise, evaluate the state using the Minimax algorithm with Alpha-Beta pruning.
                state.h = self.__minmax_alpha_beta(state, self.max_depth - 1, float("-inf"), float("inf"),
                                                   not parent_turn)


    def __minmax_alpha_beta(self, state, depth, alpha, beta, turn):
        """
        Private method implementing the Minimax algorithm with Alpha-Beta pruning.

        :param state: The current game state.
        :param depth: The current depth in the game tree.
        :param alpha: The alpha value for Alpha-Beta pruning.
        :param beta: The beta value for Alpha-Beta pruning.
        :param turn: Flag indicating if it's the maximizing player's turn.
        :return: The heuristic value of the state.
        """
        self.eval_count += 1

        # Base case: if maximum depth is reached or the game is over, return the heuristic value of the state.
        if depth == 0 or state.game_board.is_game_over():
            return self.heuristic.h(state)

        # Generate all possible moves (neighbors) from the current state.
        neighbors = self.game.neighbors(state)

        if turn:  # If it's the maximizing player's turn.
            value = float("-inf")
            for neighbor in neighbors:
                # Recursively call the function to evaluate the neighbor state, updating the value and alpha.
                value = max(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                # Alpha-Beta pruning: if alpha is greater or equal to beta, prune this branch.
                if alpha >= beta:
                    self.prune_count += 1
                    break
            return value
        else:  # If it's the minimizing player's turn.
            value = float("inf")
            for neighbor in neighbors:
                # Similarly, for the minimizing player, update the value and beta.
                value = min(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                # Alpha-Beta pruning: if beta is less or equal to alpha, prune this branch.
                if beta <= alpha:
                    self.prune_count += 1
                    break
            return value


    def search(self, state: StateChessGame):
        """
        Public method to start the Minimax search with Alpha-Beta pruning from a given state.

        :param state: The current state of the chess game.
        :return: The best next state for the current player.
        """
        # Generate all possible moves (neighbors) from the current state.
        neighbors = self.game.neighbors(state)
        # Evaluate the neighbors to update their heuristic values.
        self.evaluate(neighbors, state.game_board.turn)
        # Choose the best move based on the current player's turn.
        return self.pick(neighbors, state.game_board.turn)
