class Engine:
    """
    contains algorithms to make decisions(for cpu player) 
    """
  
    def __init__(self, s, n):
        self.s = s
        self.n = n
        self.c = self.combine_data()

    def list_of_points(self, b, v):
        """
        creates list of points of the board that have certain value
        """
        ls = []
        for x in range(self.s):
            for y in range(self.s):
                if b.board[x][y] == v:
                    ls.append((x,y))
        return ls

    def lines_hori(self):
        """
        creates list of lists, in witch points of the board are grouped 
        into horizontal lines
        """
        prelist = [[] for x in range(self.s)]
        for x in range(self.s):
            for y in range(self.s):
                prelist[x].append([x,y])
        return prelist

    def lines_verti(self):
        """
        creates list of lists, in witch points of the board are grouped 
        into vertical lines
        """
        prelist = [[] for x in range(self.s)]
        for x in range(self.s):
            for y in range(self.s):
                prelist[y].append([x,y])
        return prelist

    def lines_slan1(self):
        """
        creates list of lists, in witch points of the board are grouped 
        into slanted lines
        """
        prelist = [[] for x in range(self.s*2 - 1)]
        for x in range(self.s):
            for y in range(self.s):
                prelist[x + y].append([x,y])
        return prelist

    def lines_slan2(self):
        """
        creates list of lists, in witch points of the board are grouped 
        into slanted lines
        """
        prelist = [[] for x in range(self.s*2 - 1)]
        for x in range(self.s):
            for y in range(self.s):
                prelist[x - y + self.s - 1].append([x,y])
        return prelist

    def combine_data(self):
        """
        combines all possible lines into one list
        """
        return (self.lines_hori() + self.lines_verti() + 
                self.lines_slan1() + self.lines_slan2())

    def all_combos(self, b):
        """
        overcomplicated algorithm that creates list of what I call combo,
        combo consists of folowing fields of value 0(empty) or certain
        value i.e. 0 1 1 1 0 0 0 or 1 1 0 0 0 or 0 0 1 1 1 1
        the list that is the result of this function is made of structures
        like this: ([0,0,0,0],[]) first int is value of points in the combo
        second is number of empty fields in the beggining
        third is number of fields of one value 
        fourth is number of empty fields at the end
        and the list is a list of points in the combo
        the combo 0 1 1 0 would be represented like this:
        ([1,1,2,1],[(x,y)... ...(xn,yn)])
        """
        l = self.c
        res = []    
        second = False
        # first list in t1 & t2 consists of, value, 
        # last three values are lengths of subsequent parts
        for x in l:
            t1 = ([0,0,0,0],[])
            t2 = ([0,0,0,0],[])
            for y in x:
                v = b.get(y[0], y[1])
                if t1[0][0] != v and t1[0][0] != 0 and v != 0:
                    if t1[1] and t1[0][0] != 0 and (t1[0][1] + t1[0][2] + t1[0][3] >= self.n):
                        res.append(t1)
                    t1 = t2
                    t2 = ([0,0,0,0],[])
                if t1[0][0] == 0:
                    t1[1].append(y)
                    t1[0][0] = v
                    if v == 0: 
                        t1[0][1] += 1
                    else: 
                        t1[0][2] += 1
                else:
                    if t1[0][0] == v and t1[0][3] == 0:
                        t1[1].append(y)
                        t1[0][2] += 1 
                    elif v == 0:
                        t1[1].append(y)
                        t1[0][3] += 1
                        t2[1].append(y)
                        t2[0][1] += 1
                    elif t1[0][0] == v and t1[0][3] != 0:
                        t2[1].append(y)
                        t2[0][2] += 1
                        t2[0][0] = v
                        if t1[1] and t1[0][0] != 0 and (t1[0][1] + t1[0][2] + t1[0][3] >= self.n): 
                            res.append(t1)
                        t1 = t2
                        t2 = ([0,0,0,0],[])
                        
            if t1[1] and t1[0][0] != 0 and (t1[0][1] + t1[0][2] + t1[0][3] >= self.n):
                res.append(t1)
            if t2[1] and t2[0][0] != 0 and (t2[0][1] + t2[0][2] + t2[0][3] >= self.n):
                res.append(t2)
        return res   
          
                    
    def possibilities(self, v, b):
        """
        creates list of combos(check method above) for every possible move
        """
        zerols = self.list_of_points(b, 0)
        res = []
        for x in zerols:
            b.put(x[0], x[1], v)
            res.append((x,self.all_combos(b)))
            b.put(x[0], x[1], 0)
        return res

    def evaluate(self,a,b,c,d,v,p):
        """
        puts a value on a combo, says what is good and what is bad
        bigger value means better combo.
        a, b, c and d are paramethers of combo
        p is not used currently it was ment for putting diffrent
        settings in this method
        v is value of player, meaning player 1 or -1
        """
        val = 1.0
        if v == a:
            if c >= self.n: 
                val = self.n*10.0**13
            elif c + 1 == self.n and min(b,d) >= 1:
                val = self.n*10.0**9 
            else: 
                for i in range(c):
                    val *= 5.0
                for i in range(min(b,d)):
                    val *= 3.0
                for i in range((b+d)/2):
                    val *= 1.3
        elif v == -a:
            if c + 1 == self.n and b + d >=1:
                val = self.n*-10.0**11
            elif c + 2 == self.n and min(b,d) >= 1 and max(b,d) >= 2:
                val = self.n*-10.0**7
            else: 
                val = -1.0
                for i in range(c):
                    val *= 5.0
                for i in range(min(b,d)):
                    val *= 3.0
                for i in range((b+d)/2):
                    val *= 1.3
        return val

    def value_list(self, v, b, p):
        """
        creates a list of tuples of move and its value
        """
        ls = self.possibilities(v, b)
        valls = []
        for x in ls:
            val = 0.0
            for y in x[1]:
                val += self.evaluate(y[0][0],y[0][1],y[0][2],y[0][3],v, p)
            valls.append((x[0],val))
        return valls

    def choice(self, v, b, p):
        """
        returns move with highest value
        """
        ls = sorted(self.value_list(v, b, p), key=lambda tup: tup[1])
        return ls[-1]
        
    def is_end(self, b):
        ls = self.all_combos(b)
        for x in ls:
            if x[0][2] == self.n:
                return True 
        return False 
    

