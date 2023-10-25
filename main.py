import time

from Agent import Agent
from FifteenPuzzleGame import FifteenPuzzleGame
from State import State
from algorithms import AStar
from heuristics import ManhattanDistancePuzzleGame


def backpath(node):
    states = [node]
    parent = node.parent_state
    while parent is not None:
        states += [parent]
        parent = parent.parent_state
    return reversed(states)


def main():
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


if __name__ == '__main__':
    main()
