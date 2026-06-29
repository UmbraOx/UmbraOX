# Game Data Constants

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 215, 0)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (165, 42, 42)},
    {'name': 'Crossbow', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (139, 76, 57)},
    {'name': 'Wand', 'atk': 6, 'type': 'magic', 'val': 30, 'col': (255, 182, 193)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 20, 'col': (255, 69, 0)},
    {'name': 'Spear', 'atk': 11, 'type': 'ranged', 'val': 55, 'col': (139, 69, 19)},
    {'name': 'Orb', 'atk': 8, 'type': 'magic', 'val': 40, 'col': (255, 215, 0)},
    {'name': 'Hammer', 'atk': 13, 'type': 'melee', 'val': 70, 'col': (165, 42, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Chestplate', 'Gauntlets', 'Boots'], 'def': 5, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Chestplate', 'Gauntlets', 'Boots'], 'def': 10, 'val': 60},
    {'name': 'Steel Armor', 'parts': ['Chestplate', 'Gauntlets', 'Boots'], 'def': 15, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A fiery projectile'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 14, 'col': (135, 206, 250), 'desc': 'A shard of ice'},
    {'name': 'Lightning Bolt', 'mp': 22, 'dmg': 17, 'col': (255, 215, 0), 'desc': 'A bolt of lightning'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (34, 139, 34), 'desc': 'Restores health'},
    {'name': 'Shield', 'mp': 25, 'dmg': 0, 'col': (165, 42, 42), 'desc': 'Increases defense temporarily'},
    {'name': 'Blizzard', 'mp': 30, 'dmg': 20, 'col': (173, 216, 230), 'desc': 'A wave of ice'},
    {'name': 'Meteor Shower', 'mp': 40, 'dmg': 25, 'col': (255, 69, 0), 'desc': 'Shower of meteors'},
    {'name': 'Thunderstorm', 'mp': 35, 'dmg': 22, 'col': (255, 215, 0), 'desc': 'A storm of lightning'},
    {'name': 'Earthquake', 'mp': 45, 'dmg': 30, 'col': (165, 42, 42), 'desc': 'Shakes the ground'},
    {'name': 'Resurrection', 'mp': 50, 'dmg': -50, 'col': (34, 139, 34), 'desc': 'Brings a fallen ally back to life'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Gold Bar',
    'Silver Coin',
    'Mana Stone',
    'Dragon Scale',
    'Phoenix Feather'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Kill 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 50},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Collect 10 iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 80, 'reward_xp': 40},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandits.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 120, 'reward_xp': 60},
    {'id': 4, 'name': 'Craft Steel Armor', 'desc': 'Craft a set of steel armor.', 'target': 'Steel Armor', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 200, 'reward_xp': 80},
    {'id': 5, 'name': 'Find the Lost Artifact', 'desc': 'Retrieve the lost artifact from the ruins.', 'target': 'Artifact', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 300, 'reward_xp': 100}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Stay alert, stranger.', 'opts': ['Report a crime', 'Ask for news', 'Leave']}],
    'Blacksmith': [{'text': 'Need weapons or armor?', 'opts': ['Forge weapon', 'Craft armor', 'Leave']}],
    'Farmer': [{'text': 'Howdy! Need anything?', 'opts': ['Buy produce', 'Sell crops', 'Leave']}],
    'default': [{'text': 'Hello there.', 'opts': ['Talk', 'Leave']}]
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
    'Jasmine',
    'Kael',
    'Lila',
    'Morgan',
    'Natalie',
    'Oscar',
    'Piper'
]
