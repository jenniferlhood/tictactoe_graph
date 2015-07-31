from __future__ import division

from math import sqrt,pi,sin,cos,atan,log
from collections import Counter

width, height =  1500, 1300
header=r'''
 <!DOCTYPE html>
<html>
<head>
<script type="text/javascript" src="dist/paper-full.js"></script>
<script type="text/paperscript" canvas="tictactoe">
'''


footer=r'''
</script>
</head>
<body>
<canvas id="tictactoe" width= "{}" height = "{}" resize="true"></canvas>
</body>
</html> 
'''.format(width,height)



col_m = ['rgb(200,155,135)','rgb(135,200,155)','rgb(135,155,200)']


vertices = []
a_list = []
s_list = []
win = []
levs = [[],[],[],[],[],[],[],[],[],[]]

fractions = [.35, .3, .35] # These are the fractions of width devoted to O, draw, and X.
factor = 1

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
                        v.xy = (xblock, height*fractions2[9-m]-4*v.size/6)
                    else:
                        v.xy = (xblock, height*fractions2[9-m]+4*v.size/6)
                else:
                    v.xy = (xblock, height*fractions2[9-m])
                
 
                xblock += width*fractions[winner+1]/(len(levelmi)+1)
                v.sortkey = v.xy[0]


               


def symmetry():
    for i in range(len(vertices)):
        s_list.append([])
        for j in range(len(a_list[i])):
            s_list[i].append(0)
            
    for i in range(len(vertices)):
        v = vertices[i]
        a = list(vertices[i].symbol)
                      
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
    cols = [  (220,0,0), (200, 200, 200), (0,0,220) ]
    
    if v.w < 0:
        c =  [int(-v.w*cols[0][i] + (1+v.w)*cols[1][i]) for i in [0, 1, 2]]
    else:
        c = [int(v.w*cols[2][i] + (1-v.w)*cols[1][i]) for i in [0, 1, 2]]
    
    return 'rgb'+str(tuple(c))


   

def generate_points():

    for v in vertices:
        i = vertices.index(v)
        print ''' var p{} = new Point({},{});'''.format(i,v.xy[0],v.xy[1])
        

def draw_square(i,pos, val):
    d = dict( [('-', 'white'), ('X', 'blue'), ('O', 'red')] )
    
    board = '''var rect{} = new Rectangle(new Point({}), squareSize);
        var path = new Path.Rectangle(rect);
        path.fillColor = '{}';
        path.strokeColor = 'black';
              
        '''.format(i,pos,d[val])
      
    return board       

def draw_board2(u):
    x=u.xy[0]
    y=u.xy[1]
    s=u.size/5
    players=''
    back = '''var back = new Path.Rectangle(new Rectangle(new Point({},{}), new Point({},{})));
        back.fillColor = 'white';
        '''.format(x-3*s,y-3*s,x+3*s,y+3*s)
         
    pre = '''
        var board = new CompoundPath(
            new Path(new Point({},{}), new Point({},{})),
            new Path(new Point({},{}), new Point({},{})),
            new Path(new Point({},{}), new Point({},{})),
            new Path(new Point({},{}), new Point({},{}))
        '''.format(x-s,y-3*s,x-s,y+3*s,x+s,y-3*s,x+s,y+3*s,x-3*s,y-s,x+3*s,y-s,x-3*s,y+s,x+3*s,y+s)
    post ='''
        );
        board.strokeColor= "black";
        '''    
        
    return back + pre + post
    

