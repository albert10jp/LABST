# Predictions was taken from Hsu et al. (2019).
# For predictions and preprocessed data, visit: https://github.com/chenyuhsu/learnedsketch

from utils.aol_utils import get_data_aol_query_list

import numpy as np

from utils.treaps import Treap
from utils.redblack import RedBlackTree
# from utils.treaprb import TreapRB
from utils.avl import AVLTree
from utils.splaytree import SplayTree
from utils.btree import BTree
import random


def test_rb(query, counts, k):
    rb = RedBlackTree()
    y = 100//k

    order = np.random.permutation(len(query)//y)

    for i in range(len(counts)//y):
        rb.insert(query[order[i]])
    
    cost = 0
    for i in range(len(counts)//y):
        cost += rb.find_cost(query[i]) * counts[i]
    #print(cost)
    return cost

def test_avl(query, counts, k):
    avl = AVLTree()
    y = 100//k

    order = np.random.permutation(len(query)//y)
    for i in range(len(counts)//y):
        avl.insert(query[order[i]])
    cost = 0
    for i in range(len(counts)//y):
        cost += avl.find_cost(query[i]) * counts[i]
    #print(cost)
    return cost

def test_splay(query, counts, k):
    splay = SplayTree()
    y = 100//k

    order = np.random.permutation(len(query)//y)
    for i in range(len(counts)//y):
        splay.insert(query[order[i]])
    cost = 0
    for i in range(len(counts)//y):
        cost += splay.find_cost(query[i]) * counts[i]
    #print(cost)
    return cost

def test_b(query, counts, k):
    b = BTree(3)
    y = 100//k

    order = np.random.permutation(len(query)//y)
    for i in range(len(counts)//y):
        b.insert(query[i])
    cost = 0
    for i in range(len(counts)//y):
        cost += b.find_cost(query[i]) * counts[i]
    #print(cost)
    return cost
    
def test_treap_rb(query, counts, k):
    treaprb = TreapRB()
    y = 100//k

    order = np.random.permutation(len(query))

    for i in range(len(query)):
        if i < (len(counts)//y):
            treaprb.insert(query[i], -results[i])
        else:
            TreapRB.insert_rb(query[i])

    cost = 0
    for i in range(len(counts)):
        cost += treaprb.find_cost(query[i])*counts[i]

    #print(cost)
    return cost

    

def test(query, counts, results, mode, k, shuffle=False):
    treap = Treap()
    y = 100//k

    if shuffle:
        query = np.random.permutation(len(query))

    for i in range(len(query)//y):
        if mode == 0:
            #learned
            treap.insert(query[i], -results[i])
        else:
            #random (mode = 1)
            treap.insert(query[i], random.uniform(0, 1))
        

    cost = 0
    for i in range(len(query)//y):
        cost += treap.find_cost(query[i]) * counts[i]

    return cost

def check(t, keys):
    l = t.left
    r = t.right

    if l is not None:
        if l.key in keys:
            if t.key not in keys:
                print("left")
                print(t.key)
                print(l.key)
                return False
        if not (check(l,keys)):
            return False
    if r is not None:
        if r.key in keys:
            if t.key not in keys:
                print("right")
                print(t.key)
                print(r.key)
                return False
        if not (check(r,keys)):
            return False
    return True



if __name__ == '__main__':
    x = [1,2,5]
    trials = 20

    data = "PATH_TO_PREPROCESSED_DATA"
    res =  "PATH_TO_PREDICTION_FILE"

    queries, counts = get_data_aol_query_list([data])

    res = np.load(res)
    results = res['test_output'].squeeze()
    
    idx = np.argsort(counts)[::-1]

    results_ordered = results[idx]
    count_ordered = counts[idx]
    queries_ordered = queries[idx]

    print(sum(counts))
    print(len(counts))

    rb = []
    avl = []
    splay = []
    b = []
    learned = []
    learned_ran = []
    ran = []
    perfect = []
    perfect_ran = []

    for i in range(len(x)):
        cost_rb = 0
        cost_avl = 0
        cost_splay = 0
        cost_b = 0
        cost_learned = 0
        cost_learned_ran = 0
        cost_ran = 0
        cost_perfect = 0
        cost_perfect_ran = 0
        for j in range(trials):
            print(str(i)+ "," + str(j))
            cost_rb += test_rb(queries_ordered, count_ordered, x[i])
            cost_avl += test_avl(queries_ordered, count_ordered, x[i])
            cost_splay += test_splay(queries_ordered, count_ordered, x[i])
            cost_b += test_b(queries_ordered, count_ordered, x[i])
            cost_learned += test(queries_ordered, count_ordered, results_ordered, 0, x[i])
            cost_learned_ran += test(queries_ordered, count_ordered, results_ordered, 0, x[i], shuffle = True)
            cost_ran += test(queries_ordered, count_ordered, results_ordered, 1, x[i])
            cost_perfect += test(queries_ordered, count_ordered, count_ordered, 0, x[i])
            cost_perfect_ran += test(queries_ordered, count_ordered, count_ordered, 0, x[i], shuffle = True)
        
        cost_rb /= trials
        cost_avl /= trials
        cost_splay /= trials
        cost_b /= trials
        cost_learned /= trials
        cost_learned_ran /= trials
        cost_ran /= trials
        cost_perfect /= trials
        cost_perfect_ran /= trials
        
        rb.append(cost_rb)
        avl.append(cost_avl)
        splay.append(cost_splay)
        b.append(cost_b)
        learned.append(cost_learned)
        learned_ran.append(cost_learned_ran)
        ran.append(cost_ran)
        perfect.append(cost_perfect)
        perfect_ran.append(cost_perfect_ran)


    res = dict()
    res['rb'] = rb
    res['avl'] = avl
    res['splay'] = splay
    res['b'] = b
    res['learned'] = learned
    res['learned_ran'] = learned_ran
    res['ran'] = ran
    res['perfect'] = perfect
    res['perfect_ran'] = perfect_ran
    
    pickle.dump(res, open( "results.pkl", "wb" ))
        
    print(res)
