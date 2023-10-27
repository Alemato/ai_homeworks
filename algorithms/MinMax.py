import numpy as np

from State import State


class MinMax:
    def __init__(self, game, heuristic, max_depth=1):
        self.game = game
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.prune_count = 0
        self.eval_count = 0

    # metodo che calcola i neighbors dello stato `state`
    # passato come parametro
    def __neighbors(self, state):
        return self.game.neighbors(state)

    # metodo che estrae e ritorna dal set di stati `states`:
    # - lo stato con massimo punteggio H se il turno corrente è
    # del giocatore max
    #
    # - lo stato con minimo punteggio H se il turno corrente è
    # del giocatore min
    @staticmethod
    def pick(states, parent_turn):
        if parent_turn:
            return max(states, key=lambda state: state.h)
        else:
            return min(states, key=lambda state: state.h)

    # metodo che esegue la valutazione degli
    # stati `states` nel turno `parent_turn`
    # secondo la logica di valutazione
    # dell'algoritmo MinMax
    def evaluate(self, states, parent_turn):
        for state in states:
            # controllo se può essere chiesto un pareggio (can_claim_draw)
            # a questo livello dato che tale controllo potrebbe
            # essere molto dispendioso in termini di performance:
            # dalle esecuzioni effettuate, questo controllo ha permesso
            # di evitare sequenze di mosse ripetute nel gioco degli Scacchi
            # portando ad un miglioramento della qualità di gioco
            # (questo controllo è stato testato sul gioco degli Scacchi, ma
            # potrebbe portare beneficio su qualsiasi altro gioco)
            if self.game.ask_draw(state.game_board):
                state.h = 0.0
                state.f = state.h
            else:
                # se non viene chiesto un pareggio, proseguiamo normalmente
                # con la valutazione
                state.h = self.__minmax(state, self.max_depth - 1, not parent_turn)
                state.f = state.h

    # implementazione della valutazione MinMax
    def __minmax(self, state, depth, turn):
        self.eval_count += 1

        if depth == 0 or self.game.is_endgame(state.game_board):
            return self.heuristic.h(state)

        if turn:
            value = -np.inf
            for child in self.__neighbors(state):
                value = max(value, self.__minmax(child, depth - 1, False))
            return value
        else:
            value = np.inf
            for child in self.__neighbors(state):
                value = min(value, self.__minmax(child, depth - 1, True))
            return value

    # metodo che esegue la ricerca del prossimo stato migliore
    # a partire dallo stato `state`
    def search(self, state: State):
        children = self.__neighbors(state)

        self.evaluate(children, state.game_board.turn)
        print(state.game_board.turn)
        return self.pick(children, state.game_board.turn)
