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
            enemies.append({'type': 'bandit', 'location': camp, **ENEMY_DEFS['bandit']})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'goblin', 'location': camp, **ENEMY_DEFS['goblin']})
        enemies.append({'type': 'orc', 'location': camp, **ENEMY_DEFS['orc']})

    wild_locations = [loc for loc, biome in WORLD_MAP.items() if biome not in ['town', 'city', 'water']]
    random.shuffle(wild_locations)
    for _ in range(30):
        enemies.append({'type': random.choice(['bandit', 'goblin']), 'location': wild_locations.pop(), **ENEMY_DEFS[random.choice(['bandit', 'goblin'])]})

    for town in TOWNS:
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            name = random.choice(NPC_NAMES)
            npcs.append({'name': name, 'job': job, 'location': town})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    if 'kill_quests' not in player:
        player['kill_quests'] = {}
    for quest, details in player['kill_quests'].items():
        if details['enemy'] == enemy_name and details['progress'] < details['target']:
            details['progress'] += 1
            break

def check_item_quests(player, item_name, qty):
    if 'item_quests' not in player:
        player['item_quests'] = {}
    for quest, details in player['item_quests'].items():
        if details['item'] == item_name and details['progress'] < details['target']:
            details['progress'] += qty
            break

def complete_ready_quests(player):
    completed_quests = []
    if 'kill_quests' in player:
        for quest, details in list(player['kill_quests'].items()):
            if details['progress'] >= details['target']:
                completed_quests.append(quest)
                del player['kill_quests'][quest]
                # Add rewards here
    if 'item_quests' in player:
        for quest, details in list(player['item_quests'].items()):
            if details['progress'] >= details['target']:
                completed_quests.append(quest)
                del player['item_quests'][quest]
                # Add rewards here
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    location = player.get('location')
    biome = WORLD_MAP.get(location)
    if biome == 'forest':
        return 'chop'
    elif biome == 'mountain':
        return 'mine'
    elif biome in ['field', 'village']:
        return 'gather'
    else:
        return ''