# Game Data Constants

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 218, 185)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (165, 42, 42)},
    {'name': 'Crossbow', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (139, 76, 57)},
    {'name': 'Wand', 'atk': 6, 'type': 'magic', 'val': 30, 'col': (255, 182, 193)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 20, 'col': (255, 69, 0)},
    {'name': 'Spear', 'atk': 7, 'type': 'ranged', 'val': 35, 'col': (139, 69, 19)},
    {'name': 'Orb', 'atk': 8, 'type': 'magic', 'val': 40, 'col': (255, 218, 185)},
    {'name': 'Hammer', 'atk': 11, 'type': 'melee', 'val': 55, 'col': (165, 42, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Helmet', 'Chestplate', 'Boots'], 'def': 3, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Helmet', 'Chestplate', 'Boots'], 'def': 5, 'val': 60},
    {'name': 'Steel Armor', 'parts': ['Helmet', 'Chestplate', 'Boots'], 'def': 7, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 10, 'dmg': 8, 'col': (255, 69, 0), 'desc': 'A basic fire spell'},
    {'name': 'Ice Shard', 'mp': 12, 'dmg': 7, 'col': (135, 206, 250), 'desc': 'Throws a shard of ice'},
    {'name': 'Lightning Bolt', 'mp': 14, 'dmg': 9, 'col': (255, 255, 0), 'desc': 'Unleashes a bolt of lightning'},
    {'name': 'Heal', 'mp': 8, 'dmg': -5, 'col': (34, 139, 34), 'desc': 'Restores health'},
    {'name': 'Shield', 'mp': 6, 'dmg': 0, 'col': (220, 220, 220), 'desc': 'Increases defense temporarily'},
    {'name': 'Blizzard', 'mp': 15, 'dmg': 10, 'col': (135, 206, 250), 'desc': 'Summons a blizzard'},
    {'name': 'Meteor Shower', 'mp': 20, 'dmg': 12, 'col': (255, 69, 0), 'desc': 'Calls down meteors'},
    {'name': 'Thunderstorm', 'mp': 18, 'dmg': 11, 'col': (255, 255, 0), 'desc': 'Summons a thunderstorm'},
    {'name': 'Regenerate', 'mp': 7, 'dmg': -4, 'col': (34, 139, 34), 'desc': 'Gradually restores health'},
    {'name': 'Barrier', 'mp': 5, 'dmg': 0, 'col': (220, 220, 220), 'desc': 'Creates a protective barrier'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Mana Stone',
    'Gold Coin',
    'Healing Herb',
    'Fire Essence',
    'Ice Shard'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Defeat 5 goblins in the forest', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Bandit Raid', 'desc': 'Defeat 3 bandits in the mountains', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 30},
    {'id': 3, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 iron ore from the mines', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 40, 'reward_xp': 15},
    {'id': 4, 'name': 'Steel Ingot Quest', 'desc': 'Craft 5 steel ingots at the blacksmith', 'target': 'mat:Steel Ingot', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 25},
    {'id': 5, 'name': 'Healing Herbs', 'desc': 'Collect 8 healing herbs from the forest', 'target': 'mat:Healing Herb', 'need': 8, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 10}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom'},
    'bandit': {'rep': 0, 'name': 'Bandits'},
    'goblin': {'rep': 0, 'name': 'Goblins'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler.', 'opts': ['Quests', 'Info', 'Leave']}],
    'Blacksmith': [{'text': 'Need weapons or armor?', 'opts': ['Craft', 'Repair', 'Leave']}],
    'Farmer': [{'text': 'Hello, how can I help you?', 'opts': ['Buy Produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hi there.', 'opts': ['Talk', 'Leave']}]
}

NPC_NAMES = [
    'Alice',
    'Bob',
    'Charlie',
    'Diana',
    'Ethan',
    'Fiona',
    'George',
    'Hannah',
    'Ian',
    'Julia',
    'Kevin',
    'Lena',
    'Mike',
    'Nina',
    'Oscar',
    'Penny'
]
