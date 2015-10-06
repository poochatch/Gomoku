from timeit import timeit, repeat
from func_evaluate import *
from board import Board
##from bobby import RobertFischer

# test data

imm_dat = [   [0,1,1,1,1],
              
              [0,0,0,0,0,1,0,-1,0,1,1,0,0,0],
              [0,0,0,0,-1,-1,-1,-1,0,1,1],
              
              [0,0,0,0,0,-1-1-1,0,1,1,1,-1,-1],
              [0,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
              
              [0,0,-1,1,0,0,1,1,-1,0,1,1,1],
              [0,0,0,0,-1,0,1,1,1,0,-1,-1,-1],
              
              [0,1,1,1,-1],
              [0,1,-1,1,1,0,1,-1],
              
              [0,0,0,0,-1,0,1,1,0,1,1,-1,0,0],
              [0,-1,1,1,0,1,1,-1,-1,-1,1,0,0,0],
              
              [0,0,-1,1,1,1,1,0,-1,-1,-1,1,0,0,0],
              [0,0,1,1,1,1,-1,-1,-1,-1,0],

              [0,1,0,1,0,1,0,1,0],
              [1,0,1,0,1,0,1,0,1],
             
              [0,0,1,1,0,1,-1],
              [0,-1,-1,0,1,0,0,1,1,0,0]

              ]
imm_ans= [1, 0,0, 0,0, 0,1, 0,0, 1,1, 1,1, 0,0, 0,0]

imm_time = [0,0,-1,1,1,1,1,0,-1,-1,-1,1,0,0,0]
imm_time2 = [0] * 15*15


eval_data = {'history': [[9,9,1], [8,9,-1], [8,10,1], [9,8,-1],
                         [7,11,1], [6,12,-1], [10,8,1],[11,7,-1],
                         [12,6,-1], [10,8,1], [11,7,-1],[7,10,1],
                         [9,7,-1], [9,5,1], [6,11,-1]],
             'short_history': [[9, 9], [8, 9], [8, 10], [9, 8],
                               [7, 11], [6, 12], [10, 8], [11, 7],
                               [12, 6], [10, 8], [11, 7], [7, 10],
                               [9, 7], [9, 5], [6, 11]]

             }

##b = Board()
##b.history = eval_data['history']
##bob = RobertFischer(b,1,5)
##updt = bob.reset_globals(game= False)
##lines = updt[0]
##lines_det = updt[1]


# fuctions - corectness

def test_for(e,data):
    returned = []
    for x in data:
        returned.append(e.if_won(x,1))
    print 'is OK (immidiate, five):',imm_ans == returned
    for x in xrange(len(imm_ans)):
        print x,data[x],returned[x],imm_ans[x]
    print returned



def test_eval(*args, **kwargs):
    pass
    

    

# time complexity

set_imm_five = """

from func_evaluate import Evaluate
from __main__ import imm_time, imm_dat, eval_data
e = Evaluate()

"""


set_position_check = """

from func_evaluate import Evaluate, Iterate
from __main__ import imm_time, imm_dat, eval_data
e = Evaluate()
i = Iterate(e)

reset = i.reset_globals(eval_data['history'])
game_state = i.updt_ln(reset[0], reset[1], reset[2], reset[3])

field = game_state[0]
v = game_state[1]
lines = game_state[2]
lines_det = game_state[3]
c = 0
r = 0

"""


set_eval = """

from func_evaluate import Evaluate
from __main__ import *

"""



stmt_position_check = """
r+= 1

if e.evaluate(field, v, lines, lines_det):
    c+= 1

if r == 999:
    print c

"""
##print '_______________________timeit\n'
##
##a = timeit('e.five(imm_time,1)',setup=set_imm_five,number=10000)
##g = timeit('e.immidiate(imm_time,1)',setup=set_imm_five,number=10000)
##c = timeit('e.check_line(imm_time,1)',setup=set_imm_five,number=10000)
##d = timeit('e.if_won(imm_time,1)',setup=set_imm_five,number=10000)
##f = timeit(stmt = stmt_position_check, setup = set_position_check,number=1000)
##g = timeit('i.stay_close(eval_data[\'history\'])',setup=set_position_check, number=10000)
##h = timeit('i.updt_ln(field,v,lines, lines_det)',setup=set_position_check, number=10000)
##print 'time measure of low level evaluation functions, passing a single line 10 000 times'
##print 'time: five',a
##print 'time: immidiate',g
##print 'time: check_line',c
##print 'time: if_won',d
##print 'time: stay_close',g
##print 'time: updt_ln',h
##
##print '\ntime measure of checking 1000 times wheter a position from 15-ply game is won'
##print 'time:', f

print '\n\n_______________________corectness_check\n\n'


# calls
b = Board()
b.history = eval_data['history']
b.short_history = eval_data['short_history']
p = Garry(1,b)
print 'play',p.play()
##e.immidiate([0,1,1,1,1],1)
##test_for(e,imm_dat)

