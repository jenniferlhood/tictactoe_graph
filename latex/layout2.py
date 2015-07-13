from __future__ import division

from math import sqrt,pi,sin,cos,atan,log
from collections import Counter


header=r'''\documentclass{article}

\usepackage{tikz}

\newcommand{\xcol}{red}
\newcommand{\ocol}{blue}
\newcommand{\ecol}{white}


\usepackage{geometry}
 \geometry{
 papersize={830mm,530mm},
 left=10mm,
 right=10mm,
 top=10mm,
 bottom=10mm,
 }

\pagestyle{empty}

\definecolor{pg_red}{RGB}{255,245,240}
\definecolor{pg_green}{RGB}{240,255,245}
\definecolor{pg_blue}{RGB}{240,245,255}


\definecolor{m_red}{RGB}{225,180,170}
\definecolor{m_green}{RGB}{170,225,180}
\definecolor{m_blue}{RGB}{170,180,225}


\definecolor{b_red}{RGB}{220,80,55}
\definecolor{b_blue}{RGB}{55,80,220}

\begin{document}
\begin{tikzpicture}
'''


footer=r'''
\end{tikzpicture}
\end{document}'''


c_list_win = [(255,245,240),(240,255,245),(240,245,255)]
c_list = [(0,0,0),(200,200,200)]
c_list1 = [(200,55,35),(35,200,55),(35,55,200),(225,180,170),(170,225,180),(170,180,225)]
c_list2 = [(220,80,55),(255,255,255),(55,80,220)]



vertices = []
a_list = []
s_list = []
win = []
levs = [[],[],[],[],[],[],[],[],[],[]]
width, height =  800, 500
fractions = [.35, .3, .35] # These are the fractions of width devoted to O, draw, and X.
factor = 1
#fractions2 = [1/22,2/22,3/22,5/22,8/22,11/22,14/22,17/22,20/22,21/22]
#fractions2 = [16/17,15/17,13/71,11/17,9/17,7/17,5/17,3/17,2/17,1/17]
#fractions2 = [1/17,2/17,3/17,5/17,7/17,9/17,11/17,13/17,15/17,16/17]
fractions2 = [1/34,4/34,8/34,12/34,16/34,20/34,24/34,27/34,30/34,33/34]

class Vertex(object):
    def __init__(self,(x,y)):
        self.symbol = ""
        self.xy = (x,y)
        self.win = "-"
        self.parent = 0
        self.child = 0
        self.bp = 0
        self.size = width/57*factor
        self.thickness = 1
        self.counter = 1
        self.w = 0 #win expected value 

    def moves(self):
   
        c = Counter()
        for j in self.symbol:
            c[j]+=1
        return c['-']

def load_data(select_file):
    f=open(select_file,"r")
    f1=f.readline()
    vertices = []
    a_list = []

    #parse the lines and generate v and a lists
    f2 = f.readline() # vertices
    if f2 != '[]\n':
        f2 = f2.rstrip(')]\n')
        f2 = f2.lstrip('[(')
        f2 = f2.split('), (')
        for i in f2:
            if i is not '':
                j = i.split(', ')
                if j[0] is not '' and j[1] is not '':
                    vertices.append(Vertex((int(j[0]),int(j[1]))))
    
    
    f3 = f.readline() #a_list
    if f3 != '[]\n':
        f3 = f3.rstrip(']]\n')
        f3 = f3.lstrip('[[')
        f3 = f3.split('], [')
        for i in range(len(f3)):
            a_list.append([])
            l = f3[i].split(', ')
            for j in l:
                if j is not '':
                    a_list[i].append(vertices[int(j)])


    f4 = f.readline()

   
    #code specific to tictactoe files
    
    f = open('tictactoe.txt')
    symbol = []
    
    for i in range(765):
        a = f.readline()
        a = a.rstrip('\r\n')
        
        s_list.append([])
        
        u = vertices[i]
        u.symbol = a
        
        # append parents to adjacentcy list
        for v in a_list[i]:
            j = vertices.index(v)
            #u.child += 1
                              
            if u not in a_list[j]:
                a_list[j].append(u)
                #v.parent += 1      

    
    return vertices, a_list, s_list
    
    
