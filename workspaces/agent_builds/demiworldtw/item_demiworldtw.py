# Game Data Tables Module

WEAPONS = [
    {"name": "Iron Sword", "atk": 10, "type": "Sword", "val": 50, "mat": "Iron", "qty": 1},
    {"name": "Steel Axe", "atk": 12, "type": "Axe", "val": 75, "mat": "Steel", "qty": 1},
    {"name": "Shadow Dagger", "atk": 8, "type": "Dagger", "val": 60, "mat": "Shadow", "qty": 1},
    {"name": "Oak Bow", "atk": 7, "type": "Bow", "val": 45, "mat": "Oak", "qty": 1},
    {"name": "Flame Staff", "atk": 9, "type": "Staff", "val": 80, "mat": "Flame", "qty": 1},
    {"name": "Frost Wand", "atk": 6, "type": "Wand", "val": 70, "mat": "Frost", "qty": 1},
    {"name": "Battle Hammer", "atk": 15, "type": "Hammer", "val": 90, "mat": "Iron", "qty": 1},
    {"name": "Silver Spear", "atk": 11, "type": "Spear", "val": 85, "mat": "Silver", "qty": 1},
    {"name": "Throwing Stars", "atk": 4, "type": "Stars", "val": 30, "mat": "Steel", "qty": 5},
    {"name": "Death Scythe", "atk": 20, "type": "Scythe", "val": 150, "mat": "Shadow", "qty": 1}
]

ARMOR_SETS = [
    {"set_name": "Iron Set", "parts": ["Helmet", "Chestplate", "Gauntlets", "Greaves"], "def": 20, "val": 150, "mat": "Iron"},
    {"set_name": "Steel Set", "parts": ["Helmet", "Chestplate", "Gauntlets", "Greaves"], "def": 25, "val": 200, "mat": "Steel"},
    {"set_name": "Shadow Set", "parts": ["Helmet", "Chestplate", "Gauntlets", "Greaves"], "def": 30, "val": 250, "mat": "Shadow"}
]

SPELLS = [
    {"name": "Fireball", "mp": 15, "dmg": 20, "col": (255, 69, 0), "desc": "A fiery projectile that burns enemies."},
    {"name": "Ice Spike", "mp": 10, "dmg": 18, "col": (70, 130, 180), "desc": "Launches a spike of ice to freeze foes."},
    {"name": "Lightning Bolt", "mp": 20, "dmg": 25, "col": (255, 255, 0), "desc": "Unleashes a bolt of lightning on the target."},
    {"name": "Heal", "mp": 15, "dmg": -15, "col": (0, 255, 0), "desc": "Restores health to an ally or yourself."},
    {"name": "Shield", "mp": 10, "dmg": 0, "col": (169, 169, 169), "desc": "Creates a shield that absorbs damage for you."},
    {"name": "Teleport", "mp": 30, "dmg": 0, "col": (255, 255, 255), "desc": "Instantly teleports you to a marked location."},
    {"name": "Summon Wolf", "mp": 25, "dmg": 10, "col": (139, 69, 19), "desc": "Summons a wolf to fight by your side."},
    {"name": "Earthquake", "mp": 40, "dmg": 30, "col": (139, 75, 55), "desc": "Causes the ground to shake and damage enemies in an area."},
    {"name": "Drain Life", "mp": 20, "dmg": 15, "col": (148, 0, 211), "desc": "Drains life from an enemy to heal yourself."},
    {"name": "Time Slow", "mp": 35, "dmg": 0, "col": (255, 165, 0), "desc": "Slows down time for a short duration."}
]

MATERIALS = [
    {"mat_name": "Iron", "val": 10},
    {"mat_name": "Steel", "val": 15},
    {"mat_name": "Shadow", "val": 20},
    {"mat_name": "Oak", "val": 8},
    {"mat_name": "Flame", "val": 18},
    {"mat_name": "Frost", "val": 16},
    {"mat_name": "Silver", "val": 25}
]

QUESTS = [
    {"id": 1, "name": "Clear the Bandits", "desc": "Eliminate the bandits in the forest east of town.", "target": "Bandit", "need": 5, "reward_gold": 75, "reward_xp": 50},
    {"id": 2, "name": "Find the Lost Child", "desc": "Locate and rescue the lost child near the river.", "target": "Child", "need": 1, "reward_gold": 100, "reward_xp": 75},
    {"id": 3, "name": "Gather Herbs", "desc": "Collect 10 herbs from the nearby forest for the healer.", "target": "Herb", "need": 10, "reward_gold": 50, "reward_xp": 25},
    {"id": 4, "name": "Defend the Village", "desc": "Protect the village from an incoming goblin attack.", "target": "Goblin", "need": 8, "reward_gold": 120, "reward_xp": 100},
    {"id": 5, "name": "Retrieve Stolen Goods", "desc": "Recover stolen goods from the thieves' hideout in the mountains.", "target": "Thief", "need": 3, "reward_gold": 200, "reward_xp": 150}
]

FACTIONS = {
    "Villagers": {"alignment": "Neutral", "reputation": 50},
    "Bandits": {"alignment": "Hostile", "reputation": -20},
    "Thieves": {"alignment": "Hostile", "reputation": -30},
    "Goblins": {"alignment": "Hostile", "reputation": -40}
}


if __name__ == '__main__':
    main()
