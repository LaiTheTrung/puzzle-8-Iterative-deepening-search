from tkinter import *
from tkinter import messagebox
import numpy as np
from puzzel import *
import time
_goal_state = '1,2,3,8,0,4,7,6,5' # store state as string for easy to save in dictionary
_init_state = [0,2,3,1,4,5,8,7,6]
def _distance(pos0,pos1):
    return abs(pos0 % 3 - pos1%3) + abs(pos0//3 -pos1 //3)
def Mat2str(array):
    l = array.tolist()
    string = ','.join(str(e) for e in l)
    return string
_algo = {1:"Iterative Deepening Search", 
        2:"Breadth-First Search",
        3:"A* Misplaced Tiles", 
        4:"A* Manhattan Distances"}
class GUI():
    def __init__(self,window,puzzle) -> None:
        self.puzzle = puzzle
        self.win = window
        self._init_state = '' 
        self._goal_state = ''


        #Frame for search chosing
        self.algoFrame = Frame(self.win, width=260, relief=RAISED)
        self.algoFrame.grid(row=0, column=0,columnspan=3)
        self.select = StringVar(self.algoFrame)
        self.select.set(_algo[1]) # default value
        self.option = OptionMenu(self.algoFrame, self.select, _algo[1], _algo[2], _algo[3], _algo[4])
        self.option.grid(row=0, column=0)
        self.labelalgo = Label(self.algoFrame,text='speed from 0-10',font=('Calibri', 10))
        self.labelalgo.grid(row=0,column=1)
        #get speed 
        self.speed = StringVar()
        self.SpeedEntry = Entry(self.algoFrame, textvariable = self.speed, bg='white', font=('Calibri', 10))
        self.SpeedEntry.grid(row=0,column=2)
        #Frame for name:
        self.NameFrame = Frame(self.win, width=260, relief=RAISED)
        self.NameFrame.grid(row=1, column=0,columnspan=3)
        self.NameLabel = [Label(self.NameFrame,font=('Calibri',10)) for i in range(9)]
        nameList = ['start','goal','Running']
        for i in range(3):
            self.NameLabel[i].config(text = nameList[i])
            self.NameLabel[i].grid(row=0,column=i,padx=105)

        #Frame for start
        self.board_start = Frame(self.win, width=260, height=260, bg = 'red',relief=RAISED)
        self.board_start.grid(row=2, column=0)
        self.start_var = [StringVar() for i in range(9)]
        self.label_start = [Label(self.board_start, bg='gray', font=('Calibri', 48)) for i in range(9)]
        self.entry_start = [Entry(self.board_start,textvariable = self.start_var[i], bg='white', font=('Calibri', 10)) for i in range(9)]
        for i in range(3):
            for j in range(3):
                self.label_start[i*3+j].place(x=85*j+5,y=85*i+5, width=80, height=80)
                self.entry_start[i*3+j].place(x=85*j+37,y=85*i+37, width=20, height=20)

        #Frame for goal
        self.board_goal = Frame(self.win, width=260, height=260, bg = 'yellow', relief=RAISED)
        self.board_goal.grid(row=2, column=1)
        self.goal_var = [StringVar() for i in range(9)]
        self.label_goal = [Label(self.board_goal, bg='gray', font=('Calibri', 48)) for i in range(9)]
        self.entry_goal = [Entry(self.board_goal,textvariable = self.goal_var[i], bg='white', font=('Calibri', 10)) for i in range(9)]
        for i in range(3):
            for j in range(3):
                self.label_goal[i*3+j].place(x=85*j+5,y=85*i+5, width=80, height=80)
                self.entry_goal[i*3+j].place(x=85*j+37,y=85*i+37, width=20, height=20)

        #Frame for solving board
        self.board = Frame(self.win, width=260, height=260,bg = 'green', relief=RAISED)
        self.board.grid(row=2, column=2)
        self.var = [StringVar() for i in range(9)]
        self.label = [Label(self.board, textvariable=self.var[i], bg='gray', font=('Calibri', 48)) for i in range(9)]
        for i in range(3):
            for j in range(3):
                self.label[i*3+j].bind("<Button-1>", lambda event: self.move(event))
                self.label[i*3+j].place(x=85*j+5,y=85*i+5, width=80, height=80)

        #Frame for button contact        
        self.buttonFrame = Frame(self.win, relief=RAISED, borderwidth=1)
        self.buttonFrame.grid(row=3, column=0, columnspan=3)
        self.button = []
        self.button.append(Button(self.buttonFrame, width='8', relief=RAISED, text="Reset", command=self.reset))
        self.button.append(Button(self.buttonFrame, width='8', relief=RAISED, text="Shuffle", command=self.shuffle))
        self.button.append(Button(self.buttonFrame, width='8', relief=RAISED, text="Solve", command=self.solve)) # to be initialized
        for b in self.button:
            b.pack(side=LEFT, padx=5, pady=7)

    def getInput(self,get_from_var):
        return_var = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1])
        for i in range(len(get_from_var)):
            input = get_from_var[i].get()
            # print(f'{i}:{input}')
            try:
                int_input = int(input)
                if int_input in _init_state:
                    if not (int_input in return_var):
                        return_var[i] = int_input
                    else:
                         raise Exception('there is a repeat in your input')
                else:
                     raise Exception('input not in range 0 to 9')
            except Exception as e:
                raise(e)
        return Mat2str(return_var)
    
    def display(self):
        color = 'gray' if self.puzzle.state != self._goal_state else 'green'
        state = self.puzzle.state.split(',')
        for i in range(9):
            if state[i] != '0':
                self.var[i].set(str(state[i]))
                self.label[i].config(bg=color)
            else:
                self.var[i].set('')
                self.label[i].config(bg='white')

    def test(self):
        # a = self.getInput(self.start_var)
        print('there is no code here:')
        pass
        

    def move(self,event):
        text = event.widget.cget('text')
        if not text:
            return
        
        pos = self.puzzle.state.index(text)
        pos0 = self.puzzle.state.index('0')
        if _distance(pos0,pos) > 1:
            return

        self.puzzle.swap(pos)
        self.display()

    def reset(self):
        pass
    def shuffle(self):
        pass
    def solve(self):
        self._init_state = self.getInput(self.start_var)
        self._goal_state = self.getInput(self.goal_var)
        self.puzzle.state = self._init_state
        self.puzzle.goalState = self._goal_state
        for b in self.button:
            b.configure(state='disabled')
        self.option.configure(state='disabled')

        run = {1: self.puzzle.solve_by_IDS,
            2: self.test,
            3: self.test,
            4: self.test}

        temp = self.select.get()
        index = 1
        for k,e in _algo.items():
            if e == temp:
                index = k
                break
        
        print('Solving...')
        
        # get solving time
        stime = time.time()
        path, n = run[index]()
        ttime = time.time()

        # if 8-puzzle is unsolvable
        if not path:    
            print('This 8-puzzle is unsolvable!')
            for i in range(9):
                self.label[i].config(bg='red' if self.puzzle.state[i] != '0' else 'white')
            for b in self.button:
                b.configure(state='normal')
            self.option.configure(state='normal')
            return

        info = 'Algorithm: '+_algo[index]+'\n'          + 'Time: '+str(round(ttime-stime, 6))+'s\n'          + 'States Explored: '+str(n)+'\n'          + 'Shortest Path: '+str(len(path)-1)+' steps.'
        print(info)
        self.display_procedure(path)
    def display_procedure(self,path):
        if not path:
            for b in self.button:
                b.configure(state='normal')
            self.option.configure(state='normal')
            return
        self.puzzle.state = path.pop(0)
        self.display()
        try:
            speed = int(self.speed.get())
            if speed > 10:
                speed = 10
            elif speed <0:
                speed = 0
        except:
            speed = 0
        
        self.win.after(int(500/(speed+1)), lambda: self.display_procedure(path))    


