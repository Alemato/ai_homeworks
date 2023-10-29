from fifteenpuzzlegame import StateFifteenPuzzleGame


class BestFirst:
    """
    Represents the Best-First Search algorithm

    This class provides methods to perform the Best-First Search based on a given heuristic.
    The search selects states to expand based on the lowest heuristic value.

    Attributes:
        heuristic: The heuristic used to estimate the cost from a given state to the goal state.
        game: The Fifteen Puzzle game.
        horizon (set): The set of states that are on the boundary of the explored space.
        explored (set): The set of states that have already been explored.
    """

    def __init__(self, game, heuristic):
        """
        Initializes the BestFirst search with a game and heuristic.
        :param game: The Fifteen Puzzle game.
        :param heuristic: The heuristic used to estimate the cost from a state to the goal state.
        """
        self.heuristic = heuristic
        self.game = game
        self.horizon = set()
        self.explored = set()

    def f_value(self, states):
        """
        Computes the heuristic value for a given set of states.
        :param states: A set of states for which the heuristic values need to be computed.
        """
        for state in states:
            if state.f is None:
                state.f = self.heuristic.h(state)

    def evaluate(self, state: StateFifteenPuzzleGame):
        """
        Computes the heuristic value for a specific state.
        :param state: The state for which the heuristic value needs to be computed.
        :return:
        """
        if state.f is None:
            state.f = self.heuristic.h(state)
            state.h = state.f

    def pick(self):
        """
        Selects the state with the lowest heuristic value from the horizon.
        :return: The state with the lowest heuristic value.
        """
        return min(self.horizon, key=lambda state: state.f)

    def search(self, state):
        """
        Expands the search from the given state, evaluating neighboring states and adding them to the horizon.
        :param state: The state from which the search should be expanded.
        :return: The state with the lowest heuristic value. None otherwise.
        """
        if state not in self.horizon:
            self.evaluate(state)
            self.horizon.add(state)

        self.explored.add(state)

        neighbors = self.game.neighbors(state)

        for neighbor in neighbors:
            if neighbor not in self.horizon and neighbor not in self.explored:
                self.evaluate(neighbor)
                if neighbor.is_end_game():
                    return neighbor
                self.horizon.add(neighbor)

        self.horizon.remove(state)

        if len(self.horizon) > 0:
            return self.pick()
        else:
            return None
