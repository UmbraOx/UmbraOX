# Economy system for DemiWorldTw

import random

def generate_shop_stock(job):
    items = {
        'Fletching': ['Arrows', 'Feathers', 'Quivers'],
        'Blacksmith': ['Swords', 'Armor', 'Helmets'],
        'Alchemy': ['Potions', 'Herbs', 'Reagents'],
        'Building': ['Wood', 'Bricks', 'Tools']
    }
    stock = {}
    for item in items.get(job, []):
        price = random.randint(10, 50)
        qty = random.randint(5, 20)
        stock[item] = {'price': price, 'qty': qty}
    return stock

def buy_item(player, npc, item_name):
    if item_name not in npc.stock:
        return False, "Item not available."
    item_price = npc.stock[item_name]['price']
    if player.gold < item_price:
        return False, "Not enough gold."
    if npc.stock[item_name]['qty'] == 0:
        return False, "Out of stock."
    
    player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
    player.gold -= item_price
    npc.stock[item_name]['qty'] -= 1
    return True, f"Bought {item_name} for {item_price} gold."

def sell_item(player, npc, item_name):
    if item_name not in player.inventory or player.inventory[item_name] == 0:
        return False, "You do not have this item."
    
    sell_price = npc.stock.get(item_name, {'price': random.randint(5, 25)})['price']
    player.gold += sell_price
    player.inventory[item_name] -= 1
    if player.inventory[item_name] == 0:
        del player.inventory[item_name]
    return True, f"Sold {item_name} for {sell_price} gold."

def craft_item(player, recipe):
    if not all(material in player.inventory and player.inventory[material] >= qty for material, qty in recipe['cost'].items()):
        return False, "Insufficient materials."
    
    for material, qty in recipe['cost'].items():
        player.inventory[material] -= qty
        if player.inventory[material] == 0:
            del player.inventory[material]
    
    for item, qty in recipe['out'].items():
        player.inventory[item] = player.inventory.get(item, 0) + qty
    
    return True, f"Crafted {list(recipe['out'].keys())[0]}."

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrows', 'cost': {'Feathers': 2}, 'out': {'Arrows': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 3, 'String': 1}, 'out': {'Quiver': 1}}
    ],
    'Blacksmith': [
        {'name': 'Sword', 'cost': {'Iron': 5, 'Steel': 2}, 'out': {'Sword': 1}},
        {'name': 'Armor', 'cost': {'Leather': 4, 'Steel': 3}, 'out': {'Armor': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herbs': 2, 'Water': 1}, 'out': {'Health Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Reagents': 3, 'Water': 1}, 'out': {'Mana Potion': 1}}
    ],

if __name__ == '__main__':
    main()
