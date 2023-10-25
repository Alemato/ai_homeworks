import numpy as np

from State import State


class FifteenPuzzleGame:
    def __init__(self, game_board=None, cost_up=1, cost_down=1, cost_left=1, cost_right=1):
        self.game_board_end_game = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ])
        self.game_board_init_game_default = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [0, 15, 13, 14]
        ])

        self.cost_up = cost_up
        self.cost_down = cost_down
        self.cost_left = cost_left
        self.cost_right = cost_right

        self.game_board = game_board if game_board is not None else self.game_board_init_game_default

    @staticmethod
    def __random_game_board_gen():
        component_game_board = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
        np.random.shuffle(component_game_board)
        return component_game_board.reshape(4, 4)

    @staticmethod
    def is_solvable(game_board):
        flat_board = game_board[game_board != 0].ravel()
        sorted_indices = np.argsort(flat_board)
        inv_count = np.sum(np.arange(len(flat_board)) != sorted_indices)
        return inv_count % 2 == 0

    def is_end_game(self, game_board):
        return np.array_equal(game_board, self.game_board_end_game)

    @staticmethod
    def __find_empty_title(game_board):
        index = np.argmax(game_board == 0)
        return np.unravel_index(index, game_board.shape)

    def move_up(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if x - 1 >= 0:
            game_board_new = game_board.copy()
            game_board_new[x, y], game_board_new[x - 1, y] = game_board_new[x - 1, y], game_board_new[x, y]
            return State(game_board=game_board_new, move="UP")
        return None

    def move_down(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if x + 1 < game_board.shape[0]:  # Usiamo .shape[0] per ottenere il numero di righe dell'array
            game_board_new = game_board.copy()
            game_board_new[x, y], game_board_new[x + 1, y] = game_board_new[x + 1, y], game_board_new[x, y]
            return State(game_board=game_board_new, move="DOWN")
        return None

    def move_left(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if y - 1 >= 0:
            game_board_new = game_board.copy()
            game_board_new[x, y], game_board_new[x, y - 1] = game_board_new[x, y - 1], game_board_new[x, y]
            return State(game_board=game_board_new, move="LEFT")
        return None

    def move_right(self, game_board):
        x, y = self.__find_empty_title(game_board)
        if y + 1 < game_board.shape[1]:  # Usiamo .shape[1] per ottenere il numero di colonne dell'array
            game_board_new = game_board.copy()
            game_board_new[x, y], game_board_new[x, y + 1] = game_board_new[x, y + 1], game_board_new[x, y]
            return State(game_board=game_board_new, move="RIGHT")
        return None

    def const_move(self, move):
        return {
            "UP": self.cost_up,
            "DOWN": self.cost_down,
            "LEFT": self.cost_left,
            "RIGHT": self.cost_right,
        }.get(move, self.cost_right)

    def neighbors(self, state: State):
        neighbors_state = []
        moves = [
            self.move_up(state.game_board),
            self.move_down(state.game_board),
            self.move_left(state.game_board),
            self.move_right(state.game_board)
        ]
        for state_new in moves:
            if state_new is not None:
                state_new.parent_state = state
                neighbors_state.append(state_new)
        return set(neighbors_state)

    def __eq__(self, other):
        if not isinstance(other, FifteenPuzzleGame):
            return False
        return np.array_equal(self.game_board, other.game_board)

    def __hash__(self):
        return hash(str(self.game_board))
