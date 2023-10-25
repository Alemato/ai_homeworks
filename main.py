import time

from Agent import Agent
from ChessGame import ChessGame
from FifteenPuzzleGame import FifteenPuzzleGame
from State import State
from algorithms import AStar, MinMax
from heuristics import ManhattanDistancePuzzleGame, BoardEvaluationChessGame, LastMoveChessGame


def backpath(node):
    states = [node]
    parent = node.parent_state
    while parent is not None:
        states += [parent]
        parent = parent.parent_state
    return reversed(states)


def main_fifteen_puzzle_game():
    game = FifteenPuzzleGame()
    heuristics = ManhattanDistancePuzzleGame(game.game_board_end_game)
    search_algorithm = AStar(game, heuristics)
    state = State(game.game_board)
    agent = Agent(search_algorithm, state)

    start_time = time.time()
    while not game.is_end_game(state.game_board):
        state = agent.do_action(state)

        if state is None:
            print("L'agente non è riuscito a risolvere il problema")
            return
    end_time = time.time()
    print(f"Risultato in : {(end_time - start_time) * 1000}ms")
    for s in backpath(state):
        print(game.print_board(s))
        print(s.move)
        print(f"h(n) = {s.h}")
        print(f"g(n) = {s.g}")
        print(f"f(n) = {s.f}")

    print(f"HORIZON: {len(search_algorithm.horizon)}")
    print(f"VISITED: {len(search_algorithm.visited)}")


def main_chess_game():
    game = ChessGame()
    heuristic_a1 = BoardEvaluationChessGame()
    heuristic_a2 = LastMoveChessGame()
    search_algorithm_a1 = MinMax(game=game, heuristic=heuristic_a2, max_depth=2)
    search_algorithm_a2 = MinMax(game=game, heuristic=heuristic_a2, max_depth=1)
    state = State(game.game_board)
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    turn_agent = 0
    start_time = time.time()
    while not game.is_endgame(state.game_board):
        if turn_agent % 2:
            state = agent1.do_action(state)
        else:
            state = agent2.do_action(state)
        turn_agent = turn_agent + 1
        if state is None:
            print("L'agente non è riuscito a risolvere il problema")
            return
    end_time = time.time()
    print(f"Risultato in: {(end_time - start_time) * 1000:.2f}ms")

    for s in backpath(state):
        print(game.print_board(s))
        print(s.move)
        print(f"h(n) = {s.h}")
        print(f"g(n) = {s.g}")
        print(f"f(n) = {s.f}")
    print(f"è scacco matto? {game.is_victory(state.game_board)}")
    print(f"chi ha vinto? {game.is_fist_player_turn(state.game_board)}")
if __name__ == '__main__':
    # main_fifteen_puzzle_game()
    main_chess_game()
