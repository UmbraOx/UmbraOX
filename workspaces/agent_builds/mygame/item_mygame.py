# Game Data Constants for MyGame

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 215, 0)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (165, 42, 42)},
    {'name': 'Crossbow', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (139, 76, 57)},
    {'name': 'Wand', 'atk': 6, 'type': 'magic', 'val': 30, 'col': (255, 182, 193)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 25, 'col': (220, 20, 60)},
    {'name': 'Spear', 'atk': 11, 'type': 'ranged', 'val': 55, 'col': (139, 71, 38)},
    {'name': 'Orb', 'atk': 8, 'type': 'magic', 'val': 40, 'col': (255, 69, 0)},
    {'name': 'Hammer', 'atk': 13, 'type': 'melee', 'val': 70, 'col': (165, 42, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Helmet', 'Chestplate', 'Boots'], 'def': 5, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Helmet', 'Chestplate', 'Boots'], 'def': 10, 'val': 60},
    {'name': 'Steel Armor', 'parts': ['Helmet', 'Chestplate', 'Boots'], 'def': 15, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A fiery projectile'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 14, 'col': (135, 206, 250), 'desc': 'A shard of ice'},
    {'name': 'Lightning Bolt', 'mp': 22, 'dmg': 16, 'col': (255, 255, 0), 'desc': 'A bolt of lightning'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (34, 139, 34), 'desc': 'Restores health'},
    {'name': 'Shield', 'mp': 25, 'dmg': 0, 'col': (165, 42, 42), 'desc': 'Increases defense temporarily'},
    {'name': 'Fire Shield', 'mp': 30, 'dmg': 0, 'col': (255, 69, 0), 'desc': 'Reflects fire damage'},
    {'name': 'Ice Armor', 'mp': 28, 'dmg': 0, 'col': (135, 206, 250), 'desc': 'Reduces physical damage'},
    {'name': 'Thunder Wave', 'mp': 24, 'dmg': 12, 'col': (255, 255, 0), 'desc': 'A wave of lightning'},
    {'name': 'Earthquake', 'mp': 35, 'dmg': 20, 'col': (139, 76, 57), 'desc': 'Shakes the ground'},
    {'name': 'Meteor Shower', 'mp': 40, 'dmg': 25, 'col': (255, 69, 0), 'desc': 'Summons meteors from above'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Stone Brick',
    'Gold Nugget',
    'Silver Bar',
    'Obsidian Shard',
    'Mana Essence'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Defeat 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Bandit Raid', 'desc': 'Defeat 3 bandits in the mountains.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 30},
    {'id': 3, 'name': 'Collect Iron Ore', 'desc': 'Collect 10 iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 40, 'reward_xp': 15},
    {'id': 4, 'name': 'Steel Ingot Quest', 'desc': 'Collect 8 steel ingots from the blacksmith.', 'target': 'mat:Steel Ingot', 'need': 8, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 25},
    {'id': 5, 'name': 'Magic Crystal Hunt', 'desc': 'Find a magic crystal in the cave.', 'target': 'mat:Magic Crystal', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 40}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom'},
    'bandit': {'rep': 0, 'name': 'Bandits'},
    'goblin': {'rep': 0, 'name': 'Goblins'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Hello! What can I sell you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. How may I assist you?', 'opts': ['Quests', 'Info', 'Leave']}],
    'Blacksmith': [{'text': 'Welcome to my forge. Need anything?', 'opts': ['Forge Weapon', 'Repair Armor', 'Leave']}],
    'Farmer': [{'text': 'Hi there! How are you doing?', 'opts': ['Buy Produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hello, stranger.', 'opts': ['Talk', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caelum',
    'Daria',
    'Eldrin',
    'Fiona',
    'Galen',
    'Hannah',
    'Igor',
    'Jenna',
    'Kael',
    'Lila',
    'Morgan',
    'Nora',
    'Oscar',
    'Piper'
]
