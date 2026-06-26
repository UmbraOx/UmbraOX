# Game Data Constants for Optiopia

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 215, 0)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (165, 42, 42)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 20, 'col': (139, 0, 0)},
    {'name': 'Crossbow', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (165, 42, 42)},
    {'name': 'Wand', 'atk': 6, 'type': 'magic', 'val': 30, 'col': (75, 0, 130)},
    {'name': 'Mace', 'atk': 11, 'type': 'melee', 'val': 55, 'col': (220, 20, 60)},
    {'name': 'Spear', 'atk': 9, 'type': 'melee', 'val': 45, 'col': (139, 69, 19)},
    {'name': 'Magic Staff', 'atk': 8, 'type': 'magic', 'val': 40, 'col': (255, 215, 0)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helm', 'Leather Chestplate', 'Leather Greaves'], 'def': 3, 'val': 40},
    {'name': 'Chainmail', 'parts': ['Chain Helm', 'Chain Chestplate', 'Chain Greaves'], 'def': 5, 'val': 60},
    {'name': 'Plate Mail', 'parts': ['Plate Helm', 'Plate Chestplate', 'Plate Greaves'], 'def': 7, 'val': 80},
    {'name': 'Mage Robes', 'parts': ['Robe Hood', 'Robe Top', 'Robe Bottoms'], 'def': 2, 'val': 35}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 15, 'dmg': 10, 'col': (255, 69, 0), 'desc': 'A fiery orb that explodes on impact.'},
    {'name': 'Heal', 'mp': 10, 'dmg': -8, 'col': (34, 139, 34), 'desc': 'Restores health to the target.'},
    {'name': 'Lightning Bolt', 'mp': 20, 'dmg': 15, 'col': (75, 0, 130), 'desc': 'A bolt of lightning strikes an enemy.'},
    {'name': 'Shield', 'mp': 8, 'dmg': 0, 'col': (64, 224, 208), 'desc': 'Creates a shield to block damage.'},
    {'name': 'Ice Shard', 'mp': 12, 'dmg': 9, 'col': (0, 255, 255), 'desc': 'Launches an icy shard at the enemy.'},
    {'name': 'Thunderclap', 'mp': 18, 'dmg': 13, 'col': (255, 69, 0), 'desc': 'A powerful clap that stuns enemies.'},
    {'name': 'Poison Arrow', 'mp': 14, 'dmg': 7, 'col': (0, 128, 0), 'desc': 'Fires an arrow coated in poison.'},
    {'name': 'Earthquake', 'mp': 25, 'dmg': 20, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake and damage enemies.'},
    {'name': 'Mana Shield', 'mp': 10, 'dmg': 0, 'col': (75, 0, 130), 'desc': 'Creates a shield that absorbs magic damage.'},
    {'name': 'Blizzard', 'mp': 22, 'dmg': 14, 'col': (0, 255, 255), 'desc': 'Summons a blizzard to freeze and damage enemies.'}
]

MATERIALS = [
    'Iron Ore',
    'Gold Ore',
    'Silver Ore',
    'Wood Logs',
    'Leather Hide',
    'Magic Crystal',
    'Steel Ingot',
    'Mana Stone',
    'Dragon Scale',
    'Phoenix Feather'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 15},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 70, 'reward_xp': 25},
    {'id': 4, 'name': 'Mage Assistance', 'desc': 'Deliver a message to the Mage Tower.', 'target': 'mage', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 20},
    {'id': 5, 'name': 'Dragon Scale', 'desc': 'Retrieve a dragon scale from the cave.', 'target': 'mat:Dragon Scale', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 30}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Gang'},
    'goblin': {'rep': 0, 'name': 'Goblin Clan'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings! How can I assist you?', 'opts': ['Report Bandit Activity', 'Inquire About Quests', 'Leave']}],
    'Blacksmith': [{'text': 'Need weapons or armor? Come in!', 'opts': ['Forge Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How can I help you?', 'opts': ['Buy Produce', 'Sell Crops', 'Leave']}],
    'default': [{'text': 'Hello there.', 'opts': ['Talk', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynne',
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
    'Natalia',
    'Oscar',
    'Piper'
]


if __name__ == '__main__':
    main()
