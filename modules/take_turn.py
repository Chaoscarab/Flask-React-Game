from modules.enemy_ai import *
def check_attack_status(attack, status_array):
    print(attack)
    attack_mod = int(attack)
    if len(status_array) > 0:
        if 'hex' in status_array:
            attack_mod /= 2
        
        if "burning" in status_array:
            attack_mod *= 1.25
        
        if 'frozen' in status_array:
            attack_mod -= 2
            if attack_mod > 0:
                attack_mod = 0
    attack_mod = int(attack_mod)
    return {'attack': attack_mod, "status_array": status_array}


def check_damage_status(attack, status_array):
    damage_mod = attack
    if len(status_array) > 0:
        if 'frozen' in status_array:
            damage_mod *= 1.5
        
        if 'hex' in status_array:
            damage_mod += 2
        
        if 'dodge' in status_array:
            damage_mod = 0
            status_array.remove('dodge')

        if 'molt' in status_array:
            damage_mod = 3
            status_array.remove('molt')
            print(f"damage mod {int(damage_mod)}")
    damage_mod = int(damage_mod)
    print({'damage':damage_mod, "status_array": status_array})
    return {'damage':damage_mod, "status_array": status_array}



#playerMoves
def shoot_n_scoot(player, enemies_array):
    player_status_array = player['status']
    attack = 10 * (player['level'] / len(enemies_array))
    check_attack_status_obj = check_attack_status(attack, player_status_array)
    mod_attack = check_attack_status_obj['attack']
    player_status_array = check_attack_status_obj['status_array']
    for enemy in enemies_array:
        check_damage_status_obj = check_damage_status(mod_attack, enemy['status'])
        enemy_hp = int(enemy['hp'])
        enemy_hp -= check_damage_status_obj['damage']
        print(f"enemy_hp {enemy_hp}")
        enemy['hp'] = enemy_hp
        enemy['status'] = check_damage_status_obj['status_array']
        log = f"{player['name']} used Shoot \n scoot on {enemy['name']} for {check_damage_status_obj['damage']} consuming 3 ammo"
        #log = f'damaged {enemy['name']} for {check_damage_status_obj['damage']}'
        player['logs'].append(log)
    print(f"new_list: {enemies_array}")
    return {'player': player, 'enemies_array': enemies_array}
    
    
def punch(player, enemies_array, target_index):
    attack = 10 * player['level']/2
    player_status_array = player['status']
    check_attack_status_obj = check_attack_status(attack, player_status_array)
    mod_attack = check_attack_status_obj['attack']
    player_status_array = check_attack_status_obj['status_array']
    enemy = enemies_array[target_index]
    check_damage_status_obj = check_damage_status(mod_attack, enemy['status'])
    enemy_hp = int(enemy['hp'])
    enemy_hp -= check_damage_status_obj['damage']
    enemy['hp'] = enemy_hp
    enemy['status'] = check_damage_status_obj['status_array']
    enemies_array[target_index] = enemy
    print(enemy_hp)
    log = f"{player['name']} used puch on {enemy['name']} for {check_damage_status_obj['damage']}"
    player['logs'].append(log)
    return {'player': player, 'enemies_array': enemies_array}


#remove enemies with < 0 hp existing enemies
def remaining_enemies(player, enemies_list):
    
    new_list = []
    xp_gained = 0
    for enemy in enemies_list:
        if enemy['hp'] <= 0:
            print(f"{enemy['name']} died giving {enemy['level']} xp.")
            xp_gained += enemy['level']
        else:
            new_list.append(enemy)
    player['xp'] += xp_gained
    return {'player': player, 'enemies_array': new_list}


