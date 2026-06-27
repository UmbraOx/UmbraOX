# Game Data Constants

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 6, 'type': 'magic', 'val': 30, 'col': (255, 218, 185)},
    {'name': 'Dagger', 'atk': 4, 'type': 'melee', 'val': 20, 'col': (169, 169, 169)},
    {'name': 'Crossbow', 'atk': 7, 'type': 'ranged', 'val': 35, 'col': (148, 0, 211)},
    {'name': 'Wand', 'atk': 5, 'type': 'magic', 'val': 25, 'col': (65, 105, 225)},
    {'name': 'Mace', 'atk': 9, 'type': 'melee', 'val': 45, 'col': (255, 140, 0)},
    {'name': 'Spear', 'atk': 7, 'type': 'ranged', 'val': 30, 'col': (85, 107, 47)},
    {'name': 'Tome', 'atk': 6, 'type': 'magic', 'val': 28, 'col': (255, 255, 0)},
    {'name': 'Halberd', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (139, 0, 0)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 5, 'val': 20},
    {'name': 'Chainmail', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 10, 'val': 40},
    {'name': 'Plate Mail', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 15, 'val': 60}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A fiery orb that explodes on impact.'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (34, 139, 34), 'desc': 'Restores health to the target.'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (72, 61, 139), 'desc': 'A bolt of lightning strikes the enemy.'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (148, 0, 211), 'desc': 'Increases defense for a short time.'},
    {'name': 'Invisibility', 'mp': 30, 'dmg': 0, 'col': (65, 105, 225), 'desc': 'Makes the caster invisible for a short time.'},
    {'name': 'Fire Shield', 'mp': 20, 'dmg': 5, 'col': (255, 140, 0), 'desc': 'A shield that deals fire damage to attackers.'},
    {'name': 'Thunderclap', 'mp': 35, 'dmg': 25, 'col': (85, 107, 47), 'desc': 'Stuns the enemy with a loud clap of thunder.'},
    {'name': 'Ice Shard', 'mp': 15, 'dmg': 10, 'col': (255, 255, 0), 'desc': 'Launches an icy shard at the enemy.'},
    {'name': 'Lightning Surge', 'mp': 40, 'dmg': 30, 'col': (139, 0, 0), 'desc': 'A powerful surge of lightning that deals massive damage.'},
    {'name': 'Earthquake', 'mp': 50, 'dmg': 20, 'col': (165, 42, 42), 'desc': 'Causes the ground to shake, damaging all enemies in range.'}
]

MATERIALS = [
    'Iron',
    'Steel',
    'Wood',
    'Leather',
    'Cloth',
    'Crystal',
    'Obsidian',
    'Gold',
    'Silver',
    'Bronze'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron', 'desc': 'Gather 10 pieces of iron from the mines.', 'target': 'mat:Iron', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 10},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 150, 'reward_xp': 30},
    {'id': 4, 'name': 'Craft Sword', 'desc': 'Create a sword using the blacksmith.', 'target': 'craft:Sword', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 15},
    {'id': 5, 'name': 'Heal Farmer', 'desc': 'Use a heal spell to restore the farmer\'s health.', 'target': 'spell:Heal', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 25, 'reward_xp': 5}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings! How can I assist you?', 'opts': ['Report Bandit Activity', 'Inquire About Quests', 'Leave']}],
    'Blacksmith': [{'text': 'Need something forged?', 'opts': ['Order Weapon', 'Order Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello, traveler! How can I help you today?', 'opts': ['Buy Produce', 'Talk About Weather', 'Leave']}],
    'default': [{'text': 'Hello!', 'opts': ['Greet', 'Ask About Quests', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caelan',
    'Daria',
    'Eldrin',
    'Fiona',
    'Garren',
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
