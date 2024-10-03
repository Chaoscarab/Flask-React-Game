import random
def goblin_ai(self, player, list_length):
    if list_length < 2:
        return 'punch'
    else:
        return "kick"

def archer_ai(self, player, list_length):
    if list_length < 2:
        return 'kick'
    elif self['ammo'] == 0:
        return 'reload'
    else:
        rand_num = random.randint(1, 2)
        if rand_num == 1:
            return 'dodge'
        else:
            return 'shoot'

def wizard_ai(self, player, list_length):
    if not 'hex' in player['status']:
        return 'hex'
    elif not 'frozen' in player['status']:
        return 'frozen'
    elif not 'burning' in player['status']:
        return 'fireball'
    else:
        return 'kick'

def snake_ai(self, player, list_length):
    if not 'poison' in player['status']:
        return 'poison'
    else:
        return 'molt'