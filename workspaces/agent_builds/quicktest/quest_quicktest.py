import random

WORLD_MAP = {}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
ENEMY_DEFS = {}
NPC_NAMES = []
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']
ENEMY_TYPES = ['Bandit', 'Goblin', 'Orc']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Bandit', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10))})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10))})
        enemies.append({'name': 'Orc', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10))})

    for town in TOWNS:
        buildings.append({'type': 'Town', 'position': town})
        for job in ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']:
            npcs.append({'name': random.choice(NPC_NAMES), 'job': job, 'position': (town[0] + random.randint(-5, 5), town[1] + random.randint(-5, 5))})

    for _ in range(30):
        while True:
            x = random.randint(0, WORLD_MAP['width'])
            y = random.randint(0, WORLD_MAP['height'])
            if (x, y) not in TOWNS and (x, y) not in CITIES and WORLD_MAP.get((x, y), 'land') != 'water':
                enemies.append({'name': random.choice(ENEMY_TYPES), 'position': (x, y)})
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
    biome = WORLD_MAP.get((x, y), 'land')
    if biome == 'forest':
        return 'chop'
    elif biome == 'mountain':
        return 'mine'
    elif biome in ['field', 'garden']:
        return 'gather'
    else:
        return ''