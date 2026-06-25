# Game Data Constants

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 218, 185)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (139, 0, 0)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 50, 'col': (165, 42, 42)},
    {'name': 'Wand', 'atk': 9, 'type': 'magic', 'val': 45, 'col': (255, 182, 193)},
    {'name': 'Dagger', 'atk': 6, 'type': 'melee', 'val': 30, 'col': (255, 140, 0)},
    {'name': 'Spear', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (255, 69, 0)},
    {'name': 'Orb', 'atk': 8, 'type': 'magic', 'val': 40, 'col': (135, 206, 250)},
    {'name': 'Hammer', 'atk': 11, 'type': 'melee', 'val': 55, 'col': (165, 42, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helmet', 'Leather Chestplate', 'Leather Boots'], 'def': 5, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Iron Helmet', 'Iron Chestplate', 'Iron Boots'], 'def': 10, 'val': 60},
    {'name': 'Steel Armor', 'parts': ['Steel Helmet', 'Steel Chestplate', 'Steel Boots'], 'def': 15, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A basic fire spell'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (34, 139, 34), 'desc': 'Restores health to the target'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (255, 255, 0), 'desc': 'A powerful electric spell'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (65, 105, 225), 'desc': 'Creates a protective shield'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 12, 'col': (0, 191, 255), 'desc': 'Throws an icy shard at the enemy'},
    {'name': 'Thunderclap', 'mp': 30, 'dmg': 25, 'col': (255, 69, 0), 'desc': 'A thunderous clap that damages enemies'},
    {'name': 'Poison Arrow', 'mp': 12, 'dmg': 8, 'col': (34, 139, 34), 'desc': 'Fires an arrow coated in poison'},
    {'name': 'Earthquake', 'mp': 35, 'dmg': 30, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake and damage enemies'},
    {'name': 'Frost Nova', 'mp': 22, 'dmg': 18, 'col': (0, 191, 255), 'desc': 'Freezes nearby enemies in ice'},
    {'name': 'Meteor Shower', 'mp': 40, 'dmg': 35, 'col': (255, 69, 0), 'desc': 'Summons meteors to rain down on enemies'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Mana Stone',
    'Goblin Horn',
    'Dragon Scale',
    'Phoenix Feather',
    'Elixir of Life'
]

QUESTS = [
    {'id': 1, 'name': 'Kill Goblins', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 pieces of iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 10},
    {'id': 3, 'name': 'Defeat Bandit Leader', 'desc': 'Find and defeat the bandit leader in the mountains.', 'target': 'Bandit Leader', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 200, 'reward_xp': 50},
    {'id': 4, 'name': 'Craft Steel Armor', 'desc': 'Create a set of steel armor.', 'target': 'Steel Armor', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 150, 'reward_xp': 30},
    {'id': 5, 'name': 'Rescue Princess', 'desc': 'Save the princess from the dragon.', 'target': 'Dragon', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 500, 'reward_xp': 100}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Gang'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings! How can I assist you?', 'opts': ['Report a crime', 'Ask about quests', 'Leave']}],
    'Blacksmith': [{'text': 'Need weapons or armor? Come in!', 'opts': ['Order weapon', 'Order armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How are you today?', 'opts': ['Buy produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hi there.', 'opts': ['Talk', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caelum',
    'Daria',
    'Elian',
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

NPC_JOBS = ['Blacksmith']