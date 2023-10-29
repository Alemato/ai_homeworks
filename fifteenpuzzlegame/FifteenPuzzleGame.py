from StateFifteenPuzzleGame import StateFifteenPuzzleGame


class FifteenPuzzleGame:
    """
    Represents the operations related to the Fifteen Puzzle game.
    This class provides methods to get neighbors of a given state, which are
    the possible states that can be reached by making valid moves from the current state.
    """

    def neighbors(self, state: StateFifteenPuzzleGame):
        """
        Computes the neighboring states that can be reached from the given state.
        The method calculates the possible states that can be reached by making
        the "UP", "DOWN", "LEFT", and "RIGHT" moves from the current state.
        :param state:  The current state of the Fifteen Puzzle game.
        :return: A set of neighboring states that can be reached from the given state.
        """
        neighbors_state = set()
        moves = {
            "UP": state.game_representation.move_up(),
            "DOWN": state.game_representation.move_down(),
            "LEFT": state.game_representation.move_left(),
            "RIGHT": state.game_representation.move_right(),
        }
        for move, new_state in moves.items():
            if new_state is not None:
                neighbors_state.add(
                    StateFifteenPuzzleGame(game_representation=new_state, state_parent=state, move=move))
        return neighbors_state
