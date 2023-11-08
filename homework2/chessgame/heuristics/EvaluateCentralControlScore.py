import chess


class EvaluateCentralControlScore:
    def h(self, board):
        # Punti assegnati per il controllo di ogni casa centrale
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        score = 0

        # Valori da calibrare in base alla tua specifica euristica
        central_square_control = 0.3

        for square in center_squares:
            # Controlla se una casa centrale è controllata dai bianchi
            if board.is_attacked_by(chess.WHITE, square):
                score += central_square_control

            # Controlla se una casa centrale è controllata dai neri
            if board.is_attacked_by(chess.BLACK, square):
                score -= central_square_control

        # Adatta il punteggio al giocatore corrente
        if board.turn == chess.WHITE:
            return score
        else:
            return -score
