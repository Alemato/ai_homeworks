import random
from copy import deepcopy

from State import State


class FifteenPuzzleGame:
    def __init__(self, game_board=None, cost_up=1, cost_down=1, cost_left=1, cost_right=1):
        self.game_board_end_game = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, "#"]]
        self.game_board_init_game_default = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], ["#", 15, 13, 14]]

        self.cost_up = cost_up
        self.cost_down = cost_down
        self.cost_left = cost_left
        self.cost_right = cost_right

        if game_board is not None:
            self.game_board = game_board
        else:
            self.game_board = self.game_board_init_game_default

    @staticmethod
    def __random_game_board_gen():
        component_geme_board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, "#"]
        random.shuffle(component_geme_board)
        game_board = [component_geme_board[i:i + 4] for i in range(0, 16, 4)]
        return game_board

    @staticmethod
    def is_solvable(game_board):
        count = sum(
            1
            for i, row in enumerate(game_board)
            for j, tile1 in enumerate(row)
            for k, row_next in enumerate(game_board[i:])
            for x, tile2 in enumerate(row_next[j + 1:] if k == 0 else row_next)
            if tile1 != "#" and tile2 != "#" and tile1 > tile2
        )
        return count % 2 == 0

    def is_end_game(self, game_board):
        return all(
            game_board[x][y] == "#" or game_board[x][y] == self.game_board_end_game[x][y]
            for x in range(4)
            for y in range(4)
        )

    @staticmethod
    def __find_empty_title(game_board):
        return next(
            (x, y)
            for x in range(4)
            for y in range(4)
            if game_board[x][y] == "#"
        )

    def move_up(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if x - 1 >= 0:
            game_board_new = deepcopy(game_board)
            game_board_new[x][y], game_board_new[x - 1][y] = game_board_new[x - 1][y], game_board_new[x][y]
            return State(game_board=game_board_new, move="UP")
        return None

    def move_down(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if x + 1 < len(game_board):
            game_board_new = deepcopy(game_board)
            game_board_new[x][y], game_board_new[x + 1][y] = game_board_new[x + 1][y], game_board_new[x][y]
            return State(game_board=game_board_new, move="DOWN")
        return None

    def move_left(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if y - 1 >= 0:
            game_board_new = deepcopy(game_board)
            game_board_new[x][y], game_board_new[x][y - 1] = game_board_new[x][y - 1], game_board_new[x][y]
            return State(game_board=game_board_new, move="LEFT")
        return None

    def move_right(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if y + 1 < len(game_board[x]):
            game_board_new = deepcopy(game_board)
            game_board_new[x][y], game_board_new[x][y + 1] = game_board_new[x][y + 1], game_board_new[x][y]
            return State(game_board=game_board_new, move="RIGHT")
        return None

    def const_move(self, move):
        if move == "UP":
            return self.cost_up
        elif move == "DOWN":
            return self.cost_down
        elif move == "LEFT":
            return self.cost_left
        else:
            return self.cost_right

    def neighbors(self, state: State):
        neighbors_state = []
        moves = [
            self.move_up(state.game_board),
            self.move_down(state.game_board),
            self.move_left(state.game_board),
            self.move_right(state.game_board)
        ]
        for move in moves:
            if move is not None:
                state_new = move
                state_new.parent_state = state
                neighbors_state.append(state_new)
        return set(neighbors_state)

    def __eq__(self, __o):
        if not isinstance(__o, FifteenPuzzleGame):
            return False
        return self.game_board == __o.game_board

    def __ne__(self, __o):
        return self.__eq__(__o)

    def __hash__(self):
        return hash(str(self.game_board))
