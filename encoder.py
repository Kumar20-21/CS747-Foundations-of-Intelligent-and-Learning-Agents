import argparse
import numpy as np


def get_without_key_transitions(grid, action, row, col, transitions, n):
    k, m = 0, 0
    if n == 1:
        k = -1
    elif n == 2:
        m = 1
    elif n == 3:
        k = 1
    else:
        m = -1
    if grid[row+k][col+m] == 'W' or grid[row+k][col+m][0] == 'd':
        # Self transition without key or facing a wall
        transitions.append(f'transition {grid[row][col][n]} {action} {grid[row][col][n]} -0.5 1.0')
    elif grid[row+2*k][col+2*m] == 'W' or grid[row+2*k][col+2*m][0] == 'd':
        if grid[row+k][col+m][0] == 'k': # Next state has key
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} 0.5 1.0')
        else:
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} -0.5 1.0')
    elif grid[row+3*k][col+3*m] == 'W' or grid[row+3*k][col+3*m][0] == 'd':
        # Sliding to n=2
        if grid[row+k][col+m][0] == 'k':
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} 0.5 0.5')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+2*k][col+2*m][n]} -0.5 0.5')
        elif grid[row+2*k][col+2*m][0] == 'k':
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+2*k][col+2*m][n]} 0.5 0.5')
        else:
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+2*k][col+2*m][n]} -0.5 0.5')
    else:
        # Sliding to n=3
        if grid[row+k][col+m][0] == 'k':
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} 0.5 0.5')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+2*k][col+2*m][n]} -0.5 0.3')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+3*k][col+3*m][n]} -0.5 0.2')
        elif grid[row+2*k][col+2*m][0] == 'k':
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+2*k][col+2*m][n]} 0.5 0.3')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+3*k][col+3*m][n]} -0.5 0.2')
        elif grid[row+3*k][col+3*m][0] == 'k':
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+2*k][col+2*m][n]} -0.5 0.3')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+3*k][col+3*m][n]} 0.5 0.2')
        else:
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+k][col+m][n]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+2*k][col+2*m][n]} -0.5 0.3')
            transitions.append(f'transition {grid[row][col][n]} {action} {grid[row+3*k][col+3*m][n]} -0.5 0.2')
    
    return transitions

def get_with_key_transitions(grid, action, row, col, transitions, n):
    k, m = 0, 0
    if n == 1:
        k = -1
    elif n == 2:
        m = 1
    elif n == 3:
        k = 1
    else:
        m = -1
    if grid[row+k][col+m] == 'W':
        # Self transition with key but facing wall
        transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row][col][n+4]} -0.5 1.0')
    elif grid[row+2*k][col+2*m] == 'W':
        # Sliding to n=1
        if grid[row+k][col+m][0] == 'g':
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} 10.0 1.0')
        else:
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} -0.5 1.0')
    elif grid[row+3*k][col+3*m] == 'W':
        # Sliding to n=2
        if grid[row+k][col+m][0] == 'g':
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} 10.0 0.5')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+2*k][col+2*m][n+4]} -0.5 0.5')
        elif grid[row+2*k][col+2*m][0] == 'g':
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+2*k][col+2*m][n+4]} 10.0 0.5')
        else:
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+2*k][col+2*m][n+4]} -0.5 0.5')
    else:
        # Sliding to n=3
        if grid[row+k][col+m][0] == 'g':
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} 10.0 0.5')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+2*k][col+2*m][n+4]} -0.5 0.3')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+3*k][col+3*m][n+4]} -0.5 0.2')
        elif grid[row+2*k][col+2*m][0] == 'g':
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+2*k][col+2*m][n+4]} 10.0 0.3')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+3*k][col+3*m][n+4]} -0.5 0.2')
        elif grid[row+3*k][col+3*m][0] == 'g':
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+2*k][col+2*m][n+4]} -0.5 0.3')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+3*k][col+3*m][n+4]} 10.0 0.2')
        else:
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+k][col+m][n+4]} -0.5 0.5')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+2*k][col+2*m][n+4]} -0.5 0.3')
            transitions.append(f'transition {grid[row][col][n+4]} {action} {grid[row+3*k][col+3*m][n+4]} -0.5 0.2')
    
    return transitions

