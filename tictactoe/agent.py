from MDP import MDP
from tqdm import tqdm
import numpy as np

GAMMA = 0.95
EPSILON = 1e-3

class ValueIteration(MDP):
    def __init__(self, gamma = GAMMA, epsilon = EPSILON) -> None:
        super().__init__()
        self.gamma = gamma
        self.epsilon = epsilon
        self.policy = {}
        self.V = {}
        self.initialise()

    def _init_V(self) -> None:
        for state in self.states:
            self.V[state] = 0
    
    def _init_policy(self) -> None:
        for state in self.states:
            self.policy[state] = None
    
    def initialise(self) -> None:
        self.generate_states()
        self.generate_actions()
        self.termination_states()

        self._init_V()
        self._init_policy()

    def value_iteration(self) -> None:
        epoch = 0

        while True:
            print(f"Epoch {epoch + 1} started ...")
            epoch += 1
            delta = 0

            for s in tqdm(self.states):
                if s in self.T_states:
                    self.V[s] = self.reward_function(s)
                    continue
                
                v = self.V[s]
                new_value = float("-inf")
                for a in self.actions[s]:
                    for next_s in self.possible_next_state(s, a):
                        expected_value = self.transition_probability_function(s) * (self.reward_function(next_s) + self.gamma * self.V[next_s])
                self.V[s] = max(new_value, expected_value)
                delta = max(delta, abs(v - self.V[s]))
            if delta < self.epsilon:
                break

        for s in self.states:
            if s in self.T_states:
                continue
            best_action = None
            best_value = float("-inf")
            for a in self.actions[s]:
                expected_value = self.reward_function(s)
                for next_s in self.possible_next_state(s, a):
                    expected_value += self.transition_probability_function(s) * (self.reward_function(next_s) + self.gamma * self.V[next_s])
                
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = a
            
            self.policy[s] = best_action

class PolicyIteration(MDP):
    def __init__(self, gamma = GAMMA, epsilon = EPSILON):
        super().__init__()
        self.gamma = gamma
        self.epsilon = epsilon
        self.policy = {}
        self.V = {}
        self.initialise()

    def initialise(self) -> None:
        self.generate_states()
        self.generate_actions()
        self.termination_states()

        for s in self.states:
            self.V[s] = 0
            # init policy randomly
            self.policy[s] = np.random.choice(self.actions[s]) if self.actions[s] else None

    def policy_evaluation(self) -> None:
        while True:
            delta = 0
            for s in self.states:
                if s in self.T_states:
                    self.V[s] = self.reward_function(s)
                    continue
                v = 0
                for next_s in self.possible_next_state(s, self.policy[s]):
                    v += self.reward_function(next_s) + self.gamma * self.V[next_s]
                delta = max(delta, np.abs(v - self.V[s]))
                self.V[s] = v
            if delta < self.epsilon:
                break

    def policy_improvement(self) -> bool:
        for s in self.states:
            temp = self.policy[s]
            if s in self.T_states:
                continue
            best_action = None
            best_value = float("-inf")
            stable = True
            for a in self.actions[s]:
                expected_value = self.reward_function(s)
                for next_s in self.possible_next_state(s, a):
                    expected_value += self.transition_probability_function(s) * (self.reward_function(next_s) + self.gamma * self.V[next_s])
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = a
            
            self.policy[s] = best_action
            if temp != self.policy[s]:
                stable = False
        
        return stable
    
    def policy_iteration(self) -> dict:
        epoch = 0
        while True:
            print(f"Epoch {epoch+1} started ...")
            epoch += 1
            self.policy_evaluation()
            if self.policy_improvement():
                break
        return self.policy
        