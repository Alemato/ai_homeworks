import joblib
import pandas as pd

from chessgame import StateChessGame
from chessgame.heuristics.ObservationBoard import ObservationBoard


class MinMaxAlphaBetaPruningHrCut:
    def __init__(self, game, heuristic, k=5, max_depth=1):
        self.game = game  # The current state of the chess game.
        self.heuristic = heuristic  # Main heuristic function used to evaluate game states.
        self.k = k  # Number of states to consider after applying the h0 cutoff.
        self.max_depth = max_depth  # Maximum depth for the Minimax search.
        self.prune_count = 0  # Count of pruned branches in the main search.
        self.eval_count = 0  # Count of evaluations in the main search.
        self.eval_hr_cut_count = 0  # Count of evaluations for the h0 cutoff.
        self.prune_hr_cut_count = 0  # Count of pruned branches due to the h0 cutoff.
        self.memoization = {}  # Dictionary for storing previously calculated states.
        self.mlp_regressor = joblib.load('mlp_regressor_model.joblib')
        self.observation = ObservationBoard(normalize_result=True)

    def pick(self, states, parent_turn):
        # Choose the state with the maximum or minimum heuristic value depending on the player's turn.
        if parent_turn:
            return max(states, key=lambda state: state.h)
        else:
            return min(states, key=lambda state: state.h)

    def evaluate(self, states, parent_turn):
        for state in states:
            # If a draw can be claimed, set heuristic value to 0.0.
            if state.game_board.can_claim_draw():
                state.h = 0.0
            else:
                # Otherwise, evaluate using the Minimax algorithm with Alpha-Beta pruning.
                state.h = self.__minmax_alpha_beta(state, self.max_depth - 1, float("-inf"), float("inf"),
                                                   not parent_turn)

    def __minmax_alpha_beta(self, state, depth, alpha, beta, turn):
        self.eval_count += 1

        # Check if the state is already evaluated and stored in memoization.
        if (state, depth, turn) in self.memoization:
            return self.memoization[(state, depth, turn)]

        # Base case: if maximum depth is reached or the game is over, return the heuristic value.
        if depth == 0 or state.game_board.is_game_over():
            return self.heuristic.h(state)

        # Generate possible moves (neighbors), applying the h0 cutoff.
        neighbors = self.game.neighbors(state)
        top_neighbors = self.__hr_cut(neighbors, state.game_board.turn)

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

    def __hr_cut(self, states, turn):
        initial_count = len(states)

        for state in states:
            observations = self.observation.h_piccoli(state.game_board)
            state.hr = self.__regressor_eval(observations)
            self.eval_hr_cut_count += 1

        # Sort and select the top k states based on the hr value.
        sorted_states = sorted(states, key=lambda state: state.hr, reverse=turn)[:self.k]
        # Count how many states were pruned by this process.
        self.prune_hr_cut_count += initial_count - len(sorted_states)

        return sorted_states

    def __regressor_eval(self, observations):
        colonne = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10',
                        'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19',
                        'h20']
        df = pd.DataFrame([observations], columns=colonne)
        return self.mlp_regressor.predict(df)[0]

    def search(self, state: StateChessGame):
        # Generate possible moves, applying the h0 cutoff.
        neighbors = self.game.neighbors(state)
        top_neighbors = self.__hr_cut(neighbors, state.game_board.turn)
        # Evaluate the top neighbors and choose the best move based on the player's turn.
        self.evaluate(top_neighbors, state.game_board.turn)
        return self.pick(top_neighbors, state.game_board.turn)
