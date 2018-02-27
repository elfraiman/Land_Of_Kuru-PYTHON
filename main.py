# Multi map rpg
import time
import os
import math
import random

running = True


# Classes
class Player:
    def __init__(self, name, hp, mp, str, dex, int, con, critRate, exp, upExp, level, gold):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.mp = mp
        self.maxMp = mp
        self.str = str
        self.dex = dex
        self.int = int
        self.con = con
        self.critRate = critRate
        self.level = level
        self.exp = exp
        self.upExp = upExp
        self.gold = gold
        self.location = "a1"  # Default starting block is a1
        self.map = "default"
        self.player_class = ""
        self.inventory = ["sword", "small hp pot"]
        self.available_enemy = []
        self.damage = 0
        self.main_hand = ""
        self.hand_min_damage = 2
        self.hand_max_damage = 4
        self.quest_npc = None
        self.current_objective = ''
        self.objective_count_goal = 0
        self.objective_count = 0


class Enemy:
    def __init__(self, name,  hp, attack, defense, level, gold, exp):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.attack = attack
        self.max_attack = attack + 5
        self.defense = defense
        self.level = level
        self.gold = gold
        self.exp = exp


class Npc:
    def __init__(self, name, discrip, short_story, gold, type):
        self.name = name
        self.discrip = discrip
        self.short_story = short_story
        self.items = []
        self.gold = gold
        self.type = type


class Item:
    def __init__(self, name, value, minatt, maxatt, player_class):
        self.name = name
        self.value = value
        self.minatt = minatt
        self.maxatt = maxatt
        self.player_class = player_class


class QuestNPC:
    def __init__(self, name, discrip, count, short_story, reward, solved, type, monster):
        self.name = name
        self.discrip = discrip
        self.short_story = short_story
        self.count = count
        self.objective = short_story
        self.reward = reward
        self.solved = solved
        self.type = type
        self.monster = monster

#  Quest npc's
billy = QuestNPC("Billy the farmer", "I need your help!", 2, "The damn rats are eating my corps, please kill 2 rats.", 250, False, 'quest', 'Rat | Lv.5')


# Items name, value, minatt, maxatt, player_class
bronze_sword = Item('Bronze 2H Sword(10-14)', 50, 10, 14, "warrior")
steel_sword = Item('Steel 2H Sword(15-21)', 100, 15, 21, "warrior")
steel_mace = Item('Steel 2H Mace(13-26)', 100, 13, 26, "warrior")
mithril_sword = Item('Mithirl 2H Sword(21-28)', 250, 21, 28, "warrior")
mithril_mace = Item("Mithirl 2H Mace(17-33)", 250, 17, 33, "warrior")


# NPCS/Vendors
nina = Npc('Nina', 'General Vendor', "Welcome traveler, How can i help you?", 1000, 'store')
nina.items = [bronze_sword, steel_sword, steel_mace, mithril_sword, mithril_mace]

# Enemy Mobs by zones
# Training zone mobs
training_dummy = Enemy("Training Dummy | Lv.1", 20, 10, 1, 1, 10, 5)
spider = Enemy("Spider | Lv.2", 30, 12, 2, 2, 15, 8)
worm = Enemy("Worm | Lv.3", 35, 13, 2, 3, 15, 9)
turtle = Enemy("Turtle | Lv.3", 40, 13, 2, 3, 15, 9)
bunny = Enemy("Bunny | Lv.4", 45, 13, 3, 4, 15, 12)
rat = Enemy("Rat | Lv.5", 50, 15, 3, 5, 18, 15)
training_mobs = [training_dummy, spider, worm, turtle, bunny, rat]


# Building the Maps
ZONENAME = 'zonename'
DESCRIPTION = 'description'
EXAMINATION = 'info'
SOLVED = False
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'
NPC = ''

"""
Example of the map

[a1][a2][a3][a4]
[b1][b2][b3][b4]
[c1][c2][c3][c4]
[d1][d2][d3][d4]
"""

