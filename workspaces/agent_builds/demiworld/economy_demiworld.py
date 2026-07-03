# Economy and Crafting Module for DemiWorld

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5, 'Steel': 2}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel': 4, 'Leather': 2}, 'out': {'Steel Shield': 1}},
        {'name': 'Armor Plate', 'cost': {'Steel': 6, 'Iron Ingot': 3}, 'out': {'Armor Plate': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron Ingot': 2, 'Steel': 1}, 'out': {'Horse Shoe': 4}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water Bottle': 1}, 'out': {'Health Potion': 5}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 5}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 3, 'Paper': 1}, 'out': {'Fire Scroll': 3}},
        {'name': 'Ice Scroll', 'cost': {'Snowflake Crystal': 2, 'Paper': 1}, 'out': {'Ice Scroll': 3}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 20}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron Ingot': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Stone': 60, 'Steel': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 30, 'Soil': 40}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 228, 196), 'w': 5, 'h': 5, 'cost': {'Wood': 50, 'Stone': 20}},
    'Shop': {'col': (240, 230, 140), 'w': 6, 'h': 4, 'cost': {'Wood': 40, 'Iron Ingot': 10}},
    'Barracks': {'col': (192, 192, 192), 'w': 7, 'h': 5, 'cost': {'Stone': 60, 'Steel': 20}},
    'Farm': {'col': (144, 238, 144), 'w': 6, 'h': 6, 'cost': {'Wood': 30, 'Soil': 40}},
    'Tower': {'col': (173, 216, 230), 'w': 5, 'h': 8, 'cost': {'Stone': 80, 'Steel': 30}},
    'Warehouse': {'col': (255, 248, 220), 'w': 7, 'h': 6, 'cost': {'Wood': 60, 'Iron Ingot': 15}}
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