import time

from Agent import Agent
from ChessGame import ChessGame
from FifteenPuzzleGame import FifteenPuzzleGame
from State import State
from algorithms import AStar, MinMax, MinMaxAlphaBetaPruning
from heuristics import ManhattanDistancePuzzleGame, BoardEvaluationChessGame, LastMoveChessGame, HChessGame


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
    w = 0
    b = 0
    p = 0
    for n in range(1):
        print(f"iterazione N {n}")
        game = ChessGame()
        heuristic_a1 = BoardEvaluationChessGame()
        heuristic_a2 = LastMoveChessGame()
        heuristic_a3 = HChessGame()
        search_algorithm_a1 = MinMax(game=game, heuristic=heuristic_a1, max_depth=1)
        search_algorithm_a2 = MinMax(game=game, heuristic=heuristic_a1, max_depth=4)
        search_algorithm_a3 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a3, max_depth=1)
        search_algorithm_a4 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a3, max_depth=1)
        state = State(game.game_board)
        agent1 = Agent(search_algorithm_a1, state)
        agent2 = Agent(search_algorithm_a2, state)
        agent3 = Agent(search_algorithm_a2, state)
        agent4 = Agent(search_algorithm_a2, state)
        turn_agent = 0
        start_time = time.time()
        print("Inizio del gioco degli scacchi!")
        while not game.is_endgame(state.game_board):
            if turn_agent % 2:
                if n > 25:
                    state = agent1.do_action(state)
                else:
                    state = agent2.do_action(state)
                    print("Agente 2 ha giocato la mossa:", state.move)
            else:
                if n > 25:
                    state = agent2.do_action(state)
                else:
                    state = agent1.do_action(state)
                    print("Agente 1 ha giocato la mossa:", state.move)
            turn_agent = turn_agent + 1
            if state is None:
                # print("L'agente non è riuscito a risolvere il problema")
                return
        end_time = time.time()
        print(f"Risultato in: {(end_time - start_time) * 1000:.2f}ms")

        # for s in backpath(state):
        #   print(game.print_board(s))
        #   print(s.move)
        #   print(f"h(n) = {s.h}")
        #   print(f"g(n) = {s.g}")
        #   print(f"f(n) = {s.f}")
        print(f"è scacco matto? {game.is_victory(state.game_board)}")
        print(f"chi ha vinto? {game.is_fist_player_turn(state.game_board)}")
        print(f"patta? {game.is_pareggio(state.game_board)}")
        if game.is_fist_player_turn(state.game_board) == "White":
            w += 1
        elif game.is_fist_player_turn(state.game_board) == "Black":
            b += 1
        else:
            p += 1
    print(f"W: {w} B: {b} P: {p}")


if __name__ == '__main__':
    # main_fifteen_puzzle_game()
    main_chess_game()
