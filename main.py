import time

from Agent import Agent
from ChessGame import ChessGame
from StateChessGame import StateChessGame
from algorithms import MinMax, MinMaxAlphaBetaPruning
from heuristics import BoardEvaluationChessGame, ChessHeuristics


def backpath(node):
    states = [node]
    parent = node.state_parent
    while parent is not None:
        states += [parent]
        parent = parent.state_parent
    return reversed(states)


def main_chess_game():
    w = 0
    b = 0
    p = 0
    game = ChessGame()
    heuristic_a1 = BoardEvaluationChessGame()
    heuristic_a2 = ChessHeuristics()
    search_algorithm_a1 = MinMax(game=game, heuristic=heuristic_a2, max_depth=2)
    search_algorithm_a2 = MinMax(game=game, heuristic=heuristic_a2, max_depth=2)
    search_algorithm_a3 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a1, max_depth=3)
    search_algorithm_a4 = MinMaxAlphaBetaPruning(game=game, heuristic=heuristic_a1, max_depth=3)
    state = StateChessGame()
    agent1 = Agent(search_algorithm_a1, state)
    agent2 = Agent(search_algorithm_a2, state)
    agent3 = Agent(search_algorithm_a3, state)
    agent4 = Agent(search_algorithm_a4, state)
    turn_agent = 0
    start_time = time.time()
    print("Inizio del gioco degli scacchi!")
    while not state.is_endgame():
        if turn_agent % 2:
            state = agent4.do_action(state)
            print("Agente 2 ha giocato la mossa:", state.move)
        else:
            state = agent3.do_action(state)
            print("Agente 1 ha giocato la mossa:", state.move)
        turn_agent = turn_agent + 1
        if state is None:
            print("L'agente non è riuscito a risolvere il problema")
            return
    end_time = time.time()
    print(f"Risultato in: {(end_time - start_time) * 1000:.2f}ms")

    # for s in backpath(state):
    #   print(game.print_board(s))
    #   print(s.move)
    #   print(f"h(n) = {s.h}")
    #   print(f"g(n) = {s.g}")
    #   print(f"f(n) = {s.f}")
    print(f"è scacco matto? {state.is_victory()}")
    print(f"chi ha vinto? {state.game_representation.get_name_winner_player()}")
    print(f"patta? {state.game_representation.is_draw()}")
    print(f"Stati valutati        (agente 1): {agent3.search_algorithm.eval_count}")
    print(f"Potature effettuate   (agente 1): {agent3.search_algorithm.prune_count}")
    print()
    print(f"Stati valutati        (agente 2): {agent4.search_algorithm.eval_count}")
    print(f"Potature effettuate   (agente 2): {agent4.search_algorithm.prune_count}")
    if state.game_representation.get_name_winner_player() == "White":
        w += 1
    elif state.game_representation.get_name_winner_player() == "Black":
        b += 1
    else:
        p += 1

    print(f"W: {w} B: {b} P: {p}")


if __name__ == '__main__':
    main_fifteen_puzzle_game()
    # main_chess_game()
