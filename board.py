from random import randint
from engine import Engine

class Board:
    """
    contains the board(2-dim-array), tools to work with it
    and it can chceck if the play is over(someone won)
    """

    def __init__(self, s = 15, n = 5):
        self.board = [[0 for x in range(s)] for x in range(s)]
        self.s = s
        self.n = n
        self.engine = Engine(s, n)
        self.history = []
        self.short_history = []

    def put(self, x, y, v):
        self.board[x][y] = v
        self.history.append([x,y,v])
        self.short_history.append([x,y])

    def get(self, x, y):
        """
        returning of 333 means an error, 333 was chosen artificially
        """
        return self.board[x][y] if x >= 0 and y >= 0 and x < self.s and y < self.s else 333

    def clear(self): 
        """
        puts zeros in the board
        """
        for x in range(self.s):
            for y in range(self.s):
                self.board[x][y] = 0

    def is_end(self):
        return self.engine.is_end(self) 

    def is_full(self):
        for x in self.board:
            for y in x:
                if y == 0: 
                    return False
        return True
    
    def print_board(self):
        a = ''
        for x in self.board:
            a +='\n%s\n'%(str(x))
        return a
                 
                 
def test():
    b = Board(5)

    b.put(0,0,0)
    b.put(0,1,0)
    b.put(0,2,0)
    b.put(0,3,0)
    b.put(1,0,0)
    b.put(2,1,0)
    b.put(3,2,0)
    b.put(3,3,0)
    b.put(1,3,0)
    b.put(2,3,0)
    b.put(3,3,0)
    b.put(3,3,0)
    b.put(3,0,-1)
    b.put(3,1,0)
    b.put(3,2,1)
    b.put(3,3,1)
    b.put(3,4,1)
 #   print(b.list_of_points(1))
#    print(b.lines_horizontal(b.list_of_points(1)))
 #   print(b.lines_vertical(b.list_of_points(1)))
 #   print(b.lines_slanted1(b.list_of_points(1)))
  #  print(b.lines_slanted2(b.list_of_points(1)))
  #  b.show()
   # print(b.max_len_of_line(1))
    #print(b.best_move(1))
    #print(b.lines_hori())
    for x in b.all_combos():
        print(x)
    #print(len(b.all_combos()))
    b.show()

    #print(b.possibilities(1))
    #print(b.choice(1))
    #b.show()

#test()


