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
        self.crystals = initial_resources if self.type == CellType.CRYSTAL else 0
        self.eggs = initial_resources if self.type == CellType.EGG else 0
        self.neighbours = [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]
        self.ants = 0
        self.bugs = 0
        self.base = False
        self.enemy = False
        self.dist = 999
        self.beacons = 0
        self.crossroad = False
        #debug("cell neigh: {} {} {} {} {} {}".format(neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5))
    def update(self, resources, my_ants, opp_ants):
        self.crystals = resources if self.type == CellType.CRYSTAL else 0
        self.eggs = resources if self.type == CellType.EGG else 0
        self.ants = my_ants
        self.bugs = opp_ants
    def set_base(self):
        self.base = True
        self.dist = 0
    def set_enemy(self):
        self.enemy = True
    def place(self, beacons):
        if self.beacons < beacons:
            self.beacons = beacons
        if self.dist > 0:
            neigh = [n for n in self.neighbours if n.dist == self.neighbours[0].dist]
            neigh.sort(key=lambda x: x.dist*100 - x.beacons)
            neigh[0].place(beacons)

class Colony:
    def __init__(self, number_of_cells):
        self.cells = {}
        self.num_cells = number_of_cells
        self.num_bases = 0
        self.num_ants = 0
        self.num_bugs = 0
        self.num_crystals = 0
        self.num_eggs = 0
        self.eggs2crys = 100
    def add(self, cell):
        self.cells[cell.id] = cell
    def update(self, id, resources, my_ants, opp_ants):
        self.cells[id].update(resources, my_ants, opp_ants)
        # count things
        self.num_ants += my_ants
        self.num_bugs += opp_ants
        if self.cells[id].type == CellType.CRYSTAL:
            self.num_crystals += resources
        else:
            self.num_eggs += resources
    def set_base(self, id):
        self.cells[id].set_base()
        self.num_bases += 1
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
    def reset(self):
        # reset beacons and ants
        self.num_ants = 0
        self.num_bugs = 0
        self.num_crystals = 0
        self.num_eggs = 0
        for _,cell in self.cells.items():
            cell.beacons = 0
            cell.crossroad = False
    def calculate(self):
        debug("a {} b {} c {} e {}".format(self.num_ants, self.num_bugs, self.num_crystals, self.num_eggs))
        # place beacons
        for cell in [c for _,c in self.cells.items() if c.crystals > 0 or c.eggs > 0]:
            desired_beacons = self.num_ants // (cell.dist + 1)
            cell.place(min(desired_beacons, max(cell.crystals, cell.eggs)))
        # count beacons
        num_beacons = 0
        cells = [c for _,c in self.cells.items() if c.beacons > 0]
        cells.sort(key=lambda x: -x.dist)
        for cell in cells:
            num_beacons += cell.beacons
            debug("beacon {} #{} @{}".format(cell.id, cell.beacons, cell.dist))
            # locate crossroads
            neigh = [n for n in cell.neighbours if n.beacons > 0]
            if len(neigh) > 2:
                self.crossroad = True
        # reduce beacons
        for cell in cells:
            if cell.dist > turn:
                cell.beacons = 0
            #if num_beacons > self.num_ants:
            #    diff = num_beacons - self.num_ants
            #    if diff > cell.beacons:
            #        diff = cell.beacons
            #    num_beacons -= diff
            #    cell.beacons -= diff
    def beacons(self):
        cells = [c for _,c in self.cells.items() if c.beacons > 0]
        msg = []
        for cell in cells:
            msg.append("BEACON {} {}".format(cell.id, cell.beacons))
        print(";".join(msg))


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
turn = 0
while True:
    turn += 1

    colony.reset()

    for i in range(number_of_cells):
        # resources: the current amount of eggs/crystals on this cell
        # my_ants: the amount of your ants on this cell
        # opp_ants: the amount of opponent ants on this cell
        resources, my_ants, opp_ants = [int(j) for j in input().split()]
        colony.update(i, resources, my_ants, opp_ants)

    # Calculate beacons
    colony.calculate()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    colony.beacons()

