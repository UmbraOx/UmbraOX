# MyGame Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'Feather': 4}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow', 'cost': {'Wood': 5, 'Metal': 3, 'String': 2}, 'out': {'Crossbow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Sword', 'cost': {'Iron': 4, 'Steel': 2}, 'out': {'Sword': 1}},
        {'name': 'Armor', 'cost': {'Steel': 5, 'Leather': 3}, 'out': {'Armor': 1}},
        {'name': 'Shield', 'cost': {'Wood': 3, 'Iron': 2}, 'out': {'Shield': 1}},
        {'name': 'Axe', 'cost': {'Iron': 4, 'Stone': 2}, 'out': {'Axe': 1}}
    ],
    'Alchemy': [
        {'name': 'Potion of Healing', 'cost': {'Herb': 3, 'Water': 1}, 'out': {'Potion of Healing': 1}},
        {'name': 'Fire Potion', 'cost': {'Sulfur': 2, 'Oil': 1}, 'out': {'Fire Potion': 1}},
        {'name': 'Invisibility Potion', 'cost': {'Mushroom': 4, 'Dust': 2}, 'out': {'Invisibility Potion': 1}},
        {'name': 'Strength Potion', 'cost': {'Beast Meat': 3, 'Herb': 2}, 'out': {'Strength Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 10, 'Stone': 5}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 8, 'Iron': 4}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel': 6, 'Leather': 3}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 5, 'Stone': 2}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (204, 153, 255), 'w': 3, 'h': 3, 'cost': {'Wood': 10, 'Stone': 5}},
    'Shop': {'col': (255, 204, 153), 'w': 4, 'h': 4, 'cost': {'Wood': 8, 'Iron': 4}},
    'Barracks': {'col': (153, 204, 255), 'w': 5, 'h': 5, 'cost': {'Steel': 6, 'Leather': 3}},
    'Farm': {'col': (153, 255, 153), 'w': 4, 'h': 4, 'cost': {'Wood': 5, 'Stone': 2}},
    'Tower': {'col': (204, 153, 153), 'w': 6, 'h': 6, 'cost': {'Steel': 8, 'Stone': 10}},
    'Warehouse': {'col': (255, 255, 153), 'w': 7, 'h': 7, 'cost': {'Wood': 15, 'Iron': 6}}
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