def enemy_turn(player, enemies_array):
    move = ''
    for enemy in enemies_array:
        if enemy['name'] == 'Goblin':
            move = goblin_ai(enemy, player, len(enemies_array))
        elif enemy["name"] == 'Archer':
            move = archer_ai(enemy, player, len(enemies_array))
        elif enemy["name"] == 'Wizard':
            move = wizard_ai(enemy, player, len(enemies_array))
        elif enemy["name"] == 'snake':
            move = snake_ai(enemy, player, len(enemies_array))

        print(f"{enemy['name']}, {move}")
        
        if move == 'punch':
            attack = 3 * enemy['level']
            check_attack_status_obj = check_attack_status(attack, enemy['status'])
            mod_attack = check_attack_status_obj['attack']
            enemy['status'] = check_attack_status_obj['status_array']
            check_damage_status_obj = check_damage_status(mod_attack, player['status'])
            player['hp'] -= check_damage_status_obj['damage']
            player['status'] = check_damage_status_obj['status_array']
            player['logs'].append(f"{enemy['name']} used punch and did {check_damage_status_obj['damage']} damage")

        if move == 'kick':
            attack = 5 * enemy['level']
            check_attack_status_obj = check_attack_status(attack, enemy['status'])
            mod_attack = check_attack_status_obj['attack']
            enemy['status'] = check_attack_status_obj['status_array']
            check_damage_status_obj = check_damage_status(mod_attack, player['status'])
            player['hp'] -= check_damage_status_obj['damage']
            player['status'] = check_damage_status_obj['status_array']
            player['logs'].append(f"{enemy['name']} used kick and did {check_damage_status_obj['damage']} damage")
        
        if move == 'reload':
            enemy['ammo'] = 4
            player['logs'].append(f"{enemy['name']} reloaded.")
        
        if move == 'shoot':
            if enemy['ammo'] < 2:
                player['logs'].append(f"{enemy['name']} shot a black.")
            else:
                attack = 10 * enemy['level']
                check_attack_status_obj = check_attack_status(attack, enemy['status'])
                mod_attack = check_attack_status_obj['attack']
                enemy['status'] = check_attack_status_obj['status_array']
                check_damage_status_obj = check_damage_status(mod_attack, player['status'])
                player['hp'] -= check_damage_status_obj['damage']
                player['status'] = check_damage_status_obj['status_array']
                enemy['ammo'] -= 2
                player['logs'].append(f"{enemy['name']} used shoot and did {check_damage_status_obj['damage']} damage")
        if move == 'dodge':
            if 'dodge' in enemy['status']:
                player['logs'].append(f"{enemy['name']} tried to dodge while already dodgeing")
            else:
                enemy['status'].append('dodge')
                player['logs'].append(f"{enemy['name']} is dodging.")
        if move == 'fireball':
            if not 'buring' in player['status']:
                        player['status'].append('burning')
                        player['logs'].append(f"{enemy['name']} used fireball and {player['name']} is now burning")
            else:
                player['logs'].append(f"{enemy['name']} used burn but {player['name']} is already buring")
        if move == 'hex':
            if not 'hex' in player['status']:
                        player['status'].append('hex')
                        player['logs'].append(f"{enemy['name']} used hex and {player['name']} is now hexed")
            else:
                player['logs'].append(f"{enemy['name']} used hex but {player['name']} is already hexed")
        
        if move == 'freeze':
            if not 'frozen' in player['status']:
                        player['status'].append('frozen')
                        player['logs'].append(f"{enemy['name']} used freeze and {player['name']} is now frozen")
            else:
                player['logs'].append(f"{enemy['name']} used burn but {player['name']} is already frozen")
        
        if move == 'poison':
            if not 'poison' in player['status']:
                        player['status'].append('poison')
                        player['logs'].append(f"{enemy['name']} used poison and {player['name']} is now poisoned")
            else:
                player['logs'].append(f"{enemy['name']} used poison but {player['name']} is already poisoned")
        if move == 'molt':
            if 'molt' in enemy['status']:
                player['logs'].append(f"{enemy['name']} tried to molt while already molting")
            else:
                enemy['status'].append('dodge')
                player['logs'].append(f"{enemy['name']} is molting.")

    print(player, enemies_array)
    return {'player': player, 'enemies_array': enemies_array}