def win_loose_draw():
    
    #win:
    for v in vertices:
        s = v.symbol
     
        if s[0:3] == "XXX" or s[3:6] == "XXX" or s[6:9] == "XXX":
            win.append("x")
        elif s[0:3] == "OOO" or s[3:6] == "OOO" or s[6:9] == "OOO":     
            win.append("o")
       
        elif s[0] == "X" and s[3] == "X" and s[6] == "X":
                win.append("x")
        elif s[0] == "X" and s[4] == "X" and s[8] == "X":
                win.append("x")     
        elif s[2] == "X" and s[5] == "X" and s[8] == "X":
                win.append("x")
        elif s[2] == "X" and s[4] == "X" and s[6] == "X":
                win.append("x")
        elif s[1] == "X" and s[4] == "X" and s[7] == "X":
            win.append("x")
        

        elif s[0] == "O" and s[3] == "O" and s[6] == "O":
                win.append("o")
        elif s[0] == "O" and s[4] == "O" and s[8] == "O":
                win.append("o") 
        elif s[2] == "O" and s[5] == "O" and s[8] == "O":
                win.append("o")
        elif s[2] == "O" and s[4] == "O" and s[6] == "O":
                win.append("o")
        elif s[1] == "O" and s[4] == "O" and s[7] == "O":
            win.append("o")                
      
        else:
        
            if "-" not in s:
                win.append("d")
            else:
                win.append("")
                
                
    
        
        

    
    
#node is V in v_list, start with player X
 
def minimax(node, player):
    index = vertices.index(node)
    if win[index] == "x":
        node.win = 1
        return 1
    elif win[index] == "o":
        node.win = -1
        return -1
    elif win[index] == "d":  
        node.win = 0
        return 0
    else:    
        if player:
            bestvalue = -1
            for v in a_list[index]:
                if v.moves() < node.moves():
                    val = minimax(v, False)
                    bestvalue = max(bestvalue, val)
                    node.win = bestvalue
                    
        else:
            bestvalue = 1
            for v in a_list[index]:
                if v.moves() < node.moves():
                    val = minimax(v, True)
                    bestvalue = min(bestvalue, val)
                    node.win = bestvalue
                    
        return bestvalue     
        
            
        
