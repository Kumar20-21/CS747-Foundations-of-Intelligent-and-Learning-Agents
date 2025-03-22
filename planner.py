import argparse
import numpy as np
import pulp

def LP_iteration(mdp):
    num_states = mdp['num_states']
    num_actions = mdp['num_actions']
    transitions = mdp['transitions']
    discount = mdp['discount']
    end_states = mdp['end_states']

    # Create the LP problem instance with minimization objective.
    prob = pulp.LpProblem("MDP_LP", pulp.LpMinimize)

    # Create a decision variable V(s) for each state.
    V_vars = [pulp.LpVariable(f"V_{s}", cat='Continuous') for s in range(num_states)]

    # The objective is to minimize the sum of all V(s) values.
    prob += pulp.lpSum(V_vars)

    for s in range(num_states):
        if s in end_states:
            prob += V_vars[s] == 0
            continue
        for a in range(num_actions):
            if (s,a) in transitions:
                constraint = pulp.lpSum([probability * (reward + discount * V_vars[s_prime])
                                for (s_prime, probability, reward) in transitions[(s,a)] if probability != 0])
                prob += V_vars[s] >= constraint
    
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Extract the optimal values.
    V = [pulp.value(v) for v in V_vars]

    policy = np.zeros(num_states, dtype=int)
    for s in range(num_states):
        if s in end_states:
            continue
        q_max = -np.inf
        best_action = 0
        for a in range(num_actions):
            q = 0
            if (s, a) in transitions:
                for (s_prime, probability, reward) in transitions[(s, a)]:
                    q += probability*(reward+discount*V[s_prime])
            if q>q_max:
                q_max = q
                best_action = a
        policy[s] = best_action
    
    return V, policy

def evaluate_policy(Policy, mdp):
    num_states = mdp['num_states']
    transitions = mdp['transitions']
    discount = mdp['discount']
    end_states = mdp['end_states']

    P_pi = np.zeros((num_states, num_states))
    r_pi = np.zeros(num_states)

    for s in range(num_states):
        # For terminal states, we enforce V(s)=0 and ignore transitions.
        if s in end_states:
            continue
        
        a = Policy[s]
        if (s, a) in transitions:
            for (s_next, probability, reward) in transitions[(s, a)]:
                r_pi[s] += probability * reward
                P_pi[s, s_next] += probability
    
    A = np.eye(num_states) - discount * P_pi

    return np.linalg.solve(A, r_pi)

def Howards_iteration(mdp):
    num_states = mdp['num_states']
    num_actions = mdp['num_actions']
    transitions = mdp['transitions']
    discount = mdp['discount']
    end_states = mdp['end_states']
    policy = np.zeros( mdp['num_states'], dtype=int)
    V = np.zeros(mdp['num_states'])

    policy_stable = False
    while not policy_stable:
        V = evaluate_policy(policy, mdp)
        policy_stable = True
        policy_new = np.copy(policy)
        for s in range(num_states):
            if s in end_states:
                continue
            q_max = -np.inf
            best_action = 0
            for a in range(num_actions):
                q = 0
                if (s, a) in transitions:
                    for (s_prime, probability, reward) in transitions[(s, a)]:
                        q += probability*(reward+discount*V[s_prime])
                if q>q_max:
                    q_max = q
                    best_action = a
            policy[s] = best_action
            
            if policy[s] != policy_new[s]:
                policy_stable = False
        if policy_stable:
            break
    return V, policy


def Formulate_MDP(filename):
    # Read the file
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Parse the file
        # States
        num_states = int(lines[0].split()[1])
        # Actions
        num_actions = int(lines[1].split()[1])
        # End states
        line = lines[2].split()
        end_states = list(map(int, lines[2].split()[1:]))
        # Transition Model and rewards
        transitions = {}

        for line in lines[3:-2]:
            line = line.split()
            s, a, s_prime = map(int, line[1:4])
            probability = float(line[5])
            reward= float(line[4])
            transitions.setdefault((s, a), []).append((s_prime, probability, reward))
        
        # Discount factor
        discount = float(lines[-1].split()[1])
        return {"num_states": num_states, "num_actions": num_actions, "end_states": end_states, \
                "transitions": transitions, "discount": discount}

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mdp', type=str, required=True, help="location of MDP file")
    parser.add_argument('--algorithm', type=str, required=False, help="input hpi or lp", default='hpi', choices=['hpi','lp'])
    parser.add_argument('--policy', type=str, required=False, help="policy file with .txt")
    args = parser.parse_args()

    # Parsing MDP file
    MDP = Formulate_MDP(filename=args.mdp)
    V, policy = None, None

    # Evaluate policy only on the given MDP if given'
    if args.policy:
        # Read policy from file
        with open(args.policy, 'r') as f:
            policy = [int(line.strip().split()[-1]) for line in f.readlines()]
            
            # Evaluate given policy
            V = evaluate_policy(Policy=policy, mdp=MDP)
    
    # Running the algorithms
    elif 'hpi' == args.algorithm: # Howard's Policy Iteration
        V, policy = Howards_iteration(mdp=MDP)
        
    else:# LP-Learning Policy
        V, policy = LP_iteration(mdp=MDP)
    
    for i in range(len(V)): # Printing the value function and policy
        print(f"{V[i]} {policy[i]}")