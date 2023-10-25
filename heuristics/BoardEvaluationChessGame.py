import chess

from State import State


class BoardEvaluationChessGame:
    def __init__(self):
        # Pesi per le diverse euristiche. Questi possono essere modificati per influenzare
        # l'importanza relativa delle diverse euristiche.
        self.weights = {
            "material": 1.0,
            "mobility": 0.1,
            "king_safety": 0.5,
            "pawn_structure": 0.2,
            "center_control": 0.15,
            "piece_development": 0.1,
            "key_square_control": 0.15
        }

    def h(self, state: State):
        """
        Funzione euristica principale che combina diverse euristiche.
        """
        game_board = state.game_board
        return sum(self.weights[name] * heuristic(game_board) for name, heuristic in {
            "material": self.material_heuristic,
            "mobility": self.mobility_heuristic,
            "king_safety": self.king_safety_heuristic,
            "pawn_structure": self.pawn_structure_heuristic,
            "center_control": self.center_control_heuristic,
            "piece_development": self.piece_development_heuristic,
            "key_square_control": self.key_square_control_heuristic
        }.items())

    @staticmethod
    def material_heuristic(game_board):
        """
        Euristica che valuta il materiale (pezzi) sul tabellone.
        """
        piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,  # valori standard per i pezzi
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0  # valori negativi per i pezzi neri
        }
        return sum(piece_values[piece.symbol()] for piece in game_board.piece_map().values())

    @staticmethod
    def mobility_heuristic(game_board):
        """
        Euristica che valuta la mobilità dei pezzi.
        """
        white_mobility = len(list(game_board.legal_moves))  # conteggio delle mosse legali per il bianco
        game_board.turn = not game_board.turn  # cambio il turno
        black_mobility = len(list(game_board.legal_moves))  # conteggio delle mosse legali per il nero
        return white_mobility - black_mobility

    @staticmethod
    def king_safety_heuristic(game_board):
        """
        Euristica che valuta la sicurezza del re.
        Questa è una semplice implementazione e può essere ulteriormente raffinata.
        """
        if game_board.is_checkmate():
            if game_board.turn == chess.WHITE:
                return -float('inf')  # matto al bianco
            else:
                return float('inf')  # matto al nero
        elif game_board.is_check():
            if game_board.turn == chess.WHITE:
                return -10  # scacco al bianco
            else:
                return 10  # scacco al nero
        return 0  # nessun scacco

    @staticmethod
    def pawn_structure_heuristic(game_board):
        """Valuta la struttura dei pedoni."""
        return len(game_board.pieces(chess.PAWN, chess.WHITE)) - len(game_board.pieces(chess.PAWN, chess.BLACK))

    @staticmethod
    def center_control_heuristic(game_board):
        """Valuta il controllo del centro."""
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        return sum(1 for square in center_squares if game_board.piece_at(square) is not None)

    @staticmethod
    def piece_development_heuristic(game_board):
        """Valuta lo sviluppo armonico dei pezzi."""
        # Semplificato: valuta solo l'uscita dei cavalli e degli alfieri.
        developed_pieces = sum(
            1 for square in [chess.B1, chess.G1, chess.B8, chess.G8] if game_board.piece_at(square) is not None)
        return developed_pieces

    @staticmethod
    def key_square_control_heuristic(game_board):
        """Valuta il controllo delle case chiave."""
        # Come esempio, considera solo le case d4, d5, e4, e5.
        key_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        return sum(1 for square in key_squares if game_board.piece_at(square) is not None)
