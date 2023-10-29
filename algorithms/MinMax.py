import numpy as np

from State import State


class MinMax:
    def __init__(self, game, heuristic, max_depth=1):
        self.game = game
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.prune_count = 0
        self.eval_count = 0

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
            if state.can_claim_draw():
                state.h = 0.0
            else:
                # se non viene chiesto un pareggio, proseguiamo normalmente
                # con la valutazione
                state.h = self.__minmax(state, self.max_depth - 1, not parent_turn)

    # implementazione della valutazione MinMax
    def __minmax(self, state, depth, turn):
        self.eval_count += 1
        neighbors = self.game.neighbors(state)

        if depth == 0 or self.game.is_endgame(state.game_board):
            return self.heuristic.h(state)

        if turn:
            value = -np.inf
            for child in neighbors:
                value = max(value, self.__minmax(child, depth - 1, False))
            return value
        else:
            value = np.inf
            for child in neighbors:
                value = min(value, self.__minmax(child, depth - 1, True))
            return value

    # metodo che esegue la ricerca del prossimo stato migliore
    # a partire dallo stato `state`
    def search(self, state):
        neighbors = self.game.neighbors(state)
        self.evaluate(neighbors, state.turn())
        return self.pick(neighbors, state.turn())
