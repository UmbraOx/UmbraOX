# Quest and Spawn Systems for MyGame

import random

WORLD_MAP = {
    'Towns': ['Village of Eldoria'],
    'Cities': [],
    'BanditCamps': [(10, 20), (30, 40)],
    'GoblinCamps': [(50, 60), (70, 80)],
    'WaterAreas': [(25, 35)]
}

ENEMY_DEFS = {
    'Bandit': {'health': 50, 'damage': 10},
    'Orc': {'health': 100, 'damage': 20},
    'Goblin': {'health': 40, 'damage': 8}
}

NPC_NAMES = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace']
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'Bandit', 'position': camp, **ENEMY_DEFS['Bandit']})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'Goblin', 'position': camp, **ENEMY_DEFS['Goblin']})
        enemies.append({'type': 'Orc', 'position': camp, **ENEMY_DEFS['Orc']})

    wild_positions = [(x, y) for x in range(100) for y in range(100)
                      if (x, y) not in TOWNS and (x, y) not in CITIES
                      and all((abs(x - wx) > 5 or abs(y - wy) > 5) for wx, wy in WORLD_MAP['WaterAreas'])]
    random.shuffle(wild_positions)

    for _ in range(30):
        x, y = wild_positions.pop()
        enemy_type = random.choice(['Bandit', 'Goblin'])
        enemies.append({'type': enemy_type, 'position': (x, y), **ENEMY_DEFS[enemy_type]})

    for town in TOWNS:
        buildings.append({'type': 'TownHall', 'position': town})
        for _ in range(7):
            name = random.choice(NPC_NAMES)
            job = random.choice(NPC_JOBS)
            npcs.append({'name': name, 'job': job, 'position': town})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player['quests']:
        if quest['type'] == 'kill' and quest['enemy'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['target']:
                print(f"Quest '{quest['name']}' completed!")

def check_item_quests(player, item_name, qty):
    for quest in player['quests']:
        if quest['type'] == 'item' and quest['item'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['target']:
                print(f"Quest '{quest['name']}' completed!")

def complete_ready_quests(player):
    completed_quests = []
    for quest in player['quests']:
        if quest['progress'] >= quest['target']:
            completed_quests.append(quest['name'])
            player['rewards'].append(quest.get('reward', 'None'))
            player['quests'].remove(quest)
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    x, y = player['position']
    biome = 'Forest'  # Simplified for example
    if biome == 'Forest':
        return 'Chopped wood'
    elif biome == 'Mountain':
        return 'Mined ore'
    else:
        return 'Gathered herbs'

if __name__ == '__main__':
    main()
