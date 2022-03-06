from evo import Evo
import pandas as pd
import random as rnd
import json

def setups(L, data):
    pass

def delays(L, data):
    pass

def priority(L, data):
    pass

def swapper(solutions):
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L

def goal_directed_swapper1(solutions):
    pass

def goal_directed_swapper2(solutions):
    pass

def main():
    # Create Environment
    E = Evo()

    # Register fitness criteria
    E.add_fitness_criteria('setups', setups)
    E.add_fitness_criteria('delays', delays)
    E.add_fitness_criteria('priority', priority)

    # Register agents
    E.add_agent('swapper', swapper, 1)
    #E.add_agent('agent1', goal_directed_swapper1, 1)
    #E.add_agent('agent2', goal_directed_swapper2, 1)

    # Read data
    data_df = pd.read_json('orders.json') # Not sure if we want dict or df format
    f = open('orders.json')
    data_dict = json.load(f) # Not sure if we want dict or df format
    f.close()

    # Add initial solution
    L = [x + 1 for x in range(100)]
    E.add_solution(L)
    print(E)

    # Run Evolver
    E.evolve(100000, 500, 10000)

if __name__ == '__main__':
    main()