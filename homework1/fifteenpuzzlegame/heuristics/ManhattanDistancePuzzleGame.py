from homework1.fifteenpuzzlegame import StateFifteenPuzzleGame


class ManhattanDistancePuzzleGame:
    """
    Represents a heuristic for the Fifteen Puzzle game based on the Manhattan distance of tiles from their goal positions.

    This heuristic computes the sum of the Manhattan distances of each tile from its goal position.
    The Manhattan distance for a tile is the sum of the absolute values of the horizontal and vertical distances
    between the tile's current position and its goal position.

    Attributes:
        goal_position (tuple): The goal configuration of the game board.
    """

    def __init__(self, goal_position):
        """
        Initializes the ManhattanDistancePuzzleGameOp heuristic with a goal position.
        :param goal_position: The goal configuration of the game board.
        """
        self.goal_position = goal_position

    def h(self, state: StateFifteenPuzzleGame):
        """
        Computes the heuristic value for a given state based on the Manhattan distance of tiles.

        The heuristic value is the sum of the Manhattan distances of each tile from its goal position.
        :param state: The current state of the Fifteen Puzzle game.
        :return: The heuristic value for the given state.
        """
        distance = 0  # Initialize the total distance to 0.

        for i in range(16):
            # Iterate through each tile on a 4x4 board (16 tiles in total).
            if state.game_representation.game_board[i] == 0:  # Ignore the empty tile.
                continue

            # Convert the current tile's index to its (x, y) position on the board.
            current_position = self._index_to_position(i)
            # Find the goal position of the current tile and convert its index to (x, y) position.
            goal_position = self._index_to_position(self.goal_position.index(state.game_representation.game_board[i]))

            # Calculate the Manhattan distance between the current position and the goal position.
            # The Manhattan distance is the sum of the absolute differences of their coordinates.
            distance += abs(current_position[0] - goal_position[0]) + abs(current_position[1] - goal_position[1])

        return distance  # Return the total Manhattan distance.

    def _index_to_position(self, index):
        return index // 4, index % 4  # Returns the row and column as a tuple.
