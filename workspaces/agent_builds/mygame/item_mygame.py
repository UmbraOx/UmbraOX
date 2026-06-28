# Game Data Constants

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 190, 140)},
    {'name': 'Steel Axe', 'atk': 12, 'type': 'melee', 'val': 70, 'col': (220, 220, 220)},
    {'name': 'Shadow Dagger', 'atk': 8, 'type': 'melee', 'val': 60, 'col': (139, 0, 139)},
    {'name': 'Oak Bow', 'atk': 7, 'type': 'ranged', 'val': 45, 'col': (139, 69, 19)},
    {'name': 'Flame Staff', 'atk': 9, 'type': 'magic', 'val': 80, 'col': (255, 69, 0)},
    {'name': 'Frost Wand', 'atk': 9, 'type': 'magic', 'val': 80, 'col': (173, 216, 230)},
    {'name': 'Battle Hammer', 'atk': 15, 'type': 'melee', 'val': 100, 'col': (192, 192, 192)},
    {'name': 'Silver Spear', 'atk': 11, 'type': 'melee', 'val': 65, 'col': (192, 192, 192)},
    {'name': 'Throwing Stars', 'atk': 5, 'type': 'ranged', 'val': 30, 'col': (255, 215, 0)},
    {'name': 'Death Scythe', 'atk': 20, 'type': 'melee', 'val': 150, 'col': (0, 0, 0)}
]

ARMOR_SETS = [
    {'name': 'Iron Set', 'parts': ['Iron Helmet', 'Iron Chestplate', 'Iron Greaves'], 'def': 8, 'val': 120},
    {'name': 'Steel Set', 'parts': ['Steel Helmet', 'Steel Chestplate', 'Steel Greaves'], 'def': 10, 'val': 150},
    {'name': 'Shadow Set', 'parts': ['Shadow Hood', 'Shadow Robe', 'Shadow Boots'], 'def': 9, 'val': 140}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'Launches a fiery ball at the enemy.'},
    {'name': 'Ice Spike', 'mp': 18, 'dmg': 14, 'col': (173, 216, 230), 'desc': 'Fires an icy spike to freeze the target.'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (255, 255, 0), 'desc': 'Unleashes a bolt of lightning on the enemy.'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (0, 255, 0), 'desc': 'Restores health to an ally.'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (169, 169, 169), 'desc': 'Creates a shield to block incoming damage.'},
    {'name': 'Teleport', 'mp': 30, 'dmg': 0, 'col': (255, 255, 255), 'desc': 'Instantly teleports you to a safe location.'},
    {'name': 'Summon Wolf', 'mp': 40, 'dmg': 0, 'col': (139, 69, 19), 'desc': 'Summons a wolf to fight by your side.'},
    {'name': 'Earthquake', 'mp': 25, 'dmg': 18, 'col': (139, 76, 57), 'desc': 'Causes the ground to shake and damage enemies.'},
    {'name': 'Drain Life', 'mp': 20, 'dmg': 12, 'col': (128, 0, 0), 'desc': 'Drains life from an enemy to heal yourself.'},
    {'name': 'Time Slow', 'mp': 35, 'dmg': 0, 'col': (75, 0, 130), 'desc': 'Slows down time for a short duration.'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Shadow Crystal',
    'Oak Wood',
    'Flame Essence',
    'Frost Shard',
    'Silver Bar',
    'Wolf Fang',
    'Star Dust',
    'Dark Soul'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Defeat 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 15},
    {'id': 3, 'name': 'Shadow Crystal Quest', 'desc': 'Find a shadow crystal in the dark forest.', 'target': 'mat:Shadow Crystal', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 70, 'reward_xp': 25},
    {'id': 4, 'name': 'Bandit Ambush', 'desc': 'Defeat the bandits at the ambush point.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 20},
    {'id': 5, 'name': 'Heal the Village', 'desc': 'Use healing spells to restore health to all villagers.', 'target': 'mat:Dark Soul', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 40, 'reward_xp': 18}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Stay alert, stranger.', 'opts': ['Report Bandit Activity', 'Ask for News', 'Leave']}],
    'Blacksmith': [{'text': 'Need a weapon or armor?', 'opts': ['Craft Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'How can I help you today?', 'opts': ['Buy Produce', 'Sell Seeds', 'Leave']}],
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
    'Jenna',
    'Kael',
    'Lila',
    'Morgan',
    'Nora',
    'Oscar',
    'Piper'
]
