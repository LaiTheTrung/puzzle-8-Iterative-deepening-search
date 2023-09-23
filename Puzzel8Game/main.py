from puzzel import *
from GUI import *
from tkinter import *
win = Tk()
win.geometry('800x400')
win.title('8-Puzzle')
puzzle = Eight_Puzzel()
GUI(win,puzzle)
win.mainloop()
