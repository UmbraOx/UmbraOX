# Game Data Constants

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (204, 153, 102)},
    {'name': 'Steel Axe', 'atk': 15, 'type': 'melee', 'val': 75, 'col': (192, 192, 192)},
    {'name': 'Shadow Dagger', 'atk': 8, 'type': 'melee', 'val': 60, 'col': (139, 0, 139)},
    {'name': 'Oak Bow', 'atk': 7, 'type': 'ranged', 'val': 45, 'col': (139, 69, 19)},
    {'name': 'Flame Staff', 'atk': 12, 'type': 'magic', 'val': 80, 'col': (255, 69, 0)},
    {'name': 'Frost Wand', 'atk': 10, 'type': 'magic', 'val': 70, 'col': (0, 255, 255)},
    {'name': 'Battle Hammer', 'atk': 18, 'type': 'melee', 'val': 90, 'col': (165, 42, 42)},
    {'name': 'Silver Spear', 'atk': 13, 'type': 'melee', 'val': 75, 'col': (192, 192, 192)},
    {'name': 'Throwing Stars', 'atk': 6, 'type': 'ranged', 'val': 40, 'col': (255, 215, 0)},
    {'name': 'Death Scythe', 'atk': 20, 'type': 'melee', 'val': 100, 'col': (139, 0, 0)}
]

ARMOR_SETS = [
    {'name': 'Iron Set', 'parts': ['Iron Helmet', 'Iron Chestplate', 'Iron Greaves'], 'def': 8, 'val': 120},
    {'name': 'Steel Set', 'parts': ['Steel Helmet', 'Steel Chestplate', 'Steel Greaves'], 'def': 12, 'val': 150},
    {'name': 'Shadow Set', 'parts': ['Shadow Hood', 'Shadow Cloak', 'Shadow Boots'], 'def': 10, 'val': 130}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'Unleash a fiery ball of energy at your enemies.'},
    {'name': 'Ice Spike', 'mp': 18, 'dmg': 14, 'col': (0, 255, 255), 'desc': 'Summon an icy spike to impale your foes.'},
    {'name': 'Lightning Bolt', 'mp': 22, 'dmg': 16, 'col': (255, 255, 0), 'desc': 'Strike with a bolt of lightning from the heavens.'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (0, 255, 0), 'desc': 'Restore health to yourself or an ally.'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (169, 169, 169), 'desc': 'Create a protective shield around yourself.'},
    {'name': 'Teleport', 'mp': 30, 'dmg': 0, 'col': (255, 255, 255), 'desc': 'Instantly move to another location on the map.'},
    {'name': 'Summon Wolf', 'mp': 25, 'dmg': 0, 'col': (139, 69, 19), 'desc': 'Call forth a loyal wolf companion to fight by your side.'},
    {'name': 'Earthquake', 'mp': 40, 'dmg': 20, 'col': (139, 75, 55), 'desc': 'Cause the ground to shake and crush your enemies.'},
    {'name': 'Drain Life', 'mp': 20, 'dmg': 12, 'col': (139, 0, 0), 'desc': 'Steal life force from an enemy to heal yourself.'},
    {'name': 'Time Slow', 'mp': 50, 'dmg': 0, 'col': (75, 0, 130), 'desc': 'Slow down time, giving you more control in battle.'}
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
    'Healing Herb',
    'Mana Stone'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 50},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 pieces of iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 30},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 8, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 75},
    {'id': 4, 'name': 'Summon a Wolf', 'desc': 'Find the ancient wolf den and summon a loyal companion.', 'target': 'mat:Wolf Fang', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 125, 'reward_xp': 60},
    {'id': 5, 'name': 'Heal the Elder', 'desc': 'Find the village elder and heal him with healing herbs.', 'target': 'mat:Healing Herb', 'need': 4, 'prog': 0, 'done': False, 'reward_gold': 60, 'reward_xp': 45}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop! What can I get for you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. Are you here on business or pleasure?', 'opts': ['Business', 'Pleasure', 'Leave']}],
    'Blacksmith': [{'text': 'Need a weapon or armor? I can forge it for you.', 'opts': ['Forge Weapon', 'Forge Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How are the crops doing today?', 'opts': ['Talk About Crops', 'Buy Produce', 'Leave']}],
    'default': [{'text': 'Greetings, stranger. What brings you here?', 'opts': ['Chat', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brianna',
    'Cedric',
    'Daria',
    'Eldrin',
    'Fiona',
    'Garnett',
    'Hannah',
    'Igor',
    'Jasmine',
    'Kael',
    'Lila',
    'Morgan',
    'Natalie',
    'Oscar',
    'Penelope'
]


if __name__ == '__main__':
    main()
