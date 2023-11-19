import csv
import os
import time
from concurrent.futures import ProcessPoolExecutor

from Agent import Agent
from ChessGame import ChessGame
from StateChessGame import StateChessGame
from algoritms.MinMaxAlphaBetaPruning import MinMaxAlphaBetaPruning
from algoritms.MinMaxAlphaBetaPruningH0Cut import MinMaxAlphaBetaPruningH0Cut
from algoritms.MinMaxAlphaBetaPruningHlCut import MinMaxAlphaBetaPruningHlCut
from chessgame.algoritms.MinMaxAlphaBetaPruningHrCut import MinMaxAlphaBetaPruningHrCut
from heuristics.HardBoardEvaluationChessGame import HardBoardEvaluationChessGame
from heuristics.SoftBoardEvaluationChessGame import SoftBoardEvaluationChessGame

min_max_alpha_beta_pruning = [
    [3, 3],
    [3, 4],
    [4, 3],
    [4, 4]
]

min_max_alpha_beta_pruning_h0_cut = [
    [3, 3, 5, 5],
    [3, 4, 5, 5],
    [4, 3, 5, 5],
    [4, 4, 5, 5],
    [3, 3, 3, 5],
    [3, 4, 3, 5],
    [4, 3, 3, 5],
    [4, 4, 3, 5],
    [5, 5, 5, 5],
    [6, 5, 5, 5],
    [5, 6, 5, 5],
    [6, 6, 5, 5],
    [7, 7, 5, 5],
    [8, 8, 3, 3],
    [9, 8, 3, 3],
    [8, 9, 3, 3],
    [9, 9, 3, 3],
    [9, 10, 3, 3],
    [10, 9, 3, 3],
    [10, 10, 3, 3]
]

min_max_alpha_beta_pruning_hl_cut = [
    [3, 3, 5, 5, 2, 2],
    [3, 4, 5, 5, 2, 2],
    [4, 3, 5, 5, 2, 2],
    [4, 4, 5, 5, 2, 2],

    [3, 3, 5, 5, 3, 3],
    [3, 4, 5, 5, 3, 3],
    [4, 3, 5, 5, 3, 3],
    [4, 4, 5, 5, 3, 3],

    [3, 3, 3, 5, 2, 2],
    [3, 4, 3, 5, 2, 2],
    [4, 3, 3, 5, 2, 2],
    [4, 4, 3, 5, 2, 2],

    [3, 3, 3, 5, 3, 3],
    [3, 4, 3, 5, 3, 3],
    [4, 3, 3, 5, 3, 3],
    [4, 4, 3, 5, 3, 3],

    [4, 4, 5, 5, 2, 3],
    [4, 4, 5, 5, 3, 3],

    [5, 5, 5, 5, 2, 2],
    [6, 5, 5, 5, 2, 2],
    [5, 6, 5, 5, 2, 2],
    [6, 6, 5, 5, 2, 2],
    [7, 7, 5, 5, 2, 2],
    [8, 8, 3, 3, 2, 2],
    [9, 8, 3, 3, 2, 2],
    [8, 9, 3, 3, 2, 2],
    [9, 9, 3, 3, 2, 2],
    [9, 10, 3, 3, 2, 2],
    [10, 9, 3, 3, 2, 2],
    [10, 10, 3, 3, 2, 2]
]

min_max_alpha_beta_pruning_h0_vs_hl_cut = [
    [3, 3, 5, 5, 3],
    [3, 4, 5, 5, 3],
    [4, 3, 5, 5, 3],
    [4, 4, 5, 5, 3],
    [5, 5, 5, 5, 3],
    [6, 5, 5, 5, 3],
    [5, 6, 5, 5, 3],
    [6, 6, 5, 5, 3],
    [7, 7, 5, 5, 2],
    [8, 8, 3, 3, 2],
    [9, 8, 3, 3, 2],
    [8, 9, 3, 3, 2],
    [9, 9, 3, 3, 2],
    [9, 10, 3, 3, 2],
    [10, 9, 3, 3, 2],
    [10, 10, 3, 3, 2]

]

min_max_alpha_beta_pruning_hr = [
    [3, 3, 5],
    [3, 4, 5],
    [4, 3, 5],
    [4, 4, 5],
    [5, 5, 3],
    [6, 6, 3],
    [9, 9, 3],
    [9, 10, 3],
    [10, 9, 3],
    [10, 10, 3]
]

