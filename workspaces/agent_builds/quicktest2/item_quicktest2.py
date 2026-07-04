# Game Data Constants

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 215, 0)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (139, 87, 42)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 55, 'col': (165, 42, 42)},
    {'name': 'Wand', 'atk': 9, 'type': 'magic', 'val': 50, 'col': (75, 0, 130)},
    {'name': 'Dagger', 'atk': 6, 'type': 'melee', 'val': 25, 'col': (255, 0, 0)},
    {'name': 'Spear', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (178, 34, 34)},
    {'name': 'Orb', 'atk': 8, 'type': 'magic', 'val': 40, 'col': (255, 69, 0)},
    {'name': 'Hammer', 'atk': 11, 'type': 'melee', 'val': 70, 'col': (139, 87, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 5, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 10, 'val': 60},
    {'name': 'Steel Armor', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 15, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A basic fire spell'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 14, 'col': (135, 206, 250), 'desc': 'Throws a shard of ice'},
    {'name': 'Lightning Bolt', 'mp': 22, 'dmg': 16, 'col': (255, 255, 0), 'desc': 'Unleashes a bolt of lightning'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (34, 139, 34), 'desc': 'Restores health to the target'},
    {'name': 'Shield', 'mp': 25, 'dmg': 0, 'col': (176, 196, 222), 'desc': 'Creates a protective shield'},
    {'name': 'Meteor Shower', 'mp': 30, 'dmg': 20, 'col': (255, 69, 0), 'desc': 'Summons meteors from the sky'},
    {'name': 'Frost Nova', 'mp': 28, 'dmg': 18, 'col': (135, 206, 250), 'desc': 'Freezes enemies in a nova'},
    {'name': 'Thunder Wave', 'mp': 27, 'dmg': 19, 'col': (255, 255, 0), 'desc': 'Unleashes a wave of thunder'},
    {'name': 'Greater Heal', 'mp': 20, 'dmg': -20, 'col': (34, 139, 34), 'desc': 'Heals the target for more health'},
    {'name': 'Earthquake', 'mp': 35, 'dmg': 25, 'col': (139, 87, 42), 'desc': 'Causes an earthquake to damage enemies'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Mana Stone',
    'Gold Bar',
    'Silk Cloth',
    'Obsidian Shard',
    'Dragon Scale'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Defeat 5 goblins in the forest', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Bandit Raid', 'desc': 'Defeat 3 bandits in the mountains', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 30},
    {'id': 3, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 iron ore from the mines', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 40, 'reward_xp': 15},
    {'id': 4, 'name': 'Steel Ingot Quest', 'desc': 'Craft 5 steel ingots', 'target': 'mat:Steel Ingot', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 25},
    {'id': 5, 'name': 'Dragon Scale Collection', 'desc': 'Collect 3 dragon scales from the cave', 'target': 'mat:Dragon Scale', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 40}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom'},
    'bandit': {'rep': 0, 'name': 'Bandits'},
    'goblin': {'rep': 0, 'name': 'Goblins'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. What brings you here?', 'opts': ['Quests', 'Info', 'Leave']}],
    'Blacksmith': [{'text': 'Need weapons or armor? I can help.', 'opts': ['Forge', 'Upgrade', 'Leave']}],
    'Farmer': [{'text': 'Hello! How are you today?', 'opts': ['Trade', 'Chat', 'Leave']}],
    'default': [{'text': 'I do not understand your request.', 'opts': ['Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brianna',
    'Cedric',
    'Diana',
    'Erik',
    'Fiona',
    'Gerald',
    'Hannah',
    'Ian',
    'Jasmine',
    'Karl',
    'Lila',
    'Morgan',
    'Nina',
    'Oscar',
    'Penny'
]