training_field_map = { # Training field map # Starting zone!
    'a1': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: '',
        DOWN: 'b1',
        LEFT: '',
        RIGHT: 'a2',
        NPC: '',
    },
    'a2': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: '',
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'a3',
        NPC: nina,

    },
    'a3': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: '',
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: 'a4',
        NPC: billy,
    },
    'a4': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: '',
        DOWN: 'b4',
        LEFT: 'a3',
        RIGHT: '',
        NPC: '',
    },
    'b1': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'a1',
        DOWN: 'c1',
        LEFT: '',
        RIGHT: 'b2',
        NPC: '',
    },
    'b2': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'a2',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: 'b3',
        NPC: '',
    },
    'b3': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'a3',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: 'b4',
        NPC: '',
    },
    'b4': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'a4',
        DOWN: 'c4',
        LEFT: 'b3',
        RIGHT: '',
        NPC: '',
    },
    'c1': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'b1',
        DOWN: 'd1',
        LEFT: '',
        RIGHT: 'c2',
        NPC: '',
    },
    'c2': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'b2',
        DOWN: 'd2',
        LEFT: 'c1',
        RIGHT: 'c3',
        NPC: '',
    },
    'c3': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'b3',
        DOWN: 'd3',
        LEFT: 'c2',
        RIGHT: 'c4',
        NPC: '',
    },
    'c4': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'b4',
        DOWN: 'd4',
        LEFT: 'c3',
        RIGHT: '',
        NPC: '',
    },
    'd1': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'c1',
        DOWN: '',
        LEFT: '',
        RIGHT: 'd2',
        NPC: '',
    },
    'd2': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'c2',
        DOWN: '',
        LEFT: 'd1',
        RIGHT: 'd3',
        NPC: '',
    },
    'd3': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'c3',
        DOWN: '',
        LEFT: 'd2',
        RIGHT: 'd4',
        NPC: '',
    },
    'd4': {
        ZONENAME: "Training Field",
        DESCRIPTION: "You're a newbie! Start training!",
        EXAMINATION: 'info',
        UP: 'c4',
        DOWN: '',
        LEFT: 'd3',
        RIGHT: 'Grasslands',
        NPC: '',
    }
}
#  End of maps!


# initiate function
def initiate():  # initiates the game to ask for a name and class
    global player
    print("Welcome to Land of Koru\nI'm Toren, The prince of Koru\nWhat is your name?\n")
    player_name = input("> ")
    print("It's nice to meet you %s, I'm assuming you came to Koru to become one of the lands finest fighters" % (player_name.title()))
    print("After all, Koru is known for having the best fighters of all the lands.")
    print("What kind of fighter would you like to be?\nWarrior\nMage\n")
    player_class = input("> ")
    if player_class.lower() == "warrior":
        player = Player(player_name, 30, 30, 10, 8, 5, 10, 5.0, 0, 10, 1, 100)
        player.player_class = "warrior"
        player.map = training_field_map
        calculate_stats()
    elif player_class.lower() == "mage":
        player = Player(player_name, 25, 40, 5, 7, 12, 8, 5.0, 0, 10, 1, 100)
        player.player_class = "mage"
        player.map = training_field_map
        calculate_stats()
    else:
        print("Unknown class, Please choose again")
        initiate()


def level_up():
    if player.player_class == "warrior":
        player.con *= 1.3
        player.str *= 1.5
        player.int *= 1.1
        player.dex *= 0.6
        player.upExp *= 1.2
        player.exp = 0
        player.upExp *= 1.5 / 0.8
        player.level += 1
        calculate_stats()
        print("You have level'd up!")
        time.sleep(1)
    if player.player_class == "mage":
        player.con *= 1.1
        player.str *= 1.1
        player.int *= 1.5
        player.dex *= 0.5
        player.upExp *= 1.2
        player.exp = 0
        player.upExp *= 1.5 / 0.5
        player.level += 1
        calculate_stats()
        print("You have level'd up!")
        time.sleep(1)