def level_up(player):
    if player['xp'] >= player['level'] * 10:
        remaining_xp = player['xp'] % (player['level'] * 10)
        whole_xp = player['xp'] - remaining_xp
        player['level'] += whole_xp / (player['level'] * 10)
        player['xp'] = remaining_xp
        player['hp'] = player['level'] * 20  + (player['hp'] - 20)
        player['logs'].append(f"{player['name']} leveled up. Now level {player['level']}")

        #make status effects persist after level up
        if not 'dodge' in player['status']:
            player['status'] = []
        else:
            player['status'] = ['dodge']
    return player


def status_effects(self, status_list, logs):
    print('status effects')
    remaining_effects = []
    if "poison" in status_list:
        damage = int(self['hp'] * .1)
        self['hp'] -= damage
        logs.append(f"{self['name']} took {damage} damage from poison")
        remaining_effects.append('poison')
    if "burning" in status_list:
        damage = 1 * int(self['level'] /2) + 1
        self['hp'] -= damage
        logs.append(f"{self['name']} took {damage} damage from burning")
    return {"self":self, "effects_list": remaining_effects, "logs": logs}

def enemy_status_effects(enemy_list,logs):
    for enemy in enemy_list:
        out_obj = status_effects(enemy, enemy['status'], logs)
        enemy = out_obj['self']
        enemy['status'] = out_obj['effects_list']
        logs = out_obj['logs']
    return {'enemy_array': enemy_list, "logs": logs}




def take_turn(stateObject):

    #first get player move:
    playerMoves = stateObject["player"]['moves']
    chosenMoveIndex = stateObject['moveIndex']
    #chosenMove
    player_move = playerMoves[chosenMoveIndex]

    player_obj = stateObject["player"]
    target_index = stateObject["targetIndex"]
    enemies_array = stateObject['enemies']['array']
    player_obj['logs'] = ['Turn Start']
    #player moves:

    
    if player_move['name'] == 'shoot \'n scoot':
        if player_obj['ammo'] < 2:
            player_obj['logs'].append('Shoot \'n scoot requires at least 3 ammo')
        else:
            out_object = shoot_n_scoot(player_obj, enemies_array)
            enemies_array = out_object['enemies_array']
            player_obj = out_object['player']
            player_obj['ammo'] -= 2
            print(player_obj['ammo'])
    if player_move['name'] == 'reload':
        player_obj['logs'].append('Reloaded')
        player_obj['ammo'] = 6
    
    if player_move['name'] == 'dodge':
        if 'dodge' in player_obj['status']:
             player_obj['logs'].append('already dodging')
        else:
            player_obj['logs'].append('dodging')
            player_obj['status'].append('dodge')
    
    if player_move['name'] == 'punch':
        out_object = punch(player_obj, enemies_array, target_index)
        enemies_array = out_object['enemies_array']
        player_obj = out_object['player']

   
    #call status effects
    out_object = status_effects(player_obj, player_obj['status'], player_obj['logs'])

    player_obj = out_object['self']
    player_obj['status'] = out_object["effects_list"]
    player_obj['logs'] = out_object['logs']
    #remove enemies with hp < 0
    out_object = remaining_enemies(player_obj, enemies_array)
    enemies_array = out_object['enemies_array']
    player_obj = out_object['player']
    
    #enemy turn
    out_object = enemy_turn(player_obj, enemies_array)
    enemies_array = out_object['enemies_array']
    player_obj = out_object['player']
    
    #status effects
    out_object = enemy_status_effects(enemies_array, player_obj['logs'])
    enemies_array = out_object['enemy_array']
    player_obj['logs'] = out_object['logs']

    #check if any enemies died
    out_object = remaining_enemies(player_obj, enemies_array)
    enemies_array = out_object['enemies_array']
    player_obj = out_object['player']

    #level up player
    player_obj = level_up(player_obj)
    newStateObject = {'player': player_obj, 'enemies': enemies_array}
    return newStateObject