"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the CostlySetBanditsAlgo class. Here are the method details:
    - __init__(self, num_arms, horizon, fault): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_query_set(self): This method is called when the algorithm needs to
        provide a query set to the oracle. The method should return an array of 
        arm indices that specifies the query set.
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_query_set method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
"""

import numpy as np
from task1 import Algorithm
# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE

class CostlySetBanditsAlgo(Algorithm):
    def __init__(self, num_arms, horizon):
        # You can add any other variables you need here
        self.num_arms = num_arms
        self.horizon = horizon
        # START EDITING HERE
        self.counts = np.ones(num_arms)
        self.values = np.ones(num_arms)
        self.ks = np.arange(1, num_arms+1)
        # END EDITING HERE
    
    def give_query_set(self):
        # START EDITING HERE
        samples = np.random.beta(self.counts, self.values)
        sorted_indices = np.argsort(samples, kind='mergesort')[::-1]
        samples = samples[sorted_indices]

        best_k = (np.cumsum(samples)-1)/self.ks
        return sorted_indices[:np.argmax(best_k) + 1]
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward:
            self.counts[arm_index] += 1
        else:
            self.values[arm_index] += 1
        #END EDITING HERE