def calculate_stats():
    if player.player_class == "warrior":
        player.hand_min_damage += int((player.str + player.dex) / 2.6)
        player.hand_max_damage += int((player.str + player.dex) / 2.2)
        player.critRate += float(player.dex) / 2.5
        player.maxHp += round(player.con * 1.2)
        player.hp = player.maxHp
    elif player.player_class == "mage":
        player.hand_min_damage += int((player.int + player.dex) / 2.4)
        player.hand_max_damage += int((player.int + player.dex) / 2.0)
        player.critRate += float(player.dex) / 2.5
        player.maxHp += round(player.con * 1.2)
        player.maxMp += round(player.int * 1.2)
        player.mp = player.maxMp
        player.hp = player.maxHp


# Fighting functions
def fight():  # calculate the battle
    while player.hp > 0 and my_enemy.hp > 0:
        p_damage = player_damage()
        e_damage = enemy_damage()
        my_enemy.hp -= p_damage
        if my_enemy.hp <= 0:
            my_enemy.hp = my_enemy.maxHp
            player.exp += my_enemy.exp
            player.gold += my_enemy.gold
            player.available_enemy.remove(my_enemy)
            if CRIT == True: # Did attack Crit
                print("CRITICAL HIT! %s DAMAGE! You have killed the %s and gained %s exp, %s gold!" % (p_damage, my_enemy.name, my_enemy.exp, my_enemy.gold))
                time.sleep(2)
            else:
                print("You did %s Damage and killed the %s, You gained %s exp and %s gold!" % (p_damage,my_enemy.name,my_enemy.exp, my_enemy.gold))
                time.sleep(2)
            if player.exp >= player.upExp:
                level_up()
                break
            if player.current_objective == my_enemy.name: # Checks if monster is part of quest
                player.objective_count += 1
                print(str(player.objective_count)+"/"+str(player.objective_count_goal), player.current_objective, "killed")
                time.sleep(1)
                if player.objective_count_goal == player.objective_count:
                    player.quest_npc.solved = True
                    player.quest_npc = None
                    player.current_objective = ''
                    player.objective_count = 0
                    print("You finished your quest and gained", player.quest_npc.reward, "Gold!")
                    time.sleep(1)
            break
        if CRIT == True:
            print("CRITICAL HIT! %s DAMAGE, %s has %s hp left!" % (p_damage, my_enemy.name, my_enemy.hp))
            pass
        else:
            print("You attacked %s and did %s Damage! %s has %s hp left!" % (my_enemy.name, p_damage, my_enemy.name, my_enemy.hp))
            time.sleep(1)
            player.hp -= e_damage
            print("Enemy attacked you and did %s Damage, You have %s hp left!" % (e_damage, player.hp))
            time.sleep(1)
        if player.hp <= 0:
            player.hp = 0
            print("You have died!")
            time.sleep(1)
            break
        if my_enemy.hp > 0:
            attack_again = input("Attack again?")
            if attack_again in ["yes", "attack", "y", "1"]:
                continue
            else:
                break


def spawn_mob():  # Spawns a random mob with a chance to spawn a couple of mobs.
    random_num = random.randint(0, 101)
    if 30 < random_num < 70:
        if player.map == training_field_map:
            mob_list = [training_dummy, spider, worm, turtle, bunny, rat]
            enemys_generated = []
            random_counter = random.randint(1, 5)
            for mob in mob_list:
                if random_counter == 0:
                    break
                else:
                    random_mob = random.choice(mob_list)
                    player.available_enemy.append(random_mob)
                    enemys_generated.append(random_mob.name)
                    random_counter -= 1
            print("You ran into: " + ', '.join(enemys_generated), "|| Use the 'Fight' command to attack!")
            time.sleep(2)


def player_damage():
    crit_chance = random.randint(0, 101)
    if crit_chance <= int(player.critRate):
        min_damage = player.hand_min_damage * 2
        max_damage = player.hand_max_damage * 2
        damage = random.randrange(min_damage, max_damage)
        global CRIT
        CRIT = True
        return damage
    else:
        CRIT = False
        min_damage = player.hand_min_damage
        max_damage = player.hand_max_damage
        damage = random.randrange(min_damage, max_damage)
        return damage


def enemy_damage():
    min_damage = my_enemy.attack
    max_damage = my_enemy.max_attack
    damage = random.randrange(min_damage, max_damage)
    return damage

