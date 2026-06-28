# Game Data Constants for MyGame

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 218, 185)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 20, 'col': (169, 169, 169)},
    {'name': 'Crossbow', 'atk': 12, 'type': 'ranged', 'val': 70, 'col': (139, 0, 0)},
    {'name': 'Wand', 'atk': 9, 'type': 'magic', 'val': 60, 'col': (255, 20, 147)},
    {'name': 'Mace', 'atk': 11, 'type': 'melee', 'val': 80, 'col': (139, 0, 139)},
    {'name': 'Spear', 'atk': 6, 'type': 'ranged', 'val': 25, 'col': (0, 100, 0)},
    {'name': 'Tome', 'atk': 8, 'type': 'magic', 'val': 45, 'col': (75, 0, 130)},
    {'name': 'Hammer', 'atk': 9, 'type': 'melee', 'val': 65, 'col': (255, 140, 0)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Chestplate', 'Gauntlets', 'Boots'], 'def': 5, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Chestplate', 'Gauntlets', 'Boots'], 'def': 10, 'val': 60},
    {'name': 'Steel Armor', 'parts': ['Chestplate', 'Gauntlets', 'Boots'], 'def': 15, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A basic fire spell'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 14, 'col': (173, 216, 230), 'desc': 'Throws a shard of ice'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (255, 255, 0), 'desc': 'Unleashes a bolt of lightning'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (34, 139, 34), 'desc': 'Restores health to the target'},
    {'name': 'Shield', 'mp': 20, 'dmg': 0, 'col': (165, 42, 42), 'desc': 'Creates a protective shield'},
    {'name': 'Poison Arrow', 'mp': 10, 'dmg': 8, 'col': (34, 139, 34), 'desc': 'Fires an arrow coated in poison'},
    {'name': 'Thunderclap', 'mp': 25, 'dmg': 18, 'col': (255, 69, 0), 'desc': 'A powerful clap of thunder'},
    {'name': 'Blizzard', 'mp': 30, 'dmg': 25, 'col': (173, 216, 230), 'desc': 'Summons a blizzard'},
    {'name': 'Earthquake', 'mp': 40, 'dmg': 30, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake'},
    {'name': 'Meteor Shower', 'mp': 50, 'dmg': 40, 'col': (255, 69, 0), 'desc': 'Summons a shower of meteors'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Stone Brick',
    'Gold Bar',
    'Silver Coin',
    'Herb Bundle',
    'Potion Vial'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Defeat 5 goblins in the forest', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Bandit Raid', 'desc': 'Defeat 3 bandits in the mountains', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 30},
    {'id': 3, 'name': 'Collect Herbs', 'desc': 'Gather 10 herb bundles from the forest', 'target': 'mat:Herb Bundle', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 25, 'reward_xp': 10},
    {'id': 4, 'name': 'Mine Iron Ore', 'desc': 'Collect 8 iron ores from the mine', 'target': 'mat:Iron Ore', 'need': 8, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 25},
    {'id': 5, 'name': 'Craft Armor', 'desc': 'Create a set of leather armor', 'target': 'mat:Leather Hide', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 40}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom'},
    'bandit': {'rep': 0, 'name': 'Bandits'},
    'goblin': {'rep': 0, 'name': 'Goblins'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Hello! What can I sell you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. How may I assist you?', 'opts': ['Report Bandit Activity', 'Ask About Quests', 'Leave']}],
    'Blacksmith': [{'text': 'Welcome to my forge! What do you need?', 'opts': ['Buy Armor', 'Sell Materials', 'Leave']}],
    'Farmer': [{'text': 'Good day! How can I help you today?', 'opts': ['Buy Produce', 'Trade Seeds', 'Leave']}],
    'default': [{'text': 'Hello there. Not much to do here.', 'opts': ['Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caelum',
    'Daria',
    'Eldrin',
    'Fiona',
    'Garrick',
    'Hannah',
    'Igor',
    'Jenna',
    'Kael',
    'Lila',
    'Morgan',
    'Nora',
    'Oscar',
    'Penny'
]
