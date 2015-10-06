"""
main module of the programe
this is a game of gomoku, player who gets n of points in the line first
wins

this module:
contains the main loop of the game, gui and some extra methods 
that are not used in this moment
in every module s is size of the board and n is number of points in the 
line that make you the winner
"""

import sys
import os
import board
import Tkinter as tk
from random import uniform, randint
from operator import itemgetter
from cpu_player import CPUPlayer
from human_player import HumanPlayer

s = 15
n = 5
name = "default"
b = None
btn =  None
plrs = None


def play(x,y):
    """
    main method of the game, activated by push of button
    """

    if b.get(x,y) == 0:
        for plr in plrs:
            plr.play(x,y)
            refresh()
            if b.is_end() or b.is_full(): 
                    b.clear()
                    plr.won()
                    refresh()
                    #tv[0].set('Score: ' + str(plrs[0].get_score()) + ' : ' + str(plrs[0].get_score()))
                    break

def refresh():
    """
    used to refresh colours of buttons, acording to board
    """
    for x in range(s):
        for y in range(s):
            if b.board[x][y] == 1:
                btn[x][y].config(bg="red")
            elif b.board[x][y] == -1:
                btn[x][y].config(bg="blue")
            else :
                btn[x][y].config(bg="white")
                
def menu_page():
    root = tk.Tk()
    root.title("menu")
    btns = []
    btns.append(tk.Button(root, text="settings", command= lambda: settings_page()))
    btns.append(tk.Button(root, text=" scores ", command= lambda: scores_page()))
    btns.append(tk.Button(root, text="  play  ", command= lambda: play_page()))
    
    lab1 = tk.Label(root, text="------------------------------\n-------------GOMOKU-----------\n------------------------------")
    lab1.pack()
    for b in btns:
        b.pack()
    root.mainloop()
    
def settings_page():
    top = tk.Toplevel()
    top.title("settings")
    
    slid1 = tk.Scale(top, from_=3, to=25, orient=tk.HORIZONTAL)
    slid2 = tk.Scale(top, from_=3, to=25, orient=tk.HORIZONTAL)
    slid1.set(s)
    slid2.set(n)
    
    lab1 = tk.Label(top, text="size")
    lab2 = tk.Label(top, text="----------------- \n n to win")
    lab3 = tk.Label(top, text="-----------------")
    lab4 = tk.Label(top, text="write your name")

    b1 = tk.Button(top, text="save", command= lambda: 
                   save_params(slid1.get(), slid2.get(), e1.get(), top))
    
    e1 = tk.Entry(top)
    e1.insert(0, name)

    lab4.pack()
    e1.pack()
    lab1.pack()
    slid1.pack()
    lab2.pack()
    slid2.pack()
    lab3.pack()
    b1.pack()

    
def save_params(s1, n1, name1, top):
    if s1 >= n1:
        global s, n, name
        s = s1
        n = n1
        name = name1
        top.destroy()
    else:
        popupmsg("n cannot be greater than size")
    
def scores_page():
    pass

def play_page():
    #initializing variables
    global btn, b, plrs
    btn =  [[0 for x in xrange(s)] for x in xrange(s)]
    b = board.Board(s, n)
    plrs = [HumanPlayer(b, n, 1), CPUPlayer(b, n, -1)]
    
    top = tk.Toplevel()
    top.title("gomoku")

    frame=tk.Frame(top)
    frame.grid(row=0,column=0)
    
     
    for x in range(s):
         for y in range(s):
            btn[x][y] = tk.Button(frame, command= lambda (i,j) = (x,y): play(i,j))
            btn[x][y].grid(column=y, row=x)

    refresh()
    
    
def popupmsg(msg):
    popup = tk.Toplevel()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    
    

menu_page()
 
        
        
