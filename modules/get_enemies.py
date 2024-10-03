
import random


class Goblin:
    def __init__(self, level):
        self.name = 'Goblin'
        self.hp = 6 * (int(( level / 2 )) + 1)
        self.ammo = 0
        self.moves = ['punch', 'kick']
        self.status = []
        self.level = level

class Archer:
    def __init__(self, level):
        self.name = 'Archer'
        self.ammo = 4
        self.hp = 3 *( int((level / 2)) + 1)
        self.moves = ['shoot', 'reload', 'dodge', 'kick']
        self.status = []
        self.level = level

class Wizard:
    def __init__(self, level):
        self.name = "Wizard"
        self.ammo = 4
        self.hp = 4 * (int((level / 2)) + 1)
        self.moves = ['fireball', 'hex', 'freeze', 'kick']
        self.status = []
        self.level = level

class Snake:
    def __init__(self, level):
        self.name = "Snake"
        self.ammo = 4
        self.hp = 4 * (int((level / 2)) + 1)
        self.moves = ['poison', 'molt']
        self.status = []
        self.level = level


def get_enemies (player_lvl):
    enemies_array = []
    enemies_number = random.randint(1, player_lvl)
    x = 0
    while x < enemies_number:
        #limit to goblins
        typenum = random.randint(1, 4)
        if typenum == 1:
            enemies_array.append(Goblin(player_lvl).__dict__)
        elif typenum == 2:
            enemies_array.append(Archer(player_lvl).__dict__)
        elif typenum == 3:
            enemies_array.append(Wizard(player_lvl).__dict__)
        elif typenum == 4:
            enemies_array.append(Snake(player_lvl).__dict__)
        x += 1
    return enemies_array