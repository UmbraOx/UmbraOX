# Quest and Spawn Systems for MyGame

import random

WORLD_MAP = None
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
            enemies.append({'name': 'Bandit', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10))})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10))})
        enemies.append({'name': 'Orc', 'position': (camp[0] + random.randint(-10, 10), camp[1] + random.randint(-10, 10))})

    for town in TOWNS:
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            npcs.append({'name': random.choice(NPC_NAMES), 'job': job, 'position': (town[0] + random.randint(-5, 5), town[1] + random.randint(-5, 5))})

    wild_enemy_names = list(ENEMY_DEFS.keys())
    for _ in range(30):
        x, y = random.randint(0, WORLD_MAP['width']), random.randint(0, WORLD_MAP['height'])
        if (x, y) not in TOWNS and (x, y) not in CITIES and WORLD_MAP['tiles'][y][x] != 'W':
            enemies.append({'name': random.choice(wild_enemy_names), 'position': (x, y)})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                complete_ready_quests(player)

def check_item_quests(player, item_name, qty):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'item' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
                complete_ready_quests(player)

def complete_ready_quests(player):
    completed_quests = []
    for quest in PLAYER_QUESTS[:]:
        if quest['progress'] >= quest['required']:
            player['rewards'].append(quest['reward'])
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