def reorder():
    #some stats
   
    for m in reversed(range(10)):
        levelm = [v for v in vertices if v.moves() == m]
             
        for winner in [-1, 0, 1]:
            levelmi = [v for v in levelm if v.win == winner]
            
            if winner == (-1+(m % 2)) or winner == (0+(m %2)):
                
                levs[m] += levelmi
              
            for v in levelmi:
                i = vertices.index(v) # Ack!
                parents = [w for w in a_list[i] 
                            if w.moves() > v.moves() 
                             and w.win == v.win]
                v.bp = len([w for w in a_list[i]
                            if w.moves() > v.moves() and w.win != v.win])
                            
                children = [w for w in a_list[i] if w.moves() < v.moves()
                                and w.win == v.win]             
                bad_children = [w for w in a_list[i] if w.moves() < v.moves() 
                            and w.win != 0 and w.win != v.win ]
                
               
                
                if parents:
                    
                    v.sortkey = sum([w.xy[0] for w in parents])/len(parents)
                    
                    if not children:
                        v.sortkey = v.sortkey + -v.win*(2**20)
               
                        
                        
                else:
                    if winner == 0:

                       if v.moves() % 2 == 0:
                            v.sortkey = 2**20
                       else:
                            v.sortkey = -2**20
                    else:
                        v.sortkey = -v.win * 2**20
                   
                        
            # Bad - Omega(n^2log n) time algorithm in here.
            # levelmi = sorted(levelmi, key=lambda v: \
            #        -len(a_list[vertices.index(v)])*winner)
            levelmi = sorted(levelmi, key=lambda v: v.sortkey)
            
               
            
            
            xblock = (winner+1)*width/3 \
                    + (width/3)/(len(levelmi)+1)

            for v in levelmi:

                v.xy = int(xblock), int(height*(10-m)/11)
                xblock += (width/3)/(len(levelmi)+1)
                v.sortkey = v.xy[0]
            
                
  

    for m in range(10):
        levelm = [v for v in vertices if v.moves() == m]
             
        for winner in [-1, 0, 1]:
            levelmi = [v for v in levelm if v.win == winner]
    
            for v in levelmi:
                 i = vertices.index(v) # Ack!
      
                 children = [w for w in a_list[i] if w.moves() < v.moves()
                                and w.win == v.win]
                 
                 if children:
                    
                    v.sortkey += sum([w.xy[0] for w in children])/len(children)

            levelmi = sorted(levelmi, key=lambda v: v.sortkey)
            
            xblock = (winner+1)*width/3 \
                    + (width/3)/(len(levelmi)+1)

            for v in levelmi:

                v.xy = int(xblock), int(height*(10-m)/11)
                xblock += (width/3)/(len(levelmi)+1)
                v.sortkey = v.xy[0]
   
   
    for m in reversed(range(10)):
        levelm = [v for v in vertices if v.moves() == m]
             
        for winner in [-1, 0, 1]:
            levelmi = [v for v in levelm if v.win == winner]
    
            for v in levelmi:
                 i = vertices.index(v) # Ack!
                 parents = [w for w in a_list[i] 
                            if w.moves() > v.moves() 
                             and w.win == v.win]
                 children = [w for w in a_list[i] if w.moves() < v.moves()
                                and w.win == v.win]
                 v.child = len(children)
                 v.parent = len(parents)
                                
                 if parents:
                    v.sortkey += sum([w.xy[0] for w in parents])/len(parents)
                    if not children:
                        v.sortkey = v.sortkey + -v.win*(2**20)
                 else:
                    if winner == 0:

                       if v.moves() % 2 == 0:
                            v.sortkey = 2**22
                       else:
                            v.sortkey = -2**22
                    else:
                       v.sortkey += (-v.win * 2**20)
                        #v.sortkey = -v.win * (len(children)+1)**20
                
            levelmi = sorted(levelmi, key=lambda v: v.sortkey)

            xblock = sum(width*fractions[:winner+1]) + width*fractions[winner+1]/(len(levelmi)+1)
            n = 0
            for v in levelmi:
                n+=1
                
                if m == 3 and v.win == 1:
                    v.size = v.size/max(1,(log(len(levelmi),4)*1.3))
                else:
                    v.size = v.size/max(1,(log(len(levelmi),4)))   
                       
                if len(levelmi) > 40:
                    if n % 2 == 1:
                        v.xy = (xblock, height*fractions2[m]-4*v.size/6)
                    else:
                        v.xy = (xblock, height*fractions2[m]+4*v.size/6)
                else:
                    v.xy = (xblock, height*fractions2[m])
                
 
                xblock += width*fractions[winner+1]/(len(levelmi)+1)
                v.sortkey = v.xy[0]


               


