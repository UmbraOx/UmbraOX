# Economy and Crafting Module for DemiWorld2

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 3, 'String': 2}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron': 1, 'Wood': 1}, 'out': {'Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron': 5, 'Coal': 2}, 'out': {'Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel': 4, 'Leather': 3}, 'out': {'Shield': 1}},
        {'name': 'Chainmail Armor', 'cost': {'Iron': 8, 'Leather': 5}, 'out': {'Armor': 1}},
        {'name': 'Warhammer', 'cost': {'Steel': 6, 'Wood': 2}, 'out': {'Hammer': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal': 2, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Poison', 'cost': {'Venom': 3, 'Herb': 1}, 'out': {'Poison': 1}},
        {'name': 'Invisibility Potion', 'cost': {'Dust': 4, 'Water': 2}, 'out': {'Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 30}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron': 20}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel': 50, 'Stone': 40}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 30, 'Soil': 20}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 204, 153), 'w': 10, 'h': 10, 'cost': {'Wood': 50, 'Stone': 30}},
    'Shop': {'col': (255, 255, 153), 'w': 8, 'h': 6, 'cost': {'Wood': 40, 'Iron': 20}},
    'Barracks': {'col': (204, 153, 153), 'w': 12, 'h': 12, 'cost': {'Steel': 50, 'Stone': 40}},
    'Farm': {'col': (153, 255, 153), 'w': 10, 'h': 8, 'cost': {'Wood': 30, 'Soil': 20}},
    'Tower': {'col': (153, 153, 255), 'w': 6, 'h': 14, 'cost': {'Steel': 70, 'Stone': 50}},
    'Warehouse': {'col': (255, 153, 255), 'w': 12, 'h': 10, 'cost': {'Wood': 60, 'Iron': 40}}
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
        return True, 'Item crafted'
    else:
        return False, 'Crafting failed'