import time

from optimized.Agent import Agent
from optimized.FifteenPuzzleGame import FifteenPuzzleGame
from optimized.State import State
from optimized.algorithms.AStar import AStar
from optimized.heuristics.ManhattanDistancePuzzleGame import ManhattanDistancePuzzleGame


def backpath(node):
    states = [node]
    parent = node.parent_state
    while parent is not None:
        states.append(parent)
        parent = parent.parent_state
    return reversed(states)


def main():
    # Initialize the game
    game = FifteenPuzzleGame()

    # Define the heuristic
    heuristic = ManhattanDistancePuzzleGame(game.game_board_end_game)

    # Define the search algorithm
    search_algorithm = AStar(game, heuristic)

    # Define the initial state
    state = State(game.game_board)

    # Initialize the agent
    agent = Agent(search_algorithm, state)

    start_time = time.time()
    while not game.is_end_game(state.game_board):
        state = agent.do_action(state)

        if state is None:
            print("L'agente non è riuscito a risolvere il problema")
            return

    end_time = time.time()
    print(f"Risultato in: {(end_time - start_time) * 1000:.2f}ms")

    for s in backpath(state):
        print(s)
        print(s.move)
        print(f"h(n) = {s.h}")
        print(f"g(n) = {s.g}")
        print(f"f(n) = {s.f}")

    print(f"HORIZON: {len(search_algorithm.horizon)}")
    print(f"VISITED: {len(search_algorithm.visited)}")


if __name__ == '__main__':
    main()
