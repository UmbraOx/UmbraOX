# Quest and Spawn Systems for MyGame

import random

ENEMY_DEFS = {
    'Bandit': {'health': 20, 'damage': 5},
    'Goblin': {'health': 15, 'damage': 3},
    'Orc': {'health': 30, 'damage': 7}
}

NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Bandit', 'type': 'Enemy', 'position': camp, **ENEMY_DEFS['Bandit']})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'type': 'Enemy', 'position': camp, **ENEMY_DEFS['Goblin']})
        enemies.append({'name': 'Orc', 'type': 'Enemy', 'position': camp, **ENEMY_DEFS['Orc']})

    for town in TOWNS + CITIES:
        buildings.extend(town.get('buildings', []))
        for job in NPC_JOBS[:7]:
            name = random.choice(NPC_NAMES)
            npcs.append({'name': name, 'job': job, 'position': town['center'], 'type': 'NPC'})

    wild_positions = [(x, y) for x in range(WORLD_MAP['width']) for y in range(WORLD_MAP['height'])
                      if (x, y) not in TOWNS and (x, y) not in CITIES and WORLD_MAP['terrain'][y][x] != 'Water']
    random.shuffle(wild_positions)
    for pos in wild_positions[:30]:
        enemy_type = random.choice(['Bandit', 'Goblin'])
        enemies.append({'name': enemy_type, 'type': 'Enemy', 'position': pos, **ENEMY_DEFS[enemy_type]})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player['quests']:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                complete_ready_quests(player)

def check_item_quests(player, item_name, qty):
    for quest in player['quests']:
        if quest['type'] == 'item' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
                complete_ready_quests(player)

def complete_ready_quests(player):
    completed = []
    for quest in player['quests']:
        if quest['progress'] >= quest['required']:
            player['rewards'].extend(quest.get('rewards', []))
            completed.append(quest['name'])
    player['quests'] = [q for q in player['quests'] if q['name'] not in completed]
    return completed

def harvest_nearby(player, WORLD_MAP):
    x, y = player['position']
    biome = WORLD_MAP['terrain'][y][x]
    if biome == 'Forest':
        return 'Chopped wood'
    elif biome == 'Mountain':
        return 'Mined ore'
    elif biome == 'Field':
        return 'Gathered crop'
    else:
        return ''