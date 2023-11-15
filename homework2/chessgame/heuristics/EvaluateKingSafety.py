import chess

from chessgame import StateChessGame


# 12.1 microsecondi
# min = -7.5 -8.5
# max = 7.5 8.5
class EvaluateKingSafety:
    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.normalize_result = normalize_result
        self.h_max_value = 9.5
        self.h_min_value = -9.5

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
        score = 0
        pawn_cover_score = 0.5
        attacked_square_score = -0.75

        # Maschere di bit per i pedoni bianchi e neri
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        # Calcolo per il re bianco
        white_king_square = board.king(chess.WHITE)
        white_king_attacks = board.attacks(white_king_square)
        white_king_zone = white_pawns & white_king_attacks
        score += pawn_cover_score * bin(white_king_zone).count('1')

        # Controlla le caselle attaccate dai neri nella zona del re bianco
        for square in white_king_attacks:
            if board.is_attacked_by(chess.BLACK, square):
                score += attacked_square_score

        # Calcolo per il re nero
        black_king_square = board.king(chess.BLACK)
        black_king_attacks = board.attacks(black_king_square)
        black_king_zone = black_pawns & black_king_attacks
        score -= pawn_cover_score * bin(black_king_zone).count('1')

        # Controlla le caselle attaccate dai bianchi nella zona del re nero
        for square in black_king_attacks:
            if board.is_attacked_by(chess.WHITE, square):
                score -= attacked_square_score

        return score

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
