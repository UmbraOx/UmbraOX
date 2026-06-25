import random

WORLD_MAP = {
    'Towns': ['Village1', 'Town2'],
    'Cities': ['City1'],
    'BanditCamps': ['Camp1', 'Camp2'],
    'GoblinCamps': ['GoblinCamp1', 'GoblinCamp2'],
    'Water': ['Lake1', 'River1']
}

ENEMY_DEFS = {
    'Bandit': {'health': 50, 'damage': 10},
    'Orc': {'health': 70, 'damage': 15},
    'Goblin': {'health': 30, 'damage': 5}
}

NPC_NAMES = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace']
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Bandit', 'type': 'Bandit', **ENEMY_DEFS['Bandit']})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'type': 'Goblin', **ENEMY_DEFS['Goblin']})
        enemies.append({'name': 'Orc', 'type': 'Orc', **ENEMY_DEFS['Orc']})

    spawn_locations = [loc for loc in WORLD_MAP if loc not in TOWNS and loc not in CITIES and loc not in ['Water']]
    for _ in range(30):
        location = random.choice(spawn_locations)
        enemy_type = random.choice(list(ENEMY_DEFS.keys()))
        enemies.append({'name': enemy_type, 'type': enemy_type, **ENEMY_DEFS[enemy_type], 'location': location})

    for town in TOWNS + CITIES:
        buildings.append(town)
        npc_jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in npc_jobs:
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
    if 'kill_quests' not in player:
        player['kill_quests'] = {}
    for quest, details in list(player['kill_quests'].items()):
        if details['progress'] >= details['target']:
            player['rewards'].append(details['reward'])
            completed_quests.append(quest)
            del player['kill_quests'][quest]

    if 'item_quests' not in player:
        player['item_quests'] = {}
    for quest, details in list(player['item_quests'].items()):
        if details['progress'] >= details['target']:
            player['rewards'].append(details['reward'])
            completed_quests.append(quest)
            del player['item_quests'][quest]

    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    biome = random.choice(['Forest', 'Mountain', 'Plain'])
    if biome == 'Forest':
        resource = 'Wood'
    elif biome == 'Mountain':
        resource = 'Ore'
    else:
        resource = 'Herbs'

    player['inventory'][resource] = player.get('inventory', {}).get(resource, 0) + random.randint(1, 5)
    return f'Harvested {resource} from the {biome}'

if __name__ == '__main__':
    main()
