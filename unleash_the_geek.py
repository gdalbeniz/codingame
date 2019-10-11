import sys
import math
import random


NONE = -1
ROBOT_ALLY = 0
ROBOT_ENEMY = 1
HOLE = 1
RADAR = 2
TRAP = 3
ORE = 4

# FUCK!
width, height = [int(i) for i in input().split()]

debug_flag = True
def debug(msg):
    if debug_flag:
        print(msg, file=sys.stderr)
def debugnnl(msg):
    if debug_flag:
        print(msg, file=sys.stderr, end='')

class Pos:
    def __init__(self, x, y):
        if x < 0:
            self.x = 0
        elif x >= width:
            self.x = width - 1
        else:
            self.x = x
        if y < 0:
            self.y = 0
        elif y >= height:
            self.y = height - 1
        else:
            self.y = y

    def distance(self, pos):
        return abs(self.x - pos.x) + abs(self.y - pos.y)
    
    def delta(self, x, y):
        return Pos(self.x+x, self.y+y)


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
        self.prospect = None

    def is_dead(self):
        return self.x == -1 and self.y == -1

    def update(self, x, y, item):
        self.x = x
        self.y = y
        self.item = item

    def _cmd(self, new_cmd, message=None):
        self._cmdstr = new_cmd + (" # " + message if message else "") + (" ; " + self._cmdstr if self._cmdstr else "")

    def move(self, pos, message=None):
        self._cmd(f"MOVE {pos.x} {pos.y}", message)

    def wait(self, message=None):
        self._cmd(f"WAIT", message)

    def dig(self, pos, message=None):
        self._cmd(f"DIG {pos.x} {pos.y}", message)

    def radar(self, message=None):
        self._cmd("REQUEST RADAR", message)

    def trap(self, message=None):
        self._cmd(f"REQUEST TRAP", message)

    def do(self):
        if not self._cmdstr:
            self.wait("default") # dead bot?
        print(self._cmdstr)
        self._cmdstr = None


class Cell(Pos):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ore = 0
        self.hole = 0

    def has_hole(self):
        return self.hole > 0
    def has_ore(self):
        return self.ore > 0

    def update(self, ore, hole):
        self.ore = ore
        self.hole = hole
        self.bot = None
        self.enemy = None
        self.trap = None
        self.radar = None

    def place(self, entity):
        if entity.type == ROBOT_ALLY:
            self.bot = entity
        elif entity.type == ROBOT_ENEMY:
            self.enemy = entity
        elif entity.type == TRAP:
            self.trap = entity
        elif entity.type == RADAR:
            self.radar = entity

    def draw(self):
        debugnnl("{}{}{}{}{},".format(self.ore if self.ore >= 0 else ' ',
                                           '!' if self.hole else ' ',
                                           'B' if self.bot else ' ',
                                           'R' if self.radar else ' ',
                                           'T' if self.trap else ' '))

class Grid:
    def __init__(self, width, height):
        self.cells = []
        for y in range(height):
            for x in range(width):
                self.cells.append(Cell(x, y))
        self.width = width
        self.height = height

    def cell(self, x, y):
        if self.width > x >= 0 and self.height > y >= 0:
            return self.cells[x + self.width * y]
        return None
    def cellpos(self, pos):
        return self.cell(pos.x, pos.y)

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                self.cell(x, y).draw()
            debug(f" # {y}") # for newline


