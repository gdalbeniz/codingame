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

MINEPOSITION_X_MIN = 6
SMART_SABOTAGE_TURN = 0

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
        self.sabotage = None
        self.vein = None

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
        self.marked = False
        self.myhole = False

    def has_hole(self):
        return self.hole > 0

    def has_ore(self):
        return self.ore > 0 and not self.trap and not self.marked

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
        debugnnl("{}{},".format(self.ore if self.ore >= 0 else ' ', '!' if self.hole else ' '))
        #debugnnl("{}{}{}{}{},".format(self.ore if self.ore >= 0 else ' ',
        #                                   '!' if self.hole else ' ',
        #                                   'B' if self.bot else ' ',
        #                                   'R' if self.radar else ' ',
        #                                   'T' if self.trap else ' '))

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

    def has_ore(self, x, y):
        c = self.cell(x, y)
        if c:
            return c.has_ore()
        else:
            return False

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
        self.prospection = [Pos( 7, 3), Pos( 7,11), Pos(12, 7),
                            Pos(15, 3), Pos(15,11), Pos(20, 7),
                            Pos(23, 3), Pos(23,11), Pos(28, 7),
                            ]

        self.sabotagepos = [Pos(4, 4), Pos(3, 8), Pos(3,12),
                            Pos(2, 0), Pos(2, 4), Pos(2,7),
                            Pos(5, 13), Pos(4, 11), Pos(2,2),
                            Pos(3, 14), Pos( 5, 5), Pos( 2,11),
                            Pos(3, 5), Pos(3, 6), Pos(4,9),
                            Pos(5, 3), Pos(2, 9), Pos(3, 10),
                            Pos(3, 3), Pos(5, 6), Pos(4, 7),
                            Pos(3, 1), Pos( 4, 0), Pos( 4,2),
                            Pos(5, 8), Pos( 5, 10), Pos( 5,1),
                            ]
        self.prospecting = None
        self.sabotaging = None

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
        if self.turn % 5 == 0:
            self.grid.draw()
        

    def think(self):
        if self.radar_cooldown < 2 and len(self.prospection) > 0 and not self.prospecting:
            # choose bot nearest to hq as prospector
            prospect = self.prospection.pop(0)
            hq = prospect.delta(-width,0)
            for bot in sorted(self.bots, key=lambda b: b.distance(hq) - (100 if b.item == ORE or b.x == 0 else 0)):
                if bot.item != RADAR and bot.item != TRAP:
                    bot.prospect = prospect
                    debug(f"PROSPECT bot {bot.id} cell {bot.prospect.x},{bot.prospect.y}")
                    self.prospecting = bot
                    break
            else:
                self.prospection.append(prospect) # give back

        if self.trap_cooldown  < 2 and not self.sabotaging:
            # choose bot nearest to hq as sabotager
            for bot in sorted(self.bots, key=lambda b: b.distance(b.delta(-width,0)) - (100 if b.item == ORE or b.x == 0 else 0)):
                if (bot.item == ORE or bot.x == 0) and not bot.prospect:
                    for bestsabotage in sorted(self.grid.cells, key=lambda c: (c.ore*10-c.x-c.hole*100), reverse=True):
                        if self.turn < SMART_SABOTAGE_TURN:
                            continue
                        if bestsabotage.has_ore():
                            bot.sabotage = bestsabotage
                            debug(f"SABOTAGE bot {bot.id} cell {bot.sabotage.x},{bot.sabotage.y} ore {bot.sabotage.ore}")
                            break
                    else:
                        if len(self.sabotagepos) > 0:
                            sabpos = self.sabotagepos.pop(random.randint(0, len(self.sabotagepos)-1))
                            bot.sabotage = self.grid.cellpos(sabpos)
                        debug(f"SABOTAGE bot {bot.id} cell {bot.sabotage.x},{bot.sabotage.y} sabotagepos")
                    bot.sabotage.marked = True
                    self.sabotaging = bot
                    break


        for bot in self.bots:
            if bot.is_dead():
                # bot is dead
                bot.wait("dead")
                if bot.prospect:
                    self.prospecting = None
                    self.prospection.append(bot.prospect)
                if bot.sabotage:
                    self.sabotaging = None
                    self.sabotagepos.append(bot.sabotage)
            elif bot.prospect:
                # get radar from hq and place it
                if bot.x == 0 and self.radar_cooldown == 0:
                    bot.radar(f"bot {bot.id} radar")
                elif bot.item == RADAR:
                    while self.grid.cellpos(bot.prospect).trap:
                        bot.prospect = bot.prospect.delta(1, 0)
                    distance = bot.distance(bot.prospect)
                    if distance <= 1:
                        bot.dig(bot.prospect, f"bot {bot.id} set radar {len(self.radars)}")
                        self.grid.cellpos(bot.prospect).myhole = 1
                        bot.prospect = None
                        self.prospecting = None
                    else:
                        bot.move(bot.prospect.delta(-1, 0), f"bot {bot.id} moving left of radar dest")
                else:
                    hq = bot.prospect.delta(-width, 0)
                    distance = bot.distance(hq)
                    if distance <= 4:
                        bot.move(hq, f"bot {bot.id} moving straight to hq")
                    elif self.radar_cooldown == 1 and bot.x == 4:
                        bot.move(bot.delta(-4, 0), f"bot {bot.id} moving left to hq")
                    else:
                        bot.move(hq, f"bot {bot.id} moving slowly to hq")
            elif bot.sabotage:
                # get trap from hq and place it
                if bot.x == 0 and self.trap_cooldown == 0:
                    bot.trap(f"bot {bot.id} trap")
                elif bot.item == TRAP:
                    distance = bot.distance(bot.sabotage)
                    if distance <= 1:
                        bot.dig(bot.sabotage, f"bot {bot.id} set trap {len(self.traps)}")
                        self.grid.cellpos(bot.sabotage).myhole = 1
                        bot.sabotage = None
                        self.sabotaging = None
                    else:
                        bot.move(bot.sabotage.delta(-1, 0), f"bot {bot.id} moving left of trap dest")
                else:
                    hq = bot.sabotage.delta(-width, 0)
                    distance = bot.distance(hq)
                    if distance <= 4:
                        bot.move(hq, f"bot {bot.id} moving straight to hq")
                    elif self.trap_cooldown == 1 and bot.x == 4:
                        bot.move(bot.delta(-4, 0), f"bot {bot.id} moving left to hq")
                    else:
                        bot.move(hq, f"bot {bot.id} moving slowly to hq")
            elif bot.item == ORE:
                # take ore to hq
                bot.move(bot.delta(-width, 0), f"bot {bot.id} taking ore to hq")
            else:
                here = self.grid.cellpos(bot)
                right = self.grid.cellpos(bot.delta(1, 0))
                below = self.grid.cellpos(bot.delta(0, 1))
                above = self.grid.cellpos(bot.delta(0, -1))
                left = self.grid.cellpos(bot.delta(-1, 0))
                if bot.x >= MINEPOSITION_X_MIN and here.has_ore():
                    # mine here
                    bot.dig(here, f"bot {bot.id} mine here")
                    bot.vein = None
                    here.myhole = 1
                elif bot.x >= MINEPOSITION_X_MIN and right.has_ore():
                    # mine right
                    bot.dig(right, f"bot {bot.id} mine right")
                    bot.vein = None
                    right.myhole = 1
                elif bot.x >= MINEPOSITION_X_MIN and below.has_ore():
                    # mine below
                    bot.dig(below, f"bot {bot.id} mine below")
                    bot.vein = None
                    below.myhole = 1
                elif bot.x >= MINEPOSITION_X_MIN and above.has_ore():
                    # mine above
                    bot.dig(above, f"bot {bot.id} mine above")
                    bot.vein = None
                    above.myhole = 1
                elif bot.x >= MINEPOSITION_X_MIN and left.has_ore():
                    # mine left
                    bot.dig(left, f"bot {bot.id} mine left")
                    bot.vein = None
                    left.myhole = 1
                else:
                    # move to nearest vein
                    if not bot.vein or (bot.vein and not bot.vein.has_ore()): 
                        bot.vein = self.findvein(bot)
                    if bot.vein:
                        # move towards vein
                        bot.move(bot.vein, f"bot {bot.id} move towards vein {bot.vein.x},{bot.vein.y}")
                        bot.vein.ore = bot.vein.ore - 1
                    else:
                        # mine randomly
                        if bot.x >= MINEPOSITION_X_MIN and not right.has_hole():
                            bot.dig(right, f"bot {bot.id} mine randomly")
                        elif bot.x >= MINEPOSITION_X_MIN and not here.has_hole():
                            bot.dig(here, f"bot {bot.id} mine randomly")
                        elif bot.x >= MINEPOSITION_X_MIN and not below.has_hole():
                            bot.dig(below, f"bot {bot.id} mine randomly")
                        elif bot.x >= MINEPOSITION_X_MIN and not above.has_hole():
                            bot.dig(above, f"bot {bot.id} mine randomly")
                        elif bot.x >= MINEPOSITION_X_MIN and not left.has_hole():
                            bot.dig(left, f"bot {bot.id} mine randomly")
                        else:
                            rndpos = Pos(random.randint(MINEPOSITION_X_MIN+3,width-5), random.randint(3,height-3))
                            bot.move(rndpos, f"bot {bot.id} move randomly {rndpos.x},{rndpos.y}")


    def findvein(self, pos):
        for x in range(pos.x if pos.x > MINEPOSITION_X_MIN else MINEPOSITION_X_MIN, MINEPOSITION_X_MIN):
            # seek left
            if self.grid.has_ore(x, pos.y):
                return self.grid.cell(x, pos.y)
            elif self.grid.has_ore(x, pos.y-1):
                return self.grid.cell(x, pos.y-1)
            elif self.grid.has_ore(x, pos.y+1):
                return self.grid.cell(x, pos.y+1)
            elif self.grid.has_ore(x, pos.y-2):
                return self.grid.cell(x, pos.y-2)
            elif self.grid.has_ore(x, pos.y+2):
                return self.grid.cell(x, pos.y+2)
        for x in range(pos.x if pos.x > MINEPOSITION_X_MIN else MINEPOSITION_X_MIN, width):
            # seek right
            if self.grid.has_ore(x, pos.y):
                return self.grid.cell(x, pos.y)
            elif self.grid.has_ore(x, pos.y-1):
                return self.grid.cell(x, pos.y-1)
            elif self.grid.has_ore(x, pos.y+1):
                return self.grid.cell(x, pos.y+1)
            elif self.grid.has_ore(x, pos.y-2):
                return self.grid.cell(x, pos.y-2)
            elif self.grid.has_ore(x, pos.y+2):
                return self.grid.cell(x, pos.y+2)
        for x in range(pos.x if pos.x > MINEPOSITION_X_MIN else MINEPOSITION_X_MIN, MINEPOSITION_X_MIN):
            # seek further left
            if self.grid.has_ore(x, pos.y-3):
                return self.grid.cell(x, pos.y-3)
            if self.grid.has_ore(x, pos.y+3):
                return self.grid.cell(x, pos.y+3)
            elif self.grid.has_ore(x, pos.y-4):
                return self.grid.cell(x, pos.y-4)
            elif self.grid.has_ore(x, pos.y+4):
                return self.grid.cell(x, pos.y+4)
            elif self.grid.has_ore(x, pos.y-5):
                return self.grid.cell(x, pos.y-5)
            elif self.grid.has_ore(x, pos.y+5):
                return self.grid.cell(x, pos.y+5)
            elif self.grid.has_ore(x, pos.y-6):
                return self.grid.cell(x, pos.y-6)
            elif self.grid.has_ore(x, pos.y+6):
                return self.grid.cell(x, pos.y+6)
            elif self.grid.has_ore(x, pos.y-7):
                return self.grid.cell(x, pos.y-7)
            elif self.grid.has_ore(x, pos.y+7):
                return self.grid.cell(x, pos.y+7)
            elif self.grid.has_ore(x, pos.y-8):
                return self.grid.cell(x, pos.y-8)
            elif self.grid.has_ore(x, pos.y+8):
                return self.grid.cell(x, pos.y+8)
            elif self.grid.has_ore(x, pos.y-9):
                return self.grid.cell(x, pos.y-9)
            elif self.grid.has_ore(x, pos.y+9):
                return self.grid.cell(x, pos.y+9)
            elif self.grid.has_ore(x, pos.y-10):
                return self.grid.cell(x, pos.y-10)
            elif self.grid.has_ore(x, pos.y+10):
                return self.grid.cell(x, pos.y+10)
        for x in range(pos.x if pos.x > MINEPOSITION_X_MIN else MINEPOSITION_X_MIN, width):
            # seek further right
            if self.grid.has_ore(x, pos.y-3):
                return self.grid.cell(x, pos.y-3)
            if self.grid.has_ore(x, pos.y+3):
                return self.grid.cell(x, pos.y+3)
            elif self.grid.has_ore(x, pos.y-4):
                return self.grid.cell(x, pos.y-4)
            elif self.grid.has_ore(x, pos.y+4):
                return self.grid.cell(x, pos.y+4)
            elif self.grid.has_ore(x, pos.y-5):
                return self.grid.cell(x, pos.y-5)
            elif self.grid.has_ore(x, pos.y+5):
                return self.grid.cell(x, pos.y+5)
            elif self.grid.has_ore(x, pos.y-6):
                return self.grid.cell(x, pos.y-6)
            elif self.grid.has_ore(x, pos.y+6):
                return self.grid.cell(x, pos.y+6)
            elif self.grid.has_ore(x, pos.y-7):
                return self.grid.cell(x, pos.y-7)
            elif self.grid.has_ore(x, pos.y+7):
                return self.grid.cell(x, pos.y+7)
            elif self.grid.has_ore(x, pos.y-8):
                return self.grid.cell(x, pos.y-8)
            elif self.grid.has_ore(x, pos.y+8):
                return self.grid.cell(x, pos.y+8)
            elif self.grid.has_ore(x, pos.y-9):
                return self.grid.cell(x, pos.y-9)
            elif self.grid.has_ore(x, pos.y+9):
                return self.grid.cell(x, pos.y+9)
            elif self.grid.has_ore(x, pos.y-10):
                return self.grid.cell(x, pos.y-10)
            elif self.grid.has_ore(x, pos.y+10):
                return self.grid.cell(x, pos.y+10)      
        return None
            

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
