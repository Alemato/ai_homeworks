import heapq


class AStar:
    def __init__(self, game, heuristic):
        self.game = game
        self.heuristic = heuristic
        self.horizon = []  # Orizzonte degli stati come coda prioritaria
        self.visited = set()  # Set di stati visitati
        self.push_count = 0  # Contatore per le inserzioni nella coda prioritaria

    def pick(self):
        return heapq.heappop(self.horizon)[2]

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
            self.push_count += 1
            heapq.heappush(self.horizon, (self.evaluate(state), self.push_count, state))

        # Controlla se ci sono stati finali nell'orizzonte
        for _, _, state_in_horizon in self.horizon:
            if self.game.is_end_game(state_in_horizon.game_board):
                self.horizon.remove((state_in_horizon.f, state_in_horizon))
                self.visited.add(state_in_horizon)
                return state_in_horizon

        # Scopre nuovi stati
        neighbors = self.game.neighbors(state)
        self.visited.add(state)

        # Aggiunge al 'horizon' nuovi stati e valuta
        for n in neighbors:
            if n not in self.visited:
                self.push_count += 1
                heapq.heappush(self.horizon, (self.evaluate(n), self.push_count, n))

        # Rimuove gli stati visitati dal 'horizon'
        self.horizon = [(f, count, s) for f, count, s in self.horizon if s not in self.visited]

        if self.horizon:
            return self.pick()
        return None
