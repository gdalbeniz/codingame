import sys
import math
from enum import Enum

def debug(msg):
    print(msg, file=sys.stderr, flush=True)

class EnumType(Enum):
    @staticmethod
    def action_to_string(action):
        return action.name
    @staticmethod
    def string_to_action(_string):
        for a in ActionType:
            if a.name == _string:
                return a
            
class CellType(EnumType):
    EMPTY = 0
    EGG = 1
    CRYSTAL = 2
    BASE = 10
    ENEMY = 11


class Cell:
    def __init__(self, id, _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5):
        self.id = id
        self.type = CellType(_type)
        self.resources = initial_resources
        self.neighbours = [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]
        self.ants = 0
        self.bugs = 0
        self.base = False
        self.enemy = False
        self.dist = 999
        debug("cell neigh: {} {} {} {} {} {}".format(neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5))
    def update(self, resources, my_ants, opp_ants):
        self.resources, self.ants, self.bugs = resources, my_ants, opp_ants
    def set_base(self):
        self.base = True
        self.dist = 0
    def set_enemy(self):
        self.enemy = True

class Colony:
    def __init__(self, number_of_cells):
        self.cells = {}
        self.num_cells = number_of_cells
    def add(self, cell):
        self.cells[cell.id] = cell
    def update(self, id, resources, my_ants, opp_ants):
        self.cells[id].update(resources, my_ants, opp_ants)
    def set_base(self, id):
        self.cells[id].set_base()
    def set_enemy(self, id):
        self.cells[id].set_enemy()
    def process(self):
        # convert int to cell pointer
        for _,cell in self.cells.items():
            cell.neighbours = [c for _,c in self.cells.items() if c.id in cell.neighbours]
            #debug("process {}: ({})".format(c.id, len(cell.neighbours)))
        # set distances to nearest base
        for d in range(self.num_cells):
            for c in [c for _,c in self.cells.items() if c.dist == d]:
                #debug("proces {}: ({})".format(c.id, c.dist))
                new_dist = d+1
                for n in c.neighbours:
                    if n.dist > new_dist:
                        n.dist = new_dist
        # reorder neighbours to form directed graph towards nearest base
        for _,cell in self.cells.items():
            cell.neighbours.sort(key=lambda x: x.dist)
            #debug("proces {}: ({} {} {})".format(cell.id, cell.neighbours[0].dist, cell.neighbours[1].dist, cell.neighbours[2].dist))

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
number_of_cells = int(input())  # amount of hexagonal cells in this map
colony = Colony(number_of_cells)
for i in range(number_of_cells):
    # _type: 0 for empty, 1 for eggs, 2 for crystal
    # initial_resources: the initial amount of eggs/crystals on this cell
    # neigh_0: the index of the neighbouring cell for each direction
    _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    cell = Cell(i, _type, initial_resources, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5)
    colony.add(cell)

number_of_bases = int(input())
for i in input().split():
    colony.set_base(int(i))
for i in input().split():
    colony.set_enemy(int(i))
colony.process()

# game loop
while True:
    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        colony.update(i, resources, my_ants, opp_ants)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    print("WAIT")