# General  Functions
def print_enemy_list():
    i = 1
    for mob in player.available_enemy:
        print(str(i) + ".", mob.name)
        i += 1


def show_bag():
    print("#"*25)
    print(" "*2, "Inventory")
    print("#"*25)
    for item in player.inventory:
        print(" "*2, item)


def movement_handler(destination):
    print("\n" + " "*10 + "You have moved to %s" % (destination))
    player.location = destination
    time.sleep(1)


def show_vendor_items():
    i = 1
    for item in player_current_map[player.location][NPC].items:
        print(str(i) + ".", item.name +", ", "Price:",item.value)
        i += 1


def print_location():  # Prints the location when playing
    print("#"*60)
    print(" "*20, "Location:" + player.location)
    print(" "*20, player_current_map[player.location][ZONENAME])
    print(" "*19,"'Help' if stuck")
    print("#"*60)
    print("Class:%s|Level:%s|Hp:%s/%s|Mp:%s/%s|Exp:%s/%s|Gold:%s|Crit:%s%s" % (player.player_class.title(), player.level, player.hp, player.maxHp, player.mp, player.maxMp, player.exp, int(player.upExp), player.gold, round(player.critRate, 1), "%"))
    print("#" * 60)
    if player_current_map[player.location][NPC] != '':
        print(" "*7 + "Npc:", player_current_map[player.location][NPC].name, player_current_map[player.location][NPC].discrip)
    else:
        pass


def main_menu():  # Prints the main menu only has 3 options
    os.system("clear")
    print("#" * 25)
    print("####### Main Menu #######")
    print("#" * 25)
    global space
    space = "          "
    action = input("%sPlay\n%sHelp\n%sExit\n> " % (space, space, space))
    if action in ["play", "go", "Play", "Go"]:
        global player_current_map
        player_current_map = training_field_map
        os.system("clear")
        start_game()
    elif action in ["help", "Help"]:
        print("Acceptable actions are: go, move, help, examine, fight, attack, inventory, bag, stats, talk")
        time.sleep(2)
        key = input("> ")
        main_menu()
    elif action in ["exit", "Exit", "quit", "Quit"]:
        quit()


