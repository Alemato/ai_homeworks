from chessgame import StateChessGame


class MinMaxAlphaBetaPruningHlCut:
    """
    Extends the Minimax algorithm with Alpha-Beta pruning for a chess game, incorporating h0 and hl cutoff heuristics.

    Attributes:
        game (StateChessGame): The current state of the chess game.
        heuristic (function): Main heuristic function for evaluating game states.
        h0_cut (function): Heuristic function used for the h0 cutoff.
        k (int): Number of states to consider after applying the h0 and hl cutoffs.
        l (int): Depth for the hl cutoff calculation.
        max_depth (int): Maximum depth for the Minimax search.
        prune_count (int): Count of pruned branches in the main search.
        eval_count (int): Count of evaluations in the main search.
        eval_h0_cut_count (int): Count of evaluations for the h0 cutoff.
        prune_h0_cut_count (int): Count of pruned branches due to the h0 cutoff.
        eval_hl_cut_count (int): Count of evaluations for the hl cutoff.
        prune_hl_cut_count (int): Count of pruned branches due to the hl cutoff.
        memoization (dict): Dictionary for memoization to store previously calculated states.
    """

    def __init__(self, game, heuristic, h0_cut, k=5, l=3, max_depth=1):
        """
        Initializes the MinMaxAlphaBetaPruningHlCut class with game settings, heuristics, and search parameters.

        :param game: The current state of the chess game.
        :param heuristic: Main heuristic function used for evaluating game states.
        :param h0_cut: Heuristic function used for the h0 cutoff.
        :param k: Number of states to consider after applying the h0 and hl cutoffs. Defaults to 5.
        :param l: Depth for the hl cutoff calculation. Defaults to 3.
        :param max_depth: Maximum depth for the Minimax search. Defaults to 1.
        """
        self.game = game  # The current state of the chess game.
        self.heuristic = heuristic  # Main heuristic function for evaluating game states.
        self.h0_cut = h0_cut  # Heuristic function used for the h0 cutoff.
        self.k = k  # Number of states to consider after applying the h0 and hl cutoffs.
        self.l = l  # Depth for the hl cutoff calculation.
        self.max_depth = max_depth  # Maximum depth for the Minimax search.
        self.prune_count = 0  # Count of pruned branches in the main search.
        self.eval_count = 0  # Count of evaluations in the main search.
        self.eval_h0_cut_count = 0  # Count of evaluations for the h0 cutoff.
        self.prune_h0_cut_count = 0  # Count of pruned branches due to the h0 cutoff.
        self.eval_hl_cut_count = 0  # Count of evaluations for the hl cutoff.
        self.prune_hl_cut_count = 0  # Count of pruned branches due to the hl cutoff.
        self.memoization = {}  # Dictionary for storing previously calculated states.


    def pick(self, states, parent_turn):
        """
        Selects the best state based on the player's turn.

        :param states: A list of game states to evaluate.
        :param parent_turn: A flag indicating if it's the parent player's turn.
        :return: The state with the maximum (or minimum) heuristic value based on the player's turn.
        """
        # Choose the state with the maximum or minimum heuristic value depending on the player's turn.
        if parent_turn:
            return max(states, key=lambda state: state.h)
        else:
            return min(states, key=lambda state: state.h)


    def evaluate(self, states, parent_turn):
        """
        Evaluates a list of states and updates their heuristic values.

        :param states: A list of game states to evaluate.
        :param parent_turn: A flag indicating if it's the parent player's turn.
        """
        for state in states:
            # If a draw can be claimed, set heuristic value to 0.0.
            if state.game_board.can_claim_draw():
                state.h = 0.0
            else:
                # Evaluate using the Minimax algorithm with Alpha-Beta pruning.
                state.h = self.__minmax_alpha_beta(state, self.max_depth - 1, float("-inf"), float("inf"),
                                                   not parent_turn)

    # Private method implementing the Minimax algorithm with Alpha-Beta pruning and memoization.
    def __minmax_alpha_beta(self, state, depth, alpha, beta, turn):
        """
        Private method implementing the Minimax algorithm with Alpha-Beta pruning and memoization.

        :param state: The current game state.
        :param depth: The current depth in the game tree.
        :param alpha: The alpha value for Alpha-Beta pruning.
        :param beta: The beta value for Alpha-Beta pruning.
        :param turn: Flag indicating if it's the maximizing player's turn.
        :return: The heuristic value of the state.
        """
        self.eval_count += 1

        # Check if the state is already evaluated and stored in memoization.
        if (state, depth, turn) in self.memoization:
            return self.memoization[(state, depth, turn)]

        # Base case: if maximum depth is reached or the game is over, return the heuristic value.
        if depth == 0 or state.game_board.is_game_over():
            return self.heuristic.h(state)

        # Generate possible moves (neighbors), applying the h0 cutoff.
        neighbors = self.game.neighbors(state)
        top_neighbors = self.__h0_cut(neighbors, state.game_board.turn)

        if turn:  # Maximizing player's turn.
            value = float("-inf")
            for neighbor in top_neighbors:
                # Recursively evaluate the state, update value and alpha.
                value = max(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                # Alpha-Beta pruning: prune if alpha >= beta.
                if alpha >= beta:
                    self.prune_count += 1
                    break
            self.memoization[(state, depth, turn)] = value
            return value
        else:  # Minimizing player's turn.
            value = float("inf")
            for neighbor in top_neighbors:
                # Similar evaluation for the minimizing player.
                value = min(value, self.__minmax_alpha_beta(neighbor, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                # Prune if beta <= alpha.
                if beta <= alpha:
                    self.prune_count += 1
                    break
            self.memoization[(state, depth, turn)] = value
            return value

    def __h0_cut(self, states, turn):
        """
        Applies the h0 cutoff heuristic to limit the number of states considered.

        :param states: A list of game states.
        :param turn: Flag indicating the current player's turn.
        :return: A list of states after applying the h0 cutoff.
        """
        initial_count = len(states)
        # Evaluate states using the h0 heuristic and count evaluations.
        for state in states:
            state.h0 = self.h0_cut.h(state)
            self.eval_h0_cut_count += 1

        # Sort and select the top k states based on the h0 heuristic value.
        sorted_states = sorted(states, key=lambda state: state.h0, reverse=turn)[:self.k]
        # Count how many states were pruned by this process.
        self.prune_h0_cut_count += initial_count - len(sorted_states)

        return sorted_states

    def __hl_cut(self, states, turn):
        """
        Applies the hl cutoff heuristic to further limit the number of states considered.

        :param states: A list of game states.
        :param turn: Flag indicating the current player's turn.
        :return: A list of states after applying the hl cutoff.
        """
        initial_count = len(states)
        # Evaluate states using a deeper level of the Minimax algorithm (hl cutoff).
        for state in states:
            state.hl = self.__minmax_alpha_beta_hl(state, self.l - 1, float("-inf"), float("inf"), not turn)
        # Sort and select the top k states based on the hl heuristic value.
        sorted_states = sorted(states, key=lambda state: state.hl, reverse=turn)[:self.k]
        # Count how many states were pruned by this process.
        self.prune_hl_cut_count += initial_count - len(sorted_states)
        return sorted_states

    def __minmax_alpha_beta_hl(self, state, depth, alpha, beta, turn):
        """
        Implements a deeper level of the Minimax algorithm for the hl cutoff.

        :param state: The current game state.
        :param depth: The current depth in the game tree.
        :param alpha: The alpha value for Alpha-Beta pruning.
        :param beta: The beta value for Alpha-Beta pruning.
        :param turn: Flag indicating if it's the maximizing player's turn.
        :return: The heuristic value of the state.
        """
        self.eval_hl_cut_count += 1

        # Base case: if maximum depth is reached or the game is over, return the heuristic value from h0_cut.
        if depth == 0 or state.game_board.is_game_over():
            return self.h0_cut.h(state)

        neighbors = self.game.neighbors(state)

        if turn:  # Maximizing player's turn.
            value = float("-inf")
            for neighbor in neighbors:
                # Recursively evaluate the state for hl cutoff, update value and alpha.
                value = max(value, self.__minmax_alpha_beta_hl(neighbor, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                # Alpha-Beta pruning for hl cutoff.
                if alpha >= beta:
                    self.prune_hl_cut_count += 1
                    break
            return value
        else:  # Minimizing player's turn.
            value = float("inf")
            for neighbor in neighbors:
                # Similar evaluation for the minimizing player for hl cutoff.
                value = min(value, self.__minmax_alpha_beta_hl(neighbor, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                # Prune if beta <= alpha in hl cutoff.
                if beta <= alpha:
                    self.prune_hl_cut_count += 1
                    break
            return value

    def search(self, state: StateChessGame):
        """
        Public method to start the search with Alpha-Beta pruning, h0, and hl cutoffs.

        :param state: The current state of the chess game.
        :return: The best next state for the current player.
        """
        # Generate possible moves, applying the hl cutoff.
        neighbors = self.game.neighbors(state)
        top_neighbors = self.__hl_cut(neighbors, state.game_board.turn)
        # Evaluate the top neighbors and choose the best move based on the player's turn.
        self.evaluate(top_neighbors, state.game_board.turn)
        return self.pick(top_neighbors, state.game_board.turn)
