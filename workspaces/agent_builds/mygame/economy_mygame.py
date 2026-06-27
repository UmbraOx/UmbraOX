# MyGame Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Stick': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Stick': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 2, 'Stick': 1}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel Ingot': 3, 'Leather': 1}, 'out': {'Steel Shield': 1}},
        {'name': 'Armor Plate', 'cost': {'Steel Ingot': 5}, 'out': {'Armor Plate': 1}},
        {'name': 'Iron Pickaxe', 'cost': {'Iron Ingot': 2, 'Stick': 1}, 'out': {'Iron Pickaxe': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water Bottle': 1}, 'out': {'Health Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 1}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 3, 'Paper': 1}, 'out': {'Fire Scroll': 1}},
        {'name': 'Invisibility Potion', 'cost': {'Mushroom': 2, 'Water Bottle': 1}, 'out': {'Invisibility Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 30}},
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron Ingot': 20}},
        {'name': 'Barracks', 'cost': {'Steel Ingot': 50, 'Leather': 20}},
        {'name': 'Farm', 'cost': {'Wood': 30, 'Stone': 10}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (204, 153, 255), 'w': 6, 'h': 6, 'cost': {'Wood': 50, 'Stone': 30}},
    'Shop': {'col': (255, 204, 153), 'w': 8, 'h': 6, 'cost': {'Wood': 40, 'Iron Ingot': 20}},
    'Barracks': {'col': (153, 204, 255), 'w': 10, 'h': 8, 'cost': {'Steel Ingot': 50, 'Leather': 20}},
    'Farm': {'col': (204, 255, 153), 'w': 6, 'h': 6, 'cost': {'Wood': 30, 'Stone': 10}},
    'Tower': {'col': (255, 153, 153), 'w': 8, 'h': 10, 'cost': {'Steel Ingot': 70, 'Stone': 40}},
    'Warehouse': {'col': (153, 255, 204), 'w': 10, 'h': 10, 'cost': {'Wood': 60, 'Iron Ingot': 30}}
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