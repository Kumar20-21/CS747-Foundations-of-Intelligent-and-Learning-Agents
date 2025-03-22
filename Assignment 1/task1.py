"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need
def KL_divergence(p, q):
    if p == q:
        return 0
    if 1 == q or 0 == q:
        return float('inf')
    if 0 == p:
        return -1*math.log(1-q)
    return p * math.log(p / q) + (1 - p) * math.log((1-p)/(1-q))
    

def find_q(p, kl_threshold):
    left, right = p, 1.0
    while (right - left) > 1e-6:
        q = (left + right) / 2
        if KL_divergence(p, q) > kl_threshold:
            right = q
        else:
            left = q
    return left
        
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.horizon_completed = 0 
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.horizon_completed<self.num_arms:
            return self.horizon_completed
        return np.argmax(self.values+np.sqrt(2*math.log(self.horizon_completed)/self.counts))
        # END EDITING HERE  
        
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        self.horizon_completed += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.horizon_completed = 0
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if np.sum(self.counts)<self.num_arms:
            return int(np.sum(self.counts))
        if 1.0 in self.values:
            return np.argmax(self.values)
        a = math.log(self.horizon_completed) + 3*math.log(math.log(self.horizon_completed))
        kls = a/self.counts
        q_val = np.array([find_q(self.values[i], kls[i]) for i in range(self.num_arms)])
        return np.argmax(q_val)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        self.horizon_completed += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE

class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        maxindex = 0 # Index of the maximum sample
        samples = np.random.beta(self.counts+1, self.values+1) # Sample values
        for arm in range(1, self.num_arms):
            if samples[arm] > samples[maxindex]:
                maxindex = arm
        return maxindex
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward:
            self.counts[arm_index] += 1
        else:
            self.values[arm_index] += 1
        # END EDITING HERE

