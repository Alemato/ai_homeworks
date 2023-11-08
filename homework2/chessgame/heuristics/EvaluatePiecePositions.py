from constants import *

# 21 microsecondi
class EvaluatePiecePositions:

    def evaluate_piece_positions(self, board, piece_table, piece_type, color):
        score = 0
        pieces = board.pieces(piece_type, color)
        for square in pieces:
            piece_position_value = piece_table[square]
            score += piece_position_value if color == chess.WHITE else -piece_position_value
        return score

    def is_endgame(self, board):
        # Limite del valore complessivo dei pezzi per considerare una partita nel finale
        endgame_value_threshold = 13

        total_value = 0
        for piece_type in PIECE_VALUE:
            total_value += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUE[piece_type]
            total_value += len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUE[piece_type]

        # Se il valore totale dei pezzi, esclusi i re, è al di sotto di una certa soglia,
        # consideriamo la partita come nel finale.
        is_endgame_phase = total_value <= endgame_value_threshold

        # Ulteriori considerazioni potrebbero essere la presenza di molti pedoni, il che potrebbe
        # suggerire che non siamo ancora nel finale tipico, anche se il valore dei pezzi è basso.
        if len(board.pieces(chess.PAWN, chess.WHITE)) + len(board.pieces(chess.PAWN, chess.BLACK)) > 10:
            is_endgame_phase = False

        return is_endgame_phase

    # Funzione per calcolare il punteggio totale basato sulla posizione dei pezzi
    def h(self, board):
        total_score = 0
        if self.is_endgame(board):
            king_table_to_use = KING_ENDGAME_TABLE
        else:
            king_table_to_use = KING_INITGAME_TABLE
        total_score += self.evaluate_piece_positions(board, PAWN_TABLE, chess.PAWN, chess.WHITE)
        total_score += self.evaluate_piece_positions(board, KNIGHT_TABLE, chess.KNIGHT, chess.WHITE)
        total_score += self.evaluate_piece_positions(board, BISHOP_TABLE, chess.BISHOP, chess.WHITE)
        total_score += self.evaluate_piece_positions(board, ROOK_TABLE, chess.ROOK, chess.WHITE)
        total_score += self.evaluate_piece_positions(board, QUEEEN_TABLE, chess.QUEEN, chess.WHITE)
        total_score += self.evaluate_piece_positions(board, king_table_to_use, chess.KING, chess.WHITE)

        total_score -= self.evaluate_piece_positions(board, PAWN_TABLE, chess.PAWN, chess.BLACK)
        total_score -= self.evaluate_piece_positions(board, KNIGHT_TABLE, chess.KNIGHT, chess.BLACK)
        total_score -= self.evaluate_piece_positions(board, BISHOP_TABLE, chess.BISHOP, chess.BLACK)
        total_score -= self.evaluate_piece_positions(board, ROOK_TABLE, chess.ROOK, chess.BLACK)
        total_score -= self.evaluate_piece_positions(board, QUEEEN_TABLE, chess.QUEEN, chess.BLACK)
        total_score -= self.evaluate_piece_positions(board, king_table_to_use, chess.KING, chess.BLACK)

        return total_score
