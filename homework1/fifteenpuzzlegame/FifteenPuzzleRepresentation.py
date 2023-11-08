import numpy as np


class FifteenPuzzleRepresentation:
    """
    Represents the game board of the Fifteen Puzzle game.

    This class provides methods to check if the game board is solvable and to count the number of inversions
    in the current state of the game board.

    Attributes:
        end_game_board (tuple): The final configuration of the game board.
        game_board (tuple): The current configuration of the game board.
    """

    def __init__(self, game_board=None):
        """
        Initializes the FifteenPuzzleRepresentation with a game board.
        :param game_board: The initial configuration of the game board.
                           Defaults to a pre-defined configuration.
        """
        self.end_game_board = tuple(range(1, 16)) + (0,)

        if game_board is None:
            self.game_board = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 15, 13, 14)
            # 1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 14, 13, 0, 15 NOPE
            # 4, 2, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0 NOPE
            # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 15, 13, 14 YES
            # 4, 2, 1, 3, 6, 7, 5, 8, 9, 10, 11, 12, 13, 14, 15, 0 NOPE
            # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 14, 15, 13 YES
            # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 12, 14, 15, 13 NOPE
            # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15 YES Stupido
            # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15 YES Stupido
            # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 12, 13, 14, 15 NOPE
        else:
            self.game_board = game_board

    def game_is_solvable(self):
        """
        Determines if the current game board configuration is solvable.
        A game board is solvable if the number of inversions is even.
        :return: True if the game board is solvable, False otherwise.
        """
        # Counts the number of inversions in the state.
        inversions = self.count_inversions()
        # If the number of inversions is even, the state is solvable.
        return inversions % 2 == 0

    def count_inversions(self):
        """
        Counts the number of inversions in the current state of the game board.

        Inversions are pairs of tiles that are in the wrong order. For the game to be solvable,
        the number of inversions must be even.
        :return: The number of inversions in the game board.
        """
        state_array = np.array(self.game_board)
        state_array = state_array[state_array > 0]
        inversions = sum(np.sum(state_array[i + 1:] < state_array[i]) for i in range(len(state_array) - 1))
        return inversions

    def is_end_game(self):
        """
        Determines if the current game board configuration matches the end-game configuration.
        :return: True if the game board is in the end-game configuration, False otherwise.
        """
        return self.game_board == self.end_game_board

    def move_up(self):
        """
        Attempts to move the empty tile (0) up and returns a new game representation.

        If the move is not possible (i.e., the empty tile is already on the top row),
        the method returns None.
        :return: A new game representation if the move is possible; None otherwise.
        """
        board = np.array(self.game_board).reshape(4, 4)
        zero_row, zero_col = np.where(board == 0)  # Finds the position of the empty tile (0).
        new_row, new_col = zero_row + -1, zero_col
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_board = board.copy()
            new_board[zero_row, zero_col], new_board[new_row, new_col] = new_board[new_row, new_col], new_board[
                zero_row, zero_col]
            return FifteenPuzzleRepresentation(game_board=tuple(new_board.flatten()))
        return None

    def move_down(self):
        """
        Attempts to move the empty tile (0) down and returns a new game representation.

        If the move is not possible (i.e., the empty tile is already on the bottom row),
        the method returns None.
        :return: A new game representation if the move is possible; None otherwise.
        """
        board = np.array(self.game_board).reshape(4, 4)
        zero_row, zero_col = np.where(board == 0)  # Finds the position of the empty tile (0).
        new_row, new_col = zero_row + 1, zero_col
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_board = board.copy()
            new_board[zero_row, zero_col], new_board[new_row, new_col] = new_board[new_row, new_col], new_board[
                zero_row, zero_col]
            return FifteenPuzzleRepresentation(game_board=tuple(new_board.flatten()))
        return None

    def move_left(self):
        """
        Attempts to move the empty tile (0) to the left and returns a new game representation.

        If the move is not possible (i.e., the empty tile is already on the leftmost column),
        the method returns None.
        :return: A new game representation if the move is possible; None otherwise.
        """
        board = np.array(self.game_board).reshape(4, 4)
        zero_row, zero_col = np.where(board == 0)  # Finds the position of the empty tile (0).
        new_row, new_col = zero_row, zero_col + -1
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_board = board.copy()
            new_board[zero_row, zero_col], new_board[new_row, new_col] = new_board[new_row, new_col], new_board[
                zero_row, zero_col]
            return FifteenPuzzleRepresentation(game_board=tuple(new_board.flatten()))
        return None

    def move_right(self):
        """
        Attempts to move the empty tile (0) to the right and returns a new game representation.

        If the move is not possible (i.e., the empty tile is already on the leftmost column),
        the method returns None.
        :return: A new game representation if the move is possible; None otherwise.
        """
        board = np.array(self.game_board).reshape(4, 4)
        zero_row, zero_col = np.where(board == 0)  # Finds the position of the empty tile (0).
        new_row, new_col = zero_row, zero_col + 1
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_board = board.copy()
            new_board[zero_row, zero_col], new_board[new_row, new_col] = new_board[new_row, new_col], new_board[
                zero_row, zero_col]
            return FifteenPuzzleRepresentation(game_board=tuple(new_board.flatten()))
        return None

    def __eq__(self, other):
        if not isinstance(other, FifteenPuzzleRepresentation):
            return False
        return np.array_equal(self.game_board, other.game_board)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.game_board)

    def __str__(self):
        return str(self.game_board)
