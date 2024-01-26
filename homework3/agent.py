import random
from copy import deepcopy
from typing import Callable

import numpy as np

from world import World


class Agent:
    def __init__(self, policy_function: Callable, discount_factor=0.5, epsilon=0.1, starting_state_index=19,
                 world=None):
        if world is not None:
            self.env_representation: world
        else:
            self.env_representation = World()
        self.discount_factor = discount_factor
        self.epsilon = epsilon
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

    def compute_returns(self, episode: list, index: int, gamma: float):
        if index is None or index >= len(episode):
            return 0

        sum_returns = 0
        for i in range(len(episode) - index):
            state = self.env_representation.state_dict[episode[index + i]['s']]
            reward = self.env_representation.R[
                episode[index + i]['s'], episode[index + i]['a'].number, episode[index + i]['a'].function(state).number]
            sum_returns += reward * (gamma ** i)

        return sum_returns

    def improve_policy(self, iteration: int, gamma=None):
        if gamma is None:
            gamma = self.discount_factor
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
                        g[(episode[j], actions[j].name)] += self.compute_returns(epi, j, gamma)
                        q[(episode[j], actions[j].name)] = g[(episode[j], actions[j].name)] / n[
                            (episode[j], actions[j].name)]
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

    def __epsilon_greedy_policy(self, q: dict, epsilon: float):
        pi = {}
        for s in self.env_representation.S:
            pi[s.number] = np.random.choice(
                [self.__argmax(q, s.number), random.choice(self.actions).name],
                p=[1 - epsilon, epsilon])
        return pi

    def __argmax(self, q: dict, s: int):
        chiavi_filtrate = [chiave for chiave in q if chiave[0] == s]
        chiave_max = max(chiavi_filtrate, key=lambda k: q[k])
        return chiave_max[1]

    def __generate_episode_from_pi(self, pi: dict):
        episode = []
        for s, a in pi.items():
            episode.append({'s': s, 'a': self.env_representation.action_dict[a]})
        return episode

    def monte_carlo_online_control_on_policy_improvement(self, iterations: int, gamma=None):
        if gamma is None:
            gamma = self.discount_factor
        q = {(state.number, action.name): 0 for state in self.states for action in self.actions}
        n = {(state.number, action.name): 0 for state in self.states for action in self.actions}
        k = 1
        epsilon = 1 / k
        pi = self.__epsilon_greedy_policy(q, epsilon)

        while k <= iterations:
            state_visited = []
            episode = self.__generate_episode_from_pi(pi)
            q_k = deepcopy(q)
            g_k = 0
            for t in reversed(range(0, len(episode))):
                s_t = episode[t]['s']
                a_t = episode[t]['a']
                r_t = self.env_representation.R[
                    s_t, a_t.number, a_t.function(self.env_representation.state_dict[s_t]).number]
                g_k += (gamma ** t) * r_t
                if (s_t, a_t.name) not in state_visited:
                    n[s_t, a_t.name] += 1
                    q[s_t, a_t.name] = q_k[s_t, a_t.name] + (1 / n[s_t, a_t.name]) * (g_k - q_k[s_t, a_t.name])
                    state_visited.append((s_t, a_t.name))
            k += 1
            print(f"Iterazione: {k}/{iterations}")
            epsilon = 1 / k
            pi = self.__epsilon_greedy_policy(q, epsilon)

        # Policy Improvement
        new_policy = self.policy.copy()
        for state_no in self.states:
            for action in self.actions:
                new_policy[(state_no.number, action.name)] = 1 if action.name == pi[state_no.number] else 0

        self.change_policy(new_policy)
        return self.policy

    def __needs_extra_space(tuple_value):
        return tuple_value[1] == 4

    def print_policy(self, policy: np.ndarray = None):
        # Generate the rows in a more concise way using slicing and a loop
        rows = [list(range(i, i + 8)) for i in range(56, -1, -8)]

        for row in rows:
            for i in row:
                print(f" {self.env_representation.action_dict[policy[self.env_representation.S[i].number]].ascii} ",
                      end="")
                if Agent.__needs_extra_space(self.env_representation.S[i].position):
                    print("    ", end="")

            # Simplify the condition for adding extra newlines
            print("\n\n" if row == rows[3] else "")
        print()
