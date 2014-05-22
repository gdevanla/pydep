#!/usr/bin/python
from collections import defaultdict
import pickle

g = dict({'u': ['v', 'x'],
          'v': ['y'],
          'x': ['v'],
          'y': ['x'],
          'w': ['y', 'z'],
          'z': ['z']})

ind = defaultdict(int)
inv_ind = [k for k in g.keys()]

color = ['WHITE' for i in g.keys()]
btime = [0 for i in g.keys()]
ftime = [0 for i in g.keys()]
parent = [-1 for i in g.keys()]
other_info = defaultdict(list)


S = list()

def dfs():
    current_t = 0
    for n1 in g.keys():
        if color[ind[n1]] == 'WHITE':
            color[ind[n1]] = 'GRAY'
            current_t = current_t + 1
            btime[ind[n1]] = current_t
            S.append(n1)
            while (S):
                n = S[-1]
                if color[ind[n]] == 'RED':
                    color[ind[n]] = 'BLACK'
                    current_t = current_t + 1
                    ftime[ind[n]] = current_t
                    S.pop(-1)
                else:
                    for c in g[n]:
                        if color[ind[c]] == 'WHITE':
                            color[ind[c]] = 'GRAY'
                            current_t = current_t + 1
                            btime[ind[c]] = current_t
                            S.append(c)
                            parent[ind[c]] = ind[n]
                    color[ind[n]] = 'RED'

def build_index():
    global ind
    i = 0
    #print g.keys()
    for k in g.keys():
        ind[k] = i
        i = i + 1
    #print ind

def print_node(l):
    p = parent[l]
    if p == -1:
        print inv_ind[l]
        return 1
    else:
        level = print_node(p)
        s = inv_ind[l].rjust(level + 10)
        print ' '.ljust(level * 2) + s + ":" + ",".join([i for i in other_info[inv_ind[l]]])
        return level + 1

def print_from_parent(l, level=0):
    p = parent[l]
    s = inv_ind[l] #.rjust(level + 25)
    print ' '.ljust(level * 5) + s + ":" + ",".join([i for i in other_info[inv_ind[l]]])
    if p == -1:
        #print inv_ind[l]
        return 1
    else:
        #s = inv_ind[l].rjust(level + 10)
        #print ' '.ljust(level * 2) + s + ":" + ",".join([i for i in other_info[inv_ind[l]]])
        print_from_parent(p, level + 1)

def prepare_for_print(n, l):
    p = parent[n]
    s = inv_ind[n] #.rjust(level + 25)
    l[-1].append((s, other_info[inv_ind[n]]))
    if p == -1:
        return -1
    else:
        prepare_for_print(p, l)

def print_list(l):
    sorted_list = sorted(l, key=lambda x: x[0][0])
    for i in sorted_list:
        d = 0
        for j in i:
            if d == 0:
                print '+',  #add marker to begining
            print ' '.ljust(d * 5) + j[0] + ":" + ",".join([i for i in j[1]])
            d = d + 1


def print_tree():
    leaf_nodes = sorted([i for i in ind.values() if i not in parent], key=lambda x: inv_ind[x])
    #print 'leaf nodes=', leaf_nodes
    l = []
    for n in leaf_nodes:
        #print_node(l)
        l.append([])
        prepare_for_print(n, l)
    print_list(l)

def print_deps():
    build_index()
    #print ind
    dfs()
    #print inv_ind
    #print ind
    #print color
    #print btime
    #print ftime
    #print parent

    print_tree()

def print_from_file():
    global ind, inv_ind, color, btime, ftime, parent, g
    g1 = pickle.load(open('dependency_list'))

    #print g1.keys()

    g = defaultdict(list)
    for k, v in g1.iteritems():
        g[k] = [i[0] for i in v]
        for i in v:
            #print i[1], i[2][0]
            other_info[i[0]].append(":".join([i[1], str(i[2][0])]))

    ind = defaultdict(int)
    inv_ind = [k for k in g.keys()]

    color = ['WHITE' for i in g.keys()]
    btime = [0 for i in g.keys()]
    ftime = [0 for i in g.keys()]
    parent = [-1 for i in g.keys()]

    print_deps()

if __name__ == '__main__':
    print_from_file()