def symmetry():
    for i in range(len(vertices)):
        s_list.append([])
        for j in range(len(a_list[i])):
            s_list[i].append(0)
            
    for i in range(len(vertices)):
        v = vertices[i]
        a = list(vertices.symbol)
        v.thick = 1
              
        if v.moves() % 2 == 0:
            player = "O"
        else:
            player = "X"
        
        for u in a_list[i]:
            j = a_list[i].index(u)
            #l = vertices.index(u)
            b = u.symbol
               
            r = b[2]+b[1]+b[0]+b[5]+b[4]+b[3]+b[8]+b[7]+b[6] # reflection of the a board  
                                   
            for k in range(len(a)):
                   
                #check each possible play against the rotated board b and it's reflection r
                # increment thickness (s_list) if a play is in one of b or r
                if a[k] == "-":
                    a[k] = player
                                                
                    if "".join(a) == b\
                            or "".join(a) == b[6]+b[3]+b[0]+b[7]+b[4]+b[1]+b[8]+b[5]+b[2]\
                            or "".join(a) == b[8]+b[7]+b[6]+b[5]+b[4]+b[3]+b[2]+b[1]+b[0]\
                            or "".join(a) == b[2]+b[5]+b[8]+b[1]+b[4]+b[7]+b[0]+b[3]+b[6]:
                        s_list[i][j] += 1
                    
                    elif "".join(a) == r\
                                or "".join(a) == r[6]+r[3]+r[0]+r[7]+r[4]+r[1]+r[8]+r[5]+r[2]\
                                or "".join(a) == r[8]+r[7]+r[6]+r[5]+r[4]+r[3]+r[2]+r[1]+r[0]\
                                or "".join(a) == r[2]+r[5]+r[8]+r[1]+r[4]+r[7]+r[0]+r[3]+r[6]:
                        s_list[i][j] += 1
                    a[k] = "-"
 
 
                    
def winningness():
    
    for v in vertices:
        w = 0
        i = vertices.index(v)
        data = False
        for u in a_list[i]:
            if u.moves() < v.moves():
                w += u.win
                data = True
        v.w = w/max(1,v.moves())
        if not data:
            v.w = v.win
        
    


    
def w_col(v):
    cols = [  (255,0,0), (200, 200, 200), (0,0,255) ]
    #if v.child == 0: return (255, 255, 255)
    if v.w < 0:
        c =  [-v.w*cols[0][i] + (1+v.w)*cols[1][i] for i in [0, 1, 2]]
    else:
        c = [v.w*cols[2][i] + (1-v.w)*cols[1][i] for i in [0, 1, 2]]
    return c


def w_col2(v):
    cols = [  (240,0,0), (80, 80, 80), (0,0,240) ]
    #if v.child == 0: return (255, 255, 255)
    if v.w < 0:
        c =  [-v.w*cols[0][i] + (1+v.w)*cols[1][i] for i in [0, 1, 2]]
    else:
        c = [v.w*cols[2][i] + (1-v.w)*cols[1][i] for i in [0, 1, 2]]
    return c
    





def draw_square(pos, size, val):
    d = dict( [('-', 'white'), ('X', 'b_blue'), ('O', 'b_red')] )
    return r'\draw [black,fill={}] ({}mm,{}mm) rectangle ({}mm,{}mm);'\
          .format(d[val], pos[0], pos[1], pos[0]+size/3, pos[1]+size/3)

