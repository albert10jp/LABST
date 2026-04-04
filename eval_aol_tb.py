from utils.aol_utils import get_data_aol_query_list

import numpy as np
import pickle
import pandas as pd   # ← NEW: for pretty tables

from utils.treaps import Treap
from utils.redblack import RedBlackTree
from utils.avl import AVLTree
from utils.splaytree import SplayTree
from utils.btree import BTree
import random


def test_rb(query, counts, k):
    rb = RedBlackTree()
    y = 100 // k
    order = np.random.permutation(len(query) // y)
    for i in range(len(counts) // y):
        rb.insert(query[order[i]])
    cost = 0
    for i in range(len(counts) // y):
        cost += rb.find_cost(query[i]) * counts[i]
    return cost


def test_avl(query, counts, k):
    avl = AVLTree()
    y = 100 // k
    order = np.random.permutation(len(query) // y)
    for i in range(len(counts) // y):
        avl.insert(query[order[i]])
    cost = 0
    for i in range(len(counts) // y):
        cost += avl.find_cost(query[i]) * counts[i]
    return cost


def test_splay(query, counts, k):
    splay = SplayTree()
    y = 100 // k
    order = np.random.permutation(len(query) // y)
    for i in range(len(counts) // y):
        splay.insert(query[order[i]])
    cost = 0
    for i in range(len(counts) // y):
        cost += splay.find_cost(query[i]) * counts[i]
    return cost


def test_b(query, counts, k):
    b = BTree(3)
    y = 100 // k
    order = np.random.permutation(len(query) // y)
    for i in range(len(counts) // y):
        b.insert(query[i])
    cost = 0
    for i in range(len(counts) // y):
        cost += b.find_cost(query[i]) * counts[i]
    return cost


def test(query, counts, results, mode, k, shuffle=False):
    treap = Treap()
    y = 100 // k
    if shuffle:
        query = np.random.permutation(len(query))
    for i in range(len(query) // y):
        if mode == 0:   # learned / perfect
            treap.insert(query[i], -results[i])
        else:           # random
            treap.insert(query[i], random.uniform(0, 1))
    cost = 0
    for i in range(len(query) // y):
        cost += treap.find_cost(query[i]) * counts[i]
    return cost


if __name__ == '__main__':
    x = [1, 2, 5]      # top 1%, 2%, 5%
    trials = 20

    data = "./data/aol_00XX_len60.npz"
    pred = "./predictions/pred_exp22_aol.npz" # PATH_TO_PREDICTION_FILE

    queries, counts = get_data_aol_query_list([data])
    res_np = np.load(pred)
    results = res_np['test_output'].squeeze()

    idx = np.argsort(counts)[::-1]
    queries_ordered = queries[idx]
    count_ordered = counts[idx]
    results_ordered = results[idx]

    print("Total accesses:", sum(counts))
    print("Distinct queries:", len(counts))

    # Lists for total costs (original behaviour)
    rb, avl, splay, b = [], [], [], []
    learned, learned_ran, ran = [], [], []
    perfect, perfect_ran = [], []

    # Lists for average cost per query
    avg_rb, avg_avl, avg_splay, avg_b = [], [], [], []
    avg_learned, avg_learned_ran, avg_ran = [], [], []
    avg_perfect, avg_perfect_ran = [], []

    for i in range(len(x)):
        k = x[i]
        y = 100 // k
        num_queries = len(counts) // y

        cost_rb = cost_avl = cost_splay = cost_b = 0
        cost_learned = cost_learned_ran = cost_ran = 0
        cost_perfect = cost_perfect_ran = 0

        for j in range(trials):
            print("{},{}".format(i, j))

            cost_rb += test_rb(queries_ordered, count_ordered, k)
            cost_avl += test_avl(queries_ordered, count_ordered, k)
            cost_splay += test_splay(queries_ordered, count_ordered, k)
            cost_b += test_b(queries_ordered, count_ordered, k)

            cost_learned += test(queries_ordered, count_ordered, results_ordered, 0, k)
            cost_learned_ran += test(queries_ordered, count_ordered, results_ordered, 0, k, shuffle=True)
            cost_ran += test(queries_ordered, count_ordered, results_ordered, 1, k)
            cost_perfect += test(queries_ordered, count_ordered, count_ordered, 0, k)
            cost_perfect_ran += test(queries_ordered, count_ordered, count_ordered, 0, k, shuffle=True)

        # Average over trials
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

        # Average per query
        avg_rb.append(cost_rb / num_queries)
        avg_avl.append(cost_avl / num_queries)
        avg_splay.append(cost_splay / num_queries)
        avg_b.append(cost_b / num_queries)
        avg_learned.append(cost_learned / num_queries)
        avg_learned_ran.append(cost_learned_ran / num_queries)
        avg_ran.append(cost_ran / num_queries)
        avg_perfect.append(cost_perfect / num_queries)
        avg_perfect_ran.append(cost_perfect_ran / num_queries)

    # Build results dictionary
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

    res['avg'] = {
        'rb': avg_rb,
        'avl': avg_avl,
        'splay': avg_splay,
        'b': avg_b,
        'learned': avg_learned,
        'learned_ran': avg_learned_ran,
        'ran': avg_ran,
        'perfect': avg_perfect,
        'perfect_ran': avg_perfect_ran
    }

    pickle.dump(res, open("results.pkl", "wb"))

    # ====================== PRETTY PRINTED TABLES ======================

    trees = ['rb', 'avl', 'splay', 'b', 'learned', 'learned_ran', 'ran', 'perfect', 'perfect_ran']

    # Table 1: Total Costs
    df_total = pd.DataFrame({
        tree: res[tree] for tree in trees
    }, index=['Top 1%', 'Top 2%', 'Top 5%']).T
    df_total.columns = ['Top 1%', 'Top 2%', 'Top 5%']

    print("\n" + "="*60)
    print("=== TOTAL NUMBER OF COMPARISONS (lower is better) ===")
    print("="*60)
    print(df_total.round(1).to_string())

    # Table 2: Average Comparisons per Query
    df_avg = pd.DataFrame({
        tree: res['avg'][tree] for tree in trees
    }, index=['Top 1%', 'Top 2%', 'Top 5%']).T
    df_avg.columns = ['Top 1%', 'Top 2%', 'Top 5%']

    print("\n" + "="*60)
    print("=== AVERAGE COMPARISONS PER QUERY (lower is better) ===")
    print("="*60)
    print(df_avg.round(4).to_string())

    print("\nResults saved to results.pkl (both total and avg)")