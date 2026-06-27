# MyGame Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5, 'Stone': 2}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel Ingot': 4, 'Leather': 3}, 'out': {'Steel Shield': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron Ingot': 2, 'Nail': 5}, 'out': {'Horse Shoe': 4}},
        {'name': 'Axe', 'cost': {'Iron Ingot': 3, 'Wood': 2}, 'out': {'Axe': 1}}
    ],
    'Alchemy': [
        {'name': 'Healing Potion', 'cost': {'Herb': 5, 'Water Bottle': 1}, 'out': {'Healing Potion': 3}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 2}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 4, 'Paper': 1}, 'out': {'Fire Scroll': 1}},
        {'name': 'Invisibility Potion', 'cost': {'Mushroom': 3, 'Water Bottle': 1}, 'out': {'Invisibility Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 20, 'Stone': 15}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 30, 'Iron Ingot': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel Ingot': 25, 'Stone': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 15, 'Soil': 30}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 204, 153), 'w': 64, 'h': 64, 'cost': {'Wood': 20, 'Stone': 15}},
    'Shop': {'col': (255, 255, 153), 'w': 96, 'h': 64, 'cost': {'Wood': 30, 'Iron Ingot': 10}},
    'Barracks': {'col': (153, 204, 255), 'w': 128, 'h': 96, 'cost': {'Steel Ingot': 25, 'Stone': 20}},
    'Farm': {'col': (153, 255, 153), 'w': 96, 'h': 96, 'cost': {'Wood': 15, 'Soil': 30}},
    'Tower': {'col': (204, 153, 255), 'w': 128, 'h': 128, 'cost': {'Steel Ingot': 30, 'Stone': 40}},
    'Warehouse': {'col': (255, 153, 153), 'w': 96, 'h': 128, 'cost': {'Wood': 40, 'Iron Ingot': 20}}
}

def buy_item(player, npc, item_name):
    if item_name in npc.inventory and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Item bought successfully'
    return False, 'Not enough gold or item not available'

def sell_item(player, npc, item_name):
    if item_name in player.inventory:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Item sold successfully'
    return False, 'Item not in inventory'

def craft_item(player, recipe):
    can_craft = all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items())
    if can_craft:
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
            if player.inventory[mat] == 0:
                del player.inventory[mat]
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Item crafted successfully'
    return False, 'Not enough materials'