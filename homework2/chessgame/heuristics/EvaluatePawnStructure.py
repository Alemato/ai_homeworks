import chess

from chessgame import StateChessGame


# 60 microsecondi
# min = -420
# max = 420
class EvaluatePawnStructure:
    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.file_bb = [chess.BB_FILES[f] for f in range(8)]
        self.rank_bb = [chess.BB_RANKS[r] for r in range(8)]
        self.advance_shifts = {chess.WHITE: 8, chess.BLACK: -8}
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

    def __pawn_structure_score(self, pawns, color, board):
        score = 0
        our_pawns_bb = int(pawns)  # Convert to integer bitboard if it's not already
        all_pawns_bb = int(board.pieces(chess.PAWN, chess.WHITE)) | int(board.pieces(chess.PAWN, chess.BLACK))

        # Precompute pawn presence for files using bitwise operations
        pawns_on_file = [bool(our_pawns_bb & self.file_bb[f]) for f in range(8)]

        for square in chess.SquareSet(our_pawns_bb):
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            # Isolated pawns
            if not (pawns_on_file[file - 1] if file > 0 else False) and \
                    not (pawns_on_file[file + 1] if file < 7 else False):
                score -= 20

            # Doubled pawns
            if bin(our_pawns_bb & self.file_bb[file]).count('1') > 1:
                score -= 10

            # Backward pawns
            supported = False
            advance_square = square + self.advance_shifts[color]
            support_squares = [square - 1, square + 1] + \
                              [advance_square - 1, advance_square + 1]

            # Check if the pawn is supported by our other pawns
            for support_sq in support_squares:
                if 0 <= support_sq < 64 and (all_pawns_bb & (1 << support_sq)):
                    supported = True
                    break
            if not supported and 0 <= advance_square < 64 and board.piece_at(advance_square) is None:
                score -= 15

        return score

    def __passed_pawn_score(self, our_pawns, their_pawns, color):
        score = 0
        their_pawns_bb = int(their_pawns)  # Assicurati che sia un bitboard intero
        for our_pawn in our_pawns:
            file = chess.square_file(our_pawn)
            rank = chess.square_rank(our_pawn)
            passed = True
            if color == chess.WHITE:
                for r in range(rank + 1, 8):
                    if self.file_bb[file] & self.rank_bb[r] & their_pawns_bb:  # Utilizzo bitboard intero
                        passed = False
                        break
            else:
                for r in range(rank - 1, -1, -1):
                    if self.file_bb[file] & self.rank_bb[r] & their_pawns_bb:  # Utilizzo bitboard intero
                        passed = False
                        break
            if passed:
                score += 50

        return score

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
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        score += self.__pawn_structure_score(white_pawns, chess.WHITE, board)
        score -= self.__pawn_structure_score(black_pawns, chess.BLACK, board)

        score += self.__passed_pawn_score(white_pawns, black_pawns, chess.WHITE)
        score -= self.__passed_pawn_score(black_pawns, white_pawns, chess.BLACK)

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
