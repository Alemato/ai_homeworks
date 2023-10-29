# Dictionary defining the intrinsic values for each chess piece.
piece_values = {
    "p": 100,   # Value of a Pawn
    "n": 320,   # Value of a Knight
    "b": 330,   # Value of a Bishop
    "r": 500,   # Value of a Rook
    "q": 900,   # Value of a Queen
    "k": 20000, # Value of a King (set very high to represent its critical importance)
}

# Piece-square table for the white pawn, defining values based on pawn's position on the board.
pawn_white_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]

# The black pawn's piece-square table is just a reversed version of the white pawn's table.
pawn_black_table = list(reversed(pawn_white_table))

# Piece-square table for the white knight.
knight_white_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

# The black knight's table is a reversed version of the white knight's table.
knight_black_table = list(reversed(knight_white_table))

# Piece-square table for the white bishop.
bishop_white_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

# The black bishop's table is a reversed version of the white bishop's table.
bishop_black_table = list(reversed(bishop_white_table))

# Piece-square table for the white rook.
rook_white_table = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

# The black rook's table is a reversed version of the white rook's table.
rook_black_table = list(reversed(rook_white_table))

# Piece-square table for the white queen.
queen_white_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

# The black queen's table is a reversed version of the white queen's table.
queen_black_table = list(reversed(queen_white_table))

# Piece-square table for the white king during the middle game.
king_white_table = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

# The black king's table is a reversed version of the white king's table.
king_black_table = list(reversed(king_white_table))

# Piece-square table for the white king during the endgame.
king_white_table_endgame = [
    -50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]

# The black king's endgame table is a reversed version of the white king's endgame table.
king_black_table_endgame = list(reversed(king_white_table_endgame))

# A comprehensive dictionary containing piece-square tables for each piece and color.
# The tables indicate the value of placing a piece on a specific square.
piece_square_tables = {
    "p": pawn_black_table,  # Black pawn
    "n": knight_black_table,  # Black knight
    "b": bishop_black_table,  # Black bishop
    "r": rook_black_table,  # Black rook
    "q": queen_black_table,  # Black queen
    "k": {"early": king_black_table, "end": king_black_table_endgame},  # Black king (both middle game and endgame)

    "P": pawn_white_table,  # White pawn
    "N": knight_white_table,  # White knight
    "B": bishop_white_table,  # White bishop
    "R": rook_white_table,  # White rook
    "Q": queen_white_table,  # White queen
    "K": {"early": king_white_table, "end": king_white_table_endgame},  # White king (both middle game and endgame)
}
