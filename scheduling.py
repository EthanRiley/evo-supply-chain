from evo import Evo
import pandas as pd
import random as rnd
import json
from collections import defaultdict

def setups(L, data):
    return sum([1 for x, y in zip(L, L[1:]) if data[x]['product'] != data[y]['product']])

def delays(L, data):
    return sum([data[x]['quantity'] for x, y in zip(L, L[1:]) if y < x])

def priority(L, data):
    # Figure out number of high priority orders
    # Until every high priority order has been fulfilled, add 1 for every low priority order
    # Find index of last high priority order
    num_high_prio = sum([1 for x in L if data[x]['priority'] == 'HIGH'])
    num_low_prio = sum([1 for x in L if data[x]['priority'] == 'LOW'])
    #back_list = L[::-1]
    #end_low_prio = back_list.index()
    last_high_prio_position = 4
    return sum([data[L[x]]['quantity'] for x in range(len(L)) if x < last_high_prio_position and data[L[x]]['priority'] == 'LOW'])

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

def goal_directed_swapper3(solutions):
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
    #E.add_agent('agent3', goal_directed_swapper3, 1)

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