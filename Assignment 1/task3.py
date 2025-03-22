# Task 3
# Using inspiration from code in task1.py and simulator.py write the appropriate functions to create the plot required.

import numpy as np
import matplotlib.pyplot as plt
from bernoulli_bandit import *
from task1 import Algorithm
from multiprocessing import Pool

# DEFINE your algorithm class here
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon, eps):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = eps
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

# DEFINE single_sim_task3() HERE
def single_sim_task3(seed=0, ALGO=Eps_Greedy, PROBS=[0.7, 0.6, 0.5, 0.4, 0.3], HORIZON=30000, EPSILON = 0.1):
    np.random.seed(seed)
    shuffled_probs = np.random.permutation(PROBS)
    bandit = BernoulliBandit(probs=shuffled_probs)
    algo_inst = ALGO(num_arms=len(shuffled_probs), horizon=HORIZON, eps=EPSILON)
    for _ in range(HORIZON):
       arm_to_be_pulled = algo_inst.give_pull()
       reward = bandit.pull(arm_to_be_pulled)
       algo_inst.get_reward(arm_index=arm_to_be_pulled, reward=reward)
    return bandit.regret()

# DEFINE simulate_task3() HERE

def simulate_task3(algorithm, probs, horizon, epsilon, num_sims=50):
    """simulates algorithm of class Algorithm
    for BernoulliBandit bandit, with horizon=horizon
    """
    
    def multiple_sims(num_sims=50):
        with Pool(10) as pool:
            sim_out = pool.starmap(single_sim_task3,
                    [(i, algorithm, probs, horizon, epsilon) for i in range(num_sims)])
        return sim_out
    
    sim_out = multiple_sims(num_sims)
    regrets = np.mean(sim_out)
    return regrets 

# DEFINE task3() HERE

def task3(algorithm, probs, num_sims=50):
    """generates the plots and regrets for task3"""
    
    epsilons = [0.1*i for i in range(11)]
    horizon = 30000
    regrets = []
    for epsilon in epsilons:
        regrets.append(simulate_task3(algorithm, probs, horizon, epsilon, num_sims))
    
    print(regrets)
    plt.plot(epsilons, regrets)
    plt.title("Regret vs Epsilon")
    plt.savefig("task3-{}.png".format(algorithm.__name__))
    plt.clf()

# Call task3() to generate the plots

if __name__ == '__main__':
    probs=[0.7, 0.6, 0.5, 0.4, 0.3]
    task3(algorithm=Eps_Greedy, probs=probs, num_sims=50)