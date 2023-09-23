import copy
import random
import numpy as np

_goal_state = '1,2,3,8,0,4,7,6,5' # store state as string for easy to save in dictionary
_init_state = '0,2,3,1,4,5,8,7,6'
cutoff = False
# Node worker
class Node():
    def __init__(self, state, level, cost):
        self.state = state #state is a string '0,1,2,3,4,5,6,7,8'
        self.cost = cost
        self.level = level
    def find(self, x):
        # Specifically used to find the position of the 0 space
        index = self.state.split(',').index(str(x))
        i = index // 3
        j = index % 3
        return i,j
    
def MovePuzz(pre_node,x,y,x1,y1):
    State_Mat = copy.copy(pre_node.state)
    State_Mat = State_Mat.split(',')
    State_Mat[y*3+x] = State_Mat[y1*3+x1]
    State_Mat[y1*3+x1] = '0'
    State_Mat = ','.join(State_Mat)
    # create new Child
    new_node = Node(State_Mat,pre_node.level +1, 1)   
    return new_node

def generate_child_node(node):
    # Generate hild nodes from the given node by moving the blank space
    # either in the four direction {up,down,left,right}
    pre_node = copy.deepcopy(node)
    y, x = pre_node.find(0)
    # val_list contains position values for moving the blank space in either of
    # the 4 direction [up,down,left,right] respectively.
    act_list = [np.array([x, y - 1]), np.array([x, y + 1]), np.array([x - 1, y]), np.array([x + 1, y])]
    children = []
    for act in act_list:
        if (np.sum((act>=0) * (act<3))<2): # if any of act < 0 ==> return 0, (0+1 = 1 <2) ==> continue 
            continue
        child_node = MovePuzz(pre_node,x,y,act[0],act[1])
        children.append(child_node)
        # print('action')
        # print(act)
        #Switch the position of 0
    return children

# Problem solver
class Problem():
    def __init__(self,start = None, goal = None) -> None:
        if start is None:
            start = _init_state
        if goal is None:
            goal = _goal_state
        self.start = start
        self.goal = goal
    def GOAL_TEST(self,node_state):
        if node_state == self.goal:
            return True
        else:
            return False
    def  ACTION(self,node):
        return generate_child_node(node)
    
class IDS():
    def __init__(self,problem,limited = 5) -> None:
        self.problem = problem
        self.limited = limited
        self.Solution = []
        self.startNode = Node(problem.start,level=0, cost= 1) 
        self.frontier=[]
        self.explored = []
        self.solved = False
        self.previous = {self.startNode.state:None} # save the path that search go through
        self.nodeInLastDepth = [self.startNode]
    # backward from the goal to the start to get solution
    def retrival_path(self):
        self.Solution = [self.problem.goal]
        current = self.problem.goal
        while self.previous[current]:
            self.Solution.insert(0,self.previous[current].state)
            print("level: ",self.previous[current].level)
            current = self.previous[current].state

    def DLS(self,limit):
        if limit == 0:
            return 
        self.nodeInLastDepth = []
        poss = 0
        while (not self.solved) and (len(self.frontier) > 0):
            node = self.frontier.pop()
            print('----------------------')
            print(node.state)
            print('======================')
            self.explored.append(node.state) 
            for child in self.problem.ACTION(node):
                if not (child.state in set(self.explored + [knownnode.state for knownnode in self.frontier])): 
                    self.previous[child.state] = node # save the path that the system go through
                    if self.problem.GOAL_TEST(child.state):
                        self.solved =True
                        print('final depth:',child.level)
                        return
                    if child.level >= limit: # stop digging deeper
                        print('child state:', child.state)
                        poss+=1
                        self.nodeInLastDepth.insert(0,child)
                    else:
                        print('child state:', child.state)
                        self.frontier.append(child) 
        print('poss=',poss)
            
                    
    def search(self,step):
        while not self.solved:
            self.limited += step
            print('\n\ndepth:',self.limited-1)
            self.frontier = self.nodeInLastDepth
            self.DLS(self.limited)
        if self.solved:
            print("retrival_start")
            self.retrival_path()
            print("retrival_end")    
                
    

ref_state = '0,1,2,3,4,5,6,7,8'
def shuffle_string(string):
    state_list = string.split(',')
    random.shuffle(state_list)
    state = ','.join(state_list)
    return state
class Eight_Puzzel():
    def __init__(self, input_state=None, goal = None):
        if input_state:
            self.state = input_state
        else:       
            # generate a solvable state randomly
            self.state = shuffle_string(ref_state)
        if goal:
            self.goalState = goal
        else:       
            # generate a solvable state randomly
            self.goalState = shuffle_string(ref_state)

    def shuffle(self):
        self.state = shuffle_string(self.state)
    def solve_by_IDS(self):
        self.P = Problem(self.state, self.goalState)
        solver = IDS(problem= self.P,limited=0)
        solver.search(step=1)
        return solver.Solution, len(solver.explored)
# puzzel = Eight_Puzzel(_init_state,_goal_state)
# solution, path = puzzel.solve_by_IDS()
# for action in solution:
#     print(action)
# print("total step:",path)
        

        