min_max_alpha_beta_pruning_h0_vs_hr = [
    [3, 3, 5],
    [3, 4, 5],
    [4, 3, 5],
    [4, 4, 5],
    [5, 5, 3],
    [6, 6, 3],
    [9, 9, 3],
    [9, 10, 3],
    [10, 9, 3],
    [10, 10, 3]
]

min_max_alpha_beta_pruning_hl_vs_hr = [
    [3, 3, 5, 3],
    [3, 4, 5, 3],
    [4, 3, 5, 3],
    [4, 4, 5, 3],
    [5, 5, 3, 2],
    [6, 6, 3, 2],
    [9, 9, 3, 2],
    [9, 10, 3, 2],
    [10, 9, 3, 2],
    [10, 10, 3, 2]
]

min_max_alpha_beta_pruning_h0_vs_normal = [
    [3, 3, 5],
    [4, 3, 5],
    [5, 3, 5],
    [6, 3, 3],
    [10, 3, 3]
]

min_max_alpha_beta_pruning_vs_hl = [
    [3, 3, 5, 3],
    [3, 4, 5, 3],
    [3, 5, 5, 3],
    [3, 6, 3, 3],
    [3, 10, 3, 2]
]

min_max_alpha_beta_pruning_hr_vs_normal = [
    [3, 3, 5],
    [4, 3, 5],
    [5, 3, 5],
    [6, 3, 3],
    [10, 3, 3]
]


def main_normal():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic, max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic, max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning max_depth={setup[0]} vs min_max_alpha_beta_pruning max_depth={setup[1]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
            # print(state.game_board.fen())
            print("Agent 2 (BLACK) played the move:", state.move)
            print()
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
            # print(state.game_board.fen())
            print("Agent 1 (WHITE) played the move:", state.move)
            print()
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_games/games_{i}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Max Depth Agent 2', 'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning max_depth={setup[0]} vs min_max_alpha_beta_pruning max_depth={setup[1]}',
            'MinMax Alpha Beta Pruning', 'MinMax Alpha Beta Pruning', 'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[1], outcome_val, game_win, f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count])


def main_h0():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_h0_cut, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_h0_cut)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_h0_cut(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    cutoff_heuristic = SoftBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningH0Cut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruningH0Cut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[3],
                                                      max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_h0_cut max_depth={setup[1]} k={setup[3]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 1 WHITHE): {agent1.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_h0_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 2 BLACK): {agent2.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_h0_cut_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_h0_cut_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff H0 Agent 1', 'Max Depth Agent 2', 'Number CutOff H0 Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated H0 Agent 1', 'States evaluated H0 Agent 2', 'Pruning H0 carried out Agent 1',
                  'Pruning H0 carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_h0_cut max_depth={setup[1]} k={setup[3]}',
            'MinMax Alpha Beta Pruning H0 CutOff', 'MinMax Alpha Beta Pruning H0 CutOff',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[1], setup[3], outcome_val, game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_h0_cut_count,
            agent2.search_algorithm.eval_h0_cut_count, agent1.search_algorithm.prune_h0_cut_count,
            agent2.search_algorithm.prune_h0_cut_count])


def main_hl():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_hl_cut, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_hl_cut)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_hl_cut(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    cutoff_heuristic = SoftBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningHlCut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[2], l=setup[4],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruningHlCut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[3], l=setup[5],
                                                      max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_hl_cut max_depth={setup[0]} k={setup[2]} l={setup[4]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[3]} l={setup[5]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 1 WHITHE): {agent1.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_h0_cut_count}")
    print(f"States evaluated Hl      (agent 1 WHITHE): {agent1.search_algorithm.eval_hl_cut_count}")
    print(f"Pruning Hl carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_hl_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 2 BLACK): {agent2.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_h0_cut_count}")
    print(f"States evaluated Hl      (agent 2 BLACK): {agent2.search_algorithm.eval_hl_cut_count}")
    print(f"Pruning Hl carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_hl_cut_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_hl_cut_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff Agent 1', 'Number of l Agent 1', 'Max Depth Agent 2',
                  'Number CutOff Agent 2', 'Number of l Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated H0 Agent 1', 'States evaluated H0 Agent 2', 'Pruning H0 carried out Agent 1',
                  'Pruning H0 carried out Agent 2', 'States evaluated Hl Agent 1', 'States evaluated Hl Agent 2',
                  'Pruning Hl carried out Agent 1', 'Pruning Hl carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_hl_cut max_depth={setup[0]} k={setup[2]} l={setup[4]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[3]} l={setup[5]}',
            'MinMax Alpha Beta Pruning Hl CutOff', 'MinMax Alpha Beta Pruning Hl CutOff',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[4], setup[1], setup[3], setup[5], outcome_val,
            game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_h0_cut_count,
            agent2.search_algorithm.eval_h0_cut_count, agent1.search_algorithm.prune_h0_cut_count,
            agent2.search_algorithm.prune_h0_cut_count, agent1.search_algorithm.eval_hl_cut_count,
            agent2.search_algorithm.eval_hl_cut_count, agent1.search_algorithm.prune_hl_cut_count,
            agent2.search_algorithm.prune_hl_cut_count])


