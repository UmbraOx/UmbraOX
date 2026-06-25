import random

WORLD_BIOMES = ['Forest', 'Mountain', 'Desert', 'Plains']
ENEMY_TYPES = ['Goblin', 'Orc', 'Bandit', 'Wolf', 'Bear']

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

    wild_spawn_points = [point for point in WORLD_MAP if point not in TOWNS and point.get('type') != 'Water']
    for _ in range(30):
        spawn_point = random.choice(wild_spawn_points)
        enemy_type = random.choice([enemy for enemy in ENEMY_TYPES if enemy not in ['Bandit', 'Orc']])
        enemies.append({'name': enemy_type, 'location': spawn_point})

    for town in TOWNS:
        npc_list = [
            {'name': random.choice(NPC_NAMES), 'job': 'Merchant', 'location': town},
            {'name': random.choice(NPC_NAMES), 'job': 'Guard', 'location': town},
            {'name': random.choice(NPC_NAMES), 'job': 'Guard', 'location': town},
            {'name': random.choice(NPC_NAMES), 'job': 'Farmer', 'location': town},
            {'name': random.choice(NPC_NAMES), 'job': 'Farmer', 'location': town},
            {'name': random.choice(NPC_NAMES), 'job': 'Miner', 'location': town},
            {'name': random.choice(NPC_NAMES), 'job': 'Blacksmith', 'location': town}
        ]
        npcs.extend(npc_list)
        buildings.append({'type': 'TownHall', 'location': town})
        buildings.append({'type': 'Market', 'location': town})

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
            player['rewards'].extend(quest.get('rewards', []))
            completed_quests.append(quest['name'])
            player['quests'].remove(quest)
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    player_location = player['location']
    biome = next((point['biome'] for point in WORLD_MAP if point == player_location), None)
    if not biome:
        return 'No valid location to harvest'
    
    if biome == 'Forest':
        return 'Chopped wood'
    elif biome == 'Mountain':
        return 'Mined ore'
    elif biome == 'Desert':
        return 'Gathered sand'
    elif biome == 'Plains':
        return 'Gathered herbs'
    else:
        return 'Nothing to harvest'