# QuickTest2 Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron': 1, 'Wood': 1}, 'out': {'Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron': 5, 'Coal': 2}, 'out': {'Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel': 4, 'Leather': 3}, 'out': {'Shield': 1}},
        {'name': 'Chain Mail', 'cost': {'Iron': 8, 'Coal': 2}, 'out': {'Armor': 1}},
        {'name': 'Axe', 'cost': {'Steel': 6, 'Wood': 2}, 'out': {'Axe': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal': 2, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 3, 'Paper': 1}, 'out': {'Scroll': 1}},
        {'name': 'Ice Scroll', 'cost': {'Snowflake': 4, 'Paper': 1}, 'out': {'Scroll': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 20, 'Stone': 15}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 30, 'Iron': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel': 25, 'Leather': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 40, 'Soil': 30}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 204, 153), 'w': 64, 'h': 64, 'cost': {'Wood': 20, 'Stone': 15}},
    'Shop': {'col': (255, 255, 153), 'w': 96, 'h': 64, 'cost': {'Wood': 30, 'Iron': 10}},
    'Barracks': {'col': (204, 153, 153), 'w': 128, 'h': 64, 'cost': {'Steel': 25, 'Leather': 20}},
    'Farm': {'col': (153, 255, 153), 'w': 96, 'h': 96, 'cost': {'Wood': 40, 'Soil': 30}},
    'Tower': {'col': (153, 153, 255), 'w': 80, 'h': 128, 'cost': {'Steel': 30, 'Stone': 25}},
    'Warehouse': {'col': (255, 153, 255), 'w': 144, 'h': 96, 'cost': {'Wood': 50, 'Iron': 20}}
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