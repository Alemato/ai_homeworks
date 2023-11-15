from chessgame import StateChessGame
from .constants import *


# 21 microsecondi
# min = -285 -275
# max = 420 395
class EvaluatePiecePositions:

    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.normalize_result = normalize_result
        self.h_max_value = 420
        self.h_min_value = -420

    def h(self, state: StateChessGame):
        if self.evaluate_end_game_phase:
            return self.__h(state.game_board)
        elif self.normalize_result:
            raw_eval = self.__h(state.game_board)
            return self.__normalize(raw_eval)
        else:
            return self.__h(state.game_board)

    def h_piccolo(self, board):
        if self.evaluate_end_game_phase:
            return self.__h(board)
        elif self.normalize_result:
            raw_eval = self.__h(board)
            return self.__normalize(raw_eval)
        else:
            return self.__h(board)

    def __evaluate_piece_positions(self, board, piece_table, piece_type, color):
        score = 0
        pieces = board.pieces(piece_type, color)
        for square in pieces:
            piece_position_value = piece_table[square]
            score += piece_position_value if color == chess.WHITE else -piece_position_value
        return score

    def __is_endgame(self, board):
        # Regine
        white_queens = len(board.pieces(chess.QUEEN, chess.WHITE))
        black_queens = len(board.pieces(chess.QUEEN, chess.BLACK))

        # se entrambi i lati non hanno Regine -> endgame phase
        if white_queens == 0 and black_queens == 0:
            return True

        # Minorpieces
        white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))
        white_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
        black_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))
        white_minors = white_bishops + white_knights
        black_minors = black_bishops + black_knights

        white_rooks = len(board.pieces(chess.ROOK, chess.WHITE))
        black_rooks = len(board.pieces(chess.ROOK, chess.BLACK))

        # se ogni lato che ha una regina, non ha altri pezzi oppure ha
        # 1 Minorpiece al massimo -> endgame phase
        # fmt: off
        white_endgame_condition_with_queen = (
                white_queens == 1 and (white_rooks == 0 and white_minors <= 1)
        )
        black_endgame_condition_with_queen = (
                black_queens == 1 and (black_rooks == 0 and black_minors <= 1)
        )
        # fmt: on

        if (
                (white_endgame_condition_with_queen and black_queens == 0)
                or (black_endgame_condition_with_queen and white_queens == 0)
                or (
                white_endgame_condition_with_queen
                and black_endgame_condition_with_queen
        )
        ):
            return True

        return False

    # Funzione per calcolare il punteggio totale basato sulla posizione dei pezzi
    def __h(self, board):
        if self.evaluate_end_game_phase:
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
        total_score = 0
        if self.__is_endgame(board):
            king_table_to_use = KING_ENDGAME_TABLE
        else:
            king_table_to_use = KING_INITGAME_TABLE
        total_score += self.__evaluate_piece_positions(board, PAWN_TABLE, chess.PAWN, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, KNIGHT_TABLE, chess.KNIGHT, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, BISHOP_TABLE, chess.BISHOP, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, ROOK_TABLE, chess.ROOK, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, QUEEEN_TABLE, chess.QUEEN, chess.WHITE)
        total_score += self.__evaluate_piece_positions(board, king_table_to_use, chess.KING, chess.WHITE)

        total_score -= self.__evaluate_piece_positions(board, PAWN_TABLE, chess.PAWN, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, KNIGHT_TABLE, chess.KNIGHT, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, BISHOP_TABLE, chess.BISHOP, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, ROOK_TABLE, chess.ROOK, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, QUEEEN_TABLE, chess.QUEEN, chess.BLACK)
        total_score -= self.__evaluate_piece_positions(board, king_table_to_use, chess.KING, chess.BLACK)

        return total_score

    def __normalize(self, value):
        # Normalizza il valore in un range da -100 a +100
        if value >= 0:
            # Normalizzazione per valori positivi
            normalized = (value / self.h_max_value) * 100
        else:
            # Normalizzazione per valori negativi
            normalized = (value / abs(self.h_min_value)) * 100

        # Limita il valore normalizzato tra -100 e +100
        normalized = max(min(normalized, 100), -100)
        return normalized
