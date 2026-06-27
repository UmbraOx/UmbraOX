# Quest and Spawn Systems for MyGame

import random

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    # Spawn bandits
    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemy_type = random.choice([e for e in ENEMY_DEFS if e['type'] == 'bandit'])
            enemies.append({'name': f"Bandit_{random.randint(1, 100)}", 'type': enemy_type['type'], 'position': camp})

    # Spawn goblins and orcs
    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemy_type = random.choice([e for e in ENEMY_DEFS if e['type'] == 'goblin'])
            enemies.append({'name': f"Goblin_{random.randint(1, 100)}", 'type': enemy_type['type'], 'position': camp})
        orc_type = random.choice([e for e in ENEMY_DEFS if e['type'] == 'orc'])
        enemies.append({'name': f"Orc_{random.randint(1, 100)}", 'type': orc_type['type'], 'position': camp})

    # Spawn wild enemies
    wild_positions = [pos for pos in WORLD_MAP if pos not in TOWNS and pos not in CITIES]
    for _ in range(30):
        enemy_type = random.choice([e for e in ENEMY_DEFS if e['type'] in ['wolf', 'bear', 'skeleton']])
        enemies.append({'name': f"Wild_{random.randint(1, 100)}", 'type': enemy_type['type'], 'position': random.choice(wild_positions)})

    # Spawn NPCs
    for town in TOWNS:
        npc_roles = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for role in npc_roles:
            name = random.choice(NPC_NAMES)
            job = NPC_JOBS[role]
            npcs.append({'name': name, 'job': role, 'position': town})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player['quests']:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['goal']:
                quest['completed'] = True

def check_item_quests(player, item_name, qty):
    for quest in player['quests']:
        if quest['type'] == 'collect' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['goal']:
                quest['completed'] = True

def complete_ready_quests(player):
    completed_quests = []
    for quest in player['quests']:
        if quest['completed']:
            player['rewards'].append(quest['reward'])
            completed_quests.append(quest['name'])
            player['quests'].remove(quest)
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    biome = WORLD_MAP[player['position']]['biome']
    if biome == 'forest':
        return 'chop'
    elif biome == 'mountain':
        return 'mine'
    elif biome == 'plain':
        return 'gather'
    else:
        return ''