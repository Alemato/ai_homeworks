from constants import *

# 13 microsecondi
class EvaluateBoardWithoutKing:
    def h(self, board):
        # Se la partita è finita, restituisce un valore molto alto o molto basso
        if board.is_game_over():
            if board.is_checkmate():
                return -9999 if board.turn else 9999
            else:
                return 0  # Gestisce stallo e materiale insufficiente

        # Valutazione basata sui soli pezzi, ottimizzata
        eval = sum(PIECE_VALUE[piece] * (len(board.pieces(piece, chess.WHITE)) - len(board.pieces(piece, chess.BLACK)))
                   for piece in PIECE_VALUE)

        # Aggiungi qui altre euristiche, come la posizione dei pezzi, la mobilità, ecc.

        # Preferisce chi ha il turno di gioco, dato che potrebbe avere l'iniziativa
        eval += 0.1 if board.turn else -0.1

        return eval
