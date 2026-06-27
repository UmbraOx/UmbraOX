# MyGame Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel Ingot': 4, 'Leather': 2}, 'out': {'Steel Shield': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron Ingot': 2}, 'out': {'Horse Shoe': 4}},
        {'name': 'Axe', 'cost': {'Iron Ingot': 3, 'Wood': 2}, 'out': {'Axe': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water Bottle': 1}, 'out': {'Health Potion': 5}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 4}},
        {'name': 'Poison', 'cost': {'Venom Sac': 1, 'Herb': 2}, 'out': {'Poison': 3}},
        {'name': 'Invisibility Potion', 'cost': {'Mushroom': 5, 'Water Bottle': 1}, 'out': {'Invisibility Potion': 2}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 10, 'Stone': 5}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 8, 'Iron Ingot': 3}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel Ingot': 6, 'Stone': 7}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 5, 'Iron Ingot': 2}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (204, 153, 255), 'w': 3, 'h': 3, 'cost': {'Wood': 10, 'Stone': 5}},
    'Shop': {'col': (255, 204, 153), 'w': 4, 'h': 4, 'cost': {'Wood': 8, 'Iron Ingot': 3}},
    'Barracks': {'col': (153, 204, 255), 'w': 6, 'h': 6, 'cost': {'Steel Ingot': 6, 'Stone': 7}},
    'Farm': {'col': (153, 255, 153), 'w': 5, 'h': 5, 'cost': {'Wood': 5, 'Iron Ingot': 2}},
    'Tower': {'col': (204, 153, 153), 'w': 7, 'h': 7, 'cost': {'Steel Ingot': 8, 'Stone': 10}},
    'Warehouse': {'col': (255, 255, 153), 'w': 6, 'h': 4, 'cost': {'Wood': 12, 'Iron Ingot': 5}}
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