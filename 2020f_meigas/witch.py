import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

inventory_max = 10
castable_max = 12

def debug(fmt):
    print(fmt, file=sys.stderr, flush=True)

def can_brew(delta, inv):
    sum_0 = delta[0] + inv[0]
    sum_1 = delta[1] + inv[1]
    sum_2 = delta[2] + inv[2]
    sum_3 = delta[3] + inv[3]
    return sum_0 >= 0 and sum_1 >= 0 and sum_2 >= 0 and sum_3 >= 0

def can_cast(delta, inv, maxinv=None):
    sum_0 = delta[0] + inv[0]
    sum_1 = delta[1] + inv[1]
    sum_2 = delta[2] + inv[2]
    sum_3 = delta[3] + inv[3]
    is_needed = sum_1 <= maxinv[1] and sum_2 <= maxinv[2] and sum_3 <= maxinv[3] if maxinv else True
    fits_inventory = (sum_0 + sum_1 + sum_2 + sum_3) <= inventory_max
    return sum_0 >= 0 and sum_1 >= 0 and sum_2 >= 0 and sum_3 >= 0 and fits_inventory and is_needed

def can_learn(learn, inv):
    return inv[0] >= learn["tome_index"]

def update_maxinv(maxinv, delta):
    maxinv_0 = maxinv[0] if maxinv[0] > -delta[0] else -delta[0]
    maxinv_1 = maxinv[1] if maxinv[1] > -delta[1] else -delta[1]
    maxinv_2 = maxinv[2] if maxinv[2] > -delta[2] else -delta[2]
    maxinv_3 = maxinv[3] if maxinv[3] > -delta[3] else -delta[3]
    return (maxinv_0, maxinv_1, maxinv_2, maxinv_3)

# game loop
for turn in range(100):
    action_count = int(input())  # the number of spells and recipes in play
    actions = []
    for i in range(action_count):
        # action_id: the unique ID of this spell or recipe
        # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
        # delta_0: tier-0 ingredient change
        # delta_1: tier-1 ingredient change
        # delta_2: tier-2 ingredient change
        # delta_3: tier-3 ingredient change
        # price: the price in rupees if this is a potion
        # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax
        # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell
        # castable: in the first league: always 0; later: 1 if this is a castable player spell
        # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action = dict()
        action["aid"] = int(action_id)
        action["type"] = action_type
        action["delta"] = ( int(delta_0), int(delta_1), int(delta_2), int(delta_3) )
        action["delta_0"] = int(delta_0)
        action["delta_1"] = int(delta_1)
        action["delta_2"] = int(delta_2)
        action["delta_3"] = int(delta_3)
        action["price"] = int(price)
        action["tome_index"] = int(tome_index)
        action["tax_count"] = int(tax_count)
        action["castable"] = castable != "0"
        action["repeatable"] = repeatable != "0"
        actions.append(action)

    #actions.sort(key=lambda a: -100*a["price"] + (a["tome_index"] if a["type"] == "LEARN" else -50 if a["type"] == "CAST" else 100))
    actions.sort(key=lambda a: -100*a["price"])

    me = dict()
    other = dict()
    for i in range(2):
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        if i == 0:
            me["inv"] = (inv_0, inv_1, inv_2, inv_3)
            me["score"] = score
        else:
            other["inv"] = (inv_0, inv_1, inv_2, inv_3)
            other["score"] = score
            

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    for a in actions:
        if a["type"] == "BREW":
            debug("{type} {aid}: {price},({delta_0},{delta_1},{delta_2},{delta_3}), {tome_index},{tax_count}, {castable},{repeatable}".format(**a))
    #debug("me: {inv_0}, {inv_1}, {inv_2}, {inv_3}, {score}".format(**me))
    #debug("oth: {inv_0}, {inv_1}, {inv_2}, {inv_3}, {score}".format(**other))

    orderlist = []
    maxinv = (0, 0, 0, 0)
    cast_num = 0
    needs_rest = 0
    for a in actions:
        if a["type"] == "BREW":
            if can_brew(a["delta"], me["inv"]):
                orderlist.append("{type} {aid} #{type} {aid}".format(**a))
            maxinv = update_maxinv(maxinv, a["delta"])
        if a["type"] == "CAST":
            if a["castable"] and can_cast(a["delta"], me["inv"], maxinv):
                orderlist.append("{type} {aid} #{type} {aid}".format(**a))
            if not a["castable"]:
                needs_rest += 1
            cast_num += 1
        if False and needs_rest >= 5:
            orderlist.append("REST #REST")
        if a["type"] == "LEARN":
            if can_learn(a, me["inv"]) and (cast_num < castable_max or len(orderlist) == 0):
                orderlist.append("{type} {aid} #{type} {aid}".format(**a))
    
    if needs_rest > 0:
        orderlist.append("REST #REST")
    orderlist.append("WAIT #WAIT")

    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT
    print(orderlist[0])
