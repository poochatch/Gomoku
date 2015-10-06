from board import Board

PATTERNS = [[0, 1, 1, 1, 0],
            [0, 1, 1, 1, 1],
            [0, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1]]

s = 15

DEPTH = 2

class Garry():
    def __init__(self, v, b):
        self.v = v
        self.i = Iterate(self.v)
        self.b = b

    def play(self):
##        print 'play'
##        print self.b.history
        init_node = self.i.reset_globals(self.b.history)
        print 'DEPTH',DEPTH
        return self.i.minimax(init_node, DEPTH, self.b.history, self.v)

        



class Iterate(Garry):
    def __init__(self, v):
        self.e = Evaluate()
        self.v = v

    def minimax(self, node, depth, history, v):
##        print 'minimax'
##        print history

        
        return self.alfabeta(node, depth, history, -999999, 999999, self.v)
        

    def alfabeta(self, node, depth, history, alfa, beta, player):
##        print '\n\nalfabeta',depth,player
        children = self.stay_close(history)
        if depth == 0:
##            print '###### depth = 0'
            score = self.e.evaluate(node[0], node[1], node[2], node[3])
            if score != -100:
                for x in range(4):
                    print node[2][x]
                    for y in node[2][x]:
                        print node[3][x][y]
                print score, '\n\n', depth, '\n',history,'\n\n', alfa,'\n', beta,'\n', player,'\n',children
                
            return score
        
##        if len(children) != 135:
##            print 'hist',len(children), len(history), player, depth
##        print 'children',children,len(children)
        if player==1:
            for child in children:
                best = -999999
##                print 'child',child,
##                print 'history',history, '\n\n'
                new_hist = list(history)
                new_hist.append(child)
                new_hist[-1].append(player)
##                print 'new_history', new_hist
##                print 'len childre',len(children)
                new_node = self.updt_ln(child, 1, node[2], node[3])
                a = self.alfabeta(new_node, depth-1, new_hist, alfa, beta, -1)
##                print 'returned from below:',depth,player,a
                best = max(best,a)
##                if alfa >= beta:
##                    print 'break'
##                    return alfa
            return best
        else:
            for child in children:
                best = 999999
                new_hist = list(history)
                new_hist.append(child)
                new_hist[-1].append(player)
                best = min(best,self.alfabeta(self.updt_ln(child, -1, node[2], node[3]), depth-1, new_hist, alfa, beta, 1))
##                if alfa >= beta:
##                    break
            return best
        
                                   
            
    def stay_close(self, history):
##        print 'history',history
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
        return res

    def updt_ln(self, field, v, lines, lines_det):
        #print 'updt_ln',field,v
        s_min = s - 1
        temp = [0] * s

        # LOOP UPDATING HORIZONTAL AND VERTICAL LINES
        for x in range(2):
            if field[x] not in lines[x]:
                lines_det[x][field[x]] = list(temp)
            lines_det[x][field[x]][field[int(not x)]] = v
##            if self.check_line(lines_det[x][field[x]],v) and iterating:
##                # print 'horver check_line True'
##                # print lines_det[x][field[x]]
##                return W if v == self.v else -W/2

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
##            if self.check_line(lines_det[x][vals[x]],v) and iterating:
##                # print 'diag check_line True'
##                # print lines_det[x][vals[x]]
##                return W if v == self.v else - W/2

            lines[x].append(vals[x])
            lines[x] = set(lines[x])
            lines[x] = list(lines[x])
        # print lines
        # for x in range(4):
        #     print lines_det[x]
        # print len(lines_det)
        return field, v, lines, lines_det



    def reset_globals(self, history=None): 
        lines = [[],[],[],[]] # 0: hor, 1: ver, 2: upright, 3: upleft
        lines_det = [[[0]]*s,[[0]]*s,[[0]]*(s*2-1),[[0]]*(s*2-1)]
        history = list(self.b.history) if history == None else history
        for x in history:
##            self.create_outline(x)
            data = self.updt_ln(x[:2],x[-1],lines,lines_det)
            lines = data[2]
            lines_det = data[3]
        return data



class Evaluate(Garry):
    def __init__(self):
        self.CNT = 0
        pass


    def evaluate(self,field,v, lines, lines_det):
        """ evaluate position accodring to:
            - mobility (n
            - possible continuations
            - the current player
\

        """
        
        for x in range(4):
            for y in lines[x]:
                if self.immidiate(lines_det[x][y],v):
                    return 100 * v
        
        return 0

##
##                
##        for x in lines:
##            for y in lines_det:
##                if immidiate(lines_det[x]):
##                    return True
##        return False


    def immidiate(self, line, v, *args, **kwargs):
        """ iterate through a line in a given position
            and check if there is an immidiate win for the
            current player
        """
        if '0, %s, %s, %s, 0' %(v,v,v) in str(line):
            return True
        for y in range(len(line)):
            if line[y] == 0:
                iterated = line[:]
                iterated[y] = v
##                print 'imm', iterated
                if self.five(iterated, v):
##                    print self.five(iterated,v)
                    return True

        return False
            
            
    def five(self, line, v):
##        print 'five',line
        count = 0
        for x in range(len(line)):
            count = count + 1 if line[x] == v else 0
##            print count,
            if count == 5:
##                print 'True'
                return True
        return False

    def check_line(self, line, v):
        
        for pattern in PATTERNS:
            for y in range(4,len(line)):
                if line[y-4] == pattern[0] and line[y-3] == pattern[1] \
                   and line[y-2]== pattern[2] and line[y-1] == pattern[3]\
                   and line[y] == pattern[4]:
                    return True
##                    chain = 0
##                    for z in range(len(pattern)):
##                        if not len(pattern) + y > len(line):
##                            if line[y+z] == pattern[z]:
##                                chain +=1
##                            else:
##                                break
##                        if chain == len(pattern):
##                            return True
        return False
                    
                    
    def if_won(self, line, v, pattern_return=False):
        self.CNT += 1
        for pattern in PATTERNS:
            leng = len(pattern)
            index = 0
            for y in range(leng-1,len(line)):
                if line[index:y+1] == pattern:
                    return index if pattern_return else True
                index += 1
        return False
        
        

