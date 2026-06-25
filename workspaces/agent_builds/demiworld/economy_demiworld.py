# DemiWorld Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5, 'Coal': 2}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel Ingot': 4, 'Leather': 3}, 'out': {'Steel Shield': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron Ingot': 2, 'Nail': 5}, 'out': {'Horse Shoe': 4}},
        {'name': 'Axe', 'cost': {'Iron Ingot': 3, 'Wood': 2}, 'out': {'Axe': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 5, 'Water Bottle': 1}, 'out': {'Health Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 3, 'Water Bottle': 1}, 'out': {'Mana Potion': 1}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 2, 'Paper': 1}, 'out': {'Fire Scroll': 1}},
        {'name': 'Invisibility Potion', 'cost': {'Mushroom': 4, 'Water Bottle': 1}, 'out': {'Invisibility Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 20, 'Stone': 15}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 30, 'Iron Ingot': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Stone': 40, 'Iron Ingot': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 25, 'Soil': 30}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 218, 185), 'w': 4, 'h': 4, 'cost': {'Wood': 20, 'Stone': 15}},
    'Shop': {'col': (238, 232, 170), 'w': 6, 'h': 6, 'cost': {'Wood': 30, 'Iron Ingot': 10}},
    'Barracks': {'col': (192, 192, 192), 'w': 8, 'h': 8, 'cost': {'Stone': 40, 'Iron Ingot': 20}},
    'Farm': {'col': (173, 255, 47), 'w': 6, 'h': 6, 'cost': {'Wood': 25, 'Soil': 30}},
    'Tower': {'col': (192, 192, 192), 'w': 8, 'h': 8, 'cost': {'Stone': 50, 'Iron Ingot': 30}},
    'Warehouse': {'col': (240, 240, 240), 'w': 6, 'h': 6, 'cost': {'Wood': 40, 'Stone': 20}}
}

def buy_item(player, npc, item_name):
    if item_name not in npc.inventory:
        return False, "Item not available"
    item_cost = npc.inventory[item_name]['price']
    if player.gold < item_cost:
        return False, "Not enough gold"
    player.gold -= item_cost
    if item_name in player.inventory:
        player.inventory[item_name] += 1
    else:
        player.inventory[item_name] = 1
    del npc.inventory[item_name]
    return True, f"Bought {item_name}"

def sell_item(player, npc, item_name):
    if item_name not in player.inventory:
        return False, "Item not in inventory"
    item_price = npc.buy_prices.get(item_name, 0)
    if item_price == 0:
        return False, "NPC does not buy this item"
    player.gold += item_price
    player.inventory[item_name] -= 1
    if player.inventory[item_name] <= 0:
        del player.inventory[item_name]
    if item_name in npc.inventory:
        npc.inventory[item_name]['qty'] += 1
    else:
        npc.inventory[item_name] = {'price': item_price, 'qty': 1}
    return True, f"Sold {item_name}"

def craft_item(player, recipe):
    for mat, qty in recipe['cost'].items():
        if player.inventory.get(mat, 0) < qty:
            return False, f"Not enough {mat}"
    for mat, qty in recipe['cost'].items():
        player.inventory[mat] -= qty
        if player.inventory[mat] == 0:
            del player.inventory[mat]
    for item, qty in recipe['out'].items():
        if item in player.inventory:
            player.inventory[item] += qty
        else:
            player.inventory[item] = qty
    return True, f"Crafted {recipe['name']}"

if __name__ == '__main__':
    main()