def draw_board(u,i,col):
    s = ''
    thick = int(u.size/7)
    
    pre = '''var squareSize = new Size({},{});'''.format(u.size/3,u.size/3)
    
    for j in range(9):
        pos_move = "p{}.x+{},p{}.y+{}"\
                .format(i,(j%3*u.size/3-u.size/2),i,(j//3*u.size/3-u.size/2))
        
        
        
        
        s += draw_square(j,pos_move, u.symbol[j])
        
            
    border = '''var rect{} = new Path.Rectangle(new Rectangle(new Point(p{}.x-{},p{}.y-{}), new Size({},{})));
        path.strokeColor = 'rgb(200,200,200)';
        path.strokeWidth = {};
        '''.format(i,i,3*u.size/2,i,3*u.size/2,u.size,u.size,thick)
            
    #return s + '\n' + border + '\n'
    return pre + '\n' + s

def draw_path(points,w,col,pc):
      return '''  var {} = new Path();
                {}.add({});
                {}.strokeWidth = {};
                {}.strokeColor = '{}';'''\
                .format(pc,pc,", ".join(points),pc, w, pc, col)

    
def get_n(levs):
    count = 0
    
    for w in levs:
        i = vertices.index(w)
        countadd = False
        
        for x in a_list[i]:
            if x.moves() < w.moves() and x.win != w.win:
                countadd = True
        if countadd: count += 1    
    return count        

def draw_good_edges():
    
    for v in vertices:
        m = v.moves()
        i = vertices.index(v)
        pos = height*fractions2[9-m]
        drop_v = pos-v.xy[1] 
       
      
        for u in a_list[i]:
            k = vertices.index(u)
            pos_u = height*fractions2[9-u.moves()]
            drop_u = u.xy[1]-pos_u
            #t = {1: "thin", 2:"semithick",3:"thick",4:"very thick", 5:"very thick"}
            
            col = w_col(u)
            
            j = a_list[i].index(u)
            
            t= s_list[i][j]/2
            
            if u.moves() < v.moves() and u.win == v.win:
                #draw line down to common level in row
                zero = "new Point(p{}.x, p{}.y)".format(i,i)
                one = "new Point(p{}.x, p{}.y+{})".format(i,i,(drop_v + 3*v.size/2))
                #draw line across to perfect child
                two = "new Point(p{}.x, p{}.y-{})".format(k,k,(drop_u + 3*u.size/2))
                #draw line down to perfect child
                three = "new Point(p{}.x, p{}.y)".format(k,k)
               
                print draw_path([zero,one,two,three], 1.1,'black',"g")
                
           
def draw_bad_edges():
    
    for m in reversed(range(10)):
        n=get_n(levs[m])      
        pad = width/100
        level_m = [v for v in vertices if v.moves() == m ]
        a = min([v.xy[1] + v.size/2 for v in level_m ]) + pad      
        if m > 0:
            b = max([v.xy[1] -v.size/2 for v in vertices if v.moves() == m-1 ]) - pad
        else: 
            b = 0
            
        if m % 2 ==0: #x wins
            t = 0
            for v in reversed(sorted(levs[m], key= lambda w: w.sortkey)):
                i = vertices.index(v)
                step = False
                for u in a_list[i]:
                    j = vertices.index(u)
                    if u.moves() < v.moves() and u.win != v.win:
                        step = True
                                               
                        end_x = u.size/2 - (u.counter)/(u.bp+1)*u.size
                        u.counter += 1
                        

                                                           
                        #draw the vertical line down the the desired depth        
                        #zero = (v.xy[0]+v.size/6,v.xy[1])
                        zero = "new Point(p{}.x + {}, p{}.y)"\
                                .format(i,v.size/6,i)
                        #one = (v.xy[0]+v.size/6, v.xy[1]+ a + (t/n)*(b-a)) 
                        one = "new Point(p{}.x + {}, p{}.y+{})"\
                                .format(i,v.size/6,i,(a-v.xy[1]) + (t/n)*(b-a))
                        #draw the horizontal line across to the child vertex
                        #two = (u.xy[0]+end_x,one[1])
                        two = "new Point(p{}.x + {}, p{}.y+{})"\
                                .format(j, end_x,i,(a-v.xy[1])+ (t/n)*(b-a))
                        #draw the vertical line down to the child vertex
                        #three = (u.xy[0]+end_x,u.xy[1])
                        three = "new Point(p{}.x + {}, p{}.y)"\
                                .format(j, end_x,j)
                       
                        print draw_path([zero,one,two,three], 1, col_m[u.win+1],"m_x")

                        
                if step == True:
                    t += 1
  

        else:
            t = 0
            for v in sorted(levs[m], key= lambda w: w.sortkey):
                i = vertices.index(v)
                step = False
                for u in a_list[i]:
                    
                    j = vertices.index(u)
                    if u.moves() < v.moves() and u.win != v.win:
                        step = True
                        #calculate coordinate for edge connecting with child vertex
                        
                        end_x = (u.counter)/(u.bp+1)*u.size -u.size/2
                        
                        u.counter += 1
                                                        
                        #draw the vertical line down the the desired depth        
                        #zero = (v.xy[0]-v.size/6,v.xy[1])
                        zero = "new Point(p{}.x + {}, p{}.y)"\
                                .format(i,-v.size/6,i)
                        #one = (v.xy[0]-v.size/6,  v.xy[1]+a + (t/n)*(b-a))
                        one = "new Point(p{}.x + {}, p{}.y+{})"\
                            .format(i,-v.size/6,i, (a-v.xy[1])+(t/n)*(b-a))                        
                        #draw the horizontal line across to the child vertex
                        #two = (u.xy[0]+end_x,one[1])
                        two = "new Point(p{}.x + {}, p{}.y+{})"\
                             .format(j, end_x,i,(a-v.xy[1])+(t/n)*(b-a))                      
                        #draw the vertical line down to the child vertex
                        #three = (u.xy[0]+end_x,u.xy[1])
                        three = "new Point(p{}.x + {}, p{}.y)"\
                                .format(j, end_x,j)
                        
                        print draw_path([zero,one,two,three],1,col_m[u.win+1],"m_o")            
 
                if step == True:
                    t += 1

def draw_title():

    indent1 = width/35
    indent2 = indent1 + 30
    title = r"""{\fontsize{25mm}{40mm}\selectfont Tictactoe
     
     }"""
    
    text = r'''{    
    \fontsize{10mm}{10mm}\selectfont X wins (perfect play)
     
    O wins (perfect play)
     
    X wins (O's mistake)
    
    O wins (X's mistake)
    
    draw
    
    }'''
     
    author = r'''{\fontsize{5mm}{10mm}\selectfont
            created by Jennifer L.A. Hood and Pat Morin,
             2015, Carleton University}'''
     
    a = r'''\node [right, text width = 20 cm] at ({}mm, {}mm) {};
    \node [right, text width = 20cm] at ({}mm, {}mm) {};'''\
        .format(indent1, height-20,title,indent2, height-60, text)
    b =  r'''\draw[d_blue,line width = 2pt] ({}mm, {}mm) -- ({}mm, {}mm);
    \draw[d_red,line width = 2pt] ({}mm, {}mm) -- ({}mm, {}mm);
    \draw[m_blue] ({}mm, {}mm) -- ({}mm, {}mm);
    \draw[m_red] ({}mm, {}mm) -- ({}mm, {}mm);
    \draw[m_green] ({}mm, {}mm) -- ({}mm, {}mm);
    '''.format(indent1, height-40, indent1+20, height-40,\
            indent1, height-50, indent1+20, height-50,\
            indent1, height-60, indent1+20, height-60,\
            indent1, height-70, indent1+20, height-70,\
            indent1, height-80, indent1+20, height-80)
    
    
    c = r'''\node [right, text width = 20 cm,m_red] at ({}mm,{}mm) {};'''\
            .format(10, 10, author)
            
    return a + '\n\n' + b + '\n' + c



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
    symmetry()
    winningness()
    

    # Draw backgrounds.
    for i in [0, 1, 2]:
        col = ['rgb(255,220,220)', 'rgb(220,255,220)', 'rgb(220,220,255)'][i]
        
        print """var bg_rect = new Rectangle(new Point({},{}), new Size({},{}));
                var bg_path = new Path.Rectangle(bg_rect);
                bg_path.fillColor = '{}';
                bg_path.strokeColor = '{}';
                """.format(width*sum(fractions[:i]),0, width*fractions[i],height-10,col,col)

    
    #generate paper.js objects
    generate_points()
    
    #draw edges
 
    draw_bad_edges()
    
    draw_good_edges()
   
    # Draw the vertices.
    for u in vertices:
   
        #print draw_board(u,vertices.index(u),w_col(u))
         print draw_board2(u)
         
    # Draw the title
    
    #print draw_title()
    
       
    print footer
