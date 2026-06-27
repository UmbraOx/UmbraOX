# Game Data Constants for MyGame

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 190, 140)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 30, 'col': (160, 120, 40)},
    {'name': 'Fire Staff', 'atk': 12, 'type': 'magic', 'val': 75, 'col': (255, 69, 0)},
    {'name': 'Dagger', 'atk': 5, 'type': 'melee', 'val': 20, 'col': (184, 134, 11)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 60, 'col': (139, 69, 19)},
    {'name': 'Ice Wand', 'atk': 15, 'type': 'magic', 'val': 80, 'col': (0, 255, 255)},
    {'name': 'Great Axe', 'atk': 18, 'type': 'melee', 'val': 90, 'col': (139, 69, 19)},
    {'name': 'Longbow', 'atk': 14, 'type': 'ranged', 'val': 70, 'col': (255, 215, 0)},
    {'name': 'Thunder Rod', 'atk': 20, 'type': 'magic', 'val': 100, 'col': (255, 69, 0)},
    {'name': 'Short Sword', 'atk': 7, 'type': 'melee', 'val': 35, 'col': (200, 190, 140)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helmet', 'Leather Chestplate', 'Leather Leggings'], 'def': 8, 'val': 50},
    {'name': 'Iron Armor', 'parts': ['Iron Helm', 'Iron Breastplate', 'Iron Greaves'], 'def': 12, 'val': 100},
    {'name': 'Dragon Scale Mail', 'parts': ['Dragon Scale Helmet', 'Dragon Scale Chestplate', 'Dragon Scale Leggings'], 'def': 20, 'val': 300}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 15, 'dmg': 25, 'col': (255, 69, 0), 'desc': 'A basic fire spell that burns enemies.'},
    {'name': 'Heal', 'mp': 20, 'dmg': -30, 'col': (0, 255, 0), 'desc': 'Restores health to the caster or an ally.'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 35, 'col': (255, 215, 0), 'desc': 'A powerful electric shock that stuns enemies.'},
    {'name': 'Ice Shard', 'mp': 10, 'dmg': 15, 'col': (0, 255, 255), 'desc': 'Fires a shard of ice to freeze and damage foes.'},
    {'name': 'Shield', 'mp': 15, 'dmg': -10, 'col': (173, 216, 230), 'desc': 'Creates a shield that absorbs damage for the caster.'},
    {'name': 'Meteor Shower', 'mp': 40, 'dmg': 50, 'col': (255, 99, 71), 'desc': 'Summons meteors to rain down on enemies.'},
    {'name': 'Thunder Wave', 'mp': 30, 'dmg': 40, 'col': (255, 69, 0), 'desc': 'Unleashes a wave of electricity that damages all nearby foes.'},
    {'name': 'Earthquake', 'mp': 35, 'dmg': 45, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake and damage enemies.'},
    {'name': 'Blizzard', 'mp': 20, 'dmg': 20, 'col': (0, 255, 255), 'desc': 'Freezes enemies in place and deals cold damage over time.'},
    {'name': 'Holy Light', 'mp': 30, 'dmg': -40, 'col': (255, 255, 0), 'desc': 'Emits a radiant light that heals allies and damages undead enemies.'}
]

MATERIALS = [
    'Iron Ore',
    'Leather Hide',
    'Dragon Scale',
    'Magic Crystal',
    'Wood Logs',
    'Coal',
    'Silk Cloth',
    'Steel Ingot',
    'Mana Stone',
    'Elixir'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 10 goblins in the forest.', 'target': 'goblin', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 5 pieces of iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 10},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 30},
    {'id': 4, 'name': 'Dragon Scale Quest', 'desc': 'Retrieve a dragon scale from the dragon lair.', 'target': 'mat:Dragon Scale', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 200, 'reward_xp': 50},
    {'id': 5, 'name': 'Silk Harvest', 'desc': 'Harvest 3 pieces of silk cloth from the spider caves.', 'target': 'mat:Silk Cloth', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 40, 'reward_xp': 15}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Gang'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop! What can I get you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. Are you here for training or just passing through?', 'opts': ['Train', 'Pass Through', 'Talk More']}],
    'Blacksmith': [{'text': 'Need a weapon or armor? I can help.', 'opts': ['Forge Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How are you today?', 'opts': ['Buy Produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hi there!', 'opts': ['Talk', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caelan',
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
