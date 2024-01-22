import numpy as np
import pandas as pd

from action import Action
from state import State


class World:
    def __init__(self):
        self.S = self.__build_states()
        self.state_dict = {state.number: state for state in self.S}
        self.state_position_dict = {state.position: state for state in self.S}
        self.starting_state = np.random.choice(self.S[:32])
        self.current_state = self.starting_state
        self.am = self.__build_action_mapping()
        self.A = self.__build_actions()
        self.action_dict = {action.name: action for action in self.A}
        self.P = self.__generate_transitions()
        self.R = self.__generate_rewards()

    def __build_states(self):
        states = []
        count = 0
        for i in range(1, 9):
            for j in [x for x in range(1, 10) if x != 5]:
                states.append(State(count, (i, j)))
                count += 1
        return states

    def __needs_extra_space(tuple_value):
        return tuple_value[1] == 4

    def print_states(self, dict_view=False):
        # Generate the rows in a more concise way using slicing and a loop
        rows = [list(range(i, i + 8)) for i in range(56, -1, -8)]

        for row in rows:
            for i in row:
                if dict_view:
                    print(f" {self.S[i].position} ", end="")
                    if World.__needs_extra_space(self.S[i].position):
                        print("    ", end="")
                else:
                    print(f" {self.S[i].number:<2} ", end="")
                    if World.__needs_extra_space(self.S[i].position):
                        print("    ", end="")

            # Simplify the condition for adding extra newlines
            print("\n\n" if row == rows[3] else "")
        print()

    def action_left(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 0 in self.am[s.number]:
            title = (state.position[0], state.position[1] - 1)
        return self.state_position_dict[title]

    def action_right(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 1 in self.am[s.number]:
            title = (state.position[0], state.position[1] + 1)
        return self.state_position_dict[title]

    def action_up(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 2 in self.am[s.number]:
            title = (state.position[0] + 1, state.position[1])
        return self.state_position_dict[title]

    def action_down(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 3 in self.am[s.number]:
            title = (state.position[0] - 1, state.position[1])
        return self.state_position_dict[title]

    def action_take_whiskr(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 4 in self.am[s.number]:
            if s.number == 16:
                title = self.state_dict[48].position
            elif s.number == 22:
                title = self.state_dict[54].position
        return self.state_position_dict[title]

    def action_go_right(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 5 in self.am[s.number]:
            if s.number == 11:
                title = self.state_dict[23].position
            elif s.number == 43:
                title = self.state_dict[55].position
        return self.state_position_dict[title]

    def action_go_left(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 6 in self.am[s.number]:
            if s.number == 23:
                title = self.state_dict[11].position
            elif s.number == 55:
                title = self.state_dict[43].position
        return self.state_position_dict[title]

    def action_cook(self, s: State):
        state = self.state_dict[s.number]
        if state is None:
            raise RuntimeError("Non trovato")
        title = state.position
        if 7 in self.am[s.number]:
            title = state.position
        return self.state_position_dict[title]

    def __build_actions(self):
        actions = [Action('left', 0, self.action_left, '←'),
                   Action('right', 1, self.action_right, '→'),
                   Action('up', 2, self.action_up, '↑'),
                   Action('down', 3, self.action_down, '↓'),
                   Action('take_whiskr', 4, self.action_take_whiskr, 'T'),
                   Action('go_right', 5, self.action_go_right, 'R'),
                   Action('go_left', 6, self.action_go_left, 'L'),
                   Action('cook', 7, self.action_cook, 'C')]
        return actions

    def __build_action_mapping(self):
        states_actions_mapping = {
            0: [1],
            1: [0, 1],
            2: [0, 1],
            3: [0, 2],
            4: [1, 2],
            5: [0, 1, 2],
            6: [0, 1],
            7: [0, 2],
            8: [1, 2],
            9: [0, 1],
            10: [0, 1],
            11: [0, 2, 3, 5],
            12: [1, 2, 3],
            13: [0, 2, 3],
            14: [1, 2],
            15: [0, 2, 3],
            16: [3, 4],
            17: [1, 2],
            18: [0, 1, 2],
            19: [0, 2, 3],
            20: [1, 2, 3],
            21: [0, 2, 3],
            22: [1, 3, 4],
            23: [0, 3, 6],
            24: [1],
            25: [0, 1, 3],
            26: [0, 1, 3],
            27: [0, 3],
            28: [1, 3],
            29: [0, 1, 3],
            30: [0, 1],
            31: [0],

            32: [1],
            33: [0, 1],
            34: [0, 1],
            35: [0, 2],
            36: [1, 2],
            37: [0, 1, 2],
            38: [0, 1],
            39: [0, 2],
            40: [1, 2],
            41: [0, 1],
            42: [0, 1],
            43: [0, 2, 3, 5],
            44: [1, 2, 3],
            45: [0, 2, 3],
            46: [1, 2],
            47: [0, 2, 3],
            48: [3],
            49: [1, 2],
            50: [0, 1, 2],
            51: [0, 2, 3],
            52: [1, 2, 3],
            53: [0, 2, 3],
            54: [1, 3],
            55: [0, 3, 6],
            56: [1, 7],
            57: [0, 1, 3],
            58: [0, 1, 3],
            59: [0, 3],
            60: [1, 3],
            61: [0, 1, 3],
            62: [0, 1, 7],
            63: [0]
        }
        return states_actions_mapping

    def __get_possible_actions_from_state(self, s: int, mapping: np.ndarray):
        actions = []
        for a in self.A:
            if mapping[s, a.number] > 0.0:
                actions.append(a)
        return actions

    def __convert_to_numpy_array(self, mapping: dict, s: np.ndarray, a: np.ndarray):
        count = 0
        for i in sorted(list(mapping.keys())):
            if i != count:
                raise RuntimeError("Struttura non valida")
            count += 1
        array = np.zeros(shape=(len(s), len(a)), dtype=np.float64)
        for s, actions in mapping.items():
            prob = 1 / len(actions)
            for a in actions:
                array[s, a] = prob
        return array

    def __convert_s_a_mapping_to_numpy_arrays(self):
        s = np.array(list(self.state_dict.keys()), dtype=np.int64)
        a = np.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=np.int64)
        mapping = self.__convert_to_numpy_array(self.am, s, a)
        return s, a, mapping

    def __generate_transitions(self):
        s,  a, mapping = self.__convert_s_a_mapping_to_numpy_arrays()

        transitions = np.zeros(
            shape=(len(self.A), len(self.S), len(self.S)), dtype=np.float64
        )

        for state in self.S:
            for action in self.__get_possible_actions_from_state(state.number, mapping):
                if mapping[state.number, action.number] > 0.0:
                    # l'azione `action` è possibile dallo stato `state`
                    # non ci sono effetti imprevisti, c'è solo uno stato destinazione
                    # raggiungibile con probabilità 1
                    transitions[action.number, state.number, action.function(state).number] = 1

        return transitions

    def __get_number_action(self, action: str):
        if action in self.action_dict.keys():
            return self.action_dict[action].number
        else:
            raise ValueError("Azione Non trovata")

    def print_transitions_matrix(self, action=None):
        df = pd.DataFrame(self.P[self.__get_number_action(action)])

        df["Stati"] = df.index
        df["Stati"] = "s" + df["Stati"].astype(str)
        df.set_index("Stati", inplace=True)
        df.rename(columns=lambda x: f"s{x}", inplace=True)

        return df

    def __get_probs(self, mapping: np.ndarray, a: int, s: int):
        return mapping[s, a]

    def __generate_rewards(self):
        s, a, mapping = self.__convert_s_a_mapping_to_numpy_arrays()
        rewards = np.zeros(shape=(len(self.S), len(self.A), len(self.S)), dtype=np.float64)
        rewards[62, self.__get_number_action('cook'), 62] = 100
        rewards[56, self.__get_number_action('cook'), 56] = -1

        rewards[16, self.__get_number_action('take_whiskr'), 48] = 50
        rewards[22, self.__get_number_action('take_whiskr'), 54] = 50

        for s in self.S:
            for a in self.A:
                # settiamo il reward a -1 se l'azione `a` non è valida
                # nello stato `s`
                # (ovvero quando non è possibile eseguire l'azione
                # `a` dallo stato `s`)
                if self.__get_probs(mapping, a.number, s.number) == 0.0:
                    rewards[s.number, a.number, s.number] = -1
        return rewards
