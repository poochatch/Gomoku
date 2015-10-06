class Player:
    """
    basic class of player, needs to be extended

    in classes derived from this one, only method play must be implemented 
    """
    
    def __init__(self, board, n, v):
        self.board = board
        self.v = v
        self.n = n
        self.s = board.s
        self.score = 0
        self.games_played = 0

    def play(self, x, y):
        """
        in this method player accepts position from mouse click if the player is human
        to work properly in implementation you must put your move on the board
        with Board.put(x, y, v)
        """
        pass          

    def won(self):
        self.score += 1
        self.games_played += 1

    def lost(self):
        self.score -= 1
        self.games_played += 1
    
    def get_score(self): return self.score

    def get_games_played(self): return self.games_played

    

