import sys
import math
import random


MAX_ROUTES = 100


LAST = 0
NEXT = -1
SELF = 0
RIGHT = 1
DOWN = 2
LEFT = 3
UP = 4

def debug(msg, end='\n'):
  print(msg, file=sys.stderr, end=end)  


class Route():
    def __init__(self, a):
        self.d = [random.randint(RIGHT,UP) for _ in range(a)]
    def __len__(self):
        return len(self.d)
        
class Cell():
    def __init__(self, x=-1, y=-1, w='?'):
        self.x = x
        self.y = y
        self.w = w
    def found(self):
        return self.x != -1 and self.y != -1

class Map():
    def __init__(self):
        self.row, self.col, self.alm = [int(i) for i in input().split()]
        self.K = Cell()
        self.T = Cell()
        self.C = Cell()
        self.cells = [Cell(x,y) for x in range(self.col) for y in range(self.row)]
    def cell(self, x, y, d=SELF):
        if d == SELF:
            if x < 0:
                x = 0
            elif x >= self.col:
                x = self.col - 1
            if y < 0:
                y = 0
            elif y >= self.row:
                y = self.row - 1
            return self.cells[y*self.col + x]
        elif d == RIGHT:
            return self.cell(x + 1, y)
        elif d == DOWN:
            return self.cell(x, y + 1)
        elif d == LEFT:
            return self.cell(x - 1, y)
        elif d == UP:
            return self.cell(x, y - 1)
        else:
            raise Exception("Map:cell:wtf")
    def update(self):
        Ky, Kx = [int(i) for i in input().split()]
        self.K = self.cell(Kx, Ky)
        for y in range(self.row):
            row = input()
            for x in range(self.col):
                c = self.cell(x, y)
                c.w = row[x]
                if c.w == 'T':
                    self.T = c
                elif c.w == 'C':
                    self.C = c
    def draw(self):
        for y in range(self.row):
            for x in range(self.col):
                c = self.cell(x,y)
                debug(c.w, end='')
            debug('')
    def route(self, c1: Cell, c2: Cell, r: Route):
        #allroutes = [Route() for _ in range(MAX_ROUTES)]
        c = c1
        for t in range(len(r) + 1):
            # check if reached or in bad pos or too many moves
            if c.x == c2.x and c.y == c2.y:
                return t 
            elif c.w == '?':
                return 500
            elif c.w == '#' or t >= len(r):
                return 1000
            # move
            else:
                c = self.cell(c.x, c.y, r.d[t])
        raise Exception("Map:route:wtf")
                
        


class Kirk():
    def __init__(self):
        self.pos = Cell()
        self.last = RIGHT
    def update(self, c: Cell):
        self.pos = c
    def move(self, d):
        if d == LAST:
            return self.move(self.last)
        elif d == NEXT:
            if self.last == UP:
                return self.move(RIGHT)
            else:
                return self.move(self.last + 1)
        elif d == UP:
            print("UP")
        elif d == RIGHT:
            print("RIGHT")
        elif d == DOWN:
            print("DOWN")
        elif d == LEFT:
            print("LEFT")
        else:
            raise Exception("Kirk:move:wtf")
        self.last = d
        return d


random.seed()
mapa = Map()
kirk = Kirk()

# game loop
for turn in range(1200):
    debug(f"----{turn}----")
    mapa.update()
    mapa.draw()
    kirk.update(mapa.K)
    if mapa.C.found():
        pass
    print("RIGHT")