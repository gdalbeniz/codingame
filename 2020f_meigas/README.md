# Goal

End the game with more rupees than your opponent.  

The game takes place in a **potion shop**, in which two twin-sister **witches** are trying to prove they are the better potion brewer.  
They have set up a contest: make more rupees selling potions than your sister.  
However, the **witch's hut** in which they set up shop is quite small, so they must share the same workspace, and deal with the same **client orders**.

# Rules

Each player controls a **witch**, each witch has access to their own **inventory** of potion ingredients and a list of **spells** they have learnt. These spells can be used to turn **a certain set of ingredients into another**.  
Each **client order** is a list of ingredients required to brew a potion and earn some rupees.  

The game is played over several rounds. Each player performs one action each turn, simultaneously.  

## Ingredients

There are 4 tiers of ingredient, indexed from `0` to `3`  

A witch's **inventory** can contain up to `10` ingredients.  

Each witch starts with `3` tier-0 ingredients in their inventory.  

The inventory is represented by `inv`: **4 numbers** each representing the amount of each ingredient tier.  

## Action overview

Each round, you can perform one of the following actions:  

* `Learn` a new spell from the **magic tome**.
* `Cast` one of the spells you have learnt.
* `Rest` to refresh all previously cast spells.
* `Brew` a potion to score points. 

You may also opt to skip a turn with the `WAIT` command.  

### Casting Spells

Spells have a `delta`: 4 numbers, one for each ingredient tier.  
Positive numbers represent the amount of ingredients that are produced by the recipe.  
Negative numbers represent the amount of ingredients that are consumed by the recipe.  
For instance, a spell marked `-1,1,0,0` means it can turn one tier-0 ingredient into a tier-1 ingredient.  

You may learn any number of spells during the game, but once you have cast a spell, it becomes **exhausted**. You may not cast exhausted spells.  

Some spells are `repeatable`, meaning they can be used **multiple times on the same turn** before becoming exhausted.  

The same **four** basic spells are always available at the start of the game. Use them to build up your repertoire of more efficient spells.  

Some spells do not consume ingredients, they simply produce new ingredients.  

Each player spell has a unique `id` and can be cast with the `CAST id` command.  

Choose the number of `times` to cast a repeatable spell with the `CAST id times` command.

### Learning Spells

The **magic tome** the witch sisters are using is quite volatile. Once a witch has memorised a spell, that spell **disappears** from the tome completely and is no longer available to the other witch.  

To preserve a sense of fairness in their sisterly spat, the witches have devised a system:  

* They may only read from the first `6` available spells on each round.
* The first spell in the list may be learnt freely.
* To gain the right to memorise any spell further along in the list, they must put down a "read-ahead tax" by placing **one tier-0 ingredient** upon each spell that appears earlier in the tome.
* For instance, if you want to learn the 4th spell in the tome, you must place a tier-0 ingredient on the first, second, and third.
* You may only do this if you can afford it.
* Whenever they memorise a spell with ingredients placed upon it, they also acquire those ingredients, which become usable on the next turn. If the witch's inventory is full, the excess is discarded.

The read-ahead tax is applied **after** learnt spells have disappeared from the tome, meaning new spells may be present in the 6 available when the ingredients are placed.  

The tome is not infinite, there are exactly `42` spells within.  

Each tome spell has a unique `id` and can be learnt with the `LEARN id` command.  

### Resting

Resting lets you channel your magic, rendering all **exhausted** spells available again for casting.  

You can order your witch to rest with the `REST` command.

### Brewing

**Client orders** have a `delta`: **4 numbers**, one for each ingredient tier.  
Negative numbers represent the amount of ingredients that are consumed by the recipe.  
Therefore, the numbers are **never positive** because they represent a loss of ingredients from your inventory.  

For instance, a client order with `delta = -2, -1, 0, 0` means you have to consume 2 tier-0 ingredients and 1 tier-1 ingredients from your inventory in order to brew the potion.  

The selling `price` of the client order is the amount of rupees will you earn by completing it.  

The client orders are queued up from left to right. Only five clients can fit inside the hut so a maximum of `5` orders will be available every turn.  

You may deliver a potion for any of the clients within the hut, but the clients near the end of the queue (the left-most client orders) may earn you an **urgency bonus**. The bonus works as follows:

