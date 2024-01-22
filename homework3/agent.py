from typing import Callable

import numpy as np

from world import World


class Agent:
    def __init__(self, policy_function: Callable, discount_factor=0.5, starting_state_index=19, world=None):
        if world is not None:
            self.env_representation: world
        else:
            self.env_representation = World()
        self.discount_factor = discount_factor
        self.starting_state = self.env_representation.state_dict[starting_state_index]
        self.actions = self.env_representation.A
        self.actions_number_dict = {action.number: action for action in self.actions}
        self.policy_function = policy_function
        self.policy = self.__generate_policy()
        self.easy_policy = self.get_easy_policy()
        self.states = [self.starting_state]
        self.state_dic = {state.number: state for state in self.states}
        self.current_state = self.states[0]
        self.env_representation.starting_state = self.starting_state

    def __generate_policy(self):
        policy = {}
        for action in self.actions:
            policy[(self.starting_state.number, action.name)] = 1 if action.number == self.policy_function(
                self.starting_state) else 0
        return policy

    def get_easy_policy(self):
        pol = {}
        for k, v in self.policy.items():
            if v != 0:
                pol[k[0]] = k[1]
        return pol

    def step(self):
        action_probabilities = [self.policy[(self.current_state.number, action.name)] for action in self.actions]
        action = np.random.choice(list(self.actions), p=action_probabilities)
        return action

    def reset_state(self):
        self.current_state = self.starting_state

    def generate_episode(self, length: int, return_actions=False, first_state=None, first_action=None,
                         random_first_state=False):
        next_state = self.starting_state if first_state == None else first_state
        if random_first_state:
            while True:
                next_state = np.random.choice(self.states)
                if 0 <= next_state.number <= 32:
                    break
        actions = []
        episode = [next_state.number]

        if first_action != None:
            actions.append(first_action)
            next_state = first_action.function(next_state)
            episode.append(next_state.number)

        while len(episode) < length:
            if next_state.number not in [s.number for s in self.states]:
                self.states.append(next_state)
                for action in self.actions:
                    self.policy[(next_state.number, action.name)] = 0
                self.policy[(next_state.number, self.actions_number_dict[self.policy_function(next_state)].name)] = 1

            action_probabilities = [self.policy[(next_state.number, action.name)] for action in self.actions]
            action = np.random.choice(list(self.actions), p=action_probabilities)
            actions.append(action)
            next_state = action.function(next_state)
            episode.append(next_state.number)

            if next_state.number == 62 and action.number == 7:
                break

        actions.append(self.step())
        self.reset_state()

        state_action = []
        for i in range(len(episode)):
            state_action.append({'s': episode[i], 'a': actions[i]})

        return episode if not return_actions else state_action

    def __get_state_action_from_episodes(self, episodes):
        episode_state = []
        action_state = []
        for e in episodes:
            episode_state.append(e['s'])
            action_state.append(e['a'])
        return (episode_state, action_state)

    def change_policy(self, new_policy: dict):
        self.policy = new_policy
        self.easy_policy = self.get_easy_policy()

    def compute_returns(self, episode: list, index: int):
        if index == None:
            return 0
        episode = episode[index:]
        sum_returns = 0
        for i in range(0, len(episode)):
            state = self.env_representation.state_dict[episode[i]['s']]
            sum_returns += self.env_representation.R[
                               episode[i]['s'], episode[i]['a'].number, episode[i]['a'].function(state).number] * (
                                   self.discount_factor ** i)

        return sum_returns

    def improve_policy(self, iteration:int):
        n = {(state.number, action.name): 0 for state in self.states for action in self.actions}
        g = {(state.number, action.name): 0 for state in self.states for action in self.actions}
        q = {(state.number, action.name): 0 for state in self.states for action in self.actions}
        known_states = [state.number for state in self.states]

        for i in range(iteration):
            print(f"Iterazione: {i}/{iteration}")
            for state in self.states:
                for action in self.actions:
                    epi = self.generate_episode(100, return_actions=True, first_state=state,
                                                first_action=action)
                    episode, actions = self.__get_state_action_from_episodes(epi)
                    self.reset_state()

                    # check if all states are known
                    for state_no in episode:
                        if state_no not in known_states:
                            known_states.append(state_no)
                            for action in self.actions:
                                n[(state_no, action.name)] = 0
                                g[(state_no, action.name)] = 0
                                q[(state_no, action.name)] = 0

                    ## COMPUTATION OF Q-VALUES
                    for j in range(len(episode)):
                        n[(episode[j], actions[j].name)] += 1
                        g[(episode[j], actions[j].name)] += self.compute_returns(epi, j)
                        q[(episode[j], actions[j].name)] = g[(episode[j], actions[j].name)] / n[
                            (episode[j], actions[j].name)]
        print(q)
        ## POLICY IMPROVEMENT
        for state_no, ac in q.keys():
            if state_no not in [s.number for s in self.states]:
                self.states.append(self.env_representation.state_dict[state_no])

            max_action = None
            max_value = -np.inf
            for action in self.actions:
                if q[(state_no, action.name)] > max_value:
                    max_value = q[(state_no, action.name)]
                    max_action = action.name

            new_policy = self.policy.copy()
            for action in self.actions:
                new_policy[(state_no, action.name)] = 1 if action.name == max_action else 0

            self.change_policy(new_policy)
        return self.policy

    def __needs_extra_space(tuple_value):
        return tuple_value[1] == 4
    def print_policy(self, policy: np.ndarray = None):
        # Generate the rows in a more concise way using slicing and a loop
        rows = [list(range(i, i + 8)) for i in range(56, -1, -8)]

        for row in rows:
            for i in row:
                print(f" {self.env_representation.action_dict[policy[self.env_representation.S[i].number]].ascii} ", end="")
                if Agent.__needs_extra_space(self.env_representation.S[i].position):
                    print("    ", end="")

            # Simplify the condition for adding extra newlines
            print("\n\n" if row == rows[3] else "")
        print()
