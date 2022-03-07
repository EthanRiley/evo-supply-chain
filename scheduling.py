from evo import Evo
import pandas as pd
import random as rnd
import json
from collections import defaultdict
import functools

def setups(L, data):
    return sum([1 for x, y in zip(L, L[1:]) if data[x]['product'] != data[y]['product']])

def delays(L, data):
    return sum([data[x]['quantity'] for x, y in zip(L, L[1:]) if y < x])

def priority(L, data):
    # Filter list to list of just high priority orders
    high_only = list(filter((lambda order: data[order]['priority'] == 'HIGH'), L))
    # Find out what the last high priority is
    last = high_only[-1]
    # Determine position of last high priority order with list index
    index = L.index(last)
    return sum([data[L[x]]['quantity'] for x in range(len(L)) if x < index and data[L[x]]['priority'] == 'LOW'])

def swapper(solutions):
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L

def goal_directed_swapper1(solutions):
    # Improves setups
    pass

def delay_directed_improvement(solutions):
    # Improves by delays
    L = solutions[0]
    delay_list = [(x, y) for x, y in zip(L, L[1:]) if y < x]
    if len(delay_list) == 0:
        i = rnd.randrange(0, len(L))
        j = rnd.randrange(0, len(L))
        L[i], L[j] = L[j], L[i]
        return L
    else:
        swap_orders = delay_list[rnd.randrange(0, len(delay_list))]
        i1 = L.index(swap_orders[0])
        i2 = L.index(swap_orders[1])
        L[i1], L[i2] = L[i2], L[i1]
        i = rnd.randrange(0, len(L))
        j = rnd.randrange(0, len(L))
        L[i], L[j] = L[j], L[i]
        return L

def goal_directed_swapper3(solutions):
    # improves by priority

    # Get list of all low prio orders before last high prio order

    # Pick random agent from this list

    # Move agent behind last high prio agent
    
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