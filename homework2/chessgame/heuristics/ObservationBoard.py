from .EvaluateBoardWithoutKing import EvaluateBoardWithoutKing
from .EvaluateCentralControlScore import EvaluateCentralControlScore
from .EvaluateKingSafety import EvaluateKingSafety
from .EvaluateMobility import EvaluateMobility
from .EvaluatePawnStructure import EvaluatePawnStructure
from .EvaluatePiecePositions import EvaluatePiecePositions
from .constants import *


class ObservationBoard:
    def __init__(self, normalize_result=False):
        self.normalize_result = normalize_result
        self.evaluate_board_without_king = EvaluateBoardWithoutKing(normalize_result=normalize_result)
        self.evaluate_central_control_score = EvaluateCentralControlScore(normalize_result=normalize_result)
        self.evaluate_king_safety = EvaluateKingSafety(normalize_result=normalize_result)
        self.evaluate_mobility = EvaluateMobility(normalize_result=normalize_result)
        self.evaluate_pawn_structure = EvaluatePawnStructure(normalize_result=normalize_result)
        self.evaluate_piece_positions = EvaluatePiecePositions(normalize_result=normalize_result)

    # 87 microsecondi
    def calcola_materiale_totale_spazio_attivita_pezzi_minacce_dirette(self, board):
        """
            Calcola il valore totale dei pezzi per ciascun giocatore su una scacchiera di chess.
            Calcola lo spazio (numero di case controllate) per ciascun giocatore.
            Calcola l'attività dei pezzi (esclusi i pedoni) per ciascun giocatore.
            Calcola il numero di minacce dirette (pezzi attaccati) per ciascun giocatore.
        """
        materiale_bianco = 0
        materiale_nero = 0
        spazio_bianco = 0
        spazio_nero = 0
        attivita_pezzi_bianco = 0
        attivita_pezzi_nero = 0
        minacce_dirette_bianco = 0
        minacce_dirette_nero = 0

        attaccanti_bianco = set()
        attaccanti_nero = set()
        for square in chess.SQUARES:
            if board.is_attacked_by(chess.WHITE, square):
                spazio_bianco += 1
                attaccanti_bianco.add(square)
            if board.is_attacked_by(chess.BLACK, square):
                spazio_nero += 1
                attaccanti_nero.add(square)

        for square in chess.SQUARES:
            pezzo = board.piece_at(square)
            if pezzo:
                valore = PIECE_VALUE[pezzo.piece_type]
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
        """Calcola il controllo del centro del tavolo da parte di ciascun giocatore."""
        case_centrali = [chess.D4, chess.E4, chess.D5, chess.E5]
        controllo_centro_bianco = 0
        controllo_centro_nero = 0

        for casa in case_centrali:
            attaccanti_bianchi = board.attackers(chess.WHITE, casa)
            attaccanti_neri = board.attackers(chess.BLACK, casa)

            if attaccanti_bianchi:
                controllo_centro_bianco += 1
            if attaccanti_neri:
                controllo_centro_nero += 1

        return controllo_centro_bianco, controllo_centro_nero

    # 3.4 microsecondi
    def calcola_mossa_pedoni(self, board):
        """Calcola il numero di pedoni che hanno mosso dalla loro posizione iniziale per ciascun giocatore."""
        mossa_pedoni_bianco = 0
        mossa_pedoni_nero = 0

        for colonna in range(8):
            # Verifica pedoni bianchi sulla seconda riga
            casa_iniziale_bianco = chess.square(colonna, 1)
            pezzo_bianco = board.piece_at(casa_iniziale_bianco)
            if not (pezzo_bianco and pezzo_bianco.piece_type == chess.PAWN and pezzo_bianco.color == chess.WHITE):
                mossa_pedoni_bianco += 1

            # Verifica pedoni neri sulla settima riga
            casa_iniziale_nero = chess.square(colonna, 6)
            pezzo_nero = board.piece_at(casa_iniziale_nero)
            if not (pezzo_nero and pezzo_nero.piece_type == chess.PAWN and pezzo_nero.color == chess.BLACK):
                mossa_pedoni_nero += 1

        return mossa_pedoni_bianco, mossa_pedoni_nero

    # 10.2 microsecondi
    def calcola_struttura_pedoni(self, board):
        """Calcola un punteggio basato sulla struttura dei pedoni per ciascun giocatore."""
        punteggio_pedoni_bianco, punteggio_pedoni_nero = 0, 0
        colonna_pedoni_bianchi, colonna_pedoni_neri = [0] * 8, [0] * 8

        # Conta il numero di pedoni in ogni colonna per ciascun giocatore
        for square in chess.SQUARES:
            pezzo = board.piece_at(square)
            if pezzo and pezzo.piece_type == chess.PAWN:
                colonna = chess.square_file(square)
                if pezzo.color == chess.WHITE:
                    colonna_pedoni_bianchi[colonna] += 1
                else:
                    colonna_pedoni_neri[colonna] += 1

        # Calcola punteggi basati su pedoni isolati e doppiati
        for i in range(8):
            punteggio_pedoni_bianco -= colonna_pedoni_bianchi[i] if colonna_pedoni_bianchi[i] > 1 else 0
            punteggio_pedoni_nero -= colonna_pedoni_neri[i] if colonna_pedoni_neri[i] > 1 else 0

            if colonna_pedoni_bianchi[i] > 0:
                punteggio_pedoni_bianco -= (i == 0 or colonna_pedoni_bianchi[i - 1] == 0) and (
                        i == 7 or colonna_pedoni_bianchi[i + 1] == 0)
            if colonna_pedoni_neri[i] > 0:
                punteggio_pedoni_nero -= (i == 0 or colonna_pedoni_neri[i - 1] == 0) and (
                        i == 7 or colonna_pedoni_neri[i + 1] == 0)

        return punteggio_pedoni_bianco, punteggio_pedoni_nero

    # 1.74 microsecondo
    def calcola_mossa_pezzi_maggiori(self, board):
        """Calcola il numero di mosse effettuate dai pezzi maggiori (torri, alfieri, regine) per ciascun giocatore."""
        mossa_pezzi_maggiori_bianco = 0
        mossa_pezzi_maggiori_nero = 0

        # Posizioni iniziali dei pezzi maggiori per ciascun giocatore
        posizioni_iniziali_bianco = [chess.A1, chess.B1, chess.C1, chess.D1, chess.E1, chess.F1, chess.G1, chess.H1]
        posizioni_iniziali_nero = [chess.A8, chess.B8, chess.C8, chess.D8, chess.E8, chess.F8, chess.G8, chess.H8]

        # Controllare se i pezzi maggiori hanno mosso dalla loro posizione iniziale
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

        return mossa_pezzi_maggiori_bianco, mossa_pezzi_maggiori_nero

    # 949 nanosecondo
    def calcola_sviluppo_pezzi(self, board):
        """Calcola lo sviluppo dei pezzi (cavalli e alfieri) per ciascun giocatore."""
        sviluppo_pezzi_bianco = 0
        sviluppo_pezzi_nero = 0

        # Posizioni iniziali dei cavalli e degli alfieri per ciascun giocatore
        posizioni_iniziali_bianco = [chess.B1, chess.G1, chess.C1, chess.F1]
        posizioni_iniziali_nero = [chess.B8, chess.G8, chess.C8, chess.F8]

        # Controllare se i pezzi hanno mosso dalla loro posizione iniziale
        for posizione in posizioni_iniziali_bianco:
            pezzo = board.piece_at(posizione)
            if pezzo is None or (pezzo.piece_type != chess.KNIGHT and pezzo.piece_type != chess.BISHOP):
                sviluppo_pezzi_bianco += 1

        for posizione in posizioni_iniziali_nero:
            pezzo = board.piece_at(posizione)
            if pezzo is None or (pezzo.piece_type != chess.KNIGHT and pezzo.piece_type != chess.BISHOP):
                sviluppo_pezzi_nero += 1

        return sviluppo_pezzi_bianco, sviluppo_pezzi_nero

    def __normalize(self, value, h_max_value, h_min_value, maxv=10, minv=-10):
        # Controlla se l'intervallo di origine ha ampiezza zero
        if h_max_value == h_min_value:
            raise ValueError("Il valore massimo e minimo non possono essere uguali.")

        # Calcola l'ampiezza degli intervalli
        range_high = h_max_value - h_min_value
        range_norm = maxv - minv

        # Normalizza il valore
        normalized_value = (((value - h_min_value) * range_norm) / range_high) + minv

        return normalized_value

    def h_piccoli(self, board):
        # Creare un array vuoto
        risultati = []
        if self.normalize_result:
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
            risultati.append(self.__normalize(res[0], 0, h_min_value=-11))
            risultati.append(self.__normalize(res[1], 0, h_min_value=-11))

            res = self.calcola_mossa_pezzi_maggiori(board)
            risultati.append(self.__normalize(res[0], 9, 0))
            risultati.append(self.__normalize(res[1], 9, 0))

            res = self.calcola_sviluppo_pezzi(board)
            risultati.append(self.__normalize(res[0], 5, 0))
            risultati.append(self.__normalize(res[1], 5, 0))
        else:
            risultati.extend(self.calcola_materiale_totale_spazio_attivita_pezzi_minacce_dirette(board))
            risultati.extend(self.calcola_sicurezza_re(board))
            risultati.extend(self.calcola_controllo_centro(board))
            risultati.extend(self.calcola_mossa_pedoni(board))
            risultati.extend(self.calcola_struttura_pedoni(board))
            risultati.extend(self.calcola_mossa_pezzi_maggiori(board))
            risultati.extend(self.calcola_sviluppo_pezzi(board))

        risultati.append(self.evaluate_board_without_king.h_piccolo(board))
        risultati.append(self.evaluate_central_control_score.h_piccolo(board))
        risultati.append(self.evaluate_king_safety.h_piccolo(board))
        risultati.append(self.evaluate_mobility.h_piccolo(board))
        risultati.append(self.evaluate_pawn_structure.h_piccolo(board))
        risultati.append(self.evaluate_piece_positions.h_piccolo(board))

        # Restituire l'array risultante
        return risultati
