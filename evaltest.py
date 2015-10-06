from timeit import repeat

def check_line(line):
    v = 1
##        print 'check line'
    count = 0
    for x in range(len(line)):
        count = count + 1 if line[x] == v else 0
        if count == 5:
            self.keep_iter = False
            return True
    return False
    


def check_line_deep():
    v= 1
    line = [0,0,0,0,-1,0,1,1,1,0,-1,-1,-1]
    curr = 0
    prev = 0
    chain = 0
##    print line
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
##        print x, curr, prev, chain
        if chain>4:
            return True
    return True if chain > 4 else False


def check_deep(line):
    v = 1
    length = len(line)
    curr = 0
    prev = 0
    chain = 0
    empty = 0
##    print line
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
##        print prev,curr,chain,empty
        if empty ==3:
            chain = 0
##        if chain == 3 and empty == 1:
####            print 'try'
##            try:
##                if line[x+1] == 0:
####                    print 'try return'
##                    return True
##            except IndexError:
##                pass
        if chain >=4:
##            print 'break return'
            return True


def check_simple(line):
    test_deep = [[0,1,1,1,0],
             [0,1,0,1,1,0],
             [0,1,1,0,1,0],
             [0,1,1,1,1],
             [1,0,1,1,1],
             [1,1,0,1,1],
             [1,1,1,0,1],
             [1,1,1,1,0]
             ]
    v= 1
    for x in test_deep:
        if x in line:
            return True
    return False

def check_simpler():
    line = [0,0,0,0,-1,0,1,1,1,0,-1,-1,-1]
    v = 1
    chain = 0
    empty = 0
    offset = {(0,0):'__mul__'}








def stay_close(history):
    
    # print 'history',history
    res = []
    s=15
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
##    print 'res',len(res)
    return res




def updt_ln(field, v, lines, lines_det, iterating):
    #print 'updt_ln',field,v
    s = 15
    s_min = s - 1
    temp = [0] * s

    # LOOP UPDATING HORIZONTAL AND VERTICAL LINES
    for x in range(2):
        if field[x] not in lines[x]:
            lines_det[x][field[x]] = list(temp)
        lines_det[x][field[x]][field[int(not x)]] = v
##        if self.check_line(lines_det[x][field[x]],v) and iterating:
##            # print 'horver check_line True'
##            # print lines_det[x][field[x]]
##            return W if v == self.v else -W/2

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
##        if self.check_line(lines_det[x][vals[x]],v) and iterating:
##            # print 'diag check_line True'
##            # print lines_det[x][vals[x]]
##            return W if v == self.v else - W/2

        lines[x].append(vals[x])
        lines[x] = set(lines[x])
        lines[x] = list(lines[x])
    # print lines
    # for x in range(4):
    #     print lines_det[x]
    # print len(lines_det)
    return lines, lines_det

setup = """from __main__ import check_simple, check_deep, check_line
test_deep2 = [[0,0,0,0,0,1,0,-1,0,1,1,0,0,0],
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
test_deep = [[0,0,0,0,1,1,0,0,1,1,1,1,-1,-1,0]]

"""
cl = sum(repeat(stmt='for x in test_deep: check_line(x)',setup=setup,number=100000))/3
print 'check_line',cl


setup = """from __main__ import stay_close

history = [[11,9]]
"""

sc = sum(repeat(stmt='stay_close(history)',setup=setup,number=100000))/3
print 'stay_close',sc

setup = """from __main__ import updt_ln
field = [7,9,-1]
v = -1
lines = [[7, 8, 9, 11, 12, 13], [7, 8, 9, 11, 12, 13], [20, 22], [8, 10, 12, 14, 16, 18, 20]]
lines_det = [[[0], [0], [0], [0], [0], [0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 11, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 11, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0, 0, 11, 0, 0, 0, 0, 0, 0], [0], [0, 0, 11, 0, 0, 0, 0], [0], [0], [0], [0], [0], [0]], [[0], [0], [0], [0], [0], [0], [0], [0], [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0], [0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0], [0], [0], [0], [0], [0], [0], [0]]]

"""
ul = sum(repeat(stmt='updt_ln(field,v,lines,lines_det,iterating=False)',setup=setup,number=100000))/3
print 'updt_ln', ul

print 'SUM', cl+sc+ul
