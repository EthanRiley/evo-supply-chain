from evo import Evo
import pandas as pd
import random as rnd
import json
from collections import defaultdict
import functools
import warnings
warnings.filterwarnings("ignore")

data = pd.read_json('orders.json')

def setups(L):
    return sum([1 for x, y in zip(L, L[1:]) if data[x]['product'] != data[y]['product']])

def delays(L):
    return sum([data[x]['quantity'] for x, y in zip(L, L[1:]) if y < x])

def priority(L):
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

def setup_directed_improvement(solutions):
    # Improves setups
    L = solutions[0]
    # Return list of orders where they are sandwhiched by two different types
    crap_orders = [(x, y, z) for x, y, z in zip(L, L[1:], L[2:]) if data[x]['product'] != data[y]['product'] and data[y]['product'] != data[z]['product']]
    if len(crap_orders) > 0:
        swap_orders = crap_orders[rnd.randrange(0, len(crap_orders))]
        i = L.index(swap_orders[1])
        # Find an order with the same type
        similar_orders = [L[x] for x in range(len(L)) if data[L[i]]['product'] == data[L[x]]['product']]
        order_behind = similar_orders[rnd.randrange(0, len(similar_orders))]
        i2 = L.index(order_behind)
        # Move order adjacent to order of same type
        L.insert(i2+1, L.pop(i))
        i = rnd.randrange(0, len(L))
        j = rnd.randrange(0, len(L))
        L[i], L[j] = L[j], L[i]
    else:
        i = rnd.randrange(0, len(L))
        j = rnd.randrange(0, len(L))
        L[i], L[j] = L[j], L[i]
    return L
        

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

def priority_directed_improvement(solutions):
    # improves by priority
    L = solutions[0]
    try:
        # Get list of all low prio orders before last high prio order
        high_only = list(filter((lambda order: data[order]['priority'] == 'HIGH'), L))
        last = high_only[-1]
        index = L.index(last)
        bad_low_only = [L[x] for x in range(len(L)) if x < index and data[L[x]]['priority'] == 'LOW']
        # Pick random agent from this list
        moved_order = bad_low_only[rnd.randrange(0, len(bad_low_only))]
        i = L.index(moved_order)
        # Move agent behind last high prio agent
        L.insert(index+1, L.pop(i))
        i = rnd.randrange(0, len(L))
        j = rnd.randrange(0, len(L))
        L[i], L[j] = L[j], L[i]
    except:
        i = rnd.randrange(0, len(L))
        j = rnd.randrange(0, len(L))
        L[i], L[j] = L[j], L[i]
    return L

def random_improvement(solutions):
    decider = rnd.randint(0,2)
    if decider == 0:
       return setup_directed_improvement(solutions)
    elif decider == 1:
        return delay_directed_improvement(solutions)
    elif decider ==2:
        return priority_directed_improvement(solutions)
    else:
        return swapper(solutions)


def main():
    # Create Environment
    E = Evo()

    # Register fitness criteria
    E.add_fitness_criteria('setups', setups)
    E.add_fitness_criteria('lowpriority', priority)
    E.add_fitness_criteria('delays', delays)

    # Register agents
    #E.add_agent('swapper', swapper, 1)
    E.add_agent('setup', setup_directed_improvement, 1)
    E.add_agent('delay', delay_directed_improvement, 1)
    E.add_agent('lowpriority', priority_directed_improvement, 1)
    #E.add_agent('random', random_improvement, 1)

    # Add initial solution
    L = [x + 1 for x in range(100)]
    E.add_solution(L)
    print(E)

    # Run Evolver
    E.evolve(100000, 500, 10000)

if __name__ == '__main__':
    main()