def start_game():  # Starts the game
    while running:
        os.system('clear')
        player_current_map = training_field_map
        print_location()
        acceptable_actions = ["go", "move", "help", "examine", "fight", "attack", "inventory", "bag", "stats", "talk", "revive"]
        action = input("?> ".lower())
        if action in ["go", "move"]:  #movement
            os.system("clear")
            print_location()
            print(" "*23, "north\n", " "*18, "east", " "*3, "west\n", " "*22, "south")
            move = input("?> ".lower())
            if move in ["north", "up"] and player_current_map[player.location][UP] != '':
                destination = player_current_map[player.location][UP]
                movement_handler(destination)
                if player.available_enemy:
                    player.available_enemy = []
                else:
                    pass
                spawn_mob()
            elif move in ["east", "left"] and player_current_map[player.location][LEFT] != '':
                destination = player_current_map[player.location][LEFT]
                movement_handler(destination)
                if player.available_enemy:
                    player.available_enemy = []
                else:
                    pass
                spawn_mob()
            elif move in ["south", "down"] and player_current_map[player.location][DOWN] != '':
                destination = player_current_map[player.location][DOWN]
                movement_handler(destination)
                if player.available_enemy:
                    player.available_enemy = []
                else:
                    pass
                spawn_mob()
            elif move in ["west", 'right'] and player_current_map[player.location][RIGHT] != '':
                destination = player_current_map[player.location][RIGHT]
                movement_handler(destination)
                if player.available_enemy:
                    player.available_enemy = []
                else:
                    pass
                spawn_mob()
            else:
                print("unknown location or out of map")
                continue
        elif action in ['help', 'actions']:
            print("Acceptable actions are:", acceptable_actions)
            conti = input("press any key to continue")
        elif action in ["inventory", "bag"]:
            show_bag()
            item = input("?> ")
        elif action in ["attack", "fight"]:
            global my_enemy
            print("Enemy's here")
            print_enemy_list()
            action = input("Attack who?\n> ")
            if action == '1' and len(player.available_enemy) >= 1:  # Choose enemy
                my_enemy = player.available_enemy[0]
                fight()
            elif action == '2' and len(player.available_enemy) >= 2:
                my_enemy = player.available_enemy[1]
                fight()
            elif action == '3' and len(player.available_enemy) >= 3:
                my_enemy = player.available_enemy[2]
                fight()
            elif action == '4' and len(player.available_enemy) >= 4:
                my_enemy = player.available_enemy[3]
                fight()
            elif action == '5' and len(player.available_enemy) >= 5:
                my_enemy = player.available_enemy[4]
                fight()
            elif action == '6' and len(player.available_enemy) >= 6:
                my_enemy = player.available_enemy[5]
                fight()
            else:
                print("Wrong choice")
                time.sleep(1)
                continue
        elif action in ["talk", "shop", "vendor","npc"]:
            if player_current_map[player.location][NPC].type == 'store':
                print(player_current_map[player.location][NPC].short_story)
                show_vendor_items()
                npc = player_current_map[player.location][NPC]
                player_purchase = input("> ")
                if player_purchase == '1' and player.gold >= npc.items[0].value:
                    player.main_hand = npc.items[0].name
                    player.hand_min_damage = npc.items[0].minatt
                    player.hand_max_damage = npc.items[0].maxatt
                    player.gold -= npc.items[0].value
                    print("You bought & equipped: %s" % npc.items[0].name)
                    time.sleep(2)
                elif player_purchase == '2' and player.gold >= npc.items[1].value:
                    player.main_hand = npc.items[1].name
                    player.hand_min_damage = npc.items[1].minatt
                    player.hand_max_damage = npc.items[1].maxatt
                    player.gold -= npc.items[1].value
                    print("You bought & equipped: %s" % npc.items[1].name)
                    time.sleep(2)
                elif player_purchase == '3' and player.gold >= npc.items[2].value:
                    player.main_hand = npc.items[2].name
                    player.hand_min_damage = npc.items[2].minatt
                    player.hand_max_damage = npc.items[2].maxatt
                    player.gold -= npc.items[2].value
                    print("You bought & equipped: %s" % npc.items[2].name)
                    time.sleep(2)
                elif player_purchase == '4' and player.gold >= npc.items[3].value:
                    player.main_hand = npc.items[3].name
                    player.hand_min_damage = npc.items[3].minatt
                    player.hand_max_damage = npc.items[3].maxatt
                    player.gold -= npc.items[3].value
                    print("You bought & equipped: %s" % npc.items[3].name)
                    time.sleep(2)
                elif player_purchase == '5' and player.gold >= npc.items[4].value:
                    player.main_hand = npc.items[4].name
                    player.hand_min_damage = npc.items[4].minatt
                    player.hand_max_damage = npc.items[4].maxatt
                    player.gold -= npc.items[4].value
                    print("You bought & equipped: %s" % npc.items[4].name)
                    time.sleep(2)
                else:
                    print("Unknown item or not enough gold!")
                    time.sleep(1)
            elif player_current_map[player.location][NPC].type == "quest":
                q_npc = player_current_map[player.location][NPC]
                if q_npc.solved == False:
                    print(q_npc.objective)
                    choice = input("Will you accept the quest?")
                    if choice in ["yes", "ye", "ok", "accept", "Yes", "Ye", "Ok", "Accept"]:
                        print("Thank you! Good luck")
                        player.quest_npc = q_npc
                        player.current_objective = q_npc.monster
                        player.objective_count_goal = q_npc.count
                        time.sleep(2)
                    else:
                        print("Too bad! Please come back if you change your mind!")
                        time.sleep(2)
                        continue
                else:
                    print("Already solved!")
                    time.sleep(1)
        elif action in ["Heal", "heal", "revive", "Revive"]:
            print("It costs 100 gold to recover full health, Do you want to recover?")
            choice = input(">? ")
            if choice in ["yes", "ye", "y", "1"] and player.gold >= 100:
                player.hp = player.maxHp
                player.gold -= 100
                print("You have been restored to full health!")
                time.sleep(1)
            else:
                continue


# Main loop
initiate()
main_menu()



