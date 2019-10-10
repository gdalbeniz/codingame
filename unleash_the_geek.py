import sys
import math


NONE = -1
ROBOT_ALLY = 0
ROBOT_ENEMY = 1
HOLE = 1
RADAR = 2
TRAP = 3
ORE = 4

def debug(msg):
    print(msg, file=sys.stderr)

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, pos):
        return abs(self.x - pos.x) + abs(self.y - pos.y)


class Entity(Pos):
    def __init__(self, x, y, type, id):
        super().__init__(x, y)
        self.type = type
        self.id = id


class Robot(Entity):
    def __init__(self, x, y, type, id, item):
        super().__init__(x, y, type, id)
        self.item = item
        self._cmdstr = None

    def is_dead(self):
        return self.x == -1 and self.y == -1

    def _cmd(self, new_cmd, message=None):
        self._cmdstr = new_cmd + (" # " + message if message else "") + (" ; " + self._cmdstr if self._cmdstr else "")

    def move(self, x, y, message=None):
        self._cmd(f"MOVE {x} {y}", message)

    def wait(self, message=None):
        self._cmd(f"WAIT", message)

    def dig(self, x, y, message=None):
        self._cmd(f"DIG {x} {y}", message)

    def radar(self, message=None):
        self._cmd("REQUEST RADAR", message)

    def trap(self, message=None):
        self._cmd(f"REQUEST TRAP", message)

    def do(self):
        print(self._cmdstr)

class Cell(Pos):
    def __init__(self, x, y, ore, hole):
        super().__init__(x, y)
        self.ore = ore
        self.hole = hole

    def has_hole(self):
        return self.hole == HOLE

    def update(self, ore, hole):
        self.ore = ore
        self.hole = hole


class Grid:
    def __init__(self, width, height):
        self.cells = []
        for y in range(height):
            for x in range(width):
                self.cells.append(Cell(x, y, 0, 0))
        self.width = width
        self.height = height

    def get_cell(self, x, y):
        if self.width > x >= 0 and self.height > y >= 0:
            return self.cells[x + self.width * y]
        return None


class Game:
    def __init__(self):
        width, height = [int(i) for i in input().split()]
        self.grid = Grid(width, height)
        self.my_score = 0
        self.enemy_score = 0
        self.radar_cooldown = 0
        self.trap_cooldown = 0
        self.turn = 0
        self.radars = []
        self.traps = []
        self.my_robots = []
        self.enemy_robots = []

    def see(self):
        # my_score: Players score
        self.my_score, self.enemy_score = [int(i) for i in input().split()]
        for i in range(self.grid.height):
            inputs = input().split()
            for j in range(self.grid.width):
                # ore: amount of ore or "?" if unknown
                # hole: 1 if cell has a hole
                ore = inputs[2 * j]
                hole = int(inputs[2 * j + 1])
                self.grid.get_cell(j, i).update(ore, hole)
        # entity_count: number of entities visible to you
        # radar_cooldown: turns left until a new radar can be requested
        # trap_cooldown: turns left until a new trap can be requested
        entity_count, self.radar_cooldown, self.trap_cooldown = [int(i) for i in input().split()]

        self.radars = []
        self.traps = []
        self.my_robots = []
        self.enemy_robots = []

        for i in range(entity_count):
            # id: unique id of the entity
            # type: 0 for your robot, 1 for other robot, 2 for radar, 3 for trap
            # y: position of the entity
            # item: if this entity is a robot, the item it is carrying (-1 for NONE, 2 for RADAR, 3 for TRAP, 4 for ORE)
            id, type, x, y, item = [int(j) for j in input().split()]

            if type == ROBOT_ALLY:
                self.my_robots.append(Robot(x, y, type, id, item))
            elif type == ROBOT_ENEMY:
                self.enemy_robots.append(Robot(x, y, type, id, item))
            elif type == TRAP:
                self.traps.append(Entity(x, y, type, id))
            elif type == RADAR:
                self.radars.append(Entity(x, y, type, id))

    def think(self):
        for i in range(len(self.my_robots)):
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)

            # WAIT|
            # MOVE x y|REQUEST item
            self.my_robots[i].wait(f"Starter AI {i}")
            self.my_robots[i].radar(f"Gaydar {i}")
            self.my_robots[i].trap(f"Its a Trap! {i}")

    def do(self):
        for i in range(len(self.my_robots)):
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)

            # WAIT|
            # MOVE x y|REQUEST item
            self.my_robots[i].do()
        # Advance turn
        self.turn = self.turn + 1


game = Game()

# game loop
while True:
    debug("===== TURN {} =====".format(game.turn))
    game.see()
    game.think()
    game.do()

debug("===== END =====")
