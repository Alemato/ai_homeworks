import os
from concurrent.futures import ProcessPoolExecutor

import chess
import pandas as pd

from chessgame.heuristics.ObservationBoard import ObservationBoard


def eval_fen(csv_row):
    fen = csv_row['FEN']
    hl = csv_row['Evaluation']
    observation = ObservationBoard(normalize_result=True)
    evaluation = observation.h_piccoli(chess.Board(fen))
    return evaluation + [hl]


def generate_csv():
    # Numero di lavoratori
    number_of_workers = os.cpu_count()

    heuristic_csv = pd.DataFrame(
        columns=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16',
                 'h17', 'h18', 'h19', 'h20', 'HL'])

    csv_num_files = 130
    # Percorso della cartella dove si trovano i file
    directory = '../csv/chessdata'

    for i in range(1, csv_num_files + 1):
        csv_file = f"{directory}/chessData_partizione_{i}.csv"
        df_chunk = pd.read_csv(csv_file)
        print(f"\ncarico il csv: {csv_file}")
        # Processa il chunk
        with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
            res = list(executor.map(eval_fen, df_chunk.to_dict('records')))

        heuristic_csv = pd.concat([heuristic_csv, pd.DataFrame(res, columns=heuristic_csv.columns)])
        print("file elaborato")

    print(f"\nelaborati tutti i {csv_num_files} file. Scrivo il csv finale\n")
    # Salva il nuovo DataFrame in un file CSV
    heuristic_csv.to_csv('../csv/eval_dataset.csv', index=False)
    print("csv finale scritto\n")

    # Mostra le prime righe del nuovo DataFrame
    print(heuristic_csv.head())


if __name__ == '__main__':
    generate_csv()
