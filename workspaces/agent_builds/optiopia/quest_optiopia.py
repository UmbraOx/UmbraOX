import random

WORLD_TILES = {
    'TOWN': 'town',
    'CITY': 'city',
    'BANDIT_CAMP': 'bandit_camp',
    'GOBLIN_CAMP': 'goblin_camp',
    'FOREST': 'forest',
    'MOUNTAIN': 'mountain',
    'PLAINS': 'plains',
    'WATER': 'water'
}

ENEMY_DEFS = {
    'Bandit': {'health': 20, 'damage': 5},
    'Goblin': {'health': 15, 'damage': 3},
    'Orc': {'health': 40, 'damage': 8}
}

NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        x, y = camp
        for _ in range(4):
            enemies.append({'type': 'Bandit', 'position': (x + random.randint(-1, 1), y + random.randint(-1, 1)), **ENEMY_DEFS['Bandit']})

    for camp in GOBLIN_CAMPS:
        x, y = camp
        for _ in range(4):
            enemies.append({'type': 'Goblin', 'position': (x + random.randint(-1, 1), y + random.randint(-1, 1)), **ENEMY_DEFS['Goblin']})
        enemies.append({'type': 'Orc', 'position': (x + random.randint(-1, 1), y + random.randint(-1, 1)), **ENEMY_DEFS['Orc']})

    for town in TOWNS:
        x, y = town
        buildings.append({'type': 'TownHall', 'position': (x, y)})
        npc_jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in npc_jobs:
            npcs.append({'name': random.choice(NPC_NAMES), 'job': job, 'position': (x + random.randint(-1, 1), y + random.randint(-1, 1))})

    wild_enemy_types = list(ENEMY_DEFS.keys())
    for _ in range(30):
        while True:
            x, y = random.choice(WORLD_MAP)
            if WORLD_MAP[(x, y)] not in ['TOWN', 'CITY', 'WATER']:
                enemies.append({'type': random.choice(wild_enemy_types), 'position': (x, y), **ENEMY_DEFS[random.choice(wild_enemy_types)]})
                break

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
    player['quests'] = [quest for quest in player['quests'] if not quest['completed']]
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    x, y = player['position']
    biome = WORLD_MAP.get((x, y))
    if biome == 'FOREST':
        return 'chop'
    elif biome == 'MOUNTAIN':
        return 'mine'
    elif biome in ['PLAINS', 'FOREST']:
        return 'gather'
    else:
        return ''