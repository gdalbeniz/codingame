import sys
import math
from enum import Enum
import random


def debug(msg):
    print(msg, file=sys.stderr)

class Cell:
    def __init__(self, cell_index, richness, neighbors):
        self.cell_index = cell_index
        self.richness = richness
        self.neighbors = neighbors
        debug(f"CELL {self.cell_index} rich {self.richness} {self.neighbors}")

class Tree:
    def __init__(self, cell_index, size, is_mine, is_dormant):
        self.cell_index = cell_index
        self.size = size
        self.is_mine = is_mine
        self.is_dormant = is_dormant
        debug(f"TREE {self.cell_index} sz {self.size} mine {self.is_mine} dorm {self.is_dormant}")

class ActionType(Enum):
    WAIT = "WAIT"
    SEED = "SEED"
    GROW = "GROW"
    COMPLETE = "COMPLETE"

class Action:
    def __init__(self, type, target_cell_id=None, origin_cell_id=None):
        self.type = type
        self.target_cell_id = target_cell_id
        self.origin_cell_id = origin_cell_id
        if self.type == ActionType.WAIT:
            self.astr = 'WAIT'
            self.score = 0
        elif self.type == ActionType.SEED:
            self.astr = f'SEED {self.origin_cell_id} {self.target_cell_id}'
            self.score = 1
        elif self.type == ActionType.GROW:
            self.astr = f'{self.type.name} {self.target_cell_id}'
            self.score = 2
        elif self.type == ActionType.COMPLETE:
            self.astr = f'{self.type.name} {self.target_cell_id}'
            self.score = 3
        debug(f"ACTION {self.astr} sc {self.score}")

    def __str__(self):
        return self.astr

    @staticmethod
    def parse(action_string):
        split = action_string.split(' ')
        if split[0] == ActionType.WAIT.name:
            return Action(ActionType.WAIT)
        if split[0] == ActionType.SEED.name:
            return Action(ActionType.SEED, int(split[2]), int(split[1]))
        if split[0] == ActionType.GROW.name:
            return Action(ActionType.GROW, int(split[1]))
        if split[0] == ActionType.COMPLETE.name:
            return Action(ActionType.COMPLETE, int(split[1]))

class Game:
    def __init__(self):
        self.day = 0
        self.nutrients = 0
        self.board = []
        self.trees = []
        self.actions = []
        self.sun = 0
        self.score = 0
        self.op_sun = 0
        self.op_score = 0
        self.op_waiting = 0
        for i in range(int(input())):
            cell, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
            self.board.append(Cell(cell, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]))

    def compute_next_action(self):
        return self.actions[0]

    def read_input(self):
        self.day = int(input())
        self.nutrients = int(input())
        self.sun, self.score = [int(i) for i in input().split()]
        self.op_sun, self.op_score, self.op_waiting = [int(i) for i in input().split()]
        self.trees.clear()
        for i in range(int(input())):
            cell, size, mine, dormant = [int(i) for i in input().split()]
            self.trees.append(Tree(cell, size, mine, dormant))
        self.actions.clear()
        for i in range(int(input())):
            self.actions.append(Action.parse(input()))
        self.actions.sort(key=lambda a: a.score, reverse=True)

game = Game()

while True:
    game.read_input()
    print(game.compute_next_action())
