# Game Data Constants

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 190, 140)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 30, 'col': (160, 82, 45)},
    {'name': 'Fireball Staff', 'atk': 12, 'type': 'magic', 'val': 70, 'col': (255, 69, 0)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 20, 'col': (139, 0, 0)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 40, 'col': (85, 65, 148)},
    {'name': 'Ice Lance', 'atk': 9, 'type': 'magic', 'val': 60, 'col': (0, 255, 255)},
    {'name': 'Greatsword', 'atk': 15, 'type': 'melee', 'val': 80, 'col': (194, 178, 128)},
    {'name': 'Longbow', 'atk': 11, 'type': 'ranged', 'val': 50, 'col': (205, 133, 63)},
    {'name': 'Lightning Bolt Staff', 'atk': 14, 'type': 'magic', 'val': 90, 'col': (255, 215, 0)},
    {'name': 'Shortsword', 'atk': 7, 'type': 'melee', 'val': 35, 'col': (220, 20, 60)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helm', 'Leather Chestplate', 'Leather Greaves'], 'def': 5, 'val': 40},
    {'name': 'Chainmail Armor', 'parts': ['Chainmail Helm', 'Chainmail Chestplate', 'Chainmail Greaves'], 'def': 10, 'val': 80},
    {'name': 'Plate Armor', 'parts': ['Plate Helm', 'Plate Chestplate', 'Plate Greaves'], 'def': 15, 'val': 120}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A fiery projectile that burns enemies.'},
    {'name': 'Heal', 'mp': 30, 'dmg': -10, 'col': (0, 255, 0), 'desc': 'Restores health to an ally.'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (255, 215, 0), 'desc': 'A bolt of lightning that shocks enemies.'},
    {'name': 'Shield', 'mp': 15, 'dmg': -5, 'col': (173, 216, 230), 'desc': 'Increases defense for a short time.'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 12, 'col': (0, 255, 255), 'desc': 'Fires shards of ice at enemies.'},
    {'name': 'Fire Shield', 'mp': 35, 'dmg': -15, 'col': (255, 69, 0), 'desc': 'Creates a shield that burns attackers.'},
    {'name': 'Thunderclap', 'mp': 40, 'dmg': 25, 'col': (255, 215, 0), 'desc': 'A powerful clap of thunder that stuns enemies.'},
    {'name': 'Regenerate', 'mp': 30, 'dmg': -20, 'col': (0, 255, 0), 'desc': 'Rapidly restores health to an ally.'},
    {'name': 'Frost Nova', 'mp': 45, 'dmg': 18, 'col': (0, 255, 255), 'desc': 'Freezes enemies in a nova of frost.'},
    {'name': 'Magnetize', 'mp': 20, 'dmg': -10, 'col': (173, 216, 230), 'desc': 'Pulls nearby items to the caster.'}
]

MATERIALS = [
    'Iron Ore',
    'Wood',
    'Mana Crystal',
    'Leather',
    'Chainmail',
    'Steel Plate',
    'Herbs',
    'Gems',
    'Cloth',
    'Feathers'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Defeat 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 25},
    {'id': 2, 'name': 'Collect Herbs', 'desc': 'Gather 10 herbs from the forest.', 'target': 'mat:Herbs', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 15},
    {'id': 3, 'name': 'Bandit Ambush', 'desc': 'Defeat the bandits at the ambush point.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 70, 'reward_xp': 40},
    {'id': 4, 'name': 'Craft Armor', 'desc': 'Create a set of leather armor.', 'target': 'mat:Leather', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 35},
    {'id': 5, 'name': 'Deliver Goods', 'desc': 'Deliver the goods to the merchant.', 'target': 'Merchant', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 40, 'reward_xp': 20}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom'},
    'bandit': {'rep': 0, 'name': 'Bandits'},
    'goblin': {'rep': 0, 'name': 'Goblins'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Hello, traveler! What can I offer you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings! Are you here to report something?', 'opts': ['Report', 'Talk', 'Leave']}],
    'Blacksmith': [{'text': 'Welcome! Need a weapon or armor fixed?', 'opts': ['Repair', 'Craft', 'Leave']}],
    'Farmer': [{'text': 'Good day! How can I assist you?', 'opts': ['Buy Produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hello there!', 'opts': ['Talk', 'Leave']}]
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
    'Natalie',
    'Oscar',
    'Piper'
]