def encode_MDP(file):
    
    gridworld = []
    # Read the file
    with open(file, 'r') as f:
        lines = f.readlines()
        # Extract the grid
        for line in lines:
            line = line.strip('\n')
            gridworld.append(line.split())
    # End States
    end = None
    # Getting the number of walls
    walls_count = np.count_nonzero(np.array(gridworld) == 'W')
    # numStates = 2*non-walls
    numStates = 8*(len(gridworld)*len(gridworld[0])-walls_count)
    # Counter to assign states to the gridworld
    counter = 0
    for i in range(len(gridworld)):
        for j in range(len(gridworld[0])):
            if gridworld[i][j] == 'W':
                continue
            else:
                temp = numStates//8
                lis = [gridworld[i][j]]
                for n in range(8):
                    lis.append(counter + n*temp)
                gridworld[i][j] = tuple(lis)
                if gridworld[i][j][0] =='g':
                    end = 'end'
                    for n in range(1,9):
                        end += f' {gridworld[i][j][n]}'
                counter += 1
    
    transitions = []

    for i in range(len(gridworld)):
        for j in range(len(gridworld[0])):
            if gridworld[i][j] == 'W':
                # Do Nothing
                continue
            elif gridworld[i][j][0] =='_' or gridworld[i][j][0] =='s':
                # For action 0:
                for temp in range(1,5):
                    transitions = get_without_key_transitions(gridworld, 0, i, j, transitions, temp)
                    transitions = get_with_key_transitions(gridworld, 0, i, j, transitions, temp)
                
                # For action 1:
                for temp in range(4):
                    transitions.append(f'transition {gridworld[i][j][1+temp]} 1 {gridworld[i][j][(3+temp)%4+1]} -0.5 0.9')
                    transitions.append(f'transition {gridworld[i][j][1+temp]} 1 {gridworld[i][j][(2+temp)%4+1]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 1 {gridworld[i][j][(3+temp)%4+5]} -0.5 0.9')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 1 {gridworld[i][j][(2+temp)%4+5]} -0.5 0.1')
                
                # For action 2:
                for temp in range(4):
                    transitions.append(f'transition {gridworld[i][j][1+temp]} 2 {gridworld[i][j][(1+temp)%4+1]} -0.5 0.9')
                    transitions.append(f'transition {gridworld[i][j][1+temp]} 2 {gridworld[i][j][(2+temp)%4+1]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 2 {gridworld[i][j][(1+temp)%4+5]} -0.5 0.9')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 2 {gridworld[i][j][(2+temp)%4+5]} -0.5 0.1')

                # For action 3:
                for temp in range(4):
                    transitions.append(f'transition {gridworld[i][j][1+temp]} 3 {gridworld[i][j][(1+temp)%4+1]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][1+temp]} 3 {gridworld[i][j][(3+temp)%4+1]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][1+temp]} 3 {gridworld[i][j][(2+temp)%4+1]} -0.5 0.8')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 3 {gridworld[i][j][(1+temp)%4+5]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 3 {gridworld[i][j][(3+temp)%4+5]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 3 {gridworld[i][j][(2+temp)%4+5]} -0.5 0.8')
            elif gridworld[i][j][0] == 'k' or gridworld[i][j][0] == 'd':
                # For action 0:
                for temp in range(1,5):
                    transitions = get_with_key_transitions(gridworld, 0, i, j, transitions, temp)
                
                # For action 1:
                for temp in range(4):
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 1 {gridworld[i][j][(1+temp)%4+5]} -0.5 0.9')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 1 {gridworld[i][j][(2+temp)%4+5]} -0.5 0.1')

                # For action 2:
                for temp in range(4):
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 2 {gridworld[i][j][(3+temp)%4+5]} -0.5 0.9')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 2 {gridworld[i][j][(2+temp)%4+5]} -0.5 0.1')
                
                # For action 3:
                for temp in range(4):
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 3 {gridworld[i][j][(1+temp)%4+5]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 3 {gridworld[i][j][(3+temp)%4+5]} -0.5 0.1')
                    transitions.append(f'transition {gridworld[i][j][5+temp]} 3 {gridworld[i][j][(2+temp)%4+5]} -0.5 0.8')
    return numStates, 4, end, transitions

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--gridworld', type=str, required=True, help="location of Grid World file")
    args = parser.parse_args()

    
    mdp_file = encode_MDP(file=args.gridworld)
    #print(mdp_file)
    print(f"numStates {mdp_file[0]}")
    print(f"numActions {mdp_file[1]}")
    print(f"{mdp_file[2]}")
    for transition in mdp_file[3]:
        print(transition)
    print("mdptype episodic")
    print("discount 0.9")
"""
    with open("mdp.txt", "w") as f:
        f.write(f"numStates {mdp_file[0]}\n")
        f.write(f"numActions {mdp_file[1]}\n")
        if mdp_file[2]:
            f.write(f"{mdp_file[2]}\n")
        f.writelines(f"{transition}\n" for transition in mdp_file[3])
        f.write("mdptype episodic\n")
        f.write("discount 0.75\n")"""
