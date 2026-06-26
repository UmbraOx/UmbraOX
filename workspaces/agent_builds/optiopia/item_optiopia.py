# Game Data Constants

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 190, 140)},
    {'name': 'Longbow', 'atk': 8, 'type': 'ranged', 'val': 75, 'col': (139, 69, 19)},
    {'name': 'Fire Staff', 'atk': 12, 'type': 'magic', 'val': 100, 'col': (255, 69, 0)},
    {'name': 'Steel Dagger', 'atk': 7, 'type': 'melee', 'val': 30, 'col': (220, 220, 220)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 90, 'col': (85, 65, 130)},
    {'name': 'Ice Wand', 'atk': 9, 'type': 'magic', 'val': 85, 'col': (0, 255, 255)},
    {'name': 'Battle Axe', 'atk': 14, 'type': 'melee', 'val': 60, 'col': (139, 0, 0)},
    {'name': 'Shortbow', 'atk': 6, 'type': 'ranged', 'val': 55, 'col': (218, 165, 32)},
    {'name': 'Lightning Rod', 'atk': 11, 'type': 'magic', 'val': 95, 'col': (255, 255, 0)},
    {'name': 'Mystic Blade', 'atk': 15, 'type': 'melee', 'val': 70, 'col': (148, 0, 211)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helmet', 'Leather Chestplate', 'Leather Leggings'], 'def': 5, 'val': 30},
    {'name': 'Chainmail Armor', 'parts': ['Chainmail Helm', 'Chainmail Mail', 'Chainmail Greaves'], 'def': 10, 'val': 60},
    {'name': 'Plate Armor', 'parts': ['Steel Helmet', 'Steel Chestplate', 'Steel Leggings'], 'def': 15, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A basic fire spell that burns enemies.'},
    {'name': 'Heal', 'mp': 30, 'dmg': -10, 'col': (0, 255, 0), 'desc': 'Restores health to the target.'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (255, 255, 0), 'desc': 'A powerful electric shock that stuns enemies.'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 12, 'col': (0, 255, 255), 'desc': 'Throws a shard of ice at the enemy.'},
    {'name': 'Shield', 'mp': 22, 'dmg': -5, 'col': (220, 220, 220), 'desc': 'Creates a shield to absorb damage.'},
    {'name': 'Fire Shield', 'mp': 35, 'dmg': -15, 'col': (255, 69, 0), 'desc': 'A fiery shield that burns attackers.'},
    {'name': 'Thunderclap', 'mp': 40, 'dmg': 25, 'col': (255, 255, 0), 'desc': 'A thunderous clap that damages all enemies in range.'},
    {'name': 'Frost Nova', 'mp': 30, 'dmg': 18, 'col': (0, 255, 255), 'desc': 'Freezes nearby enemies, dealing damage over time.'},
    {'name': 'Magnetize', 'mp': 27, 'dmg': -10, 'col': (139, 69, 19), 'desc': 'Pulls in nearby items and enemies.'},
    {'name': 'Meteor Shower', 'mp': 50, 'dmg': 40, 'col': (255, 69, 0), 'desc': 'Summons meteors to rain down on enemies.'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Coal',
    'Silk Cloth',
    'Dragon Scale',
    'Goblin Horn',
    'Phoenix Feather'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 10 goblins in the forest.', 'target': 'goblin', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Bandit Raid', 'desc': 'Defeat the bandits at the village entrance.', 'target': 'bandit', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 30},
    {'id': 3, 'name': 'Collect Iron Ore', 'desc': 'Gather 15 iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 15, 'prog': 0, 'done': False, 'reward_gold': 40, 'reward_xp': 15},
    {'id': 4, 'name': 'Silk Harvest', 'desc': 'Collect 20 silk cloth from the spider caves.', 'target': 'mat:Silk Cloth', 'need': 20, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 25},
    {'id': 5, 'name': 'Dragon Scale Quest', 'desc': 'Retrieve a dragon scale from the ancient ruins.', 'target': 'mat:Dragon Scale', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 40}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Gang'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop! What can I get you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. Are you here for trouble?', 'opts': ['Yes', 'No', 'Leave']}],
    'Blacksmith': [{'text': 'Need a weapon or armor? Come take a look.', 'opts': ['Forge Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How can I help you today?', 'opts': ['Buy Produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hi there. Not much to do here.', 'opts': ['Leave']}]
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


if __name__ == '__main__':
    main()
