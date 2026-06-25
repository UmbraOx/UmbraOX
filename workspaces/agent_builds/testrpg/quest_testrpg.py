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
            enemies.append({'name': 'Bandit', 'position': camp['position'], **ENEMY_DEFS['Bandit']})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'position': camp['position'], **ENEMY_DEFS['Goblin']})
        enemies.append({'name': 'Orc', 'position': camp['position'], **ENEMY_DEFS['Orc']})

    wild_positions = [pos for pos, tile in WORLD_MAP.items() if tile not in ['Town', 'City', 'Water']]
    random.shuffle(wild_positions)
    for _ in range(30):
        position = wild_positions.pop()
        enemy_type = random.choice(['Goblin', 'Bandit'])
        enemies.append({'name': enemy_type, 'position': position, **ENEMY_DEFS[enemy_type]})

    for town in TOWNS:
        buildings.append({'type': 'Town', 'position': town['position']})
        npc_positions = [pos for pos, tile in WORLD_MAP.items() if tile == 'Town' and pos != town['position']]
        random.shuffle(npc_positions)
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            position = npc_positions.pop()
            name = random.choice(NPC_NAMES)
            npcs.append({'name': name, 'job': job, 'position': position})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'kill' and quest['target'] == enemy_name and not quest['completed']:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def check_item_quests(player, item_name, qty):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'item' and quest['target'] == item_name and not quest['completed']:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def complete_ready_quests(player):
    completed_quests = []
    for quest in PLAYER_QUESTS:
        if quest['completed']:
            player['gold'] += quest.get('reward', 0)
            completed_quests.append(quest['name'])
    PLAYER_QUESTS[:] = [quest for quest in PLAYER_QUESTS if not quest['completed']]
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    position = player['position']
    tile_type = WORLD_MAP.get(position)
    if tile_type == 'Forest':
        return 'Chopped wood'
    elif tile_type == 'Mountain':
        return 'Mined ore'
    elif tile_type == 'Field':
        return 'Gathered crops'
    else:
        return 'Nothing to harvest'