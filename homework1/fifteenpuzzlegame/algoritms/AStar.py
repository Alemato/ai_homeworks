class AStar:
    """
    Represents the A* Search algorithm

    This class provides methods to perform the A* Search based on a given heuristic.
    The search selects states to expand based on a combined cost (f value) which is
    the sum of the actual cost to reach the state (g value) and the estimated cost
    from the state to the goal (h value).

    Attributes:
        heuristic: The heuristic used to estimate the cost from a given state to the goal state.
        game: The Fifteen Puzzle game.
        horizon (set): The set of states that are on the boundary of the explored space.
        explored (set): The set of states that have already been explored.
    """

    def __init__(self, game, heuristic):
        """
        Initializes the AStarOp search with a game and heuristic.
        :param game: The Fifteen Puzzle game.
        :param heuristic: The heuristic used to estimate the cost from a state to the goal state.
        """
        self.heuristic = heuristic
        self.game = game
        self.horizon = set()  # A set to store the frontier nodes yet to be explored.
        self.explored = set()  # A set to keep track of already explored nodes.

    def evaluate(self, state):
        """
        Computes the cost (g value), heuristic value (h value), and combined cost (f value) for a given state.

        The g value is the actual cost to reach the state, the h value is the estimated cost from the state to the goal,
        and the f value is the sum of the g and h values.
        :param state: The state for which the costs need to be computed.
        """
        if state.g is None:
            if state.state_parent is None:
                state.g = 0
            else:
                state.g = state.state_parent.g + 1  # fixed cost set to 1

            state.h = self.heuristic.h(state)

            state.f = state.g + state.h

    def pick(self):
        """
        Selects the state with the lowest combined cost (f value) from the horizon.
        :return: The state with the lowest combined cost (f value).
        """
        return min(self.horizon, key=lambda state: state.f)

    def search(self, state):
        """
        Expands the search from the given state by exploring its neighbors.

        The method evaluates neighboring states of the given state, calculates their costs,
        and adds them to the search horizon if they haven't been explored before. It also updates the
        set of explored states.
        :param state: The state from which the search should be expanded.
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
