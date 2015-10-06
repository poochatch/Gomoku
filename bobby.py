from player import Player
from random import randrange
import engine
import board
"""
b - instancja klasy board?
v - identyfikator gracza

"""
s = 15
n = 5
o = 1 # outline`s capacity
W = 5.0 # wieght unit of random game that was won

horizon = 5 # n of random moves in a game
events = 100 # n of random games per field

def rand_move(area,v):
    x = randrange(area[0],area[2]+1)
    y = randrange(area[1],area[3]+1)
    return [x,y,v]

    
def create_lines(printed=False,zero=False):
    e = engine.Engine(s,n)
    commands = ['lines_hori','lines_verti','lines_slan1','lines_slan2']
    lines = []
    for x in commands:
        lines.append(getattr(e,x)())
        if printed:
            c = 0
            for y in lines:
                for x in y:
                    print c, x
                    c+=1

    return lines




class RobertFischer(Player):

    def __init__(self, b,v,n):
        self.outline = [8,8,8,8]
        self.b = b
        self.board=b.board
        self.v = v
        self.n = n
        # self.lines = [[],[],[],[]] # 0: hor, 1: ver, 2: upright, 3: upleft
        # self.lines_det = [[[0]]*s,[[0]]*s,[[0]]*(s*2-1),[[0]]*(s*2-1)]
        self.area = []
        self.big_area = []
        self.score = 0
        self.keep_iter = True



    def updt_ln(self, field, v, lines, lines_det, iterating):
        #print 'updt_ln',field,v
        s_min = s - 1
        temp = [0] * s

        # LOOP UPDATING HORIZONTAL AND VERTICAL LINES
        for x in range(2):
            if field[x] not in lines[x]:
                lines_det[x][field[x]] = list(temp)
            lines_det[x][field[x]][field[int(not x)]] = v
            if self.check_line(lines_det[x][field[x]],v) and iterating:
                # print 'horver check_line True'
                # print lines_det[x][field[x]]
                return W if v == self.v else -W/2

            lines[x].append(field[x])
            lines[x] = set(lines[x])
            lines[x] = list(lines[x])


        # DATA CALCULATIONS OF DIAGONAL LINES
        idx_r = sum(field[:2])
        if field[0] >= field[1]:
            idx_l = s_min - field[0] + field[1]
            y = int(s_min)
        else:
            idx_l = s_min + field[1] - field[0]
            y = field[1] - field[0]
        idx_l = s_min - field[0] + field[1] if \
                    field[0] >= field[1] else s_min + field[1] - field[0]

        f_idx_r = field[0] - 1 if idx_r < s else s_min -field[1] - 1

        f_idx_l = field[1] if field[0] >= field[1] else field[0]

        leng_r = idx_r if idx_r < s else s_min - (idx_r -s)
        leng_l = y + 1 if  field[0] >= field[1] else s_min + y + 1

        vals = [leng_r, leng_l, idx_r, idx_l, f_idx_r, f_idx_l]

        # LOOP UPDATING DIAGONAL LINES
        for x in range(2,4):
            temp = [0] if vals[x-2]==0 else [0] * vals[x-2]
            if vals[x] not in lines[x]:
                lines_det[x][vals[x]] = list(temp)
                lines_det[x][vals[x]][vals[x+2]] = v
            if self.check_line(lines_det[x][vals[x]],v) and iterating:
                # print 'diag check_line True'
                # print lines_det[x][vals[x]]
                return W if v == self.v else - W/2

            lines[x].append(vals[x])
            lines[x] = set(lines[x])
            lines[x] = list(lines[x])
        # print lines
        # for x in range(4):
        #     print lines_det[x]
        # print len(lines_det)
        return lines, lines_det

        
                     





    def random_game(self,data):
        lines = data[0]
        lines_det = data[1]
        v = int(self.v)
        score = 0
        for x in range(horizon):
            v = -v
            field = rand_move(self.outline,v) 
            update = self.updt_ln(field,v,lines,lines_det,True) 
            if type(update) == float:
                return update
            lines = []
            lines_det = []
            lines += update[0]
            lines_det += update[1]

        return 0

    def play_game(data):
        lines = data[0]
        lines_det = data[1]
        v = int(self.v)
        score = 0
        for x in range(horizon):
            v = -v
            


    def play_random(self,field,data):
        # print 'play random'
        g_scores = []
        f_score = []    
        for x in range(events):
            
            score = self.random_game(data)
            g_scores.append(score)
        f_score = sum(g_scores)/events
        # print 'pl random field:',field
        # print 'score of a field:',f_score
        return f_score

    def choice(self):
        print 'choice',self.v
        area = self.stay_close() 
        area = [[8,8]] if area == [] else area
        print 'outline',self.outline
        scores = []
        # print 'area',area
        for field in area:
            # print 'choice iterating field',field
            data = self.reset_globals(field,True)
            score = self.play_random(field,data)
            scores.append([score,field])
                # print 'pl',self.v,'score',score,scores

        scores.sort()
        print 'scores',scores[-5:]
        return scores[-1][-1]

    def reset_globals(self,field=0, game = True): 
        lines = [[],[],[],[]] # 0: hor, 1: ver, 2: upright, 3: upleft
        lines_det = [[[0]]*s,[[0]]*s,[[0]]*(s*2-1),[[0]]*(s*2-1)]
        history = list(self.b.history)
        if game:
            history += [field + [self.v]]
        for x in history:
            self.create_outline(x)
            data = self.updt_ln(x,x[-1],lines,lines_det,False)
            lines = data[0]
            lines_det = data[1]
        return lines, lines_det





    def play(self,a,b):
        print '\n\nplay:'
        field = self.choice()
        print 'returned by choice:',field,self.v
        self.b.put(field[0],field[1],self.v)
                 
            



    def create_outline(self,field,iterate=True):
