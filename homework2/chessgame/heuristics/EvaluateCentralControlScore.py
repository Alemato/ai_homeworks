import chess

from chessgame import StateChessGame


# 5.64 microsecondi
# min = -1.2
# max = 1.2
class EvaluateCentralControlScore:
    def __init__(self, evaluate_end_game_phase=False, normalize_result=False):
        self.evaluate_end_game_phase = evaluate_end_game_phase
        self.normalize_result = normalize_result
        self.h_max_value = 1.2
        self.h_min_value = -1.2

    def h(self, state: StateChessGame):
        if self.evaluate_end_game_phase:
            return self.__h(state.game_board)
        elif self.normalize_result:
            raw_eval = self.__h(state.game_board)
            return self.__normalize(raw_eval)
        else:
            return self.__h(state.game_board)

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