class Game:
    def __init__(self):
        self.grid = Grid(width, height)
        self.my_score = 0
        self.enemy_score = 0
        self.radar_cooldown = 0
        self.trap_cooldown = 0
        self.turn = 0
        self.radars = []
        self.traps = []
        self.bots = []
        self.enemies = []
        self.prospection = [( 5, 3), (10, 7), ( 5,11),
                            (13, 3), (18, 7), (13,11),
                            (21, 3), (26, 7), (21,11),]
                            #(26, 4), (21, 8), (26,12),
                            #(18, 4), (13, 8), (18,12),
                            #(10, 4), ( 5, 8), (10,12),]
        self.prospecting = True

    def see(self):
        # reset
        self.oreseen = 0
        self.radars = []
        self.traps = []
        self.enemies = []

        # my_score: Players score
        self.my_score, self.enemy_score = [int(i) for i in input().split()]
        for i in range(self.grid.height):
            inputs = input().split()
            for j in range(self.grid.width):
                # ore: amount of ore or "?" if unknown
                # hole: 1 if cell has a hole
                ore = int(inputs[2 * j]) if inputs[2 * j] != '?' else -1
                hole = int(inputs[2 * j + 1])
                self.grid.cell(j, i).update(ore, hole)
                if ore > 0:
                    self.oreseen = self.oreseen + ore
        # entity_count: number of entities visible to you
        # radar_cooldown: turns left until a new radar can be requested
        # trap_cooldown: turns left until a new trap can be requested
        entity_count, self.radar_cooldown, self.trap_cooldown = [int(i) for i in input().split()]

        for i in range(entity_count):
            # id: unique id of the entity
            # type: 0 for your robot, 1 for other robot, 2 for radar, 3 for trap
            # y: position of the entity
            # item: if this entity is a robot, the item it is carrying (-1 for NONE, 2 for RADAR, 3 for TRAP, 4 for ORE)
            id, type, x, y, item = [int(j) for j in input().split()]

            if type == ROBOT_ALLY:
                for bot in self.bots:
                    if id == bot.id:
                        bot.update(x, y, item)
                        if self.grid.cell(x,y):
                            self.grid.cell(x,y).place(bot)
                        break
                else:
                    bot = Robot(x, y, type, id, item)
                    self.bots.append(bot)
                    self.grid.cell(x,y).place(bot)
            elif type == ROBOT_ENEMY:
                bot = Robot(x, y, type, id, item)
                self.enemies.append(bot)
                if self.grid.cell(x,y):
                    self.grid.cell(x,y).place(bot)
            elif type == TRAP:
                entity = Entity(x, y, type, id)
                self.traps.append(entity)
                self.grid.cell(x,y).place(entity)
            elif type == RADAR:
                entity = Entity(x, y, type, id)
                self.radars.append(entity)
                self.grid.cell(x,y).place(entity)
            
        debug(f" -- score: {self.my_score} - {self.enemy_score} radar in: {self.radar_cooldown} trap in: {self.trap_cooldown}")
        if self.turn % 10 == 0:
            self.grid.draw()
        

    def think(self):
        if self.radar_cooldown < 2 and len(self.prospection) > 0 and self.prospecting:
            # choose bot nearest hq as prospector
            radar_coor = self.prospection.pop(0)
            radar_pos = Pos(radar_coor[0], radar_coor[1])
            headq_pos = Pos(0, radar_coor[1])
            for bot, _ in sorted([(bot, bot.distance(headq_pos)) for bot in self.bots], key=lambda x: x[1]):
                if bot.item != RADAR and bot.item != TRAP:
                    bot.prospect = (radar_pos, headq_pos)
                    self.prospecting = False # pause prospecting until radar is placed
                    break
            else:
                self.prospection.append(radar_coor) # give back
        #for x in range(len(self.grid))

        for bot in self.bots:
            if bot.is_dead():
                # bot is dead
                bot.wait("dead")
            elif bot.prospect:
                # get radar from hq and place it
                if bot.x == 0 and self.radar_cooldown == 0:
                    bot.radar()
                elif bot.item == RADAR:
                    distance = bot.distance(bot.prospect[0])
                    if distance <= 1:
                        bot.dig(bot.prospect[0], f"bot {bot.id} set radar {len(self.radars)}")
                        bot.prospect = None
                        self.prospecting = True
                    else:
                        bot.move(bot.prospect[0].delta(-1, 0), f"bot {bot.id} moving left of radar dest")
                else:
                    distance = bot.distance(bot.prospect[1])
                    if distance <= 4:
                        bot.move(bot.prospect[1], f"bot {bot.id} moving straight to hq")
                    elif self.radar_cooldown == 1 and bot.x <= 4:
                        bot.move(bot.delta(-4, 0), f"bot {bot.id} moving left to hq")
                    else:
                        bot.move(bot.prospect[1], f"bot {bot.id} moving slowly to hq")
            elif bot.item == ORE:
                # take ore to hq
                bot.move(bot.delta(-5, 0))
            elif self.grid.cellpos(bot.delta(1, 0)).has_ore():
                # mine right
                bot.dig(bot.delta(1, 0))
            elif self.grid.cellpos(bot).has_ore():
                # mine here
                bot.dig(bot)
            elif self.grid.cellpos(bot.delta(0, 1)).has_ore():
                # mine below
                bot.dig(bot.delta(0, 1))
            elif self.grid.cellpos(bot.delta(0, -1)).has_ore():
                # mine above
                bot.dig(bot.delta(0, -1))
            elif self.grid.cellpos(bot.delta(-1, 0)).has_ore():
                # mine left
                bot.dig(bot.delta(-1, 0))
            else:
                # move to nearest vein
                vein = None
                for x in range(2, bot.x):
                    # seek left
                    if self.grid.cellpos(bot.delta(-x, 0)).has_ore():
                        vein = bot.delta(-x, 0)
                    elif self.grid.cellpos(bot.delta(-x, -1)).has_ore():
                        vein = bot.delta(-x, -1)
                    elif self.grid.cellpos(bot.delta(-x, 1)).has_ore():
                        vein = bot.delta(-x, 1)
                    elif self.grid.cellpos(bot.delta(-x, -2)).has_ore():
                        vein = bot.delta(-x, -2)
                    elif self.grid.cellpos(bot.delta(-x, 2)).has_ore():
                        vein = bot.delta(-x, 2)
                    if vein:
                        bot.move(vein, "seeking left")
                        break
                for x in range(2, bot.x):
                    if vein:
                        break
                    # seek left up
                    elif self.grid.cellpos(bot.delta(-x, -3)).has_ore():
                        vein = bot.delta(-x, -3)
                    elif self.grid.cellpos(bot.delta(-x, -4)).has_ore():
                        vein = bot.delta(-x, -4)
                    elif self.grid.cellpos(bot.delta(-x, -5)).has_ore():
                        vein = bot.delta(-x, -5)
                    elif self.grid.cellpos(bot.delta(-x, -6)).has_ore():
                        vein = bot.delta(-x, -6)
                    if vein:
                        bot.move(vein, "seeking left up")
                        break
                for x in range(2, bot.x):
                    if vein:
                        break
                    # seek left down
                    elif self.grid.cellpos(bot.delta(-x, 3)).has_ore():
                        vein = bot.delta(-x, 3)
                    elif self.grid.cellpos(bot.delta(-x, 4)).has_ore():
                        vein = bot.delta(-x, 4)
                    elif self.grid.cellpos(bot.delta(-x, 5)).has_ore():
                        vein = bot.delta(-x, 5)
                    elif self.grid.cellpos(bot.delta(-x, 6)).has_ore():
                        vein = bot.delta(-x, 6)
                    if vein:
                        bot.move(vein, "seeking left down")
                        break
                for x in range(2, 7):
                    if vein:
                        break
                    # seek right
                    if self.grid.cellpos(bot.delta(x, 0)).has_ore():
                        vein = bot.delta(x, 0)
                    elif self.grid.cellpos(bot.delta(x, -1)).has_ore():
                        vein = bot.delta(x, -1)
                    elif self.grid.cellpos(bot.delta(x, 1)).has_ore():
                        vein = bot.delta(x, 1)
                    elif self.grid.cellpos(bot.delta(x, -2)).has_ore():
                        vein = bot.delta(x, -2)
                    elif self.grid.cellpos(bot.delta(x, 2)).has_ore():
                        vein = bot.delta(x, 2)
                    if vein:
                        bot.move(vein, "seeking right")
                        break
                for x in range(2, 7):
                    if vein:
                        break
                    # seek right up
                    elif self.grid.cellpos(bot.delta(x, -3)).has_ore():
                        vein = bot.delta(x, -3)
                    elif self.grid.cellpos(bot.delta(x, -4)).has_ore():
                        vein = bot.delta(x, -4)
                    elif self.grid.cellpos(bot.delta(x, -5)).has_ore():
                        vein = bot.delta(x, -5)
                    elif self.grid.cellpos(bot.delta(x, -6)).has_ore():
                        vein = bot.delta(x, -6)
                    if vein:
                        bot.move(vein, "seeking right up")
                        break
                for x in range(2, 7):
                    if vein:
                        break
                    # seek right down
                    elif self.grid.cellpos(bot.delta(x, 3)).has_ore():
                        vein = bot.delta(x, 3)
                    elif self.grid.cellpos(bot.delta(x, 4)).has_ore():
                        vein = bot.delta(x, 4)
                    elif self.grid.cellpos(bot.delta(x, 5)).has_ore():
                        vein = bot.delta(x, 5)
                    elif self.grid.cellpos(bot.delta(x, 6)).has_ore():
                        vein = bot.delta(x, 6)
                    if vein:
                        bot.move(vein, "seeking right down")
                        break
                if not vein:
                    # move randomly
                    bot.move(bot.delta(random.randint(2,5), random.randint(-2,3)))
                
                        


            

    def do(self):
        for bot in self.bots:
            bot.do()
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
