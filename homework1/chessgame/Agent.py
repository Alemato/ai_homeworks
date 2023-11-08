class Agent:
    """
    Represents an agent that can act based on a given search algorithm and its current view of the world.

    Attributes:
        search_algorithm: A search algorithm that the agent uses to make decisions.
        view: The agent's current view of the world.
        old_view: The agent's previous view of the world.
    """

    def __init__(self, search_algorithm, initial_state):
        """
        Initializes the Agent with a search algorithm and an initial state.

        :param search_algorithm: The search algorithm to be used by the agent.
        :param initial_state: The initial state of the world as perceived by the agent.
        """
        self.search_algorithm = search_algorithm
        self.view = initial_state
        self.old_view = None

    def do_action(self, current_state_world):
        """
        Updates the agent's view based on the current state of the world and the search algorithm.
        :param current_state_world: The current state of the world.
        :return: The updated view of the agent.
        """
        self.view = self.search_algorithm.search(current_state_world)
        self.old_view = current_state_world
        return self.view
