# TestRPG Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron': 1, 'Wood': 1}, 'out': {'Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron': 5, 'Coal': 2}, 'out': {'Sword': 1}},
        {'name': 'Steel Armor', 'cost': {'Steel': 8, 'Leather': 3}, 'out': {'Armor': 1}},
        {'name': 'Axe', 'cost': {'Iron': 4, 'Wood': 2}, 'out': {'Axe': 1}},
        {'name': 'Shield', 'cost': {'Wood': 5, 'Leather': 3}, 'out': {'Shield': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 2, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal': 1, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Poison', 'cost': {'Venom': 2, 'Herb': 1}, 'out': {'Poison': 1}},
        {'name': 'Fire Potion', 'cost': {'Sulfur': 3, 'Water': 1}, 'out': {'Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 20, 'Stone': 15}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 30, 'Iron': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel': 25, 'Stone': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 15, 'Soil': 30}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 228, 196), 'w': 4, 'h': 4, 'cost': {'Wood': 20, 'Stone': 15}},
    'Shop': {'col': (238, 232, 170), 'w': 5, 'h': 5, 'cost': {'Wood': 30, 'Iron': 10}},
    'Barracks': {'col': (196, 228, 255), 'w': 6, 'h': 6, 'cost': {'Steel': 25, 'Stone': 20}},
    'Farm': {'col': (173, 255, 47), 'w': 5, 'h': 5, 'cost': {'Wood': 15, 'Soil': 30}},
    'Tower': {'col': (169, 169, 169), 'w': 8, 'h': 8, 'cost': {'Steel': 40, 'Stone': 30}},
    'Warehouse': {'col': (255, 228, 181), 'w': 7, 'h': 7, 'cost': {'Wood': 40, 'Iron': 20}}
}

def buy_item(player, npc, item_name):
    if item_name in npc.inventory and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Item bought successfully'
    else:
        return False, 'Not enough gold or item not available'

def sell_item(player, npc, item_name):
    if item_name in player.inventory and player.inventory[item_name] > 0:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Item sold successfully'
    else:
        return False, 'Item not in inventory'

def craft_item(player, recipe):
    if all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items()):
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Item crafted successfully'
    else:
        return False, 'Not enough materials'