def main_h0_vs_hl():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_h0_vs_hl_cut, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_h0_vs_hl_cut)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_h0_vs_hl_cut(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    cutoff_heuristic = SoftBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningH0Cut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruningHlCut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[3], l=setup[4],
                                                      max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[3]} l={setup[4]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 1 WHITHE): {agent1.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_h0_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 2 BLACK): {agent2.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_h0_cut_count}")
    print(f"States evaluated Hl      (agent 2 BLACK): {agent2.search_algorithm.eval_hl_cut_count}")
    print(f"Pruning Hl carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_hl_cut_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_h0_vs_hl_cut_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff Agent 1', 'Max Depth Agent 2',
                  'Number CutOff Agent 2', 'Number of l Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated H0 Agent 1', 'States evaluated H0 Agent 2', 'Pruning H0 carried out Agent 1',
                  'Pruning H0 carried out Agent 2', 'States evaluated Hl Agent 2', 'Pruning Hl carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[3]} l={setup[4]}',
            'MinMax Alpha Beta Pruning H0 CutOff', 'MinMax Alpha Beta Pruning Hl CutOff',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[1], setup[3], setup[4], outcome_val,
            game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_h0_cut_count,
            agent2.search_algorithm.eval_h0_cut_count, agent1.search_algorithm.prune_h0_cut_count,
            agent2.search_algorithm.prune_h0_cut_count,
            agent2.search_algorithm.eval_hl_cut_count,
            agent2.search_algorithm.prune_hl_cut_count])


