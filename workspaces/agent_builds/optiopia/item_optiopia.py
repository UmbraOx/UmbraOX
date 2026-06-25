# Game Data Constants for Optiopia

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
    {'name': 'Death Scythe', 'atk': 20, 'type': 'melee', 'val': 100, 'col': (69, 69, 69)}
]

ARMOR_SETS = [
    {'name': 'Iron Set', 'parts': ['Iron Helmet', 'Iron Chestplate', 'Iron Greaves'], 'def': 8, 'val': 200},
    {'name': 'Steel Set', 'parts': ['Steel Helmet', 'Steel Chestplate', 'Steel Greaves'], 'def': 12, 'val': 300},
    {'name': 'Shadow Set', 'parts': ['Shadow Hood', 'Shadow Robe', 'Shadow Boots'], 'def': 10, 'val': 250}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'Unleash a fiery ball of energy at your enemies.'},
    {'name': 'Ice Spike', 'mp': 18, 'dmg': 14, 'col': (0, 255, 255), 'desc': 'Create an icy spike to impale your foes.'},
    {'name': 'Lightning Bolt', 'mp': 22, 'dmg': 16, 'col': (255, 255, 0), 'desc': 'Strike with a bolt of lightning from the sky.'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (0, 255, 0), 'desc': 'Restore health to yourself or an ally.'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (169, 169, 169), 'desc': 'Create a protective shield around yourself.'},
    {'name': 'Teleport', 'mp': 30, 'dmg': 0, 'col': (255, 255, 255), 'desc': 'Instantly move to another location on the map.'},
    {'name': 'Summon Wolf', 'mp': 25, 'dmg': 0, 'col': (139, 69, 19), 'desc': 'Call forth a loyal wolf companion to fight by your side.'},
    {'name': 'Earthquake', 'mp': 40, 'dmg': 20, 'col': (139, 75, 55), 'desc': 'Cause the ground to shake and crush your enemies.'},
    {'name': 'Drain Life', 'mp': 20, 'dmg': 12, 'col': (139, 0, 139), 'desc': 'Steal life force from an enemy to heal yourself.'},
    {'name': 'Time Slow', 'mp': 50, 'dmg': 0, 'col': (148, 0, 211), 'desc': 'Slow down time for a short duration, giving you the upper hand in battle.'}
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
    'Earth Stone',
    'Life Dew'
]

QUESTS = [
    {'id': 1, 'name': 'Goblin Hunt', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 75, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 pieces of iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 15},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 25},
    {'id': 4, 'name': 'Shadow Crystal Quest', 'desc': 'Find a rare shadow crystal in the dark forest.', 'target': 'mat:Shadow Crystal', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 150, 'reward_xp': 30},
    {'id': 5, 'name': 'Summon Wolf Companion', 'desc': 'Find a wolf fang and summon your first loyal companion.', 'target': 'mat:Wolf Fang', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 200, 'reward_xp': 40}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop! What can I get you?', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings traveler. Are you here for training or just passing through?', 'opts': ['Train', 'Pass Through', 'Talk More']}],
    'Blacksmith': [{'text': 'Need a weapon or armor? I can forge it.', 'opts': ['Forge Weapon', 'Forge Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How are you today?', 'opts': ['Buy Produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hi there. Not much to do here.', 'opts': ['Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caela',
    'Darius',
    'Elena',
    'Finn',
    'Gwen',
    'Harken',
    'Iris',
    'Jasper',
    'Kara',
    'Liam',
    'Mira',
    'Nathaniel',
    'Olivia',
    'Paxton'
]


if __name__ == '__main__':
    main()
