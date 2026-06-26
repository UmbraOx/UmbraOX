import random

WORLD_MAP = {}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
ENEMY_DEFS = {}
NPC_NAMES = []
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']
PLAYER_QUESTS = []

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Bandit', 'position': camp['position'], 'health': 10})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'position': camp['position'], 'health': 5})
        enemies.append({'name': 'Orc', 'position': camp['position'], 'health': 20})

    wild_positions = [(x, y) for x in range(WORLD_MAP['width']) for y in range(WORLD_MAP['height'])
                      if (x, y) not in TOWNS and (x, y) not in CITIES and WORLD_MAP['tiles'][y][x] != 'W']
    random.shuffle(wild_positions)
    for _ in range(30):
        pos = wild_positions.pop()
        enemies.append({'name': random.choice(list(ENEMY_DEFS.keys())), 'position': pos, 'health': ENEMY_DEFS[random.choice(list(ENEMY_DEFS.keys()))]['health']})

    for town in TOWNS:
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            npcs.append({'name': random.choice(NPC_NAMES), 'job': job, 'position': town['position']})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def check_item_quests(player, item_name, qty):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'collect' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def complete_ready_quests(player):
    completed_quests = []
    for quest in PLAYER_QUESTS[:]:
        if quest['completed']:
            player['gold'] += quest.get('reward', 0)
            completed_quests.append(quest['name'])
            PLAYER_QUESTS.remove(quest)
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    x, y = player['position']
    biome = WORLD_MAP['tiles'][y][x]
    if biome == 'F':
        return 'chop'
    elif biome == 'M':
        return 'mine'
    elif biome in ['G', 'S']:
        return 'gather'
    else:
        return ''