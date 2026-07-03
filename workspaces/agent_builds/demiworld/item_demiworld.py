# Game Data Constants

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 190, 140)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 30, 'col': (160, 82, 45)},
    {'name': 'Fire Staff', 'atk': 12, 'type': 'magic', 'val': 70, 'col': (255, 69, 0)},
    {'name': 'Dagger', 'atk': 6, 'type': 'melee', 'val': 20, 'col': (138, 43, 226)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 50, 'col': (165, 42, 42)},
    {'name': 'Ice Wand', 'atk': 9, 'type': 'magic', 'val': 60, 'col': (0, 255, 255)},
    {'name': 'Great Axe', 'atk': 15, 'type': 'melee', 'val': 80, 'col': (139, 69, 19)},
    {'name': 'Longbow', 'atk': 11, 'type': 'ranged', 'val': 40, 'col': (255, 140, 0)},
    {'name': 'Lightning Rod', 'atk': 13, 'type': 'magic', 'val': 75, 'col': (255, 215, 0)},
    {'name': 'Spear', 'atk': 9, 'type': 'melee', 'val': 45, 'col': (165, 42, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helm', 'Leather Chestplate', 'Leather Greaves'], 'def': 8, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Iron Helm', 'Iron Chestplate', 'Iron Greaves'], 'def': 15, 'val': 70},
    {'name': 'Dragon Scale Mail', 'parts': ['Dragon Helm', 'Dragon Chestplate', 'Dragon Greaves'], 'def': 25, 'val': 150}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 15, 'dmg': 20, 'col': (255, 69, 0), 'desc': 'A fiery projectile that burns enemies.'},
    {'name': 'Heal', 'mp': 10, 'dmg': -15, 'col': (0, 255, 0), 'desc': 'Restores health to an ally.'},
    {'name': 'Lightning Bolt', 'mp': 20, 'dmg': 30, 'col': (255, 215, 0), 'desc': 'A bolt of lightning that shocks enemies.'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (173, 216, 230), 'desc': 'Raises a shield to block incoming damage.'},
    {'name': 'Ice Shard', 'mp': 15, 'dmg': 18, 'col': (0, 255, 255), 'desc': 'Fires shards of ice that freeze enemies.'},
    {'name': 'Mana Shield', 'mp': 25, 'dmg': 0, 'col': (138, 43, 226), 'desc': 'Creates a shield that absorbs magic damage.'},
    {'name': 'Earthquake', 'mp': 30, 'dmg': 25, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake and damage enemies.'},
    {'name': 'Blizzard', 'mp': 20, 'dmg': 22, 'col': (173, 216, 230), 'desc': 'Summons a blizzard that damages all enemies.'},
    {'name': 'Meteor Shower', 'mp': 40, 'dmg': 35, 'col': (255, 69, 0), 'desc': 'Calls down meteors to rain fire upon enemies.'},
    {'name': 'Resurrection', 'mp': 50, 'dmg': -100, 'col': (0, 255, 0), 'desc': 'Brings a fallen ally back to life with full health.'}
]

MATERIALS = [
    'Iron Ore',
    'Leather Hide',
    'Dragon Scale',
    'Mana Crystal',
    'Wood',
    'Coal',
    'Herbs',
    'Gems',
    'Silk',
    'Steel'
]

QUESTS = [
    {'id': 1, 'name': 'Kill Goblins', 'desc': 'Eliminate 10 goblins in the forest.', 'target': 'goblin', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Herbs', 'desc': 'Gather 5 herbs from the forest.', 'target': 'mat:Herbs', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 10},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 70, 'reward_xp': 30},
    {'id': 4, 'name': 'Craft Armor', 'desc': 'Create a set of Iron Armor.', 'target': 'Iron Armor', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 80, 'reward_xp': 25},
    {'id': 5, 'name': 'Discover Ancient Ruins', 'desc': 'Find the ancient ruins hidden in the mountains.', 'target': 'mat:Gems', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 40}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Stay alert, stranger.', 'opts': ['Report Bandit Activity', 'Ask About Village News', 'Leave']}],
    'Blacksmith': [{'text': 'Need a weapon or armor?', 'opts': ['Craft Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How can I help you?', 'opts': ['Buy Produce', 'Sell Materials', 'Leave']}],
    'default': [{'text': 'Greetings!', 'opts': ['Talk', 'Leave']}]
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
    'Natalia',
    'Oscar',
    'Piper'
]

NPC_JOBS = ['Blacksmith', 'Merchant', 'Healer']