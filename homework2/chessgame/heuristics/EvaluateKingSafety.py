import chess


class EvaluateKingSafety:
    def h(self, board):
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