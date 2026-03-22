import copy
import random

class Node:
    def  __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None

    def __repr__(self):
        return hex(id(self))
  

class SplayTree: 
    def __init__(self):
        self.root = None

    def compare(self, x, y):
        if x < y:
            return -1
        if x > y:
            return 1
        return 0

    def insert(self, data):
        new_node = Node(data)
        if self.root == None:
            self.root = new_node
        else:
            curr_node = self.root
            curr_parent = None
            while(curr_node != None):
                comp = self.compare(new_node.data,curr_node.data)
                if comp == 0:
                    return
                elif comp < 0:
                    curr_parent = curr_node
                    curr_node = curr_node.left
                elif comp > 0:
                    curr_parent = curr_node
                    curr_node = curr_node.right
            if comp < 0:
                curr_parent.left = new_node
            elif comp > 0:
                curr_parent.right = new_node
            new_node.parent = curr_parent
            self.splay(new_node)


    def __search_tree_helper(self, node, key):
        if node == None:
            return (0, None)

        comp = self.compare(key,node.data)

        if comp == 0:
            return (0,node)

        if comp < 0:
            (cost, node) = self.__search_tree_helper(node.left, key)
            return (cost+1, node)

        (cost, node) = self.__search_tree_helper(node.right, key)
        return (cost+1, node)
            

    # rotate left at node x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def right_rotate(self, x):  
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x
        
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        y.right = x
        x.parent = y

    # Splaying operation. It moves x to the root of the tree
    def splay(self, x):
        while x.parent != None:
            p = x.parent
            g = x.parent.parent

            if g == None:
                if x == p.left:
                    # zig rotation
                    self.right_rotate(p)

                else:
                    # zag rotation
                    self.left_rotate(p)


            elif x == p.left and p == g.left:
                # zig-zig rotation
                self.right_rotate(x.parent.parent)
                self.right_rotate(x.parent)


            elif x == p.right and p == g.right:
                # zag-zag rotation
                self.left_rotate(x.parent.parent)
                self.left_rotate(x.parent)

            elif x == p.right and p == g.left:
                # zig-zag rotation
                self.left_rotate(x.parent)
                self.right_rotate(x.parent)

            else:
                # zag-zig rotation
                self.right_rotate(x.parent)
                self.left_rotate(x.parent)

    # search the tree for the key k
    # and return the corresponding node
    



    def access_splay(self, k):
        (cost, x) = self.__search_tree_helper(self.root, k)
        self.splay(x)
        return (cost, x)

    def access(self, k):
        return self.__search_tree_helper(self.root, k)

    def find_cost(self, k):
        (cost, x) = self.access_splay(k)
        return cost

if __name__ == "__main__":
    t = Tree()
    for i in range(200):
        t.insert(i)

    for i in range(1000):
        k = random.randint(0,199)
        print(k)
        (a,b,c) = t.access(k, -1)
        t.splay(b)
        
    t.access_splay(0)

