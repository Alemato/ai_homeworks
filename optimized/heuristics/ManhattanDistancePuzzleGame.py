import numpy as np


class ManhattanDistancePuzzleGame:

    def __init__(self, game_board_end_game):
        self.game_board_end_game = np.array(game_board_end_game)

    def h(self, state):
        total_distance = 0

        for number in range(16):  # Includiamo 0 ora
            if number == 0:  # Salta la casella vuota
                continue

            curr_coords = np.array(np.where(state.game_board == number))
            target_coords = np.array(np.where(self.game_board_end_game == number))

            curr_x, curr_y = curr_coords.T[0]
            target_x, target_y = target_coords.T[0]

            # Calcolo della Manhattan distance
            distance = abs(curr_x - target_x) + abs(curr_y - target_y)
            total_distance += distance.item()

        return total_distance
