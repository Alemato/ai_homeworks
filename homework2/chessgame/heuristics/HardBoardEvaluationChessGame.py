from chessgame import StateChessGame
from .EvaluateBoardWithoutKing import EvaluateBoardWithoutKing
from .EvaluateCentralControlScore import EvaluateCentralControlScore
from .EvaluateKingSafety import EvaluateKingSafety
from .EvaluateMobility import EvaluateMobility
from .EvaluatePawnStructure import EvaluatePawnStructure
from .EvaluatePiecePositions import EvaluatePiecePositions


class HardBoardEvaluationChessGame:
    """
    This class provides an in-depth evaluation of a chess game board by integrating various evaluation
    metrics like material balance, central control, king safety, mobility, pawn structure, and piece
    positioning. It offers a holistic approach to assessing the strengths and weaknesses of a chess
    position, making it suitable for advanced analysis.

    Attributes:
        balance_evaluation (bool): If True, combines evaluation scores using a weighted approach.
                                   This gives a balanced evaluation considering all aspects of the game.
        print_evaluation (bool): If True, prints the evaluation results for debugging or analysis purposes.
        evaluate_board_without_king (EvaluateBoardWithoutKing): Evaluation component focusing on the board
                                                                without considering the king's position.
        evaluate_central_control_score (EvaluateCentralControlScore): Evaluation component focusing on
                                                                      the control of central squares.
        evaluate_king_safety (EvaluateKingSafety): Evaluation component focusing on the safety of the king.
        evaluate_mobility (EvaluateMobility): Evaluation component focusing on the mobility of pieces.
        evaluate_pawn_structure (EvaluatePawnStructure): Evaluation component focusing on the pawn structure.
        evaluate_piece_positions (EvaluatePiecePositions): Evaluation component focusing on the positions
                                                           of all pieces except the king.
        """

    def __init__(self, balance_evaluation=True, print_evaluation=False):
        """
        Initializes the evaluation components for different aspects of the chess game.

        :param balance_evaluation: If True, uses a weighted approach for combining different evaluation metrics.
        :param print_evaluation: If True, prints the evaluation scores.
        """
        self.balance_evaluation = balance_evaluation  # Flag to use weighted evaluation scores.
        self.print_evaluation = print_evaluation  # Flag to print the evaluation results.
        # Initialize individual evaluation components with normalization enabled.
        self.evaluate_board_without_king = EvaluateBoardWithoutKing(normalize_result=True)
        self.evaluate_central_control_score = EvaluateCentralControlScore(normalize_result=True)
        self.evaluate_king_safety = EvaluateKingSafety(normalize_result=True)
        self.evaluate_mobility = EvaluateMobility(normalize_result=True)
        self.evaluate_pawn_structure = EvaluatePawnStructure(normalize_result=True)
        self.evaluate_piece_positions = EvaluatePiecePositions(normalize_result=True)

    def h(self, state: StateChessGame):
        """
        Evaluates the chess board state using various evaluation metrics.

        :param state: The current state of the chess game.
        :return: A combined heuristic score representing the board evaluation.
        """
        board = state.game_board
        # Special handling for endgame phase.
        game_over_eval = None
        # Assign extreme values for checkmate situations.
        if board.is_checkmate():
            outcome = board.outcome()
            if outcome is not None:
                if outcome.winner:
                    game_over_eval = float("inf")
                else:
                    game_over_eval = float("-inf")
        # Assign zero for draw situations.
        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            game_over_eval = 0

        if game_over_eval is not None:
            return game_over_eval
        else:
            # Evaluate different aspects of the board.
            board_without_king = self.evaluate_board_without_king.h(state)
            central_control_score = self.evaluate_central_control_score.h(state)
            king_safety = self.evaluate_king_safety.h(state)
            mobility = self.evaluate_mobility.h(state)
            pawn_structure = self.evaluate_pawn_structure.h(state)
            piece_positions = self.evaluate_piece_positions.h(state)
            # Optionally print the evaluation scores.
            if self.print_evaluation:
                print("Valutazione: ", board_without_king, central_control_score, king_safety, mobility, pawn_structure,
                      piece_positions)
            # Combine the scores either using weighted or simple sum approach.
            if self.balance_evaluation:
                return (
                        board_without_king * 0.35 +  # Bilancio del materiale
                        central_control_score * 0.20 +  # Controllo del centro
                        king_safety * 0.15 +  # Sicurezza del re
                        mobility * 0.10 +  # Mobilità
                        pawn_structure * 0.10 +  # Struttura dei pedoni
                        piece_positions * 0.10  # Posizione dei pezzi
                )
            return (
                    board_without_king +
                    central_control_score +
                    king_safety +
                    mobility +
                    pawn_structure +
                    piece_positions
            )
