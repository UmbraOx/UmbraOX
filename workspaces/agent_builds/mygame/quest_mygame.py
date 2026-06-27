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
            enemies.append({'name': enemy_type['name'], 'position': (camp[0] + random.randint(-5, 5), camp[1] + random.randint(-5, 5))})

    # Spawn goblins and orcs
    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemy_type = random.choice([e for e in ENEMY_DEFS if e['type'] == 'goblin'])
            enemies.append({'name': enemy_type['name'], 'position': (camp[0] + random.randint(-5, 5), camp[1] + random.randint(-5, 5))})
        orc_type = random.choice([e for e in ENEMY_DEFS if e['type'] == 'orc'])
        enemies.append({'name': orc_type['name'], 'position': (camp[0] + random.randint(-5, 5), camp[1] + random.randint(-5, 5))})

    # Spawn wild enemies
    for _ in range(30):
        x = random.randint(0, WORLD_MAP['width'] - 1)
        y = random.randint(0, WORLD_MAP['height'] - 1)
        if (x, y) not in TOWNS and (x, y) not in CITIES and WORLD_MAP['tiles'][y][x] != 'WATER':
            enemy_type = random.choice([e for e in ENEMY_DEFS if e['type'] == 'wild'])
            enemies.append({'name': enemy_type['name'], 'position': (x, y)})

    # Spawn NPCs
    for town in TOWNS:
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            name = random.choice(NPC_NAMES)
            npcs.append({'name': name, 'job': job, 'position': (town[0] + random.randint(-2, 2), town[1] + random.randint(-2, 2))})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player['quests']:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def check_item_quests(player, item_name, qty):
    for quest in player['quests']:
        if quest['type'] == 'collect' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
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
    x, y = player['position']
    biome = WORLD_MAP['tiles'][y][x]
    if biome == 'FOREST':
        return 'chop'
    elif biome == 'MOUNTAIN':
        return 'mine'
    elif biome in ['GRASSLAND', 'PLAINS']:
        return 'gather'
    else:
        return ''