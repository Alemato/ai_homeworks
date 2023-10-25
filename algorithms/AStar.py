class AStar:
    def __init__(self, game, heuristic):
        self.game = game
        self.heuristic = heuristic
        self.horizon = []  # Orizzonte degli stati
        self.visited = set()  # Insieme degli stati visitati

    def pick(self):
        # Ordina gli stati in base al valore euristico f (dal più basso al più alto)
        self.horizon.sort(key=lambda state: state.f, reverse=False)
        return self.horizon[0]

    def evaluate(self, state):
        state.h = self.heuristic.h(state)
        if state.parent_state is None:
            state.g = 0
        else:
            state.g = state.parent_state.g + self.game.const_move(state.move)
        state.f = state.h + state.g
        return state.f

    def search(self, state):
        if state not in self.horizon:
            self.horizon.append(state)
            self.evaluate(state)

        neighbors = self.game.neighbors(state)
        self.visited.add(state)

        for n in neighbors:
            if n not in self.horizon and n not in self.visited:
                self.horizon.append(n)
                self.evaluate(n)

        for s in self.horizon:
            if self.game.is_end_game(s.game_board):
                self.horizon.remove(s)
                self.visited.add(s)
                return s

        for s in self.horizon:
            if s in self.visited:
                self.horizon.remove(s)

        if len(self.horizon) > 0:
            s = self.pick()
            return s
        return None
