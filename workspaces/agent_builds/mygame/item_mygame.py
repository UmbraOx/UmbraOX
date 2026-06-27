# Game Data Constants

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 6, 'type': 'magic', 'val': 30, 'col': (255, 215, 0)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 70, 'col': (165, 42, 42)},
    {'name': 'Crossbow', 'atk': 9, 'type': 'ranged', 'val': 50, 'col': (139, 0, 0)},
    {'name': 'Wand', 'atk': 7, 'type': 'magic', 'val': 40, 'col': (255, 69, 0)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 30, 'col': (128, 0, 0)},
    {'name': 'Spear', 'atk': 7, 'type': 'ranged', 'val': 40, 'col': (165, 42, 42)},
    {'name': 'Tome', 'atk': 9, 'type': 'magic', 'val': 50, 'col': (255, 215, 0)},
    {'name': 'Hammer', 'atk': 11, 'type': 'melee', 'val': 60, 'col': (139, 0, 0)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 5, 'val': 20},
    {'name': 'Chainmail', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 10, 'val': 40},
    {'name': 'Plate Armor', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 15, 'val': 60}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A fiery projectile that burns enemies.'},
    {'name': 'Heal', 'mp': 30, 'dmg': -10, 'col': (0, 255, 0), 'desc': 'Restores health to an ally.'},
    {'name': 'Shield', 'mp': 25, 'dmg': 0, 'col': (173, 216, 230), 'desc': 'Creates a protective barrier around the caster.'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (255, 255, 0), 'desc': 'Unleashes a bolt of lightning on an enemy.'},
    {'name': 'Ice Shard', 'mp': 15, 'dmg': 10, 'col': (173, 216, 230), 'desc': 'Hurls a shard of ice at the target.'},
    {'name': 'Thunderclap', 'mp': 30, 'dmg': 25, 'col': (255, 255, 0), 'desc': 'Stuns and damages enemies in an area.'},
    {'name': 'Regenerate', 'mp': 40, 'dmg': -15, 'col': (0, 255, 0), 'desc': 'Gradually restores health to the caster over time.'},
    {'name': 'Frost Nova', 'mp': 35, 'dmg': 15, 'col': (173, 216, 230), 'desc': 'Freezes enemies in an area, dealing damage and slowing them down.'},
    {'name': 'Arcane Shield', 'mp': 40, 'dmg': 0, 'col': (255, 255, 0), 'desc': 'Creates a powerful magical barrier around the caster.'},
    {'name': 'Earthquake', 'mp': 30, 'dmg': 20, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake, damaging all enemies in range.'}
]

MATERIALS = [
    'Iron',
    'Steel',
    'Wood',
    'Leather',
    'Cloth',
    'Magic Crystal',
    'Mana Stone',
    'Obsidian',
    'Adamantite',
    'Ethereal Dust'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 pieces of iron ore from the mines.', 'target': 'mat:Iron', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 15},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 70, 'reward_xp': 25},
    {'id': 4, 'name': 'Craft Armor', 'desc': 'Create a set of leather armor.', 'target': 'mat:Leather', 'need': 15, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 20},
    {'id': 5, 'name': 'Rescue Merchant', 'desc': 'Escort the merchant safely to the market.', 'target': 'merchant', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 80, 'reward_xp': 30}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Hello! What can I offer you today?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. Are you here to report something?', 'opts': ['Report', 'Talk', 'Leave']}],
    'Blacksmith': [{'text': 'Welcome, brave warrior! Need a new weapon or armor?', 'opts': ['Forge Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'Good day! How can I assist you with your journey?', 'opts': ['Buy Food', 'Talk', 'Leave']}],
    'default': [{'text': 'Hello there. Not much to say.', 'opts': ['Leave']}]
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
    'Marius',
    'Nora',
    'Oscar',
    'Piper'
]
