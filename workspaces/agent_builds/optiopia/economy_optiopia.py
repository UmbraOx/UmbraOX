# Optiopia Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Bolt': 10}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5, 'Coal': 2}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel Ingot': 4, 'Leather': 3}, 'out': {'Steel Shield': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron Ingot': 2, 'Nail': 5}, 'out': {'Horse Shoe': 4}},
        {'name': 'Axe', 'cost': {'Iron Ingot': 3, 'Wood': 2}, 'out': {'Axe': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 5, 'Water Bottle': 1}, 'out': {'Health Potion': 3}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 2}},
        {'name': 'Poison Arrow', 'cost': {'Arrow': 5, 'Venom Sac': 1}, 'out': {'Poison Arrow': 3}},
        {'name': 'Invisibility Cloak', 'cost': {'Cloth': 4, 'Mystic Dust': 2}, 'out': {'Invisibility Cloak': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 30}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron Ingot': 20}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Stone': 60, 'Iron Ingot': 30}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 20, 'Soil': 40}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 239, 213), 'w': 4, 'h': 4, 'cost': {'Wood': 50, 'Stone': 30}},
    'Shop': {'col': (255, 255, 224), 'w': 5, 'h': 4, 'cost': {'Wood': 40, 'Iron Ingot': 20}},
    'Barracks': {'col': (196, 187, 157), 'w': 6, 'h': 5, 'cost': {'Stone': 60, 'Iron Ingot': 30}},
    'Farm': {'col': (240, 230, 140), 'w': 5, 'h': 4, 'cost': {'Wood': 20, 'Soil': 40}},
    'Tower': {'col': (169, 169, 169), 'w': 7, 'h': 6, 'cost': {'Stone': 80, 'Iron Ingot': 50}},
    'Warehouse': {'col': (238, 232, 170), 'w': 6, 'h': 5, 'cost': {'Wood': 40, 'Stone': 40}}
}

def buy_item(player, npc, item_name):
    if npc.inventory.get(item_name, 0) == 0:
        return False, "Item not available"
    price = npc.prices[item_name]
    if player.gold < price:
        return False, "Not enough gold"
    player.gold -= price
    player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
    npc.inventory[item_name] -= 1
    return True, f"Bought {item_name} for {price} gold"

def sell_item(player, npc, item_name):
    if player.inventory.get(item_name, 0) == 0:
        return False, "You do not have this item"
    price = npc.prices[item_name]
    player.gold += price
    player.inventory[item_name] -= 1
    npc.inventory[item_name] += 1
    return True, f"Sold {item_name} for {price} gold"

def craft_item(player, recipe):
    if not all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items()):
        return False, "Not enough materials"
    for mat, qty in recipe['cost'].items():
        player.inventory[mat] -= qty
    for item, qty in recipe['out'].items():
        player.inventory[item] = player.inventory.get(item, 0) + qty
    return True, f"Crafted {recipe['name']}"