import random

WORLD_MAP = {}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
ENEMY_DEFS = {'bandit': {}, 'goblin': {}, 'orc': {}}
NPC_NAMES = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'bandit', 'name': f'Bandit_{random.choice(NPC_NAMES)}', 'location': camp})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'goblin', 'name': f'Goblin_{random.choice(NPC_NAMES)}', 'location': camp})
        enemies.append({'type': 'orc', 'name': f'Orc_{random.choice(NPC_NAMES)}', 'location': camp})

    for town in TOWNS:
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            npcs.append({'name': random.choice(NPC_NAMES), 'job': job, 'location': town})

    wild_locations = [loc for loc, biome in WORLD_MAP.items() if biome not in ['town', 'city', 'water']]
    for _ in range(30):
        location = random.choice(wild_locations)
        enemy_type = random.choices(['bandit', 'goblin'], weights=[2, 1], k=1)[0]
        enemies.append({'type': enemy_type, 'name': f'{enemy_type.capitalize()}_{random.choice(NPC_NAMES)}', 'location': location})

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
    player['quests'] = [q for q in player['quests'] if not q['completed']]
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    location = player['location']
    biome = WORLD_MAP.get(location)
    if biome == 'forest':
        return 'chop'
    elif biome == 'mountain':
        return 'mine'
    elif biome in ['field', 'village']:
        return 'gather'
    else:
        return ''