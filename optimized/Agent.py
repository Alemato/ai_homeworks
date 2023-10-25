class Agent:
    def __init__(self, search_algorithm, initial_state):
        self.search_algorithm = search_algorithm
        self.view = initial_state
        self.old_view = None

    def do_action(self, current_state_world):
        self.view = self.search_algorithm.search(current_state_world)
        self.old_view = current_state_world
        return self.view
