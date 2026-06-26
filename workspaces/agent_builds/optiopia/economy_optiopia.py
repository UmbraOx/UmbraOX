# Optiopia Economy and Crafting Module

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
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water Bottle': 1}, 'out': {'Health Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 1}},
        {'name': 'Poison', 'cost': {'Venom Sac': 1, 'Herb': 1}, 'out': {'Poison': 1}},
        {'name': 'Invisibility Potion', 'cost': {'Mushroom': 2, 'Crystal Dust': 3}, 'out': {'Invisibility Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 20}}, 
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron Ingot': 10}},
        {'name': 'Barracks', 'cost': {'Stone': 60, 'Iron Ingot': 30}},
        {'name': 'Farm', 'cost': {'Wood': 20, 'Soil': 50}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (194, 178, 128), 'w': 64, 'h': 64, 'cost': {'Wood': 50, 'Stone': 20}},
    'Shop': {'col': (255, 235, 205), 'w': 96, 'h': 64, 'cost': {'Wood': 40, 'Iron Ingot': 10}},
    'Barracks': {'col': (165, 42, 42), 'w': 128, 'h': 96, 'cost': {'Stone': 60, 'Iron Ingot': 30}},
    'Farm': {'col': (34, 139, 34), 'w': 96, 'h': 96, 'cost': {'Wood': 20, 'Soil': 50}},
    'Tower': {'col': (139, 0, 0), 'w': 80, 'h': 128, 'cost': {'Stone': 100, 'Iron Ingot': 40}},
    'Warehouse': {'col': (255, 255, 224), 'w': 128, 'h': 96, 'cost': {'Wood': 70, 'Stone': 30}}
}

def buy_item(player, npc, item_name):
    if npc.inventory.get(item_name, 0) > 0 and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Item bought successfully'
    else:
        return False, 'Not enough gold or item not available'

def sell_item(player, npc, item_name):
    if player.inventory.get(item_name, 0) > 0 and npc.gold >= npc.prices[item_name]:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Item sold successfully'
    else:
        return False, 'Not enough gold or item not available'

def craft_item(player, recipe):
    can_craft = all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items())
    if can_craft:
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Item crafted successfully'
    else:
        return False, 'Not enough materials'