* Brewing a potion for the very first client awards a **+3 rupee bonus,** but this can only happen **4** times during the game.
* Brewing a potion for the second client awards a **+1 rupee bonus**, but this also can only happen **4** times during the game.
* If all **+3 bonuses** have been used up, the **+1 bonus** will be awarded by the first client instead of the second client.

At the start of each new turn, new orders are queued up to fill the missing spaces.  

Each order has a unique `id` and can be undertaken with the `BREW id` command.

## Game end

The game ends once at least one witch has brewed **6** potions.  

The game stops automatically after **100 rounds**.  

Players gain **1 rupee** for each tier-1 ingredient or higher in their inventory.  

### Victory Conditions

* The winner is the player with the most rupees. 

### Defeat Conditions

* Your program does not provide a command in the alloted time or one of the commands is unrecognized. 


# Debugging tips

* Hover over a spell or recipe to see extra information about it
* Append text after any command and that text will appear next to your witch
* Press the gear icon on the viewer to access extra display options
* Use the keyboard to control the action: space to play/pause, arrows to step 1 frame at a time

# Technical Details

* When both witches perform the same action, they both reap the rewards for that action. This applies namely to potion prices, the urgency bonus, the read-ahead tax, and learning spells.
* If both witches complete an order with an urgency bonus, two bonuses of that bonus level are consumed. If there is only one, it is consumed and both witches still get the same rewards.
* The order in which spells appear in the tome is random. However, the list of all possible spells is always the same.
* After learning a spell, the learnt version of the spell has a different id from the one previously within the tome.
* You can check out the source code of this game on this GitHub repo. You can find a list of all possible spells in the tome.
* A witch cannot obtain an ingredient from the tome on the same turn as it is placed there by the other witch.
* If the absolute final spell is learnt on the same turn as a read-ahead tax is applied, the extra tier-0 ingredient is discarded.

# Game Protocol

## Input for One Game Turn

**Line 1**: one integer `actionCount` for the sum total of all available tome spells, both sets of player spells, and every available client order.  
**Next `actionCount` lines: 11** space-separated values to describe a game action.  

* `actionId`: the id of this action
* `actionType`: a string
    * `CAST` for one of your learnt spells
    * `OPPONENT_CAST` for one of your opponent's learnt spells
    * `LEARN` for a tome spell
    * `BREW` for a potion recipe 
* `delta0`, `delta1`, `delta2`, `delta3`: the four numbers describing the consumption/producion of ingredients for each tier.
* `price`: the amount of rupees this will win you if this is a potion recipe, 0 otherwise. This includes the urgency bonus.
* `tomeIndex`: the index in the tome of this action if this is a tome spell, -1 otherwise. Is equal to the read-ahead tax to learn this spell.  
This is also the **value** of the urgency bonus if this is a potion recipe.
* `taxCount`: the amount of tier-0 ingredients you will gain by learning this spell if this is a tome spell, 0 otherwise.  
This is also the amount of times an urgency bonus can still be gained if this is a potion recipe.
* `castable`: `1` if this is a player spell that is not exhausted, `0` otherwise.
* `repeatable`: `1` if this is a repeatable spell, `0` otherwise.

**Next 2 lines: 5** integers to describe each player, your data is always first:  

* `inv0` for the amount of tier-0 ingredients in their inventory.
* `inv1` for the amount of tier-1 ingredients in their inventory.
* `inv2` for the amount of tier-2 ingredients in their inventory.
* `inv3` for the amount of tier-3 ingredients in their inventory.
* `score` for the amount of rupees earned so far.

## Output

A single line with your command:  

* `BREW id`: your witch attempts to brew the potion with the given id.
* `CAST id`: your witch attempts to cast the spell with the given id.
* `CAST id` times: your witch casts a repeatable spell the given amount of times.
* `LEARN id`: your witch attempts to learn the tome spell with the given id.
* `REST`: your witch channels her magic and your exhausted spells become castable again.
* `WAIT`: your witch does nothing. 

## Constraints

0 < `actionCount` ≤ 100  
6 ≤ `price` ≤ 23  
Response time per turn ≤ 50ms  
Response time for the first turn ≤ 1000ms  
