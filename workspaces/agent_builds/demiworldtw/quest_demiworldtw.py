# Quest and Faction System Module for DemiWorldTw

import random

class Player:
    def __init__(self):
        self.inventory = {}
        self.completed_quests = []
        self.active_quests = {}

class Quest:
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives  # dict of {objective: (type, target, progress)}
        self.rewards = rewards

class Faction:
    def __init__(self, name, reputation=0):
        self.name = name
        self.reputation = reputation

class NPC:
    def __init__(self, name, faction, dialog):
        self.name = name
        self.faction = faction
        self.dialog = dialog

def spawn_world_entities(world_map, towns, cities, bandit_camps, goblin_camps, enemy_defs, npc_names):
    enemies_list = []
    npcs_list = []
    buildings_list = []

    for town in towns:
        buildings_list.append(f"Town Hall {town}")
        for _ in range(random.randint(3, 5)):
            faction_name = random.choice(list(npc_names.keys()))
            faction = Faction(faction_name)
            npc_name = random.choice(npc_names[faction_name])
            dialog = "Hello traveler!"
            npcs_list.append(NPC(npc_name, faction, dialog))

    for city in cities:
        buildings_list.append(f"City Hall {city}")
        for _ in range(random.randint(5, 10)):
            faction_name = random.choice(list(npc_names.keys()))
            faction = Faction(faction_name)
            npc_name = random.choice(npc_names[faction_name])
            dialog = "Greetings!"
            npcs_list.append(NPC(npc_name, faction, dialog))

    for camp in bandit_camps:
        enemies_list.extend([enemy_defs['bandit'] for _ in range(random.randint(2, 4))])

    for camp in goblin_camps:
        enemies_list.extend([enemy_defs['goblin'] for _ in range(random.randint(3, 6))])

    return enemies_list, npcs_list, buildings_list

def check_quest_kill(player, enemy_name):
    for quest_name, quest in player.active_quests.items():
        if 'kill' in quest.objectives:
            obj_type, target, progress = quest.objectives['kill']
            if target == enemy_name:
                quest.objectives['kill'] = (obj_type, target, progress + 1)

def check_quest_item(player, item_name, qty):
    for quest_name, quest in player.active_quests.items():
        if 'item' in quest.objectives:
            obj_type, target, progress = quest.objectives['item']
            if target == item_name and player.inventory.get(item_name, 0) >= qty:
                quest.objectives['item'] = (obj_type, target, progress + qty)

def complete_ready_quests(player):
    completed = []
    for quest_name, quest in list(player.active_quests.items()):
        all_completed = True
        for obj_type, _, progress in quest.objectives.values():
            if progress < 1:
                all_completed = False
                break
        if all_completed:
            player.completed_quests.append(quest.name)
            completed.append(quest.name)
            del player.active_quests[quest_name]
    return completed

def harvest_nearby(player, world_map):
    resources = ['wood', 'ore', 'herbs']
    gathered_resource = random.choice(resources)
    if gathered_resource in player.inventory:
        player.inventory[gathered_resource] += 1
    else:
        player.inventory[gathered_resource] = 1
    return f"You have gathered {gathered_resource}."