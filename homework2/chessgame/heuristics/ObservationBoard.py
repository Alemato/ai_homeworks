from .EvaluateBoardWithoutKing import EvaluateBoardWithoutKing
from .EvaluateCentralControlScore import EvaluateCentralControlScore
from .EvaluateKingSafety import EvaluateKingSafety
from .EvaluateMobility import EvaluateMobility
from .EvaluatePawnStructure import EvaluatePawnStructure
from .EvaluatePiecePositions import EvaluatePiecePositions
from .constants import *


class ObservationBoard:
    """
    This class observes various aspects of a chess game board, offering a comprehensive analysis of material,
    space, piece activity, direct threats.

    Attributes:
        normalize_result (bool): If true, normalizes the evaluation score within a specific range.
    """

    def __init__(self, normalize_result=False):
        """
        Initializes the observation components for different aspects of the chess game.

        :param normalize_result: Indicates whether to normalize the evaluation scores.
        """
        self.normalize_result = normalize_result

    # 87 microsecondi
    def calcola_materiale_totale_spazio_attivita_pezzi_minacce_dirette(self, board):
        """
        Calculates and evaluates several aspects of the chessboard for both players: the total material value,
        space control, activity of pieces (excluding pawns), and the number of direct threats (attacked pieces).

        :param board: The chess board to be evaluated.
        :return: A tuple containing the total material value, space control, piece activity, and direct threats
                 for both players (white and black).
        """
        materiale_bianco = 0  # Total material value for white player.
        materiale_nero = 0  # Total material value for black player.
        spazio_bianco = 0  # Number of squares controlled by white player.
        spazio_nero = 0  # Number of squares controlled by black player.
        attivita_pezzi_bianco = 0  # Activity of pieces (excluding pawns) for white player.
        attivita_pezzi_nero = 0  # Activity of pieces (excluding pawns) for black player.
        minacce_dirette_bianco = 0  # Number of white pieces under direct threat.
        minacce_dirette_nero = 0  # Number of black pieces under direct threat.

        attaccanti_bianco = set()  # Set of squares attacked by white player.
        attaccanti_nero = set()  # Set of squares attacked by black player.

        # Calculate space control and attackers for each square.
        for square in chess.SQUARES:
            if board.is_attacked_by(chess.WHITE, square):
                spazio_bianco += 1
                attaccanti_bianco.add(square)
            if board.is_attacked_by(chess.BLACK, square):
                spazio_nero += 1
                attaccanti_nero.add(square)

        # Evaluate material, piece activity, and direct threats.
        for square in chess.SQUARES:
            pezzo = board.piece_at(square)
            if pezzo:
                valore = PIECE_VALUE[pezzo.piece_type]  # Value of the piece based on its type.
                if pezzo.color == chess.WHITE:
                    materiale_bianco += valore
                    if square in attaccanti_nero:
                        minacce_dirette_bianco += 1
                    if pezzo.piece_type != chess.PAWN:
                        attivita_pezzi_bianco += len(board.attacks(square))
                else:
                    materiale_nero += valore
                    if square in attaccanti_bianco:
                        minacce_dirette_nero += 1
                    if pezzo.piece_type != chess.PAWN:
                        attivita_pezzi_nero += len(board.attacks(square))

        # Return a tuple with the calculated values.
        return (materiale_bianco, materiale_nero, spazio_bianco, spazio_nero, attivita_pezzi_bianco,
                attivita_pezzi_nero, minacce_dirette_bianco, minacce_dirette_nero)

    # 2.55 microsecondi
    def calcola_sicurezza_re(self, board):
        """Calcola la sicurezza del re per ciascun giocatore su una scacchiera di chess."""
        sicurezza_re_bianco = 0
        sicurezza_re_nero = 0

        posizione_re_bianco = board.king(chess.WHITE)
        posizione_re_nero = board.king(chess.BLACK)

        pedone_bianco = chess.Piece(chess.PAWN, chess.WHITE)
        pedone_nero = chess.Piece(chess.PAWN, chess.BLACK)

        # Direzioni per i pedoni bianchi e neri
        direzioni_bianche = [8, 7, 9]  # Nord, Nord-Ovest, Nord-Est
        direzioni_nere = [-8, -7, -9]  # Sud, Sud-Est, Sud-Ovest

        # Calcolare la sicurezza basandosi sui pedoni circostanti e la posizione
        for direzione in direzioni_bianche:
            casa_pedone_bianco = posizione_re_bianco + direzione
            if casa_pedone_bianco in chess.SQUARES and board.piece_at(casa_pedone_bianco) == pedone_bianco:
                sicurezza_re_bianco += 1

        for direzione in direzioni_nere:
            casa_pedone_nero = posizione_re_nero + direzione
            if casa_pedone_nero in chess.SQUARES and board.piece_at(casa_pedone_nero) == pedone_nero:
                sicurezza_re_nero += 1

        return sicurezza_re_bianco, sicurezza_re_nero

    # 6.41 microsecondi
    def calcola_controllo_centro(self, board):
        """
        Calculates the control of the board's center by each player. It assesses which player controls
        the central squares (D4, E4, D5, E5) and by how much, providing an indication of the central dominance
        in the chess game.

        :param board: The chess board to be evaluated.
        :return: A tuple containing the control of the center score for both the white and black players.
        """
        case_centrali = [chess.D4, chess.E4, chess.D5, chess.E5]  # Central squares of the chessboard.
        controllo_centro_bianco = 0  # Control of the center by white player.
        controllo_centro_nero = 0  # Control of the center by black player.

        # Iterate through each central square to assess control by white and black.
        for casa in case_centrali:
            attaccanti_bianchi = board.attackers(chess.WHITE, casa)
            attaccanti_neri = board.attackers(chess.BLACK, casa)

            if attaccanti_bianchi:
                controllo_centro_bianco += 1  # Increase score if white controls the square.
            if attaccanti_neri:
                controllo_centro_nero += 1  # Increase score if black controls the square.

        # Return the control scores for white and black players.
        return controllo_centro_bianco, controllo_centro_nero

    # 3.4 microsecondi
    def calcola_mossa_pedoni(self, board):
        """
        Calculates the number of pawns that have moved from their initial position for each player. This metric
        gives an insight into the pawn advancement and structure in the game, which is a key aspect of chess strategy.

        :param board: The chess board to be evaluated.
        :return: A tuple containing the count of moved pawns for both white and black players.
        """
        mossa_pedoni_bianco = 0  # Number of white pawns that have moved from their initial positions.
        mossa_pedoni_nero = 0  # Number of black pawns that have moved from their initial positions.

        # Iterate through each column to check if pawns have moved from their starting rows.
        for colonna in range(8):
            # Check for white pawns on the second rank.
            casa_iniziale_bianco = chess.square(colonna, 1)
            pezzo_bianco = board.piece_at(casa_iniziale_bianco)
            if not (pezzo_bianco and pezzo_bianco.piece_type == chess.PAWN and pezzo_bianco.color == chess.WHITE):
                mossa_pedoni_bianco += 1

            # Check for black pawns on the seventh rank.
            casa_iniziale_nero = chess.square(colonna, 6)
            pezzo_nero = board.piece_at(casa_iniziale_nero)
            if not (pezzo_nero and pezzo_nero.piece_type == chess.PAWN and pezzo_nero.color == chess.BLACK):
                mossa_pedoni_nero += 1

        # Return the count of moved pawns for both white and black players.
        return mossa_pedoni_bianco, mossa_pedoni_nero

    # 10.2 microsecondi
    def calcola_struttura_pedoni(self, board):
        """
        Calculates a score based on the pawn structure for each player. This evaluation considers aspects like
        isolated and doubled pawns, which are crucial for understanding the pawn dynamics and structural weaknesses
        or strengths in a chess game.

        :param board: The chess board to be evaluated.
        :return: A tuple containing the pawn structure score for both the white and black players.
        """
        punteggio_pedoni_bianco = 0  # Score for the pawn structure of white player.
        punteggio_pedoni_nero = 0  # Score for the pawn structure of black player.
        colonna_pedoni_bianchi = [0] * 8  # Count of white pawns in each column.
        colonna_pedoni_neri = [0] * 8  # Count of black pawns in each column.

        # Count the number of pawns in each column for each player.
        for square in chess.SQUARES:
            pezzo = board.piece_at(square)
            if pezzo and pezzo.piece_type == chess.PAWN:
                colonna = chess.square_file(square)
                if pezzo.color == chess.WHITE:
                    colonna_pedoni_bianchi[colonna] += 1
                else:
                    colonna_pedoni_neri[colonna] += 1

        # Calculate scores based on isolated and doubled pawns.
        for i in range(8):
            # Subtract points for doubled pawns.
            punteggio_pedoni_bianco -= colonna_pedoni_bianchi[i] if colonna_pedoni_bianchi[i] > 1 else 0
            punteggio_pedoni_nero -= colonna_pedoni_neri[i] if colonna_pedoni_neri[i] > 1 else 0

            # Subtract points for isolated pawns.
            if colonna_pedoni_bianchi[i] > 0:
                punteggio_pedoni_bianco -= (i == 0 or colonna_pedoni_bianchi[i - 1] == 0) and (
                        i == 7 or colonna_pedoni_bianchi[i + 1] == 0)
            if colonna_pedoni_neri[i] > 0:
                punteggio_pedoni_nero -= (i == 0 or colonna_pedoni_neri[i - 1] == 0) and (
                        i == 7 or colonna_pedoni_neri[i + 1] == 0)

        # Return the pawn structure score for both white and black players.
        return abs(punteggio_pedoni_bianco), abs(punteggio_pedoni_nero)

    # 1.74 microsecondo
    def calcola_mossa_pezzi_maggiori(self, board):
        """
        Calculates the number of moves made by major pieces (rooks, bishops, queens) for each player.
        This metric assesses how many major pieces have moved from their initial positions,
        providing an insight into the player's development and strategy in the game.

        :param board: The chess board to be evaluated.
        :return: A tuple containing the count of major pieces that have moved for both white and black players.
        """
        mossa_pezzi_maggiori_bianco = 0  # Count of white major pieces that have moved.
        mossa_pezzi_maggiori_nero = 0  # Count of black major pieces that have moved.

        # Initial positions of major pieces for white player.
        posizioni_iniziali_bianco = [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]
        # Initial positions of major pieces for black player.
        posizioni_iniziali_nero = [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]

        # Check if major pieces have moved from their initial positions.
        for posizione in posizioni_iniziali_bianco:
            pezzo = board.piece_at(posizione)
            if pezzo is None or (
                    pezzo.piece_type != chess.ROOK and pezzo.piece_type != chess.BISHOP and pezzo.piece_type != chess.QUEEN):
                mossa_pezzi_maggiori_bianco += 1

        for posizione in posizioni_iniziali_nero:
            pezzo = board.piece_at(posizione)
            if pezzo is None or (
                    pezzo.piece_type != chess.ROOK and pezzo.piece_type != chess.BISHOP and pezzo.piece_type != chess.QUEEN):
                mossa_pezzi_maggiori_nero += 1

        # Return the count of moved major pieces for both white and black players.
        return mossa_pezzi_maggiori_bianco, mossa_pezzi_maggiori_nero

    # 949 nanosecondo
    def calcola_sviluppo_pezzi(self, board):
        """
        Calculates the development of pieces (knights and bishops) for each player. This metric assesses how
        many knights and bishops have moved from their initial positions, providing insight into the early
        game development and piece activity, which are crucial aspects of chess strategy.

        :param board: The chess board to be evaluated.
        :return: A tuple containing the count of developed knights and bishops for both white and black players.
        """
        sviluppo_pezzi_bianco = 0  # Count of white knights and bishops that have moved.
        sviluppo_pezzi_nero = 0  # Count of black knights and bishops that have moved.

        # Initial positions of knights and bishops for white player.
        posizioni_iniziali_bianco = [chess.B1, chess.G1, chess.C1, chess.F1]
        # Initial positions of knights and bishops for black player.
        posizioni_iniziali_nero = [chess.B8, chess.G8, chess.C8, chess.F8]

        # Check if knights and bishops have moved from their initial positions.
        for posizione in posizioni_iniziali_bianco:
            pezzo = board.piece_at(posizione)
            if pezzo is None or (pezzo.piece_type != chess.KNIGHT and pezzo.piece_type != chess.BISHOP):
                sviluppo_pezzi_bianco += 1

        for posizione in posizioni_iniziali_nero:
            pezzo = board.piece_at(posizione)
            if pezzo is None or (pezzo.piece_type != chess.KNIGHT and pezzo.piece_type != chess.BISHOP):
                sviluppo_pezzi_nero += 1

        # Return the count of developed knights and bishops for both white and black players.
        return sviluppo_pezzi_bianco, sviluppo_pezzi_nero

    def __normalize(self, valore, max_val, min_val):
        if max_val - min_val == 0:
            return 0  # Evita la divisione per zero se min e max sono uguali
        return (valore - min_val) / (max_val - min_val)

    def h_piccoli(self, board):
        """
        Combines various metrics into a comprehensive array of evaluations for the board. This method
        serves as an aggregator that compiles a wide range of metrics from material value to pawn structure,
        piece activity, and other specialized evaluations, offering a multifaceted view of the board state.

        :param board: The chess board to be evaluated.
        :return: An array containing a diverse set of evaluation results.
        """
        risultati = []  # Array to store the results of various evaluations.

        # Apply normalization if enabled.
        if self.normalize_result:
            # Calculate and normalize various metrics.
            res = self.calcola_materiale_totale_spazio_attivita_pezzi_minacce_dirette(board)
            risultati.append(self.__normalize(res[0], 48, 0))
            risultati.append(self.__normalize(res[1], 48, 0))
            risultati.append(self.__normalize(res[2], 57, 0))
            risultati.append(self.__normalize(res[3], 57, 0))
            risultati.append(self.__normalize(res[4], 84, 0))
            risultati.append(self.__normalize(res[5], 84, 0))
            risultati.append(self.__normalize(res[6], 12, 0))
            risultati.append(self.__normalize(res[7], 12, 0))

            res = self.calcola_sicurezza_re(board)
            risultati.append(self.__normalize(res[0], 4, 0))
            risultati.append(self.__normalize(res[1], 4, 0))

            res = self.calcola_controllo_centro(board)
            risultati.append(self.__normalize(res[0], 5, 0))
            risultati.append(self.__normalize(res[1], 5, 0))

            res = self.calcola_mossa_pedoni(board)
            risultati.append(self.__normalize(res[0], 9, 0))
            risultati.append(self.__normalize(res[1], 9, 0))

            res = self.calcola_struttura_pedoni(board)
            risultati.append(self.__normalize(res[0], 11, 0))
            risultati.append(self.__normalize(res[1], 11, 0))

            res = self.calcola_mossa_pezzi_maggiori(board)
            risultati.append(self.__normalize(res[0], 9, 0))
            risultati.append(self.__normalize(res[1], 9, 0))

            res = self.calcola_sviluppo_pezzi(board)
            risultati.append(self.__normalize(res[0], 5, 0))
            risultati.append(self.__normalize(res[1], 5, 0))
        else:
            # Directly calculate and store the results without normalization.
            risultati.extend(self.calcola_materiale_totale_spazio_attivita_pezzi_minacce_dirette(board))
            risultati.extend(self.calcola_sicurezza_re(board))
            risultati.extend(self.calcola_controllo_centro(board))
            risultati.extend(self.calcola_mossa_pedoni(board))
            risultati.extend(self.calcola_struttura_pedoni(board))
            risultati.extend(self.calcola_mossa_pezzi_maggiori(board))
            risultati.extend(self.calcola_sviluppo_pezzi(board))

        # Return the resulting array.
        return risultati
