import argparse
import numpy as np
import copy


def get_states(gridworld):
    # Getting the number of walls
    walls_count = np.count_nonzero(np.array(gridworld) == 'W')
    # numStates = 2*non-walls
    numStates = 8*(len(gridworld)*len(gridworld[0])-walls_count)
    counter = 0
    for i in range(len(gridworld)):
        for j in range(len(gridworld[0])):
            if gridworld[i][j] == 'W':
                continue
            else:
                temp = numStates//8
                lis = [gridworld[i][j]]
                for n in range(8):
                    lis += [counter + n*temp]
                gridworld[i][j] = tuple(lis)
                counter += 1
    return gridworld


def get_state_identifier(gridworld):
    # Getting if the agent has picked the key or not
    has_key = np.count_nonzero(np.array(gridworld)=='k')
    if not has_key:
        has_key = True
    else:
        has_key = False
    # Getting where the agent is present at start state or other state
    has_different_state = [0, '', '']
    for sybm in ['>', '<', '^', 'v']:
        has_different_state[0] += np.count_nonzero(np.array(gridworld)==sybm)
        if has_different_state[0]:
            # Storing the symbol and location of the symbol
            has_different_state[1] = sybm
            has_different_state[2] = list(np.argwhere(np.array(gridworld) == sybm)[0])
            break
    if not has_different_state[0]:
        # Storing the location of start state if agent is at start state
        has_different_state[1] = 's'
        has_different_state[2] = list(np.argwhere(np.array(gridworld) == 's')[0])
    
    return has_key, has_different_state

def get_grid_world(file):
    # Getting the grid worlds from the file
    gridworlds = []
    # Reading the files
    with open(file, 'r') as f:
        lines = f.readlines()
        # Extract the gridworld
        gridworld = []
        for line in lines[2:]:
            line = line.strip('\n')
            if line =='Testcase':
                gridworlds +=[gridworld]
                gridworld = []
                continue
            gridworld += [line.split()]
        gridworlds += [gridworld]
    
    # Forming a grid world with states mapped
    gridworld_with_states = get_states(copy.deepcopy(gridworlds[0]))

    # Identifing the state in which the agent is located
    state_numbers = []
    for i in range(len(gridworlds)):
        state_number = []
        has_key, has_different_state = get_state_identifier(gridworlds[i])
        location = has_different_state[2]
        if has_key:
            if has_different_state[0]:
                if has_different_state[1] == '^':
                    state_number = [gridworld_with_states[location[0]][location[1]][5]]
                elif has_different_state[1] == '>':
                    state_number = [gridworld_with_states[location[0]][location[1]][6]]
                elif has_different_state[1] == 'v':
                    state_number = [gridworld_with_states[location[0]][location[1]][7]]
                else:
                    state_number = [gridworld_with_states[location[0]][location[1]][8]]
            else:
                for i in range(5,9):
                    state_number += [gridworld_with_states[location[0]][location[1]][i]]
        else:
            if has_different_state[0]:
                if has_different_state[1] == '^':
                    state_number = [gridworld_with_states[location[0]][location[1]][1]]
                elif has_different_state[1] == '>':
                    state_number = [gridworld_with_states[location[0]][location[1]][2]]
                elif has_different_state[1] == 'v':
                    state_number = [gridworld_with_states[location[0]][location[1]][3]]
                else:
                    state_number = [gridworld_with_states[location[0]][location[1]][4]]
            else:
                for i in range(1,5):
                    state_number += [gridworld_with_states[location[0]][location[1]][i]]
        state_numbers += [state_number]
    return state_numbers
    
    
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mdp', type=str, required=True, help="location of MDP file")
    parser.add_argument('--value-policy', type=str, required=True, help="input hpi or lp")
    parser.add_argument('--gridworld', type=str, required=True, help="policy file with .txt")
    args = parser.parse_args()

    state_numbers = get_grid_world(args.gridworld)

    with open(args.value_policy, "r") as f:
        lines = f.readlines()
        for i in range(len(state_numbers)):
            if len(state_numbers[i])==1:
                print(int(lines[state_numbers[i][0]].strip().split()[1]))
            else:
                act = 0
                maxi = float(lines[state_numbers[i][0]].replace('\n','').split()[0])
                for j in range(1, len(state_numbers[i])):
                    if float(lines[state_numbers[i][j]].replace('\n','').split()[0] )> maxi:
                        maxi = float(lines[state_numbers[i][j]].replace('\n','').split()[0])
                        act = int(lines[state_numbers[i][j]].replace('\n','').split()[1])
                print(act)
