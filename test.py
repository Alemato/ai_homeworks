class FifteenPuzzleGame:
    def init(self):
        # Stato obiettivo per il 15-Puzzle.
        self.goal_state = tuple(list(range(1, 16)) + [0])

    def is_goal(self, state):
        """Verifica se uno stato è l'obiettivo."""
        return state == self.goal_state

    def get_neighbors(self, state):
        """Restituisce gli stati raggiungibili da uno stato corrente."""
        neighbors = []
        # Trova l'indice della casella vuota (0) nella tupla
        zero_index = state.index(0)
        zero_row, zero_col = divmod(zero_index, 4)

        # Possibili mosse: (dx, dy)
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for move in moves:
            new_row, new_col = zero_row + move[0], zero_col + move[1]
            if 0 <= new_row < 4 and 0 <= new_col < 4:  # Verifica che la mossa non esca fuori dai limiti
                new_index = new_row * 4 + new_col
                # Crea un nuovo stato scambiando la casella vuota con la casella adiacente
                new_state = list(state)
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                neighbors.append(tuple(new_state))

        return neighbors

    def get_cost(self, current, neighbor):
        """Restituisce il costo di transizione tra due stati. Per il 15-Puzzle, questo sarà sempre 1 per ogni mossa."""
        return 1

    def is_solvable(self, state):
        """ Verifica se uno stato del 15-Puzzle è risolvibile. """
        inversions = self.count_inversions(state)
        # Se il numero di inversioni è pari, lo stato è risolvibile.
        return inversions % 2 == 0

    def count_inversions(self, state):
        """ Conta il numero di inversioni in uno stato del 15-Puzzle. """
        inversions = 0
        for i in range(len(state) - 1):
            for j in range(i + 1, len(state)):
                if state[i] > 0 and state[j] > 0 and state[i] > state[j]:
                    inversions += 1
        return inversions
