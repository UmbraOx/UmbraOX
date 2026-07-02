# Economy and Crafting Module for Demiworld

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron': 1, 'Wood': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron': 5, 'Coal': 2}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Armor', 'cost': {'Steel': 8, 'Leather': 3}, 'out': {'Steel Armor': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron': 4, 'Nail': 5}, 'out': {'Horse Shoe': 2}},
        {'name': 'Shield', 'cost': {'Wood': 6, 'Leather': 3}, 'out': {'Shield': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 4, 'Water': 1}, 'out': {'Health Potion': 2}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 3, 'Water': 1}, 'out': {'Mana Potion': 2}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 5, 'Paper': 1}, 'out': {'Fire Scroll': 1}},
        {'name': 'Invisibility Potion', 'cost': {'Mushroom': 3, 'Crystal Dust': 4}, 'out': {'Invisibility Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 20, 'Stone': 15}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 30, 'Iron': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Stone': 40, 'Iron': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 25, 'Soil': 30}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (204, 153, 255), 'w': 5, 'h': 5, 'cost': {'Wood': 20, 'Stone': 15}},
    'Shop': {'col': (255, 204, 153), 'w': 6, 'h': 6, 'cost': {'Wood': 30, 'Iron': 10}},
    'Barracks': {'col': (153, 204, 255), 'w': 8, 'h': 8, 'cost': {'Stone': 40, 'Iron': 20}},
    'Farm': {'col': (153, 255, 153), 'w': 7, 'h': 7, 'cost': {'Wood': 25, 'Soil': 30}},
    'Tower': {'col': (255, 153, 153), 'w': 9, 'h': 9, 'cost': {'Stone': 60, 'Iron': 30}},
    'Warehouse': {'col': (204, 255, 204), 'w': 7, 'h': 8, 'cost': {'Wood': 40, 'Stone': 25}}
}

def buy_item(player, npc, item_name):
    if item_name in npc.inventory and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Item purchased'
    else:
        return False, 'Purchase failed'

def sell_item(player, npc, item_name):
    if item_name in player.inventory and player.inventory[item_name] > 0:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Item sold'
    else:
        return False, 'Sale failed'

def craft_item(player, recipe):
    if all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items()):
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Crafting successful'
    else:
        return False, 'Crafting failed'