import random

WORLD_MAP = {}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
ENEMY_DEFS = {'Bandit': {}, 'Goblin': {}, 'Orc': {}}
NPC_NAMES = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Bandit', 'type': 'Enemy', 'location': camp})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'type': 'Enemy', 'location': camp})
        enemies.append({'name': 'Orc', 'type': 'Enemy', 'location': camp})

    wild_locations = [loc for loc, biome in WORLD_MAP.items() if biome not in ['Town', 'City', 'Water']]
    random.shuffle(wild_locations)
    for _ in range(30):
        enemies.append({'name': random.choice(list(ENEMY_DEFS.keys())), 'type': 'Enemy', 'location': wild_locations.pop()})

    for town in TOWNS:
        npc_roles = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in npc_roles:
            name = random.choice(NPC_NAMES)
            npcs.append({'name': name, 'job': job, 'location': town})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    if 'kill_quests' not in player:
        player['kill_quests'] = {}
    for quest, details in player['kill_quests'].items():
        if details['enemy'] == enemy_name and details['progress'] < details['target']:
            details['progress'] += 1
            if details['progress'] >= details['target']:
                print(f"Quest {quest} completed!")

def check_item_quests(player, item_name, qty):
    if 'item_quests' not in player:
        player['item_quests'] = {}
    for quest, details in player['item_quests'].items():
        if details['item'] == item_name and details['progress'] < details['target']:
            details['progress'] += qty
            if details['progress'] >= details['target']:
                print(f"Quest {quest} completed!")

def complete_ready_quests(player):
    completed_quests = []
    for quest, details in list(player.get('kill_quests', {}).items()):
        if details['progress'] >= details['target']:
            player['rewards'].extend(details['rewards'])
            del player['kill_quests'][quest]
            completed_quests.append(quest)

    for quest, details in list(player.get('item_quests', {}).items()):
        if details['progress'] >= details['target']:
            player['rewards'].extend(details['rewards'])
            del player['item_quests'][quest]
            completed_quests.append(quest)
    
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    location = player.get('location')
    biome = WORLD_MAP.get(location)

    if biome == 'Forest':
        return 'chop'
    elif biome == 'Mountain':
        return 'mine'
    elif biome in ['Field', 'Grassland']:
        return 'gather'
    else:
        return ''