class State:
    def __init__(self, game_board, move=None, parent_state=None):
        self.game_board = game_board
        self.parent_state = parent_state
        self.move = move
        self.h = None
        self.f = None
        self.g = None

    def __eq__(self, __o):
        if not isinstance(__o, State):
            return False
        return self.game_board == __o.game_board

    def __ne__(self, __o):
        return self.__eq__(__o)

    def __hash__(self):
        return hash(str(self.game_board))

    def __str__(self):
        strs = "\n"
        for i in range(4):
            for j in range(4):
                strs = strs + str(self.game_board[i][j]) + "\t"
            strs = strs + "\n"
        return strs
