import chess

# 32 microsecondi
class EvaluateMobility:
    def h(self, board):
        white_mobility = 0
        black_mobility = 0

        # Calculate mobility in one pass over the legal moves
        for move in board.legal_moves:
            if board.color_at(move.from_square) == chess.WHITE:
                white_mobility += 1
            else:
                black_mobility += 1

        mobility_balance = white_mobility - black_mobility
        return mobility_balance if board.turn == chess.WHITE else -mobility_balance
