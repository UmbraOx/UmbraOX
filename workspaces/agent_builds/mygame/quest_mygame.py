import random

WORLD_BIOMES = ['Forest', 'Mountain', 'Desert', 'Plains']
ENEMY_TYPES = ['Bandit', 'Goblin', 'Orc', 'Wolf', 'Bear']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Bandit', 'location': camp})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'location': camp})
        enemies.append({'name': 'Orc', 'location': camp})

    wild_enemy_locations = [loc for loc, biome in WORLD_MAP.items() if loc not in TOWNS and loc not in CITIES and biome != 'Water']
    for _ in range(30):
        location = random.choice(wild_enemy_locations)
        enemy_type = random.choice(ENEMY_TYPES)
        enemies.append({'name': enemy_type, 'location': location})

    for town in TOWNS:
        npc_list = [
            {'name': NPC_NAMES.pop(), 'job': 'Merchant', 'location': town},
            {'name': NPC_NAMES.pop(), 'job': 'Guard', 'location': town},
            {'name': NPC_NAMES.pop(), 'job': 'Guard', 'location': town},
            {'name': NPC_NAMES.pop(), 'job': 'Farmer', 'location': town},
            {'name': NPC_NAMES.pop(), 'job': 'Farmer', 'location': town},
            {'name': NPC_NAMES.pop(), 'job': 'Miner', 'location': town},
            {'name': NPC_NAMES.pop(), 'job': 'Blacksmith', 'location': town}
        ]
        npcs.extend(npc_list)

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
            player['rewards'].extend(quest['rewards'])
            completed_quests.append(quest['name'])
    player['quests'] = [quest for quest in player['quests'] if not quest['completed']]
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    location = player['location']
    biome = WORLD_MAP.get(location)
    if biome == 'Forest':
        return 'chop'
    elif biome == 'Mountain':
        return 'mine'
    else:
        return 'gather'