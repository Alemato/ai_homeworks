import chess

from State import State


class SimpleBoardEvaluationChessGame:
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # Il re ha un valore speciale in quanto la sua cattura determina la fine del gioco
    }

    @staticmethod
    def h(state: State):
        """
        Funzione euristica che valuta la scacchiera.
        Ritorna un valore positivo se la posizione è favorevole al bianco e un valore negativo se è favorevole al nero.
        """
        board = state.game_board
        evaluation = 0.0

        for square, piece in board.piece_map().items():
            piece_value = SimpleBoardEvaluationChessGame.PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                evaluation += piece_value
            else:
                evaluation -= piece_value

        return evaluation
