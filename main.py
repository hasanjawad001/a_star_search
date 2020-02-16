"""
In addition to coding of A* search algorithm, provide state space representation, operators,
g (cost) and two heuristic functions of the 8-puzzle problem. Your program should accept
initial and goal states from user and will compute the best path. You will turn in the
following as hard copy directly to me in the class, in addition to submitting everything in
canvas:
● A report covering 8-puzzle problem formulation, program structure, global variables,
functions and procedures, etc. [10 points]
● Analyze six input/output cases:
○ For each input/output sample, for each heuristic report the following: (1) The
solution path from initial state to goal state (2) the number of nodes generated,
and (3) the number of nodes expanded.
■ For each heuristic (6 x (1.5 + 1.5 + 1.5)) = 27 points
■ Total 54 points [27 + 27]
○ Summarize the results in a table. [6 points]
● Error free source code with adequate inline documentation.
● Quality of the report and code (e.g. taking user input) [5 points]
Sample initial and goal states:
"""

import math

class Node:
    def __init__(self, state=None, depth=None, f=None, g=None, h=None):
        self.state = state
        self.depth = depth
        self.f = f
        self.g = g
        self.h = h

    def print_state(self):
        for row in self.state:
            for col in row:
                print(col, end=" ")
            print()
        return ""

class Puzzle:
    def __init__(self, no_tiles=8):
        self.n = int(math.sqrt(no_tiles+1))
        self.frontier = []
        self.explored = []

    def get_state(self, state_name='', file_name=''):
        lines = []
        with open(file_name) as f:
            lines = f.readlines()
            state = [line.strip('\n').split(' ') for line in lines]
        if state_name=='initial':
            self.initial_state = state
            self.initial_node = Node(self.initial_state, 0, None, 0, None)
        elif state_name=='goal':
            self.goal_state = state
            self.goal_node = Node(self.goal_state, None, None, None, 0)

    def get_g_score(self, source, dest):
        return source.depth

    def get_h_score(self, source, dest):
        h_score = 0
        if self.heuristic == 1:
            for i in range(self.n):
                for j in range(self.n):
                    if source.state[i][j] != '0' and source.state[i][j] != dest.state[i][j]:
                        h_score += 1
        if self.heuristic == 2:
            #TODO: inplement
            pass
        return h_score

    def get_f_score(self, source, dest):
        return self.get_g_score(source, dest) + self.get_h_score(source, dest)

    def get_location(self, state, elem):
        for r in range(self.n):
            for c in range(self.n):
                if state[r][c] == elem:
                    return r,c

    def swap_elem(self, state, r1, c1, r2, c2):
        new_state = []
        for row in state:
            new_row = []
            for col in row:
                new_row.append(col)
            new_state.append(new_row)
        temp = new_state[r1][c1]
        new_state[r1][c1] = new_state[r2][c2]
        new_state[r2][c2] = temp
        return new_state

    def expand(self, current_node):
        r_blank, c_blank = self.get_location(current_node.state, '0')
        possible_options = [[r_blank, c_blank+1], [r_blank-1, c_blank], [r_blank, c_blank-1], [r_blank+1, c_blank]]
        possible_children = []
        for opt in possible_options:
            r = opt[0]
            c = opt[1]
            if r >= 0 and c >= 0 and r <= self.n-1 and c <= self.n-1:
                possible_children.append(opt)
        children = []
        for pc in possible_children:
            child_state = self.swap_elem(current_node.state, r_blank, c_blank, pc[0], pc[1])
            child_node = Node(child_state, current_node.depth+1, None, current_node.depth+1, None)
            children.append(child_node)
        return children

    def run(self, heuristic=1):
        self.heuristic = heuristic
        self.initial_node.f = self.get_f_score(self.initial_node, self.goal_node)
        self.frontier.append(self.initial_node)
        while len(self.frontier) != 0:
            current_node = self.frontier[0]
            self.frontier.remove(current_node)
            print(current_node.print_state())
            print()
            print()
            if self.is_goal(current_node):
                print('Goal State Reached!!!')
                return
            children = self.expand(current_node)
            for child in children:
                child.f = self.get_f_score(child, self.goal_node)
                self.frontier.append(child)
            self.frontier.sort(key=lambda x: x.f, reverse=False)
            self.explored.append(current_node)

    def is_goal(self, node):
        if self.get_h_score(node, self.goal_node) == 0:
            return True
        else:
            return False

if __name__=="__main__":
    p = Puzzle(no_tiles=8)
    p.get_state(state_name='initial', file_name='initial_state.txt')
    p.get_state(state_name='goal', file_name='goal_state.txt')

    ''' using heuristic 1 '''
    print('Using heuristic 1: Miss-placed Tiles')
    p.run(heuristic=1)

    ''' using heuristic 2 '''
    print('Using heuristic 2: Manhattan Distance')
    p.run(heuristic=2)