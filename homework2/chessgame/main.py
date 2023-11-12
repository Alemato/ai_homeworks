import time

from homework1.chessgame.Agent import Agent

from ChessGame import ChessGame
from StateChessGame import StateChessGame
from algoritms.MinMaxAlphaBetaPruning import MinMaxAlphaBetaPruning
from heuristics.HardBoardEvaluationChessGame import HardBoardEvaluationChessGame


def main_chess_game():
    game = ChessGame()
    heuristic_a1 = HardBoardEvaluationChessGame()
    search_algorithm_a1 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a1, max_depth=2)
    search_algorithm_a2 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a1, max_depth=2)
    state = StateChessGame()
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    move_agent_1 = 1
    move_agent_2 = 1
    start_time = time.time()
    print("The game of chess begins!")
    print(state.game_board)
    while not state.is_endgame():
        if turn_agent % 2:
            state = agent2.do_action(state)
            move_agent_2 += 1
            print(state.game_board)
            print("Agent 2 (BLACK) played the move:", state.move)
            print()
        else:
            state = agent1.do_action(state)
            move_agent_1 += 1
            print(state.game_board)
            print("Agent 1 (WHITE) played the move:", state.move)
            print()
        turn_agent = turn_agent + 1

        if state is None:
            print("The agent was unable to resolve the issue")
            return

    end_time = time.time()
    print(f"Result in: {(end_time - start_time) * 1000:.2f}ms")
    print(
        f"OUTCOME: {state.game_board.game_board.outcome().termination.name}")
    if state.game_board.get_name_winner_player() is not None:
        print(f"Player Win: {state.game_board.get_name_winner_player().upper()}")
    print(f"Number of Moves       (agent 1 WHITHE): {move_agent_1}")
    print(f"States evaluated      (agent 1 WHITHE): {agent1.search_algorithm.eval_count}")
    print(f"Pruning carried out   (agent 1 WHITHE): {agent1.search_algorithm.prune_count}")
    print()
    print(f"Number of Moves       (agent 2 BLACK): {move_agent_2}")
    print(f"States evaluated      (agent 2 BLACK): {agent2.search_algorithm.eval_count}")
    print(f"Pruning carried out   (agent 2 BLACK): {agent2.search_algorithm.prune_count}")


if __name__ == '__main__':
    main_chess_game()
