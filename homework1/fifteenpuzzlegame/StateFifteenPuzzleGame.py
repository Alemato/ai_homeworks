from FifteenPuzzleRepresentation import FifteenPuzzleRepresentation


class StateFifteenPuzzleGame:
    """
    Represents a state in the Fifteen Puzzle game.

    This class provides methods to determine if the state is an end-game configuration,
    print the game board, and compare states.

    Attributes:
        game_representation (FifteenPuzzleRepresentation): The current Representation of the game board.
        state_parent (StateFifteenPuzzleGame): The parent state from which this state was derived.
        move (str): The move that led to this state.
        h (float): The heuristic value of the state.
        g (float): The cost to reach the current state from the start state.
        f (float): The estimated cost of the cheapest solution through the current state.
    """

    def __init__(self, game_representation=None, state_parent=None, move=None):
        """
        Initializes the StateFifteenPuzzleGame with a game representation, parent state, and move.
        :param game_representation: The game board representation.
        :param state_parent: The parent state.
        :param move: The move that led to this state.
        """
        self.game_representation = game_representation
        self.state_parent = state_parent
        self.move = move
        self.h = None
        self.g = None
        self.f = None

        if self.game_representation is None:
            self.game_representation = FifteenPuzzleRepresentation()

    def is_end_game(self):
        """
        Determines if the current state matches the end-game configuration.
        :return: True if the state is an end-game configuration, False otherwise.
        """
        return self.game_representation.is_end_game()

    def print_board(self):
        """
        Returns a console representation of the game board of the current state.
        """
        for i in range(4):
            for j in range(4):
                print(self.game_representation.game_board[i * 4 + j], end="\t")
            print()
        print()

    def __eq__(self, other):
        if not isinstance(other, StateFifteenPuzzleGame):
            return False
        return self.game_representation.game_board == other.game_representation.game_board

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.game_representation.__hash__()

    def __lt__(self, other):
        if self.f is None or other.f is None:
            raise ValueError("Cannot compare states")
        return self.f < other.f
