import time

from Agent import Agent
from ChessGame import ChessGame
from StateChessGame import StateChessGame
from algoritms.MinMaxAlphaBetaPruning import MinMaxAlphaBetaPruning
from algoritms.MinMaxAlphaBetaPruningH0Cut import MinMaxAlphaBetaPruningH0Cut
from algoritms.MinMaxAlphaBetaPruningHlCut import MinMaxAlphaBetaPruningHlCut
from heuristics.HardBoardEvaluationChessGame import HardBoardEvaluationChessGame
from heuristics.SoftBoardEvaluationChessGame import SoftBoardEvaluationChessGame


def main_chess_game():
    game = ChessGame()
    heuristic_a1 = HardBoardEvaluationChessGame()
    heuristic_a2 = SoftBoardEvaluationChessGame()
    # search_algorithm_a1 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a1, max_depth=1)
    # search_algorithm_a2 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a1, max_depth=4)
    # search_algorithm_a1 = MinMaxAlphaBetaPruningH0Cut(game=game, heuristic=heuristic_a1, h0_cut=heuristic_a2, k=5, max_depth=6)
    # search_algorithm_a2 = MinMaxAlphaBetaPruningH0Cut(game=game, heuristic=heuristic_a1, h0_cut=heuristic_a2, k=5, max_depth=6)
    search_algorithm_a1 = MinMaxAlphaBetaPruningHlCut(game=game, heuristic=heuristic_a1, h0_cut=heuristic_a2, k=5, max_depth=6)
    search_algorithm_a2 = MinMaxAlphaBetaPruningHlCut(game=game, heuristic=heuristic_a1, h0_cut=heuristic_a2, k=5, max_depth=6)
    state = StateChessGame()
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 1
    move_agent_2 = 1
    start_time = time.time()
    print("The game of chess begins!")
    print(state.game_board)
    while not state.game_board.is_game_over():
        if turn_agent % 2:
            state = agent2.do_action(state)
            move_agent_2 += 1
            #print(state.game_board.fen())
            print("Agent 2 (BLACK) played the move:", state.move)
            print()
        else:
            state = agent1.do_action(state)
            move_agent_1 += 1
            #print(state.game_board.fen())
            print("Agent 1 (WHITE) played the move:", state.move)
            print()
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return

    end_time = time.time()
    print(f"Result in: {(end_time - start_time) * 1000:.2f}ms")
    print(
        f"OUTCOME: {state.game_board.outcome().termination.name}")
    if game.get_name_winner_player(state.game_board) is not None:
        print(f"Player Win: {game.get_name_winner_player(state.game_board)}")
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
    print(f"States evaluated Hl      (agent 1 BLACK): {agent2.search_algorithm.eval_hl_cut_count}")
    print(f"Pruning Hl carried out   (agent 1 BLACK): {agent2.search_algorithm.prune_hl_cut_count}")


if __name__ == '__main__':
    main_chess_game()
