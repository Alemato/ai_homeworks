class ManhattanDistancePuzzleGame:

    def __init__(self, game_board_end_game):
        self.game_board_end_game = game_board_end_game

    def h(self, state):
        total_distance = 0

        for number in range(1, 16):  # We don't consider the empty tile.
            for i in range(4):
                for j in range(4):
                    if state.game_board[i][j] == number:
                        curr_x, curr_y = i, j

            for i in range(4):
                for j in range(4):
                    if self.game_board_end_game[i][j] == number:
                        target_x, target_y = i, j

            distance = abs(curr_x - target_x) + abs(curr_y - target_y)
            total_distance += distance

        return total_distance
