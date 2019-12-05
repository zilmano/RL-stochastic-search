import numpy as np
import enum

class PolicyType(enum.Enum):
    greedy = 1
    e_soft = 2

class Policy(object):
    def action_prob(self,state:int,action:int) -> float:
        """
        input:
            state, action
        return:
            \pi(a|s)
        """
        raise NotImplementedError()

    def action(self,state:int,greedy=False) -> int:
        """
        input:
            state
        return:
            action
        """
        raise NotImplementedError()

class NewPolicy(Policy):
    def __init__(self,nA,nS):
        self._nA = nA
        self._nS = nS
        self._p = np.ones([nS,nA])*(1/nA)

    def action_prob(self,state:int,action:int):
        return self._p[state][action]

    def action(self,state, greedy=False):
        if not greedy:
            return np.random.choice(self._nA, p=self._p[state])
        else:
            max_actions = np.argwhere(self._p[state] == self._p[state].max()).flatten()
            return np.random.choice(max_actions)

    def set_greedy_action(self,state,new_greedy_actions):
        self._p[state] = np.zeros(self._nA)
        for action in new_greedy_actions:
           self._p[state][action] = 1/len(new_greedy_actions)

    def set_e_soft_action(self, state, new_action, e):
        self._p[state] = np.array(self._nA*[e/self.nA])
        self._p[state][new_action] = 1 - e + e/self.nA

    @property
    def P(self) -> np.array:
        return self._p

    @property
    def nA(self) -> int:
        return self._nA

    @nA.setter
    def nA(self,nA):
        self._nA = nA

    @property
    def nS(self) -> int:
        return self._nS

    @nS.setter
    def nS(self, nS):
        self._nS = nS

class ApproximatePolicy(Policy):
    def __init__(self,nA,nS):
        self._nA = nA
        self.approximators = nA*[]

    def action_prob(self, features, action):
        return self.approximators[action](*features)

    def action(self,state, greedy=False):
        for Qvalue in approximators:

        if not greedy:
            return np.random.choice(self._nA, p=self._p[state])
        else:
            max_actions = np.argwhere(self._p[state] == self._p[state].max()).flatten()
            return np.random.choice(max_actions)

    def set_greedy_action(self,state,new_greedy_actions):
        self._p[state] = np.zeros(self._nA)
        for action in new_greedy_actions:
           self._p[state][action] = 1/len(new_greedy_actions)

    def set_e_soft_action(self, state, new_action, e):
        self._p[state] = np.array(self._nA*[e/self.nA])
        self._p[state][new_action] = 1 - e + e/self.nA

    @property
    def P(self) -> np.array:
        return self._p

    @property
    def nA(self) -> int:
        return self._nA

    @nA.setter
    def nA(self,nA):
        self._nA = nA

    @property
    def nS(self) -> int:
        return self._nS

    @nS.setter
    def nS(self, nS):
        self._nS = nS




class HandMadeSweepPolicy(Policy):
    '''
    Criss-Cross sweeping policy to cover all cells on the grid.
    Will be a complete sweep only if starting state is m-1. (bottom left corner of the grid)
    '''

    def __init__(self, nA, m, n):
        self._nA = nA
        self._nS = m*n
        self.m = m
        self.n = n
        self._p = self._hand_craft_init()

    def _hand_craft_init(self):
        p = np.zeros([self.nS, self.nA])
        for col in range(0,self.n):
            rows = range(0,self.m)
            if col % 2 == 0:
                rows = reversed(rows)
            for row in rows:
                state = int(col * self.m + row)
                if col % 2:
                    if row == self.m-1:
                        action = 2
                    else:
                        action = 3
                else:
                    if row == 0:
                        action = 2
                    else:
                        action = 1
                p[state][action] = 1
        return p

    def action_prob(self,state:int,action:int):
        if state >= self.nS:
            state = state % self.nS
        return self._p[state][action]

    def action(self,state,greedy=False):
        if state >= self.nS:
            state = state % self.nS
        return np.random.choice(self._nA, p=self._p[state])

    def set_greedy_action(self,state,new_greedy_actions):
        if state >= self.nS:
            state = state % self.nS
        self._p[state] = np.zeros(self._nA)
        for action in new_greedy_actions:
           self._p[state][action] = 1/len(new_greedy_actions)

    def set_e_soft_action(self, state, new_action, e):
        if state >= self.nS:
            state = state % self.nS
        self._p[state] = np.array(self._nA*[e/self.nA])
        self._p[state][new_action] = 1 - e + e/self.nA

    @property
    def P(self) -> np.array:
        return self._p

    @property
    def nA(self) -> int:
        return self._nA

    @nA.setter
    def nA(self,nA):
        self._nA = nA

    @property
    def nS(self) -> int:
        return self._nS

    @nS.setter
    def nS(self, nS):
        self._nS = nS
