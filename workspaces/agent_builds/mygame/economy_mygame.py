# MyGame Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5, 'Steel': 2}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel': 4, 'Leather': 3}, 'out': {'Steel Shield': 1}},
        {'name': 'Iron Helmet', 'cost': {'Iron Ingot': 3, 'Leather': 2}, 'out': {'Iron Helmet': 1}},
        {'name': 'Iron Armor', 'cost': {'Iron Ingot': 8, 'Leather': 5}, 'out': {'Iron Armor': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water Bottle': 1}, 'out': {'Health Potion': 2}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 2}},
        {'name': 'Poison Vial', 'cost': {'Venom Sac': 1, 'Glass Bottle': 1}, 'out': {'Poison Vial': 1}},
        {'name': 'Fire Oil', 'cost': {'Sulfur': 3, 'Oil': 2}, 'out': {'Fire Oil': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 20}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron Ingot': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Stone': 60, 'Iron Ingot': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 30, 'Soil': 40}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (128, 64, 0), 'w': 5, 'h': 5, 'cost': {'Wood': 50, 'Stone': 20}},
    'Shop': {'col': (255, 192, 0), 'w': 4, 'h': 3, 'cost': {'Wood': 40, 'Iron Ingot': 10}},
    'Barracks': {'col': (64, 64, 64), 'w': 6, 'h': 5, 'cost': {'Stone': 60, 'Iron Ingot': 20}},
    'Farm': {'col': (34, 177, 76), 'w': 5, 'h': 4, 'cost': {'Wood': 30, 'Soil': 40}},
    'Tower': {'col': (192, 192, 192), 'w': 8, 'h': 7, 'cost': {'Stone': 100, 'Iron Ingot': 50}},
    'Warehouse': {'col': (64, 32, 0), 'w': 6, 'h': 6, 'cost': {'Wood': 80, 'Stone': 30}}
}

def buy_item(player, npc, item_name):
    if npc.inventory.get(item_name, 0) > 0 and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Item bought successfully'
    else:
        return False, 'Not enough gold or item not available'

def sell_item(player, npc, item_name):
    if player.inventory.get(item_name, 0) > 0 and npc.gold >= npc.prices[item_name]:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Item sold successfully'
    else:
        return False, 'Not enough gold or item not available'

def craft_item(player, recipe):
    if all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items()):
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Item crafted successfully'
    else:
        return False, 'Not enough materials'