##        print 'create outline',self.v

        minimax = list(self.outline) # 0: min x, 1: min y, 2: max x, 3: max y (expressed in board indexes)
        for x in range(2):
            minimax[x] = field[x] if minimax[x] > field[x] else minimax[x]
        for x in range(2,4):
            minimax[x] = field[x-2] if minimax[x] < field[x-2] else minimax[x]
        
        self.outline = minimax if iterate==True else self.outline


    def stay_close(self):
        history = list(self.b.short_history)
        # print 'history',history
        res = []
        for field in history:
            # print '\nfield',field
            x = field[0]
            y = field[1]
            around = []
            for r in xrange(-1,2):
                for q in xrange(-1,2):
                    zero = x + q
                    one = y + r
                    # print '\nout',[zero,one],
                    if not (zero < 0 or zero > s or one < 0 or one > s or [zero,one] in history):
                        around.append([zero,one])
                        # print 'append'
            res += around
        print 'res',len(res)
        return res
                


    def build_area(self,outline = None):
        print 'build'
        minimax = list(self.outline) if outline==None else outline

        offset = [ -o, -o, o, o ]
        for x in range(4):
            if 0 <= (minimax[x] + offset[x]) < s:
                minimax[x] += offset[x]
        print minimax
        area = []
        print area
        c = 0
        for x in range(minimax[0],minimax[2]+1):
            for y in range(minimax[1],minimax[3]+1):
                area.append([x,y])
            c+=1
        self.area = list(minimax)
        big_offset = [-2, -2, 2, 2]
        for x in range(4):
            if 0 <= (minimax[x] + big_offset[x]) < s:
                minimax[x] += big_offset[x]
        self.big_area = list(minimax)
        return area

    def check_line_deep(self, line, v):
        curr = 0
        prev = 0
        chain = 0
        print line
        for x in range(len(line)):
            prev = int(curr)
            curr = line[x]

            if curr == v and prev == 0:
                # ext = [prev,curr] if len(chain)<2 else [curr]
                chain += 1 if chain<2 else 1
            elif curr == 0 and prev == v:
                chain +=1
            elif curr == v and prev == v:
                chain +=1
            elif curr ==v:
                chain = 1
            elif curr == 0 and prev == 0:
                chain = 0
            elif curr == -v:
                chain = 0
            print x, curr, prev, chain
            if chain>4:
                return True
        return True if chain > 4 else False

    def check_line(self, line, v):
##        print 'check line'
        count = 0
        for x in range(len(line)):
            count = count + 1 if line[x] == v else 0
            if count == self.n:
                self.keep_iter = False
                return True
        return False

    def check_deep(self,line,v):
        length = len(line)
        curr = 0
        prev = 0
        chain = 0
        empty = 0
        print line
        for x in range(1,length):
            curr = line[x]
            prev = line[x-1]
            if curr == v:
                chain +=1
                # if prev ==0:
                #     empty = 0
            if curr == -v:
                chain = 0
                empty = 0
            if curr == 0:
                if prev==0:
                    chain = 0
                empty += 1
            print prev,curr,chain,empty
            if empty ==3:
                chain = 0
            if chain == 3 and empty == 1:
                print 'try'
                try:
                    if line[x+1] == 0:
                        print 'try return'
                        return True
                except IndexError:
                    pass
            if chain >=4 and empty>0:
                print 'break return'
                return True
            


        print 'normal return'
        return True if chain > 3 else False

    def get_copy(self,data):
        return list(data)
            

           


       
                






# b = board.Board(s,n)
# bobby = RobertFischer(b,-1,n)

# robby = RobertFischer(b,1,n)


def game():
    global s,n,bobby,robby,b
    c = 10
    while c!=0:
        bobby.play()
        robby.play()
        print b.print_board()
        c -=1
def test():
    global bobby, robby, b
    b.put(2,0,1)
    b.put(2,4,1)
    b.put(4,2,2)
    b.put(5,2,2)
##game()
##test()

##
##print b.history





# 1
##bobby.play(10,10)
##robby.play(10,11)
##bobby.play(11,11)
##robby.play(9,10)
##bobby.play(9,9)
##robby.play(8,8)
##bobby.play(12,12)

# 2
##robby.play(4,3)
##bobby.play(2,2)
##robby.play(3,4)
##bobby.play(3,3)
##robby.play(5,3)
##bobby.play(5,5)
##robby.play(1,1)
##bobby.play(4,4)
##print b.print_board()
##for x in bobby.lines_det: print '\n\n',x
##bobby.evaluate(-1)
##bobby.create_outline()
##a = bobby.lines_det[3][14]
##print b.print_board()
##print bobby.check_line(a,-1)
