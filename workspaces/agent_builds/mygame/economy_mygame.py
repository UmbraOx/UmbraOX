# MyGame Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Feather': 1}, 'out': {'Bolt': 10}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5}, 'out': {'Sword': 1}},
        {'name': 'Steel Armor', 'cost': {'Steel Ingot': 8, 'Leather': 2}, 'out': {'Armor': 1}},
        {'name': 'Iron Shield', 'cost': {'Iron Ingot': 6}, 'out': {'Shield': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron Ingot': 3}, 'out': {'Shoe': 4}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 2, 'Water Bottle': 1}, 'out': {'Potion': 5}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 3, 'Water Bottle': 1}, 'out': {'Potion': 4}},
        {'name': 'Poison', 'cost': {'Venom Sac': 2, 'Herb': 1}, 'out': {'Poison': 5}},
        {'name': 'Elixir of Life', 'cost': {'Phoenix Feather': 1, 'Crystal Dust': 5}, 'out': {'Elixir': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 20, 'Stone': 10}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 30, 'Iron Ingot': 5}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Stone': 40, 'Steel Ingot': 8}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 25, 'Iron Ingot': 3}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (204, 153, 255), 'w': 5, 'h': 5, 'cost': {'Wood': 20, 'Stone': 10}},
    'Shop': {'col': (255, 204, 153), 'w': 6, 'h': 6, 'cost': {'Wood': 30, 'Iron Ingot': 5}},
    'Barracks': {'col': (153, 204, 255), 'w': 8, 'h': 8, 'cost': {'Stone': 40, 'Steel Ingot': 8}},
    'Farm': {'col': (153, 255, 153), 'w': 7, 'h': 7, 'cost': {'Wood': 25, 'Iron Ingot': 3}},
    'Tower': {'col': (204, 153, 153), 'w': 9, 'h': 9, 'cost': {'Stone': 60, 'Steel Ingot': 10}},
    'Warehouse': {'col': (255, 255, 153), 'w': 7, 'h': 8, 'cost': {'Wood': 40, 'Iron Ingot': 10}}
}

def buy_item(player, npc, item_name):
    if npc.inventory.get(item_name, 0) > 0 and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Purchase successful'
    return False, 'Insufficient gold or item not available'

def sell_item(player, npc, item_name):
    if player.inventory.get(item_name, 0) > 0:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Sale successful'
    return False, 'Item not in inventory'

def craft_item(player, recipe):
    if all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items()):
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Crafting successful'
    return False, 'Insufficient materials'