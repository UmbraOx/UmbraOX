# Quest and Spawn Systems for MyGame

import random

WORLD_MAP = {}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
ENEMY_DEFS = {}
NPC_NAMES = []
NPC_JOBS = {}

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            bandit = {'name': 'Bandit', 'type': 'enemy', 'position': (camp[0] + random.randint(-5, 5), camp[1] + random.randint(-5, 5))}
            enemies.append(bandit)

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            goblin = {'name': 'Goblin', 'type': 'enemy', 'position': (camp[0] + random.randint(-5, 5), camp[1] + random.randint(-5, 5))}
            enemies.append(goblin)
        orc = {'name': 'Orc', 'type': 'enemy', 'position': (camp[0] + random.randint(-5, 5), camp[1] + random.randint(-5, 5))}
        enemies.append(orc)

    for town in TOWNS:
        npc_jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in npc_jobs:
            name = random.choice(NPC_NAMES)
            npc = {'name': name, 'job': job, 'type': 'npc', 'position': (town[0] + random.randint(-5, 5), town[1] + random.randint(-5, 5))}
            npcs.append(npc)

    for _ in range(30):
        while True:
            x = random.randint(min(WORLD_MAP.keys()), max(WORLD_MAP.keys()))
            y = random.randint(min(WORLD_MAP[x].keys()), max(WORLD_MAP[x].keys()))
            if WORLD_MAP[x][y] not in ['town', 'city', 'water']:
                enemy_name = random.choice(list(ENEMY_DEFS.keys()))
                wild_enemy = {'name': enemy_name, 'type': 'enemy', 'position': (x, y)}
                enemies.append(wild_enemy)
                break

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player['quests']:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                complete_ready_quests(player)

def check_item_quests(player, item_name, qty):
    for quest in player['quests']:
        if quest['type'] == 'collect' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
                complete_ready_quests(player)

def complete_ready_quests(player):
    completed_quests = []
    for quest in player['quests']:
        if quest['progress'] >= quest['required']:
            player['rewards'].append(quest['reward'])
            completed_quests.append(quest['name'])
            player['quests'].remove(quest)
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    x, y = player['position']
    biome = WORLD_MAP[x][y]
    if biome == 'forest':
        return 'chop'
    elif biome == 'mountain':
        return 'mine'
    elif biome in ['field', 'grassland']:
        return 'gather'
    else:
        return ''