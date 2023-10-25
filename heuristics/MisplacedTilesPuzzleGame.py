class MisplacedTittlesPuzzleGame:
    @staticmethod
    def h(current_state):
        misplaced_count = 0
        for i in range(4):
            for j in range(4):
                if current_state.game_board[i][j] != "#" and current_state.game_board[i][j] != \
                        current_state.game_board_end_game[i][j]:
                    misplaced_count += 1
        return misplaced_count
