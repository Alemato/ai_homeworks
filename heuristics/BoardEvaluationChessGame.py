import chess

from ChessGame import ChessGame
from State import State


class BoardEvaluationChessGame:
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # Il re ha un valore speciale
    }

    # Tabelle di pezzi
    PAWN_TABLE = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    KNIGHT_TABLE = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    BISHOP_TABLE = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    ROOK_TABLE = [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    QUEEN_TABLE = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    KING_TABLE = [
        [20, 30, 10, 0, 0, 10, 30, 20],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

    # Pesi, Penalità e bonus
    ISOLATED_PAWN_PENALTY = -10
    DOUBLED_PAWN_PENALTY = -5
    SEMI_OPEN_FILE_PENALTY = -15
    OPEN_FILE_PENALTY = -25
    PASSED_PAWN_BONUS = 20
    ADJACENT_PAWN_BONUS = 10
    BISHOP_PAIR_BONUS = 50
    KING_SAFETY_WEIGHT = 0.5
    MOBILITY_WEIGHT = 0.1
    QUEEN_ACTIVITY_WEIGHT = 0.5
    KNIGHT_ACTIVITY_WEIGHT = 0.3
    CENTER_CONTROL_WEIGHT = 0.5
    CENTER_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]

    def __init__(self,
                 heuristic_piece_material_weight=0.5,
                 heuristic_piece_position_weight=0.5,
                 heuristic_pawn_structure_weight=0.5,
                 heuristic_mobility_weight=0.6,
                 heuristic_king_safety_weight=0.8,
                 heuristic_center_control_weight=0.4,
                 heuristic_bishop_pair_weight=0.4,
                 heuristic_queen_activity_weight=0.5,
                 heuristic_king_activity_weight=0.5
                 ):
        self.H_PIECE_MATERIAL_WEIGHT = heuristic_piece_material_weight
        self.H_PIECE_POSITION_WEIGHT = heuristic_piece_position_weight
        self.H_PAWN_STRUCTURE_WEIGHT = heuristic_pawn_structure_weight
        self.H_MOBILITY_WEIGHT = heuristic_mobility_weight
        self.H_KING_SAFETY_WEIGHT = heuristic_king_safety_weight
        self.H_CENTER_CONTROL_WEIGHT = heuristic_center_control_weight
        self.H_BISHOP_PAIR_WEIGHT = heuristic_bishop_pair_weight
        self.H_QUEEN_ACTIVITY_WEIGHT = heuristic_queen_activity_weight
        self.H_KNIGHT_ACTIVITY_WEIGHT = heuristic_king_activity_weight

    def h(self, state: State):
        board = state.game_board
        h1 = ChessGame.game_over_eval(state.game_board)
        if h1 is not None:
            return h1
        else:
            # Combiniamo diverse metriche di valutazione
            total_evaluation = (
                    self.piece_material_evaluation(board) * self.H_PIECE_MATERIAL_WEIGHT +
                    self.piece_position_evaluation(board) * self.H_PIECE_POSITION_WEIGHT +
                    self.pawn_structure_evaluation(board) * self.H_PAWN_STRUCTURE_WEIGHT +
                    self.mobility_evaluation(board) * self.H_MOBILITY_WEIGHT +
                    self.king_safety_evaluation(board) * self.H_KING_SAFETY_WEIGHT +
                    self.center_control_evaluation(board) * self.H_CENTER_CONTROL_WEIGHT +
                    self.bishop_pair_evaluation(board) * self.H_BISHOP_PAIR_WEIGHT +
                    self.queen_activity_evaluation(board) * self.H_QUEEN_ACTIVITY_WEIGHT +
                    self.knight_activity_evaluation(board) * self.H_KNIGHT_ACTIVITY_WEIGHT
            )
            return total_evaluation

    def piece_material_evaluation(self, board):
        """ Valuta la scacchiera in base al materiale. """
        evaluation = 0.0
        for square, piece in board.piece_map().items():
            piece_value = BoardEvaluationChessGame.PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                evaluation += piece_value
            else:
                evaluation -= piece_value
        return evaluation

    def piece_position_evaluation(self, board):
        """ Valuta la scacchiera in base alla posizione dei pezzi. """

        evaluation = 0.0

        for square, piece in board.piece_map().items():
            if piece.piece_type == chess.PAWN:
                table = BoardEvaluationChessGame.PAWN_TABLE
            elif piece.piece_type == chess.KNIGHT:
                table = BoardEvaluationChessGame.KNIGHT_TABLE
            elif piece.piece_type == chess.BISHOP:
                table = BoardEvaluationChessGame.BISHOP_TABLE
            elif piece.piece_type == chess.ROOK:
                table = BoardEvaluationChessGame.ROOK_TABLE
            elif piece.piece_type == chess.QUEEN:
                table = BoardEvaluationChessGame.QUEEN_TABLE
            elif piece.piece_type == chess.KING:
                table = BoardEvaluationChessGame.KING_TABLE

            row = square // 8
            col = square % 8

            if piece.color == chess.WHITE:
                evaluation += table[row][col]
            else:
                # Le tabelle sono fatte per il bianco, quindi invertiamo per il nero
                evaluation -= table[7 - row][col]

        return evaluation

    def pawn_structure_evaluation(self, board):
        """ Valuta la struttura dei pedoni. """
        evaluation = 0.0

        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        for square in chess.SQUARES:
            if board.piece_at(square) and board.piece_at(square).piece_type == chess.PAWN:
                col = square % 8

                # Verifica pedoni isolati
                if col == 0 or not (board.pieces(chess.PAWN, board.piece_at(square).color) & chess.BB_FILES[col - 1]):
                    if col == 7 or not (
                            board.pieces(chess.PAWN, board.piece_at(square).color) & chess.BB_FILES[col + 1]):
                        evaluation += BoardEvaluationChessGame.ISOLATED_PAWN_PENALTY if board.piece_at(
                            square).color == chess.WHITE else -BoardEvaluationChessGame.ISOLATED_PAWN_PENALTY

                # Verifica pedoni doppi
                if (white_pawns if board.piece_at(square).color == chess.WHITE else black_pawns) & chess.BB_SQUARES[
                    square]:
                    evaluation += BoardEvaluationChessGame.DOUBLED_PAWN_PENALTY if board.piece_at(
                        square).color == chess.WHITE else -BoardEvaluationChessGame.DOUBLED_PAWN_PENALTY

                # Verifica pedoni passati
                rank = square // 8
                if board.piece_at(square).color == chess.WHITE:
                    if rank < 7:
                        for r in range(rank + 1, 8):
                            if black_pawns & chess.BB_RANKS[r]:
                                break
                        else:
                            evaluation += BoardEvaluationChessGame.PASSED_PAWN_BONUS
                else:
                    if rank > 0:
                        for r in range(0, rank):
                            if white_pawns & chess.BB_RANKS[r]:
                                break
                        else:
                            evaluation -= BoardEvaluationChessGame.PASSED_PAWN_BONUS

        return evaluation

    def mobility_evaluation(self, board):
        """ Valuta la mobilità delle pedine. """
        evaluation = 0.0

        # Calcola la mobilità per il bianco e per il nero
        white_mobility = len(list(board.legal_moves))
        board.push(chess.Move.null())  # Esegui una mossa nulla per cambiare il turno
        black_mobility = len(list(board.legal_moves))
        board.pop()  # Torna al turno originale

        # Valuta la mobilità in base ai pesi
        evaluation += BoardEvaluationChessGame.MOBILITY_WEIGHT * (white_mobility - black_mobility)

        return evaluation

    def king_safety_evaluation(self, board):
        """ Valuta la sicurezza del re. """

        evaluation = 0.0

        # Posizioni dei re
        white_king_square = list(board.pieces(chess.KING, chess.WHITE))[0]
        black_king_square = list(board.pieces(chess.KING, chess.BLACK))[0]

        # Valuta la sicurezza del re bianco
        if board.attacks(white_king_square) & board.pieces(chess.PAWN, chess.BLACK):
            evaluation += BoardEvaluationChessGame.OPEN_FILE_PENALTY
        for square in chess.SQUARES:
            if abs(square - white_king_square) in [1, 7, 8, 9] and board.piece_at(
                    square) == chess.PAWN and board.color_at(square) == chess.WHITE:
                evaluation += BoardEvaluationChessGame.ADJACENT_PAWN_BONUS

        # Valuta la sicurezza del re nero
        if board.attacks(black_king_square) & board.pieces(chess.PAWN, chess.WHITE):
            evaluation -= BoardEvaluationChessGame.OPEN_FILE_PENALTY
        for square in chess.SQUARES:
            if abs(square - black_king_square) in [1, 7, 8, 9] and board.piece_at(
                    square) == chess.PAWN and board.color_at(square) == chess.BLACK:
                evaluation -= BoardEvaluationChessGame.ADJACENT_PAWN_BONUS

        return evaluation * BoardEvaluationChessGame.KING_SAFETY_WEIGHT

    def center_control_evaluation(self, board):
        """ Valuta il controllo del centro. """
        # Pesi per il controllo del centro (puoi regolarli in base alle tue esigenze)

        evaluation = 0.0

        for square in BoardEvaluationChessGame.CENTER_SQUARES:
            # Se una casella centrale è occupata da un pezzo, assegna un punteggio
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    evaluation += 1
                else:
                    evaluation -= 1

            # Assegna punteggi aggiuntivi in base ai pezzi che controllano le caselle centrali
            attackers = board.attackers(chess.WHITE, square)
            evaluation += len(attackers)
            attackers = board.attackers(chess.BLACK, square)
            evaluation -= len(attackers)

        return evaluation * BoardEvaluationChessGame.CENTER_CONTROL_WEIGHT

    def bishop_pair_evaluation(self, board):
        """ Valuta la coppia di alfieri. """

        # Peso per il vantaggio della coppia di alfieri

        evaluation = 0.0

        white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))

        if white_bishops == 2:
            evaluation += BoardEvaluationChessGame.BISHOP_PAIR_BONUS
        if black_bishops == 2:
            evaluation -= BoardEvaluationChessGame.BISHOP_PAIR_BONUS

        return evaluation

    def queen_activity_evaluation(self, board):
        """ Valuta l'attività della regina. """
        # Peso per l'attività della regina

        evaluation = 0.0

        white_queens = board.pieces(chess.QUEEN, chess.WHITE)
        black_queens = board.pieces(chess.QUEEN, chess.BLACK)

        for queen_square in white_queens:
            # Ottieni tutte le caselle che la regina può attaccare da quella posizione
            legal_moves = board.attacks(queen_square)
            evaluation += BoardEvaluationChessGame.QUEEN_ACTIVITY_WEIGHT * len(legal_moves)

        for queen_square in black_queens:
            legal_moves = board.attacks(queen_square)
            evaluation -= BoardEvaluationChessGame.QUEEN_ACTIVITY_WEIGHT * len(legal_moves)

        return evaluation

    def knight_activity_evaluation(self, board):
        """ Valuta l'attività dei cavalli. """

        evaluation = 0.0

        white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
        black_knights = board.pieces(chess.KNIGHT, chess.BLACK)

        for knight_square in white_knights:
            # Ottieni tutte le caselle che il cavallo può attaccare da quella posizione
            legal_moves = board.attacks(knight_square)
            evaluation += BoardEvaluationChessGame.KNIGHT_ACTIVITY_WEIGHT * len(legal_moves)

        for knight_square in black_knights:
            legal_moves = board.attacks(knight_square)
            evaluation -= BoardEvaluationChessGame.KNIGHT_ACTIVITY_WEIGHT * len(legal_moves)

        return evaluation
