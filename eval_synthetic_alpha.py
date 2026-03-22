from utils.treaps import Treap
from utils.redblack import RedBlackTree
from utils.treaprb import TreapRB
from utils.avl import AVLTree
from utils.splaytree import SplayTree
from utils.btree import BTree
import numpy as np
import random
import pickle


def test(n, alpha):
  pdf = [0]*n

  for i in range(n):
    pdf[i] = 1/((i+1)**alpha)

  s = sum(pdf)

  for i in range(n):
    pdf[i] = pdf[i]/s

  m = np.random.permutation(n)

  treap_ran = Treap()
  treap_learned = Treap()
  rb = RedBlackTree()
  avl = AVLTree()
  splay = SplayTree()
  b = BTree(3)

  order = np.random.permutation(n)

  for i in range(n):
    treap_ran.insert(m[i], random.random())
    treap_learned.insert(m[i], -pdf[i])
    rb.insert(order[i])
    avl.insert(order[i])
    splay.insert(order[i])
    b.insert(order[i])

  
  cost_ran = 0
  cost_learned = 0
  cost_rb = 0
  cost_avl = 0
  cost_splay = 0
  cost_b = 0

  for i in range(10000):
    s = np.random.choice(m, p = pdf)
    cost_ran += treap_ran.find_cost(s)
    cost_learned += treap_learned.find_cost(s)
    cost_rb += rb.find_cost(s)
    cost_avl += avl.find_cost(s)
    cost_splay += splay.find_cost(s)
    cost_b += b.find_cost(s)

  return cost_learned, cost_ran, cost_rb, cost_avl, cost_splay, cost_b





if __name__ == '__main__':
  #testing alpha

  n = [10000]
  alpha = [1, 1.25, 1.5, 2, 3]
  trials = 20

  res_learned = []
  res_ran = []
  res_rb = []
  res_avl = []
  res_splay = []
  res_b = []


  for i in range(len(alpha)):
    cost_ran = 0
    cost_learned = 0
    cost_rb = 0
    cost_avl = 0
    cost_splay = 0
    cost_b = 0
    for j in range(trials):
      learned, ran, rb, avl, splay, b = test(n[0], alpha[i])
      cost_learned += learned
      cost_ran += ran
      cost_rb += rb
      cost_avl += avl
      cost_splay += splay
      cost_b += b
      print(str(i)+","+str(j))
    res_learned.append(cost_learned/trials)
    res_ran.append(cost_ran/trials)
    res_rb.append(cost_rb/trials)
    res_avl.append(cost_avl/trials)
    res_splay.append(cost_splay/trials)
    res_b.append(cost_b/trials)

  res = dict()
  res['rb'] = res_rb
  res['avl'] = res_avl
  res['splay'] = res_splay
  res['b'] = res_b
  res['learned'] = res_learned
  res['ran'] = res_ran

  pickle.dump(res, open( "results.pkl", "wb" ))
      
  print(res)



  


  





  

  