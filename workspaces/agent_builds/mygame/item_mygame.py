# Game Data Constants for MyGame

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 190, 140)},
    {'name': 'Steel Sword', 'atk': 15, 'type': 'melee', 'val': 75, 'col': (220, 220, 220)},
    {'name': 'Longbow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Composite Bow', 'atk': 12, 'type': 'ranged', 'val': 60, 'col': (165, 42, 42)},
    {'name': 'Magic Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (138, 43, 226)},
    {'name': 'Enchanted Staff', 'atk': 10, 'type': 'magic', 'val': 55, 'col': (75, 0, 130)},
    {'name': 'Dagger', 'atk': 4, 'type': 'melee', 'val': 20, 'col': (85, 65, 139)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 50, 'col': (165, 42, 42)},
    {'name': 'Wand', 'atk': 5, 'type': 'magic', 'val': 30, 'col': (138, 43, 226)},
    {'name': 'Greatsword', 'atk': 20, 'type': 'melee', 'val': 100, 'col': (255, 215, 0)}
]

ARMOR_SETS = [
    {'name': 'Warrior Armor', 'parts': ['Helmet', 'Chestplate', 'Greaves'], 'def': 15, 'val': 75},
    {'name': 'Archer Armor', 'parts': ['Light Helmet', 'Leather Chest', 'Leggings'], 'def': 8, 'val': 40},
    {'name': 'Mage Robe', 'parts': ['Cowl', 'Robe', 'Boots'], 'def': 5, 'val': 30}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 15, 'dmg': 20, 'col': (255, 69, 0), 'desc': 'A fiery orb that explodes on impact.'},
    {'name': 'Arrow Storm', 'mp': 10, 'dmg': 15, 'col': (139, 69, 19), 'desc': 'Rains a barrage of arrows down on enemies.'},
    {'name': 'Ice Shield', 'mp': 20, 'dmg': 0, 'col': (0, 191, 255), 'desc': 'Creates a shield that reflects damage.'},
    {'name': 'Lightning Bolt', 'mp': 18, 'dmg': 25, 'col': (255, 255, 0), 'desc': 'Strikes an enemy with lightning.'},
    {'name': 'Heal', 'mp': 12, 'dmg': -15, 'col': (34, 139, 34), 'desc': 'Restores health to a target.'},
    {'name': 'Mana Shield', 'mp': 25, 'dmg': 0, 'col': (75, 0, 130), 'desc': 'Absorbs magic damage for a short time.'},
    {'name': 'Fire Aura', 'mp': 20, 'dmg': 10, 'col': (255, 69, 0), 'desc': 'Deals fire damage over time to nearby enemies.'},
    {'name': 'Shadow Step', 'mp': 15, 'dmg': 0, 'col': (0, 0, 0), 'desc': 'Teleports a short distance away from danger.'},
    {'name': 'Frost Nova', 'mp': 25, 'dmg': 30, 'col': (0, 191, 255), 'desc': 'Freezes enemies in place and deals damage.'},
    {'name': 'Thunderclap', 'mp': 20, 'dmg': 20, 'col': (255, 255, 0), 'desc': 'Stuns enemies with a powerful clap of thunder.'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Wooden Plank',
    'Leather Hide',
    'Mana Crystal',
    'Enchanted Silk',
    'Dragon Scale',
    'Phoenix Feather',
    'Obsidian Shard',
    'Ethereal Dust'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 25},
    {'id': 2, 'name': 'Bandit Ambush', 'desc': 'Defeat the bandits at the bridge.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 40},
    {'id': 3, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 pieces of iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 25, 'reward_xp': 10},
    {'id': 4, 'name': 'Mage Request', 'desc': 'Find the lost mana crystal.', 'target': 'mat:Mana Crystal', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 5, 'name': 'Forest Guardian', 'desc': 'Defeat the forest guardian to clear the path.', 'target': 'forest guardian', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 50}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop! What can I get for you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. Are you here on business or just passing through?', 'opts': ['Business', 'Passing Through', 'Leave']}],
    'Blacksmith': [{'text': 'Need a weapon or armor? I can help with that.', 'opts': ['Forge Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How are you today?', 'opts': ['Good', 'Not Good', 'Leave']}],
    'default': [{'text': 'I do not understand your request. Can you please clarify?', 'opts': ['Yes', 'No']}]
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
