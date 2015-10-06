from player import Player
from engine import Engine

class CPUPlayer(Player):
    
    def __init__(self, b, n, v, p = [1.0, 1.0, 1.0, 1.0, 1.0]):
        self.b = b
        self.board = b.board
        self.v = v
        self.n = n
        self.p = p
        self.s = b.s
        self.score = 0
        self.games_played = 0
        self.engine = Engine(self.s, n)

    def play(self, x, y):
        r = self.engine.choice(self.v, self.b, self.p)
        self.b.put(r[0][0], r[0][1], self.v)
        
        
        
        
"""
        if r[1] < 10.0**7:
            self.deeper_choice(r)        

    def deeper_choice(self,(x,y)):
        r = self.choice(-self.v, self.p)
        if r[1] > 10.0**7:
            self.b.put(r[0][0], r[0][1], self.v)
            self.b.put(x[0], x[1], 0)
"""

