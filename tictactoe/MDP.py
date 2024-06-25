import numpy as np
from common import Cell

WIN_REWARD = 1
LOSE_REWARD = -1
DRAW_REWARD = 0

class MDP:
    def __init__(self) -> None:
        self.states = set()
        self.T_states = set()
        self.actions = {}

    def _check_2_winner(self, state) -> bool:
        hor, vert = 0, 0
        for i in range(3):
            if (state[i*3] == state[i*3+1] == state[i*3+2]) and (state[i*3] != Cell.NO_MOVE.value):
                hor += 1
            if (state[i] == state[i+3] == state[6+i]) and (state[i] != Cell.NO_MOVE.value):
                vert += 1
        
        if hor == 2 or vert == 2:
            return True
        else:
            return False

    def generate_states(self) -> None:
        # initialise with all possible and impossible states
        for values in np.ndindex(3, 3, 3, 3, 3, 3, 3, 3, 3):
            state = tuple(values)
            self.states.add(state)
        
        # remove states that are not possible
        for state in self.states.copy():
            # computer is always X, so there is strictly more O than X
            if state.count(Cell.X.value) > state.count(Cell.O.value):
                self.states.remove(state)
            elif abs(state.count(Cell.X.value) - state.count(Cell.O.value)) > 1:
                self.states.remove(state)
            elif self._check_2_winner(state):
                self.states.remove(state)

    def termination_states(self) -> None:
        for state in self.states:
            if self.win(state):
                self.T_states.add(state)
            elif state.count(Cell.NO_MOVE.value) == 0:
                self.T_states.add(state)

    def generate_actions(self) -> None:
        for state in self.states:
            self.actions[state] = None
            if state not in self.T_states:
                self.actions[state] = []
                for i in range(9):
                    if state[i] == Cell.NO_MOVE.value:
                        self.actions[state].append(i)

    def transition_probability_function(self, state) -> float:
        if state in self.T_states:
            return 0.0
        else:
            return 1/(len(self.actions[state]) - 1)

    def reward_function(self, state) -> int:
        winner = self.winner(state)
        if winner == Cell.X.value:
            return WIN_REWARD
        elif winner == Cell.O.value:
            return LOSE_REWARD
        else:
            return DRAW_REWARD

    def winner(self, state) -> int:
        for i in range(3):
            if state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] != Cell.NO_MOVE.value:
                return state[i*3]
            if state[i] == state[i+3] == state[i+6] and state[i] != Cell.NO_MOVE.value:
                return state[i]
        if state[2] == state[4] == state[6] and state[2] != Cell.NO_MOVE.value:
            return state[2]
        elif state[0] == state[4] == state[8] and state[0] != Cell.NO_MOVE.value:
            return state[0]
        else:
            return 0
        
    def win(self, state) -> bool:
        winner = self.winner(state)
        if winner == Cell.X.value or winner == Cell.O.value:
            return True
        else:
            return False

    def possible_next_state(self, state, action) -> list:
        new_state = list(state)
        new_state[action] = 1
        if self.win(new_state):
            return []
        possible_next_states = []
        for i, case in enumerate(new_state):      
            if case == Cell.NO_MOVE.value:
                next_new_state = new_state.copy()
                next_new_state[i] = Cell.O.value
                possible_next_states.append(tuple(next_new_state))
        return possible_next_states