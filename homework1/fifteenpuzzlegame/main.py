import time

from Agent import Agent
from FifteenPuzzleGame import FifteenPuzzleGame
from StateFifteenPuzzleGame import StateFifteenPuzzleGame
from algoritms.AStar import AStar
from algoritms.BestFirst import BestFirst
from heuristics.ManhattanDistancePuzzleGame import ManhattanDistancePuzzleGame
from heuristics.MisplacedTilesPuzzleGame import MisplacedTittlesPuzzleGame


def backpath(node):
    states = [node]
    parent = node.state_parent
    while parent is not None:
        states += [parent]
        parent = parent.state_parent
    return reversed(states)


def main_fifteen_puzzle_game():
    state = StateFifteenPuzzleGame()
    heuristics = ManhattanDistancePuzzleGame(state.game_representation.end_game_board)
    heuristics1 = MisplacedTittlesPuzzleGame(state.game_representation.end_game_board)
    run_agent("BestFirst", "ManhattanDistance", BestFirst(FifteenPuzzleGame(), heuristics), StateFifteenPuzzleGame())
    run_agent("AStar", "ManhattanDistance", AStar(FifteenPuzzleGame(), heuristics), StateFifteenPuzzleGame())
    run_agent("BestFirst", "MisplacedTittles", BestFirst(FifteenPuzzleGame(), heuristics1), StateFifteenPuzzleGame())
    run_agent("AStar", "MisplacedTittles", AStar(FifteenPuzzleGame(), heuristics1), StateFifteenPuzzleGame())


def run_agent(search_algorithm_name, heuristics_name, search_algorithm, state):
    print(f"Run Agent with {search_algorithm_name} and {heuristics_name}")
    agent = Agent(search_algorithm, state)
    start_time = time.time()
    start_time_message = time.time()
    explored_states = 0
    if not state.game_representation.game_is_solvable():
        print("Not Solvable")
        return
    print("Solvable")

    while not state.is_end_game():
        state = agent.do_action(state)
        explored_states += 1
        if time.time() - start_time_message >= 1:
            print(f"Explored so far: {explored_states} in {time.time() - start_time:.0f}s")
            start_time_message = time.time()

        if state is None:
            print("The agent was unable to resolve the issue")
            return
    end_time = time.time()
    print(f"Result in : {(end_time - start_time) * 1000}ms")

    n = 0
    for s in backpath(state):
        s.print_board()
        n += 1
        if s.move is not None:
            print(f"The empty square was moved towards: {s.move}")
        print(f"h(n) = {s.h}")
        if search_algorithm_name == "AStar":
            print(f"g(n) = {s.g}")
            print(f"f(n) = {s.f}")
        print()
    print(f"Number of steps {n}")
    print(f"HORIZON: {len(search_algorithm.horizon)}")
    print(f"VISITED: {len(search_algorithm.explored)} \n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


if __name__ == '__main__':
    main_fifteen_puzzle_game()
