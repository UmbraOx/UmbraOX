# Game Data Constants

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 200, 200)},
    {'name': 'Steel Axe', 'atk': 15, 'type': 'melee', 'val': 75, 'col': (180, 180, 180)},
    {'name': 'Shadow Dagger', 'atk': 8, 'type': 'melee', 'val': 60, 'col': (50, 50, 150)},
    {'name': 'Oak Bow', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (139, 69, 19)},
    {'name': 'Flame Staff', 'atk': 12, 'type': 'magic', 'val': 80, 'col': (255, 69, 0)},
    {'name': 'Frost Wand', 'atk': 10, 'type': 'magic', 'val': 70, 'col': (0, 191, 255)},
    {'name': 'Battle Hammer', 'atk': 18, 'type': 'melee', 'val': 100, 'col': (165, 42, 42)},
    {'name': 'Silver Spear', 'atk': 13, 'type': 'melee', 'val': 90, 'col': (192, 192, 192)},
    {'name': 'Throwing Stars', 'atk': 7, 'type': 'ranged', 'val': 55, 'col': (255, 215, 0)},
    {'name': 'Death Scythe', 'atk': 20, 'type': 'melee', 'val': 120, 'col': (64, 0, 64)}
]

ARMOR_SETS = [
    {'name': 'Iron Set', 'parts': ['Iron Helmet', 'Iron Chestplate', 'Iron Greaves'], 'def': 8, 'val': 150},
    {'name': 'Steel Set', 'parts': ['Steel Helmet', 'Steel Chestplate', 'Steel Greaves'], 'def': 12, 'val': 225},
    {'name': 'Shadow Set', 'parts': ['Shadow Hood', 'Shadow Robe', 'Shadow Boots'], 'def': 10, 'val': 200}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 30, 'dmg': 25, 'col': (255, 69, 0), 'desc': 'A fiery orb that explodes on impact.'},
    {'name': 'Ice Spike', 'mp': 25, 'dmg': 20, 'col': (0, 191, 255), 'desc': 'Launches a sharp ice shard at the target.'},
    {'name': 'Lightning Bolt', 'mp': 40, 'dmg': 30, 'col': (255, 255, 0), 'desc': 'Unleashes a bolt of lightning from your fingertips.'},
    {'name': 'Heal', 'mp': 20, 'dmg': -15, 'col': (0, 255, 0), 'desc': 'Restores health to the target.'},
    {'name': 'Shield', 'mp': 35, 'dmg': 0, 'col': (169, 169, 169), 'desc': 'Creates a protective barrier around you.'},
    {'name': 'Teleport', 'mp': 50, 'dmg': 0, 'col': (238, 130, 238), 'desc': 'Instantly moves you to a marked location.'},
    {'name': 'Summon Wolf', 'mp': 45, 'dmg': 0, 'col': (192, 192, 192), 'desc': 'Summons a loyal wolf companion.'},
    {'name': 'Earthquake', 'mp': 60, 'dmg': 35, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake and crush enemies.'},
    {'name': 'Drain Life', 'mp': 40, 'dmg': 25, 'col': (128, 0, 128), 'desc': 'Absorbs life force from the target.'},
    {'name': 'Time Slow', 'mp': 70, 'dmg': 0, 'col': (255, 255, 255), 'desc': 'Slows down time for a short duration.'}
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
    {'id': 1, 'name': 'Goblin Raid', 'desc': 'Defeat the goblins raiding the village.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 200},
    {'id': 2, 'name': 'Bandit Hideout', 'desc': 'Find and destroy the bandit hideout.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 150, 'reward_xp': 300},
    {'id': 3, 'name': 'Iron Ore Hunt', 'desc': 'Collect iron ore for the blacksmith.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 100},
    {'id': 4, 'name': 'Shadow Crystal Quest', 'desc': 'Retrieve a shadow crystal from the dark forest.', 'target': 'mat:Shadow Crystal', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 200, 'reward_xp': 400},
    {'id': 5, 'name': 'Farmer\'s Request', 'desc': 'Help the farmer with his crops.', 'target': 'mat:Oak Wood', 'need': 8, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 150}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Gang'},
    'goblin': {'rep': 0, 'name': 'Goblin Clan'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop! What can I get you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. How may I assist you?', 'opts': ['Report Bandit Activity', 'Ask About Town News', 'Leave']}],
    'Blacksmith': [{'text': 'Need a weapon or armor? Come on in.', 'opts': ['Forge Weapon', 'Repair Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How can I help you today?', 'opts': ['Buy Produce', 'Ask About Crops', 'Leave']}],
    'default': [{'text': 'Hi there. Not much to do here.', 'opts': ['Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynne',
    'Caelum',
    'Daria',
    'Eldrin',
    'Fiona',
    'Garrick',
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


if __name__ == '__main__':
    main()
