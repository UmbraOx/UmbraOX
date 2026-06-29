# MyGame Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron': 1, 'Wood': 1}, 'out': {'Bolt': 10}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron': 5, 'Coal': 2}, 'out': {'Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel': 4, 'Leather': 1}, 'out': {'Shield': 1}},
        {'name': 'Iron Helmet', 'cost': {'Iron': 3, 'Coal': 1}, 'out': {'Helmet': 1}},
        {'name': 'Chain Mail', 'cost': {'Steel': 5, 'Leather': 2}, 'out': {'Armor': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal': 2, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 3, 'Paper': 1}, 'out': {'Scroll': 1}},
        {'name': 'Ice Scroll', 'cost': {'Snowflake': 2, 'Paper': 1}, 'out': {'Scroll': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 10, 'Stone': 5}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 8, 'Iron': 3}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel': 6, 'Leather': 4}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 5, 'Soil': 8}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (200, 190, 140), 'w': 3, 'h': 3, 'cost': {'Wood': 10, 'Stone': 5}},
    'Shop': {'col': (255, 215, 0), 'w': 4, 'h': 4, 'cost': {'Wood': 8, 'Iron': 3}},
    'Barracks': {'col': (165, 42, 42), 'w': 5, 'h': 5, 'cost': {'Steel': 6, 'Leather': 4}},
    'Farm': {'col': (0, 255, 0), 'w': 3, 'h': 3, 'cost': {'Wood': 5, 'Soil': 8}},
    'Tower': {'col': (192, 192, 192), 'w': 4, 'h': 6, 'cost': {'Steel': 10, 'Stone': 10}},
    'Warehouse': {'col': (139, 69, 19), 'w': 5, 'h': 5, 'cost': {'Wood': 12, 'Iron': 8}}
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