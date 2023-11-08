from homework1.fifteenpuzzlegame import StateFifteenPuzzleGame


class MisplacedTittlesPuzzleGame:
    """
    Represents a heuristic for the Fifteen Puzzle game based on the number of misplaced tiles.
    This heuristic computes the number of tiles that are not in their goal position, excluding the empty tile (0).

    Attributes:
        goal_position (tuple): The goal configuration of the game board.
    """

    def __init__(self, goal_position):
        """
        Initializes the MisplacedTilesPuzzleGame heuristic with a goal position.
        :param goal_position: (tuple) The goal configuration of the game board.
        """
        self.goal_position = goal_position

    def h(self, state: StateFifteenPuzzleGame):
        """
        Computes the heuristic value for a given state based on the number of misplaced tiles.

        The heuristic value is the number of tiles that are not in their goal position, excluding the empty tile (0).
        :param state: The current state of the Fifteen Puzzle game.
        :return: The heuristic value for the given state.
        """
        return sum(
            1 for s, g in zip(state.game_representation.game_board, self.goal_position)
            if s != g and s != 0
        )