def draw_board(pos, size, board, winner):
    pos = pos[0]-size/2, pos[1]-size/2
    s = ''
 
    for i in range(9):
        s += draw_square( ( pos[0]+(i%3)*(size/3), pos[1]+(i//3)*(size/3) ),
                          size, board[i]);
    return s + '\n'
    

def draw_path(points, options):
    t = ["({}mm,{}mm)".format(p[0],p[1]) for p in points]
    return r'\draw [{}]'.format(options) + "--".join(t) + ';';

def get_n(levs):
    count = 0
    countadd = False
    for w in levs:
        i = vertices.index(w)
        
        for x in a_list[i]:
            if x.moves() < w.moves() and x.win != w.win:
                countadd = True
        count += 1    
    return count        

def draw_good_edges():

    for v in vertices:
        m = v.moves()
        i = vertices.index(v)
        pos = height*fractions2[m]
        drop_v = v.xy[1]-pos 
        
        for u in a_list[i]:
            pos_u = height*fractions2[u.moves()]
            drop_u = pos_u-u.xy[1] 
            if u.moves() < v.moves() and u.win == v.win:
                #draw line down to common level in row
                zero = v.xy
                one = (v.xy[0], v.xy[1] - (drop_v + 3*v.size/2))
                #draw line across to perfect child
                two = (u.xy[0], u.xy[1] + (drop_u + 3*u.size/2))
                #draw line down to perfect child
                three = u.xy
                print draw_path([zero,one,two,three], 
                                    'black, rounded corners')
            
           
def draw_bad_edges():
    col = {-1: "m_red", 0: "m_green", 1: "m_blue"}
    for m in reversed(range(10)):
        
        v_step = 0
        pos =height*fractions2[m]
        maxsize = 0
        n=get_n(levs[m])
        
        if m % 2 ==0: #x wins
            
            for v in reversed(sorted(levs[m], key= lambda w: w.sortkey)):
                j = vertices.index(v)
                          
                maxsize = max(maxsize,v.size)
                drop = (v.xy[1]-pos)+maxsize
                step = False
                for u in a_list[j]:
                     
                    if u.moves() < v.moves() and u.win != v.win:
                        step = True
                        
                        #end_x = (u.xy[0] + 2*u.size) - (u.size*3/(u.bp+1)*u.counter)
                        
                        end_x = u.xy[0] + u.size/2 - (u.counter)/(u.bp+1)*u.size
                        u.counter += 1
                                                           
                        #draw the vertical line down the the desired depth        
                        zero = (v.xy[0]+v.size/6,v.xy[1])
                        one = (v.xy[0]+v.size/6, v.xy[1]-v_step-drop) 
                        
                        #draw the horizontal line across to the child vertex
                        two = (end_x,one[1])
                        
                        #draw the vertical line down to the child vertex
                        three = (end_x,u.xy[1])
                        
                        options = '{}, rounded corners'.format(col[u.win])
                        print draw_path([zero,one,two,three], 
                                    options)
                        
                        
                if step == True:
                    
                    v_step += (height*(fractions2[m]-fractions2[m-1])-maxsize)/n
                        

        else:
            
            for v in sorted(levs[m], key= lambda w: w.sortkey):
                j = vertices.index(v)
                maxsize = max(maxsize,v.size)
                drop = (v.xy[1]-pos)+maxsize
                step = False
                for u in a_list[j]:
                    
                    
                    if u.moves() < v.moves() and u.win != v.win:
                        step = True
                        #calculate coordinate for edge connecting with child vertex
                        
                        end_x = u.xy[0] - u.size/2 + (u.counter)/(u.bp+1)*u.size
                        
                        u.counter += 1
                                                        
                        #draw the vertical line down the the desired depth        
                        zero = (v.xy[0]-v.size/6,v.xy[1])
                        one = (v.xy[0]-v.size/6, v.xy[1]-v_step-drop)
                                                
                        #draw the horizontal line across to the child vertex
                        two = (end_x,one[1])
                                                
                        #draw the vertical line down to the child vertex
                        three = (end_x,u.xy[1])
                        
                        options = '{}, rounded corners'.format(col[u.win])
                        print draw_path([zero,one,two,three], 
                                    options)            
                                    
                if step == True:
                    
                    v_step += (height*(fractions2[m]-fractions2[m-1])-2*maxsize)/n




if __name__ == "__main__":
    """Program entry point."""
   
    # Print LaTeX preamble.
    print header
    
    # Read the input graph.
    #vertices = read_graph('tictactoe.txt')
    
    
    vertices, a_list, s_list = load_data("tictactoe1.graph")

    
    # Determine the winner for each node -1=O, 0=draw, 1=X.
    #minimax(vertices)
    
    
    win_loose_draw()         
    
    minimax(vertices[0], True)
   
   
   
    # Assign coordinates to the nodes.
    reorder()
    
    #symmetry()
    #winningness()
    

    # Draw backgrounds.
    for i in [0, 1, 2]:
        col = ['pg_red', 'pg_green', 'pg_blue'][i]
        print r'\draw [{},fill={}] ({}mm,{}mm) rectangle ({}mm,{}mm);'\
              .format(col, col, width*sum(fractions[:i]), 0, width, height)
    
    
    #draw edges
    draw_bad_edges()
    
    draw_good_edges()
   
    # Draw the vertices.
    for u in vertices:
        print draw_board(u.xy, u.size, u.symbol, u.win)
   
    
    print footer

