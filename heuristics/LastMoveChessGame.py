import chess


class LastMoveChessGame:
    def __init__(self):
        # Pesi per le diverse euristiche. Questi possono essere modificati per influenzare
        # l'importanza relativa delle diverse euristiche.
        self.weights = {
            "capture_value": 1.0,
            "threat_creation": 0.5,
            "defensive_move": 0.5,
            "central_control": 0.3
        }

    @staticmethod
    def get_last_move(game_board):
        if len(game_board.move_stack) > 0:
            return game_board.move_stack[-1]
        else:
            return None

    def h(self, state):
        """
        Funzione euristica principale che combina diverse euristiche basate sull'ultima mossa.
        """
        game_board = state.game_board
        last_move = self.get_last_move(game_board)
        return sum(self.weights[name] * heuristic(game_board, last_move) for name, heuristic in {
            "capture_value": self.capture_value_heuristic,
            "threat_creation": self.threat_creation_heuristic,
            "defensive_move": self.defensive_move_heuristic,
            "central_control": self.central_control_heuristic
        }.items())

    def capture_value_heuristic(self, game_board, move):
        """Valuta il valore della cattura effettuata nell'ultima mossa."""
        captured_piece = game_board.piece_at(move.to_square)
        if captured_piece:
            return self._get_piece_value(captured_piece)
        return 0

    @staticmethod
    def threat_creation_heuristic(game_board, move):
        """Valuta se l'ultima mossa ha creato minacce."""
        threats = len(game_board.attackers(game_board.turn, move.to_square))
        return threats

    @staticmethod
    def defensive_move_heuristic(game_board, move):
        """Valuta se l'ultima mossa era difensiva."""
        if len(game_board.attackers(not game_board.turn, move.from_square)) > len(
                game_board.attackers(not game_board.turn, move.to_square)):
            return 1
        return 0

    @staticmethod
    def central_control_heuristic(self, game_board, move):
        """Valuta se l'ultima mossa controlla il centro."""
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        if move.to_square in center_squares:
            return 1
        return 0

    @staticmethod
    def _get_piece_value(piece):
        """Restituisce il valore di un pezzo."""
        values = {
            chess.PAWN: 1.0,
            chess.KNIGHT: 3.0,
            chess.BISHOP: 3.0,
            chess.ROOK: 5.0,
            chess.QUEEN: 9.0,
            chess.KING: 0.0
        }
        return values[piece.piece_type]