def main_hr():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_hr_cut, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_hr)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_hr_cut(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningHrCut(game=game, heuristic=heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruningHrCut(game=game, heuristic=heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_hr_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hr_cut max_depth={setup[1]} k={setup[2]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated Hr      (agent 1 WHITHE): {agent1.search_algorithm.eval_hr_cut_count}")
    print(f"Pruning Hr carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_hr_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print(f"States evaluated Hr      (agent 2 BLACK): {agent2.search_algorithm.eval_hr_cut_count}")
    print(f"Pruning Hr carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_hr_cut_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_hr_cut_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff Hr Agent 1', 'Max Depth Agent 2', 'Number CutOff Hr Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated Hr Agent 1', 'States evaluated Hr Agent 2', 'Pruning Hr carried out Agent 1',
                  'Pruning Hr carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_hr_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hr_cut max_depth={setup[1]} k={setup[3]}',
            'MinMax Alpha Beta Pruning Hr CutOff', 'MinMax Alpha Beta Pruning Hr CutOff',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[1], setup[2], outcome_val, game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_hr_cut_count,
            agent2.search_algorithm.eval_hr_cut_count, agent1.search_algorithm.prune_hr_cut_count,
            agent2.search_algorithm.prune_hr_cut_count])


def main_h0_vs_hr():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_h0_vs_hr_cut, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_h0_vs_hr)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_h0_vs_hr_cut(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    cutoff_heuristic = SoftBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningH0Cut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruningHrCut(game=game, heuristic=heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hr_cut max_depth={setup[1]} k={setup[2]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A2 in: {time_avg_a2:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 1 WHITHE): {agent1.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_h0_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print(f"States evaluated HR      (agent 2 BLACK): {agent2.search_algorithm.eval_hr_cut_count}")
    print(f"Pruning HR carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_hr_cut_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_h0_vs_hr_cut_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff Agent 1', 'Max Depth Agent 2',
                  'Number CutOff Agent 2', 'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated H0 Agent 1', 'States evaluated Hr Agent 2', 'Pruning H0 carried out Agent 1',
                  'Pruning Hr carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hr_cut max_depth={setup[1]} k={setup[2]} ',
            'MinMax Alpha Beta Pruning H0 CutOff', 'MinMax Alpha Beta Pruning Hr CutOff',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[1], setup[2], outcome_val,
            game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_h0_cut_count,
            agent2.search_algorithm.eval_hr_cut_count, agent1.search_algorithm.prune_h0_cut_count,
            agent2.search_algorithm.prune_hr_cut_count])


def main_hr_vs_hl():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_hr_vs_hl_cut, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_hl_vs_hr)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_hr_vs_hl_cut(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    cutoff_heuristic = SoftBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningHrCut(game=game, heuristic=heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruningHlCut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[2], l=setup[3],
                                                      max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_hr_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[2]} l={setup[3]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated Hr      (agent 1 WHITHE): {agent1.search_algorithm.eval_hr_cut_count}")
    print(f"Pruning Hr carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_hr_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 2 BLACK): {agent2.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_h0_cut_count}")
    print(f"States evaluated Hl      (agent 2 BLACK): {agent2.search_algorithm.eval_hl_cut_count}")
    print(f"Pruning Hl carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_hl_cut_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_hr_vs_hl_cut_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff Agent 1', 'Max Depth Agent 2',
                  'Number CutOff Agent 2', 'Number of l Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated Hr Agent 1', 'States evaluated H0 Agent 2', 'Pruning Hr carried out Agent 1',
                  'Pruning H0 carried out Agent 2', 'States evaluated Hl Agent 2', 'Pruning Hl carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_hr_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[2]} l={setup[3]}',
            'MinMax Alpha Beta Pruning Hr CutOff', 'MinMax Alpha Beta Pruning Hl CutOff',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[1], setup[3], setup[4], outcome_val,
            game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_hr_cut_count,
            agent2.search_algorithm.eval_h0_cut_count, agent1.search_algorithm.prune_hr_cut_count,
            agent2.search_algorithm.prune_h0_cut_count,
            agent2.search_algorithm.eval_hl_cut_count,
            agent2.search_algorithm.prune_hl_cut_count])


def main_h0_vs_normal():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_h0_vs_normal, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_h0_vs_normal)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_h0_vs_normal(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    cutoff_heuristic = SoftBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningH0Cut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic, max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning max_depth={setup[1]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 1 WHITHE): {agent1.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_h0_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_h0_vs_normal_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff Agent 1', 'Max Depth Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated H0 Agent 1', 'Pruning H0 carried out Agent 1']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_h0_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning max_depth={setup[1]}',
            'MinMax Alpha Beta Pruning H0 CutOff', 'MinMax Alpha Beta Pruning',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[1], outcome_val,
            game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_h0_cut_count,
            agent1.search_algorithm.prune_h0_cut_count])


def main_normal_vs_hl():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_vs_hl_cut, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_vs_hl)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_vs_hl_cut(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    cutoff_heuristic = SoftBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic,
                                                 max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruningHlCut(game=game, heuristic=heuristic, h0_cut=cutoff_heuristic,
                                                      k=setup[2], l=setup[3],
                                                      max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning max_depth={setup[0]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[2]} l={setup[3]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print(f"States evaluated H0      (agent 2 BLACK): {agent2.search_algorithm.eval_h0_cut_count}")
    print(f"Pruning H0 carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_h0_cut_count}")
    print(f"States evaluated Hl      (agent 2 BLACK): {agent2.search_algorithm.eval_hl_cut_count}")
    print(f"Pruning Hl carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_hl_cut_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_vs_hl_cut_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Max Depth Agent 2',
                  'Number CutOff Agent 2', 'Number of l Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated H0 Agent 2',
                  'Pruning H0 carried out Agent 2', 'States evaluated Hl Agent 2', 'Pruning Hl carried out Agent 2']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning max_depth={setup[0]} vs min_max_alpha_beta_pruning_hl_cut max_depth={setup[1]} k={setup[2]} l={setup[3]}',
            'MinMax Alpha Beta Pruning', 'MinMax Alpha Beta Pruning Hl CutOff',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[1], setup[3], setup[4], outcome_val,
            game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count,
            agent2.search_algorithm.eval_h0_cut_count,
            agent2.search_algorithm.prune_h0_cut_count,
            agent2.search_algorithm.eval_hl_cut_count,
            agent2.search_algorithm.prune_hl_cut_count])


def main_hr_vs_normal():
    number_of_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(run_min_max_alpha_beta_pruning_hr_vs_normal, setup, index)
            for index, setup in enumerate(min_max_alpha_beta_pruning_hr_vs_normal)]

        # Aspetta che tutte le esecuzioni siano completate (opzionale, a seconda del tuo caso d'uso)
        for future in futures:
            future.result()


def run_min_max_alpha_beta_pruning_hr_vs_normal(setup, index):
    i = index + 1
    game = ChessGame()
    heuristic = HardBoardEvaluationChessGame()
    state = StateChessGame(game_board=game.game_board)
    search_algorithm_a1 = MinMaxAlphaBetaPruningHrCut(game=game, heuristic=heuristic,
                                                      k=setup[2],
                                                      max_depth=setup[0])
    search_algorithm_a2 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic, max_depth=setup[1])
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 0
    move_agent_2 = 0
    time_a1 = 0
    time_a2 = 0
    start_time = time.time()
    print(
        f"The game of chess begins!\n min_max_alpha_beta_pruning_hr_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning max_depth={setup[1]}")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            start_time_a2 = time.time()
            state = agent2.do_action(state)
            end_time_a2 = time.time()
            time_a2 += (end_time_a2 - start_time_a2) * 1000
            move_agent_2 += 1
        else:
            start_time_a1 = time.time()
            state = agent1.do_action(state)
            end_time_a1 = time.time()
            time_a1 += (end_time_a1 - start_time_a1) * 1000
            move_agent_1 += 1
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    time_total = (end_time - start_time) * 1000
    print(f"Result in: {time_total:.2f}ms")
    time_avg_a1 = time_a1 / move_agent_1
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    time_avg_a2 = time_a2 / move_agent_2
    print(f"Result time avg A1 in: {time_avg_a1:.2f}ms")
    outcome_val = state.game_board.outcome().termination.name
    print(
        f"OUTCOME: {outcome_val}")
    game_win = game.get_name_winner_player(state.game_board)
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game_win}")
    print(f"Number of Moves          (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated         (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print(f"States evaluated Hr      (agent 1 WHITHE): {agent1.search_algorithm.eval_hr_cut_count}")
    print(f"Pruning Hr carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_hr_cut_count}")
    print()
    print(f"Number of Moves          (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated         (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out      (agent 2 BLACK): {agent2.search_algorithm.prune_count}")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    with open(f'../csv/min_max_alpha_beta_pruning_hr_vs_normal_games/games_{i}.csv', 'w', newline='',
              encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Title', 'Algorithm Agent 1', 'Algorithm Agent 2', 'Heuristic Agent 1', 'Heuristic Agent 2',
                  'Max Depth Agent 1', 'Number CutOff Agent 1', 'Max Depth Agent 2',
                  'OUTCOME', 'Winner', 'Total Time', 'AVG Time Agent 1',
                  'AVG Time Agent 2',
                  'Number of Moves Agent 1', 'Number of Moves Agent 2', 'States Evaluated Agent 1',
                  'States Evaluated Agent 2', 'Pruning carried out Agent 1', 'Pruning carried out Agent 2',
                  'States evaluated Hr Agent 1', 'Pruning Hr carried out Agent 1']
        writer.writerow(header)
        writer.writerow([
            f'min_max_alpha_beta_pruning_hr_cut max_depth={setup[0]} k={setup[2]} vs min_max_alpha_beta_pruning max_depth={setup[1]}',
            'MinMax Alpha Beta Pruning Hr CutOff', 'MinMax Alpha Beta Pruning',
            'HardBoardEvaluationChessGame',
            'HardBoardEvaluationChessGame', setup[0], setup[2], setup[1], outcome_val,
            game_win,
            f'{time_total:.2f}ms',
            f'{time_avg_a1:.2f}ms', f'{time_avg_a2:.2f}ms', move_agent_1, move_agent_2,
            agent1.search_algorithm.eval_count, agent2.search_algorithm.eval_count,
            agent1.search_algorithm.prune_count,
            agent2.search_algorithm.prune_count, agent1.search_algorithm.eval_hr_cut_count,
            agent1.search_algorithm.prune_hr_cut_count])


if __name__ == '__main__':
    # main_normal()
    # main_h0()
    # main_hl()
    main_h0_vs_hl()
    main_hr()
    main_h0_vs_hr()
    main_hr_vs_hl()
    main_h0_vs_normal()
    main_normal_vs_hl()
    main_hr_vs_normal()
