import numpy as np


class MinMax:
    def __init__(self, game, heuristic, max_depth):
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
    def pick(self, states, parent_turn):
        if parent_turn:
            return max(states, key=lambda state: state.H)
        else:
            return min(states, key=lambda state: state.H)

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
                state.H = 0.0
            else:
                # se non viene chiesto un pareggio, proseguiamo normalmente
                # con la valutazione
                state.H = self.__minmax(state, self.max_depth - 1, not parent_turn)

    # implementazione della valutazione MinMax
    def __minmax(self, state, depth, turn):
        self.eval_count += 1

        if depth == 0 or state.is_endgame():
            return self.heuristic.H(state)

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
    def search(self, state: TurnBasedState):
        children = self.__neighbors(state)

        self.evaluate(children, state.turn())

        return self.pick(children, state.turn())
