class BestFirst:
    def __init__(self, game, heuristic):
        self.game = game
        self.heuristic = heuristic
        self.horizon = []
        self.visited = set()

    def pick(self):
        # Ordina gli stati in base al valore euristico (dal più basso al più alto)
        self.horizon.sort(key=lambda state: state.f, reverse=False)
        # Rimuovi ed estrai il primo stato dall'orizzonte
        return self.horizon.pop(0)

    def evaluate(self, state):
        state.h = self.heuristic.h(state)
        state.f = state.h
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

        if len(self.horizon) > 0:
            return self.pick()

        return None
