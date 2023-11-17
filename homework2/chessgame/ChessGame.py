import chess

from chessgame.StateChessGame import StateChessGame


class ChessGame:
    """
    Represents a chess game, providing functionalities to manage the game state and compute possible moves.

    Attributes:
        game_board (chess.Board): The current chess board configuration.
    """
    def __init__(self, game_board=None):
        """
        Initializes a new chess game.

        :param game_board: The current chess board configuration. If None, initializes a new chess board.
        """
        self.game_board = game_board  # The current chess board.

        # If no game board is provided, initialize a new chess board.
        if game_board is None:
            self.game_board = chess.Board()

    def neighbors(self, state: StateChessGame):
        """
        Generates all possible next states (neighbors) from a given state.

        :param state: The current state of the chess game from which to compute neighbors.
        :return: A list of StateChessGame objects representing possible next states.
        """
        neighbors = []

        # Iterate through all legal moves from the current state.
        for legal_move in state.game_board.legal_moves:
            # Copy the current game board and make the legal move.
            new_game_board = state.game_board.copy()
            new_game_board.push(legal_move)

            # Create a new StateChessGame object for the resulting game state.
            neighbor = StateChessGame(game_board=new_game_board, state_parent=state, move=legal_move)
            neighbors.append(neighbor)
        return neighbors


    def get_name_winner_player(self, game_board):
        """
        Determines the name of the winning player if the game is in checkmate.

        :param game_board: The chess board to check for checkmate and winner.
        :return: The name of the winning player ("White" or "Black") if there's a checkmate, otherwise None.
        """
        # Check if the current game state is a checkmate.
        if game_board.is_checkmate():
            # Get the outcome of the game.
            outcome = game_board.outcome()
            if outcome is not None:
                # Return "White" or "Black" depending on the winner.
                return "White" if outcome.winner else "Black"
        return None