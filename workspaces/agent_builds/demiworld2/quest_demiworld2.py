import random

WORLD_BIOMES = ['forest', 'mountain', 'desert', 'plains']
ENEMY_TYPES = ['goblin', 'orc', 'bandit', 'wolf', 'bear']

class Quest:
    def __init__(self, name, description, objective, reward):
        self.name = name
        self.description = description
        self.objective = objective
        self.reward = reward
        self.progress = 0

    def update_progress(self, amount):
        self.progress += amount

    def is_complete(self):
        return self.progress >= self.objective

class Player:
    def __init__(self):
        self.quests = []
        self.inventory = {}

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append(random.choice(ENEMY_DEFS['bandit']))

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append(random.choice(ENEMY_DEFS['goblin']))
        enemies.append(random.choice(ENEMY_DEFS['orc']))

    wild_spawn_points = [point for point in WORLD_MAP if point not in TOWNS and point not in CITIES]
    for _ in range(30):
        spawn_point = random.choice(wild_spawn_points)
        enemies.append(random.choice([enemy for enemy in ENEMY_DEFS.values()]))

    for town in TOWNS:
        npc_jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in npc_jobs:
            name = random.choice(NPC_NAMES)
            npcs.append({'name': name, 'job': job, 'location': town})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player.quests:
        if 'kill' in quest.objective and enemy_name in quest.objective:
            quest.update_progress(1)

def check_item_quests(player, item_name, qty):
    for quest in player.quests:
        if 'collect' in quest.objective and item_name in quest.objective:
            quest.update_progress(qty)

def complete_ready_quests(player):
    completed_quests = []
    for quest in player.quests[:]:
        if quest.is_complete():
            completed_quests.append(quest.name)
            player.quests.remove(quest)
            # Add reward logic here
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    biome = random.choice(WORLD_BIOMES)  # Simplified for example
    if biome == 'forest':
        item = 'wood'
    elif biome == 'mountain':
        item = 'ore'
    elif biome == 'desert':
        item = 'sand'
    else:
        item = 'herbs'

    if item in player.inventory:
        player.inventory[item] += 1
    else:
        player.inventory[item] = 1

    return f'Gathered {item} from the {biome}'

if __name__ == '__main__':
    main()
