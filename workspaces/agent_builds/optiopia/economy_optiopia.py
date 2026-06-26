# Optiopia Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 2, 'Stone': 1}, 'out': {'Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel Ingot': 3, 'Leather': 1}, 'out': {'Shield': 1}},
        {'name': 'Iron Helmet', 'cost': {'Iron Ingot': 2}, 'out': {'Helmet': 1}},
        {'name': 'Chain Mail', 'cost': {'Iron Ingot': 5}, 'out': {'Armor': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water Bottle': 1}, 'out': {'Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Potion': 1}},
        {'name': 'Poison', 'cost': {'Venom Sac': 1, 'Herb': 1}, 'out': {'Poison': 1}},
        {'name': 'Elixir of Strength', 'cost': {'Giant Root': 2, 'Crystal Dust': 1}, 'out': {'Elixir': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 30}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron Ingot': 20}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel Ingot': 50, 'Stone': 40}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 30, 'Soil': 20}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 204, 153), 'w': 3, 'h': 3, 'cost': {'Wood': 50, 'Stone': 30}},
    'Shop': {'col': (255, 255, 153), 'w': 4, 'h': 3, 'cost': {'Wood': 40, 'Iron Ingot': 20}},
    'Barracks': {'col': (204, 153, 153), 'w': 5, 'h': 4, 'cost': {'Steel Ingot': 50, 'Stone': 40}},
    'Farm': {'col': (153, 255, 153), 'w': 4, 'h': 4, 'cost': {'Wood': 30, 'Soil': 20}},
    'Tower': {'col': (153, 153, 255), 'w': 6, 'h': 5, 'cost': {'Steel Ingot': 70, 'Stone': 60}},
    'Warehouse': {'col': (255, 153, 255), 'w': 5, 'h': 5, 'cost': {'Wood': 40, 'Iron Ingot': 30}}
}

def buy_item(player, npc, item_name):
    if npc.inventory.get(item_name, 0) > 0 and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Item bought successfully'
    return False, 'Not enough gold or item not available'

def sell_item(player, npc, item_name):
    if player.inventory.get(item_name, 0) > 0:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Item sold successfully'
    return False, 'Item not in inventory'

def craft_item(player, recipe):
    if all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items()):
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Item crafted successfully'
    return False, 'Not enough materials'