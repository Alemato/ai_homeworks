from chessgame import StateChessGame
from .EvaluateBoardWithoutKing import EvaluateBoardWithoutKing
from .EvaluateCentralControlScore import EvaluateCentralControlScore
from .EvaluateKingSafety import EvaluateKingSafety
from .EvaluatePiecePositions import EvaluatePiecePositions


class SoftBoardEvaluationChessGame:
    """
    This class provides a more nuanced evaluation of a chess game board by combining various aspects such
    as material balance, central control, king safety, and piece positions. It offers a more balanced
    perspective on the chessboard, making it suitable for a comprehensive game analysis.

    Attributes:
        balance_evaluation (bool): If True, uses a weighted approach for combining different evaluation metrics.
        print_evaluation (bool): If True, prints the evaluation scores for debugging or analysis purposes.
        evaluate_board_without_king (EvaluateBoardWithoutKing): Component for evaluating the board without considering the king's position.
        evaluate_central_control_score (EvaluateCentralControlScore): Component for evaluating central control.
        evaluate_king_safety (EvaluateKingSafety): Component for evaluating king safety.
        evaluate_piece_positions (EvaluatePiecePositions): Component for evaluating piece positions.
    """
    def __init__(self, balance_evaluation=True, print_evaluation=False):
        """
        Initializes the evaluation components for different aspects of the chess game.

        :param balance_evaluation: Indicates whether to use a weighted combination of evaluation metrics.
        :param print_evaluation: Indicates whether to print the evaluation scores for each component.
        """
        self.balance_evaluation = balance_evaluation  # Flag for using weighted evaluation scores.
        self.print_evaluation = print_evaluation  # Flag for printing the evaluation results.
        # Initialize individual evaluation components with normalization.
        self.evaluate_board_without_king = EvaluateBoardWithoutKing(normalize_result=True)
        self.evaluate_central_control_score = EvaluateCentralControlScore(normalize_result=True)
        self.evaluate_king_safety = EvaluateKingSafety(normalize_result=True)
        self.evaluate_piece_positions = EvaluatePiecePositions(normalize_result=True)

    def h(self, state: StateChessGame):
        """
        Evaluates the chess board state using a combination of various evaluation metrics.

        :param state: The current state of the chess game.
        :return: A comprehensive heuristic score representing the board evaluation.
        """
        board = state.game_board
        # Handle special game-over conditions like checkmate and stalemate.
        game_over_eval = None
        if board.is_checkmate():
            outcome = board.outcome()
            if outcome is not None:
                if outcome.winner:
                    game_over_eval = float("inf")
                else:
                    game_over_eval = float("-inf")
        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            game_over_eval = 0

        if game_over_eval is not None:
            return game_over_eval
        else:
            # Calculate individual evaluation scores.
            board_without_king = self.evaluate_board_without_king.h(state)
            central_control_score = self.evaluate_central_control_score.h(state)
            king_safety = self.evaluate_king_safety.h(state)
            piece_positions = self.evaluate_piece_positions.h(state)

            # Optionally print the evaluation scores.
            if self.print_evaluation:
                print("Valutazione: ", board_without_king, central_control_score, king_safety, piece_positions)

            # Combine the scores using weighted or simple sum approach.
            if self.balance_evaluation:
                return (
                        board_without_king * 0.35 +  # Bilancio del materiale
                        central_control_score * 0.20 +  # Controllo del centro
                        king_safety * 0.25 +  # Sicurezza del re
                        piece_positions * 0.20  # Posizione dei pezzi
                )
            return (
                    board_without_king +
                    central_control_score +
                    king_safety +
                    piece_positions
            )
