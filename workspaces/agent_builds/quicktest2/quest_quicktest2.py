import random

ENEMY_DEFS = {
    'Bandit': {'health': 20, 'damage': 5},
    'Goblin': {'health': 15, 'damage': 3},
    'Orc': {'health': 30, 'damage': 8}
}

NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'Bandit', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10)), **ENEMY_DEFS['Bandit']})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'Goblin', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10)), **ENEMY_DEFS['Goblin']})
        enemies.append({'type': 'Orc', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10)), **ENEMY_DEFS['Orc']})

    for town in TOWNS:
        buildings.append({'type': 'Town', 'position': town})
        npc_jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in npc_jobs:
            npcs.append({'name': random.choice(NPC_NAMES), 'job': job, 'position': (town[0] + random.randint(-5, 5), town[1] + random.randint(-5, 5))})

    for city in CITIES:
        buildings.append({'type': 'City', 'position': city})

    wild_positions = [(x, y) for x in range(WORLD_MAP['width']) for y in range(WORLD_MAP['height']) if (x, y) not in TOWNS and (x, y) not in CITIES and WORLD_MAP['terrain'][y][x] != 'Water']
    random.shuffle(wild_positions)
    for _ in range(30):
        pos = wild_positions.pop()
        enemy_type = random.choice(['Bandit', 'Goblin'])
        enemies.append({'type': enemy_type, 'position': pos, **ENEMY_DEFS[enemy_type]})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player['quests']:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def check_item_quests(player, item_name, qty):
    for quest in player['quests']:
        if quest['type'] == 'item' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def complete_ready_quests(player):
    completed_quests = []
    for quest in player['quests']:
        if quest['completed']:
            player['rewards'].append(quest['reward'])
            completed_quests.append(quest['name'])
    player['quests'] = [quest for quest in player['quests'] if not quest['completed']]
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    x, y = player['position']
    biome = WORLD_MAP['biome'][y][x]
    if biome == 'Forest':
        return 'Chopped Wood'
    elif biome == 'Mountain':
        return 'Mined Ore'
    elif biome == 'Field':
        return 'Gathered Crop'
    else:
        return ''