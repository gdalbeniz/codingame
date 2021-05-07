import sys
from enum import Enum


MAX_INVENTORY_SIZE = 10


def debug(msg):
    print(msg, file=sys.stderr)


class ActionType(Enum):
    BREW = 1
    CAST = 2
    OPPONENT_CAST = 3
    LEARN = 4

    @staticmethod
    def action_to_string(action):
        return action.name

    @staticmethod
    def string_to_action(_string):
        for a in ActionType:
            if a.name == _string:
                return a


class Inventory():
    def __init__(self, delta0, delta1, delta2, delta3):
        self.deltas = [delta0, delta1, delta2, delta3]

    def __add__(self, other):
        aux = [self.deltas[i] + other.deltas[i] for i in range(len(self.deltas))]
        return Inventory(aux[0], aux[1], aux[2], aux[3])

    def __iter__(self):
        yield self.deltas[0]
        yield self.deltas[1]
        yield self.deltas[2]
        yield self.deltas[3]


class Action():
    def __init__(self, action_id, action_type, price, castable, deltas, repeatable, tome_index, tax_count):
        self.action_type = ActionType.string_to_action(action_type)
        self.action_id = action_id
        self.price = price
        self.deltas = deltas
        self.castable = castable
        self.repeatable = repeatable
        self.tome_index = tome_index
        self.tax_count = tax_count

    def output(self):
        print(ActionType.action_to_string(self.action_type) + " " + str(self.action_id))

    def is_doable(self, inventory):
        inventory_after_action = inventory + self.deltas
        if all(z >= 0 for z in inventory_after_action) and self.check_overflow(inventory):
            return True
        return False

    def check_overflow(self, inventory):
        size = sum(inventory) + sum(self.deltas)
        if size <= MAX_INVENTORY_SIZE:
            return True
        return False

    @staticmethod
    def read_next_action():
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action_id = int(action_id)
        delta_0 = int(delta_0)
        delta_1 = int(delta_1)
        delta_2 = int(delta_2)
        delta_3 = int(delta_3)
        price = int(price)
        tome_index = int(tome_index)
        tax_count = int(tax_count)
        castable = castable != "0"
        repeatable = repeatable != "0"
        return Action(action_id, action_type, price, castable,
                      Inventory(delta_0, delta_1, delta_2, delta_3),
                      repeatable, tome_index, tax_count)

    @staticmethod
    def read_next_actions(num_action):
        result = []
        for _ in range(0, num_action):
            result.append(Action.read_next_action())
        return result

    @staticmethod
    def get_action_higher_price(lst_actions):
        if len(lst_actions) != 0:
            return max(lst_actions, key=lambda act: act.price)
        return None


def get_all_actionstype(lst_actions, atype):
    result = []
    for action in lst_actions:
        if action.action_type == atype:
            result.append(action)
    return result


class Witch():
    def __init__(self):
        self.inventory = Inventory(3, 0, 0, 0)  # default resources
        self.score = 0
        self.next_action = None

    def read_next_witch_info(self):
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        self.inventory = Inventory(inv_0, inv_1, inv_2, inv_3)
        self.score = score


def any_cast_exhausted(lst_actions):
    for action in lst_actions:
        if action.action_type == ActionType.CAST and not action.castable:
            return True
    return False


def eval_solution(brew, cast, depth):
    return brew.price


def find_iterative_solution(inventory, casts, brews, depth=0, max_depth=4):
    if depth >= max_depth:
        return None

    best_option = None
    best_score = 0

    for cast in casts:
        if cast.is_doable(inventory):
            new_inventory = inventory + cast.deltas
            # TODO: Manage correctly repeatable casts and optimize rests
            for brew in brews:
                if brew.is_doable(new_inventory):
                    return (brew, cast)

            val = find_iterative_solution(new_inventory, casts, brews, depth+1, max_depth)
            if val:
                return (val[0], cast)
                new_score = eval_solution(val[0], val[1], depth)
                if new_score > best_score:
                    best_score = new_score
                    best_option = (val[0], cast)

    return best_option


class CodingameFall():
    def __init__(self):
        self.nround = 0  # Round number
        self.my_witch = Witch()
        self.oponent_witch = Witch()
        self.actions = []

    def loop(self):
        while True:
            self.get_new_input_data()
            self.think()
            self.output()
            self.nround += 1

    def get_new_input_data(self):
        self.actions.clear()
        self.my_witch.next_action = None
        action_count = int(input())  # the number of spells and recipes in play
        self.actions = Action.read_next_actions(action_count)
        self.my_witch.read_next_witch_info()
        self.oponent_witch.read_next_witch_info()

    def think(self):
        all_brew = get_all_actionstype(self.actions, ActionType.BREW)
        doable_brew = [brew for brew in all_brew if brew.is_doable(self.my_witch.inventory)]
        self.my_witch.next_action = Action.get_action_higher_price(doable_brew)

        if self.my_witch.next_action:
            return

        all_cast = get_all_actionstype(self.actions, ActionType.CAST)
        max_depth = 7
        all_brew.sort(key=lambda a: a.price)
        res = find_iterative_solution(self.my_witch.inventory, all_cast, all_brew, max_depth=max_depth)

        if res:
            if not any_cast_exhausted([res[1]]):
                self.my_witch.next_action = res[1]
        else:
            for act in get_all_actionstype(self.actions, ActionType.LEARN):
                if act.tome_index == 0:
                    self.my_witch.next_action = act
                    return

    def output(self):
        # Write an action using print
        if self.my_witch.next_action:
            self.my_witch.next_action.output()
        else:
            print("REST")


def main():
    game = CodingameFall()
    game.loop()


if __name__ == "__main__":
    main()
