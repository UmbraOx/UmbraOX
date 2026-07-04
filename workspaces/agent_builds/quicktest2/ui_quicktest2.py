# QuickTest2 UI Drawing Functions Module

import pygame
from collections import defaultdict

font_cache = {}

def font_cache(sz):
    if sz not in font_cache:
        font_cache[sz] = pygame.font.Font(None, sz)
    return font_cache[sz]

def txt(surf, text, x, y, sz, col, center=False):
    font = font_cache(sz)
    txt_surf = font.render(text, True, col)
    if center:
        rect = txt_surf.get_rect(center=(x, y))
    else:
        rect = txt_surf.get_rect(topleft=(x, y))
    surf.blit(txt_surf, rect.topleft)
    return rect

def bar(surf, x, y, w, h, val, mx, col, bg):
    pygame.draw.rect(surf, bg, (x, y, w, h), 0)
    fill_w = int(w * (val / mx))
    if fill_w > 0:
        pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    pygame.draw.rect(surf, (100, 100, 100), (rx, ry, rw, rh), 2)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.Rect(rx + rw - 30, ry + 5, 20, 20)
    txt(surf, 'X', rx + rw - 27, ry + 8, 16, (255, 0, 0), center=True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    pygame.draw.rect(surf, (255, 255, 255), (x, y, w, h), 2)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, center=True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (50, 50, 50))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (50, 50, 50))
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (0, 255, 0), (50, 50, 50))
    txt(surf, f'Gold: {player.gold}', 10, 100, 24, (255, 255, 0))
    txt(surf, f'Lvl: {player.level} XP: {player.xp}/{player.next_level_xp}', 10, 130, 24, (255, 255, 255))
    txt(surf, f'Equipped: {player.equipped}', 10, 160, 24, (255, 255, 255))
    txt(surf, f'Biome: {player.biome}', 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x, min_y = max(0, player.x - 63), max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < WORLD_MAP.height and 0 <= x < WORLD_MAP.width:
                biome = WORLD_MAP.get_biome(x, y)
                color = BIOME_COL[biome]
                pygame.draw.rect(surf, color, (x - min_x + surf.get_width() - 126, y - min_y, 1, 1))
    for enemy in enemies:
        ex, ey = enemy.x - min_x + surf.get_width() - 126, enemy.y - min_y
        pygame.draw.rect(surf, (255, 0, 0), (ex, ey, 2, 2))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    starfield = [(pygame.Color('white'), x, y) for x in range(0, surf.get_width(), 16) for y in range(0, surf.get_height(), 16)]
    for color, x, y in starfield:
        pygame.draw.circle(surf, color, (x, y), random.randint(1, 3))
    moon = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(moon, (255, 255, 255, 128), (25, 25), 25)
    surf.blit(moon, (surf.get_width() - 70, 30))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 64, (255, 255, 255), center=True)
    play_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Play', (0, 128, 0), (255, 255, 255), 36)
    load_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Load', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 140, 200, 50, 'Quit', (128, 0, 0), (255, 255, 255), 36)
    return [play_btn, load_btn, quit_btn]

def draw_class_select(surf):
    class_cards = [
        {'name': 'Warrior', 'portrait': pygame.Surface((100, 100)), 'x': 100, 'y': 100},
        {'name': 'Mage', 'portrait': pygame.Surface((100, 100)), 'x': 350, 'y': 100},
        {'name': 'Rogue', 'portrait': pygame.Surface((100, 100)), 'x': 600, 'y': 100}
    ]
    for card in class_cards:
        pygame.draw.rect(surf, (50, 50, 50), (card['x'], card['y'], 200, 300), 0)
        pygame.draw.rect(surf, (100, 100, 100), (card['x'], card['y'], 200, 300), 2)
        surf.blit(card['portrait'], (card['x'] + 50, card['y'] + 20))
        txt(surf, card['name'], card['x'] + 100, card['y'] + 140, 36, (255, 255, 255), center=True)
    return [pygame.Rect(card['x'], card['y'], 200, 300) for card in class_cards]

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Inventory')
    slots = []
    eq_btn = btn(surf, 20, 530, 190, 40, 'Equip', (0, 128, 0), (255, 255, 255), 24)
    drop_btn = btn(surf, 230, 530, 160, 40, 'Drop', (128, 0, 0), (255, 255, 255), 24)
    for i in range(10):
        slot_rect = pygame.Rect(20 + (i % 5) * 76, 30 + (i // 5) * 76, 70, 70)
        slots.append(slot_rect)
        pygame.draw.rect(surf, (50, 50, 50), slot_rect, 0)
        pygame.draw.rect(surf, (100, 100, 100), slot_rect, 2)
    if selected is not None:
        pygame.draw.rect(surf, (255, 255, 0), slots[selected], 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.name}: {quest.description}', 20, 30 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        item_rect = pygame.Rect(20 + (i % 3) * 190, 30 + (i // 3) * 76, 180, 70)
        items.append(item_rect)
        pygame.draw.rect(surf, (50, 50, 50), item_rect, 0)
        pygame.draw.rect(surf, (100, 100, 100), item_rect, 2)
        txt(surf, f'{item.name} - {item.price}', item_rect.x + 10, item_rect.y + 10, 24, (255, 255, 255))
        buy_btn = btn(surf, item_rect.x + 10, item_rect.y + 40, 80, 26, 'Buy', (0, 128, 0), (255, 255, 255), 18)
        buy_btns.append(buy_btn)
    if selected is not None:
        pygame.draw.rect(surf, (255, 255, 0), items[selected], 3)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        tab_btn = btn(surf, 20 + i * 190, 30, 180, 40, t, (50, 50, 50) if tab != i else (100, 100, 100), (255, 255, 255), 24)
        tab_btns.append(tab_btn)
    for i, recipe in enumerate(recipes[tab]):
        item_rect = pygame.Rect(20 + (i % 3) * 190, 80 + (i // 3) * 76, 180, 70)
        pygame.draw.rect(surf, (50, 50, 50), item_rect, 0)
        pygame.draw.rect(surf, (100, 100, 100), item_rect, 2)
        txt(surf, recipe.name, item_rect.x + 10, item_rect.y + 10, 24, (255, 255, 255))
        craft_btn = btn(surf, item_rect.x + 10, item_rect.y + 40, 80, 26, 'Craft', (0, 128, 0), (255, 255, 255), 18)
        craft_btns.append(craft_btn)
    if selected is not None:
        pygame.draw.rect(surf, (255, 255, 0), item_rect, 3)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 10, 10, 600, 400, f'Dialogue with {npc.name}')
    txt(surf, npc.dialogues[dial_idx], 20, 30, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        opt_btn = btn(surf, 20 + i * 190, 350, 180, 40, option.text, (50, 50, 50), (255, 255, 255), 24)
        opt_btns.append(opt_btn)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'Paused')
    resume_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, 'Resume', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'Quit', (128, 0, 0), (255, 255, 255), 36)
    return [resume_btn, quit_btn]

def draw_game_over(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'Game Over')
    restart_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, 'Restart', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'Quit', (128, 0, 0), (255, 255, 255), 36)
    return [restart_btn, quit_btn]

def draw_city(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'City')
    shop_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, 'Shop', (0, 128, 0), (255, 255, 255), 36)
    quest_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'Quests', (0, 128, 0), (255, 255, 255), 36)
    return [shop_btn, quest_btn]

def draw_world_map(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'World Map')
    travel_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, 'Travel', (0, 128, 0), (255, 255, 255), 36)
    return [travel_btn]

def draw_battle(surf, player, enemy):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'Battle')
    attack_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, 'Attack', (0, 128, 0), (255, 255, 255), 36)
    defend_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'Defend', (0, 128, 0), (255, 255, 255), 36)
    return [attack_btn, defend_btn]

def draw_player_stats(surf, player):
    panel(surf, 10, 10, 200, 100, 'Player Stats')
    txt(surf, f'HP: {player.hp}/{player.max_hp}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', 20, 60, 24, (255, 255, 255))

def draw_enemy_stats(surf, enemy):
    panel(surf, surf.get_width() - 210, 10, 200, 100, 'Enemy Stats')
    txt(surf, f'HP: {enemy.hp}/{enemy.max_hp}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'MP: {enemy.mp}/{enemy.max_mp}', 20, 60, 24, (255, 255, 255))

def draw_player_inventory(surf, player):
    panel(surf, surf.get_width() - 210, surf.get_height() - 110, 200, 100, 'Inventory')
    for i, item in enumerate(player.inventory[:3]):
        txt(surf, f'{item.name}', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_player_equipment(surf, player):
    panel(surf, surf.get_width() - 210, surf.get_height() - 220, 200, 100, 'Equipment')
    txt(surf, f'Weapon: {player.equipment["weapon"].name}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'Armor: {player.equipment["armor"].name}', 20, 60, 24, (255, 255, 255))

def draw_player_skills(surf, player):
    panel(surf, surf.get_width() - 210, surf.get_height() - 330, 200, 100, 'Skills')
    for i, skill in enumerate(player.skills[:3]):
        txt(surf, f'{skill.name}', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_player_quests(surf, player):
    panel(surf, surf.get_width() - 210, surf.get_height() - 440, 200, 100, 'Quests')
    for i, quest in enumerate(player.quests[:3]):
        txt(surf, f'{quest.name}', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_player_gold(surf, player):
    panel(surf, surf.get_width() - 210, surf.get_height() - 550, 200, 100, 'Gold')
    txt(surf, f'Gold: {player.gold}', 20, 30, 24, (255, 255, 255))

def draw_player_xp(surf, player):
    panel(surf, surf.get_width() - 210, surf.get_height() - 660, 200, 100, 'XP')
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 20, 30, 24, (255, 255, 255))

def draw_player_level(surf, player):
    panel(surf, surf.get_width() - 210, surf.get_height() - 770, 200, 100, 'Level')
    txt(surf, f'Level: {player.level}', 20, 30, 24, (255, 255, 255))

def draw_player_stats_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Player Stats')
    txt(surf, f'HP: {player.hp}/{player.max_hp}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', 20, 60, 24, (255, 255, 255))
    txt(surf, f'Weapon: {player.equipment["weapon"].name}', 20, 90, 24, (255, 255, 255))
    txt(surf, f'Armor: {player.equipment["armor"].name}', 20, 120, 24, (255, 255, 255))
    for i, skill in enumerate(player.skills):
        txt(surf, f'Skill {i+1}: {skill.name}', 20, 150 + i * 30, 24, (255, 255, 255))
    for i, item in enumerate(player.inventory):
        txt(surf, f'Item {i+1}: {item.name}', 20, 360 + i * 30, 24, (255, 255, 255))
    for i, quest in enumerate(player.quests):
        txt(surf, f'Quest {i+1}: {quest.name}', 20, 570 + i * 30, 24, (255, 255, 255))
    txt(surf, f'Gold: {player.gold}', 20, 780, 24, (255, 255, 255))
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 20, 810, 24, (255, 255, 255))
    txt(surf, f'Level: {player.level}', 20, 840, 24, (255, 255, 255))

def draw_player_inventory_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Inventory')
    for i, item in enumerate(player.inventory):
        txt(surf, f'Item {i+1}: {item.name}', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_player_skills_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Skills')
    for i, skill in enumerate(player.skills):
        txt(surf, f'Skill {i+1}: {skill.name}', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_player_quests_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Quests')
    for i, quest in enumerate(player.quests):
        txt(surf, f'Quest {i+1}: {quest.name}', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_player_equipment_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Equipment')
    txt(surf, f'Weapon: {player.equipment["weapon"].name}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'Armor: {player.equipment["armor"].name}', 20, 60, 24, (255, 255, 255))

def draw_player_gold_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Gold')
    txt(surf, f'Gold: {player.gold}', 20, 30, 24, (255, 255, 255))

def draw_player_xp_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'XP')
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 20, 30, 24, (255, 255, 255))

def draw_player_level_full(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Level')
    txt(surf, f'Level: {player.level}', 20, 30, 24, (255, 255, 255))

def draw_player_full_info(surf, player):
    panel(surf, surf.get_width() - 210, 10, 200, 860, 'Player Info')
    txt(surf, f'HP: {player.hp}/{player.max_hp}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', 20, 60, 24, (255, 255, 255))
    txt(surf, f'Weapon: {player.equipment["weapon"].name}', 20, 90, 24, (255, 255, 255))
    txt(surf, f'Armor: {player.equipment["armor"].name}', 20, 120, 24, (255, 255, 255))
    for i, skill in enumerate(player.skills):
        txt(surf, f'Skill {i+1}: {skill.name}', 20, 150 + i * 30, 24, (255, 255, 255))
    for i, item in enumerate(player.inventory):
        txt(surf, f'Item {i+1}: {item.name}', 20, 360 + i * 30, 24, (255, 255, 255))
    for i, quest in enumerate(player.quests):
        txt(surf, f'Quest {i+1}: {quest.name}', 20, 570 + i * 30, 24, (255, 255, 255))
    txt(surf, f'Gold: {player.gold}', 20, 780, 24, (255, 255, 255))
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 20, 810, 24, (255, 255, 255))
    txt(surf, f'Level: {player.level}', 20, 840, 24, (255, 255, 255))

def draw_enemy_full_info(surf, enemy):
    panel(surf, surf.get_width() - 210, 10, 200, 360, 'Enemy Info')
    txt(surf, f'HP: {enemy.hp}/{enemy.max_hp}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'MP: {enemy.mp}/{enemy.max_mp}', 20, 60, 24, (255, 255, 255))
    txt(surf, f'Weapon: {enemy.equipment["weapon"].name}', 20, 90, 24, (255, 255, 255))
    txt(surf, f'Armor: {enemy.equipment["armor"].name}', 20, 120, 24, (255, 255, 255))
    for i, skill in enumerate(enemy.skills):
        txt(surf, f'Skill {i+1}: {skill.name}', 20, 150 + i * 30, 24, (255, 255, 255))

def draw_shop_items(surf, shop):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 180, 300, 360, 'Shop Items')
    for i, item in enumerate(shop.items):
        txt(surf, f'Item {i+1}: {item.name} - {item.price} Gold', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_shop_menu(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 60, 300, 120, 'Shop Menu')
    buy_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 50, 280, 50, 'Buy', (0, 128, 0), (255, 255, 255), 36)
    sell_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'Sell', (0, 128, 0), (255, 255, 255), 36)
    return buy_btn, sell_btn

def draw_sell_items(surf, player):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 180, 300, 360, 'Sell Items')
    for i, item in enumerate(player.inventory):
        txt(surf, f'Item {i+1}: {item.name} - {item.price} Gold', 20, 30 + i * 30, 24, (255, 255, 255))

def draw_confirm_purchase(surf, item):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 60, 300, 120, 'Confirm Purchase')
    txt(surf, f'Buy {item.name} for {item.price} Gold?', 20, 40, 24, (255, 255, 255))
    yes_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 130, 50, 'Yes', (0, 128, 0), (255, 255, 255), 36)
    no_btn = btn(surf, surf.get_width() // 2 + 10, surf.get_height() // 2 + 10, 130, 50, 'No', (255, 0, 0), (255, 255, 255), 36)
    return yes_btn, no_btn

def draw_confirm_sell(surf, item):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 60, 300, 120, 'Confirm Sell')
    txt(surf, f'Sell {item.name} for {item.price} Gold?', 20, 40, 24, (255, 255, 255))
    yes_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 130, 50, 'Yes', (0, 128, 0), (255, 255, 255), 36)
    no_btn = btn(surf, surf.get_width() // 2 + 10, surf.get_height() // 2 + 10, 130, 50, 'No', (255, 0, 0), (255, 255, 255), 36)
    return yes_btn, no_btn

def draw_purchase_success(surf, item):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 60, 300, 120, 'Purchase Success')
    txt(surf, f'You bought {item.name} for {item.price} Gold.', 20, 40, 24, (255, 255, 255))
    ok_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'OK', (0, 128, 0), (255, 255, 255), 36)
    return ok_btn

def draw_sell_success(surf, item):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 60, 300, 120, 'Sell Success')
    txt(surf, f'You sold {item.name} for {item.price} Gold.', 20, 40, 24, (255, 255, 255))
    ok_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'OK', (0, 128, 0), (255, 255, 255), 36)
    return ok_btn

def draw_purchase_fail(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 60, 300, 120, 'Purchase Fail')
    txt(surf, f'You do not have enough Gold.', 20, 40, 24, (255, 255, 255))
    ok_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'OK', (0, 128, 0), (255, 255, 255), 36)
    return ok_btn

def draw_sell_fail(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 60, 300, 120, 'Sell Fail')
    txt(surf, f'You do not have this item.', 20, 40, 24, (255, 255, 255))
    ok_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'OK', (0, 128, 0), (255, 255, 255), 36)
    return ok_btn

def draw_main_menu(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Main Menu')
    play_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 70, 280, 50, 'Play', (0, 128, 0), (255, 255, 255), 36)
    shop_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 10, 280, 50, 'Shop', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return play_btn, shop_btn, quit_btn

def draw_game_over(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Game Over')
    txt(surf, f'You have been defeated.', 20, 40, 24, (255, 255, 255))
    restart_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'Restart', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 70, 280, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return restart_btn, quit_btn

def draw_victory(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Victory')
    txt(surf, f'You have defeated the enemy.', 20, 40, 24, (255, 255, 255))
    next_level_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 10, 280, 50, 'Next Level', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 70, 280, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return next_level_btn, quit_btn

def draw_inventory(surf, player):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 180, 300, 360, 'Inventory')
    for i, item in enumerate(player.inventory):
        txt(surf, f'Item {i+1}: {item.name}', 20, 40 + i * 30, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 160, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_stats(surf, player):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Stats')
    txt(surf, f'Health: {player.health}', 20, 40, 24, (255, 255, 255))
    txt(surf, f'Gold: {player.gold}', 20, 70, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_battle(surf, player, enemy):
    panel(surf, surf.get_width() // 4 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player')
    txt(surf, f'Health: {player.health}', 20, 40, 24, (255, 255, 255))
    panel(surf, surf.get_width() * 3 // 4 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy')
    txt(surf, f'Health: {enemy.health}', 20, 40, 24, (255, 255, 255))
    attack_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 10, 280, 50, 'Attack', (0, 128, 0), (255, 255, 255), 36)
    inventory_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 70, 280, 50, 'Inventory', (0, 128, 0), (255, 255, 255), 36)
    stats_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 130, 280, 50, 'Stats', (0, 128, 0), (255, 255, 255), 36)
    return attack_btn, inventory_btn, stats_btn

def draw_attack(surf, player, enemy):
    panel(surf, surf.get_width() // 4 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player')
    txt(surf, f'Health: {player.health}', 20, 40, 24, (255, 255, 255))
    panel(surf, surf.get_width() * 3 // 4 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy')
    txt(surf, f'Health: {enemy.health}', 20, 40, 24, (255, 255, 255))
    attack_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 10, 280, 50, 'Attack', (0, 128, 0), (255, 255, 255), 36)
    inventory_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 70, 280, 50, 'Inventory', (0, 128, 0), (255, 255, 255), 36)
    stats_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 130, 280, 50, 'Stats', (0, 128, 0), (255, 255, 255), 36)
    return attack_btn, inventory_btn, stats_btn

def draw_defend(surf, player, enemy):
    panel(surf, surf.get_width() // 4 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player')
    txt(surf, f'Health: {player.health}', 20, 40, 24, (255, 255, 255))
    panel(surf, surf.get_width() * 3 // 4 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy')
    txt(surf, f'Health: {enemy.health}', 20, 40, 24, (255, 255, 255))
    defend_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 10, 280, 50, 'Defend', (0, 128, 0), (255, 255, 255), 36)
    inventory_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 70, 280, 50, 'Inventory', (0, 128, 0), (255, 255, 255), 36)
    stats_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() * 3 // 4 + 130, 280, 50, 'Stats', (0, 128, 0), (255, 255, 255), 36)
    return defend_btn, inventory_btn, stats_btn

def draw_use_item(surf, player):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 180, 300, 360, 'Use Item')
    for i, item in enumerate(player.inventory):
        txt(surf, f'Item {i+1}: {item.name}', 20, 40 + i * 30, 24, (255, 255, 255))
    use_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 160, 280, 50, 'Use', (0, 128, 0), (255, 255, 255), 36)
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 220, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return use_btn, close_btn

def draw_item_used(surf, item):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Item Used')
    txt(surf, f'Used {item.name}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_item_effect(surf, effect):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Item Effect')
    txt(surf, f'Effect: {effect}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_game_over(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Game Over')
    txt(surf, f'You have been defeated.', 20, 40, 24, (255, 255, 255))
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return quit_btn

def draw_win(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'You Win!')
    txt(surf, f'Congratulations!', 20, 40, 24, (255, 255, 255))
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return quit_btn

def draw_level_up(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Level Up!')
    txt(surf, f'You have leveled up!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_level_up_stats(surf, player):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Level Up!')
    txt(surf, f'Health: {player.health}', 20, 40, 24, (255, 255, 255))
    txt(surf, f'Gold: {player.gold}', 20, 70, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_shop(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 180, 300, 360, 'Shop')
    txt(surf, f'Welcome to the shop!', 20, 40, 24, (255, 255, 255))
    buy_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 160, 280, 50, 'Buy', (0, 128, 0), (255, 255, 255), 36)
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 220, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return buy_btn, close_btn

def draw_buy_item(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 180, 300, 360, 'Buy Item')
    txt(surf, f'Which item would you like to buy?', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 220, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_item_bought(surf, item):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Item Bought')
    txt(surf, f'Bought {item.name}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_not_enough_gold(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Not Enough Gold')
    txt(surf, f'You do not have enough gold to buy this item.', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_escape(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Escape')
    txt(surf, f'You have successfully escaped!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_fight(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Fight')
    txt(surf, f'You have chosen to fight!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_run(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Run')
    txt(surf, f'You have chosen to run!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_defend(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Defend')
    txt(surf, f'You have chosen to defend!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_use_item(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Use Item')
    txt(surf, f'You have chosen to use an item!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_turn(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Your Turn')
    txt(surf, f'It is your turn!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_turn(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Turn')
    txt(surf, f'It is the enemy\'s turn!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_attack(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Attack')
    txt(surf, f'You have attacked the enemy!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_attack(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Attack')
    txt(surf, f'The enemy has attacked you!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_defend(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Defend')
    txt(surf, f'You have defended!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_defend(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Defend')
    txt(surf, f'The enemy has defended!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_use_item(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Use Item')
    txt(surf, f'You have used an item!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_use_item(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Use Item')
    txt(surf, f'The enemy has used an item!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_win(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Win')
    txt(surf, f'You have won the battle!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_win(surf):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Win')
    txt(surf, f'The enemy has won the battle!', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_health(surf, health):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Health')
    txt(surf, f'Your health: {health}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_health(surf, health):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Health')
    txt(surf, f'Enemy health: {health}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_inventory(surf, inventory):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Inventory')
    txt(surf, f'Your inventory: {inventory}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_inventory(surf, inventory):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Inventory')
    txt(surf, f'Enemy inventory: {inventory}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_level(surf, level):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Level')
    txt(surf, f'Your level: {level}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_level(surf, level):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Level')
    txt(surf, f'Enemy level: {level}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_experience(surf, experience):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Experience')
    txt(surf, f'Your experience: {experience}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_experience(surf, experience):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Experience')
    txt(surf, f'Enemy experience: {experience}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_gold(surf, gold):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Gold')
    txt(surf, f'Your gold: {gold}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_gold(surf, gold):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Gold')
    txt(surf, f'Enemy gold: {gold}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_attack(surf, attack):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Attack')
    txt(surf, f'Your attack: {attack}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_attack(surf, attack):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Attack')
    txt(surf, f'Enemy attack: {attack}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_defense(surf, defense):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Defense')
    txt(surf, f'Your defense: {defense}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_defense(surf, defense):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Defense')
    txt(surf, f'Enemy defense: {defense}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_speed(surf, speed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Speed')
    txt(surf, f'Your speed: {speed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_speed(surf, speed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Speed')
    txt(surf, f'Enemy speed: {speed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_magic(surf, magic):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Magic')
    txt(surf, f'Your magic: {magic}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_magic(surf, magic):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Magic')
    txt(surf, f'Enemy magic: {magic}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_resistance(surf, resistance):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Resistance')
    txt(surf, f'Your resistance: {resistance}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_resistance(surf, resistance):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Resistance')
    txt(surf, f'Enemy resistance: {resistance}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_luck(surf, luck):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Luck')
    txt(surf, f'Your luck: {luck}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_luck(surf, luck):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Luck')
    txt(surf, f'Enemy luck: {luck}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_accuracy(surf, accuracy):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Accuracy')
    txt(surf, f'Your accuracy: {accuracy}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_accuracy(surf, accuracy):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Accuracy')
    txt(surf, f'Enemy accuracy: {accuracy}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_evasion(surf, evasion):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Evasion')
    txt(surf, f'Your evasion: {evasion}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_evasion(surf, evasion):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Evasion')
    txt(surf, f'Enemy evasion: {evasion}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_critical(surf, critical):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Critical')
    txt(surf, f'Your critical: {critical}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_critical(surf, critical):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Critical')
    txt(surf, f'Enemy critical: {critical}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_dodge(surf, dodge):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Dodge')
    txt(surf, f'Your dodge: {dodge}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_dodge(surf, dodge):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Dodge')
    txt(surf, f'Enemy dodge: {dodge}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_parry(surf, parry):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Parry')
    txt(surf, f'Your parry: {parry}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_parry(surf, parry):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Parry')
    txt(surf, f'Enemy parry: {parry}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_block(surf, block):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Block')
    txt(surf, f'Your block: {block}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_block(surf, block):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Block')
    txt(surf, f'Enemy block: {block}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_counter(surf, counter):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Counter')
    txt(surf, f'Your counter: {counter}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_counter(surf, counter):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Counter')
    txt(surf, f'Enemy counter: {counter}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_reflect(surf, reflect):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Reflect')
    txt(surf, f'Your reflect: {reflect}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_reflect(surf, reflect):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Reflect')
    txt(surf, f'Enemy reflect: {reflect}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_absorb(surf, absorb):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Absorb')
    txt(surf, f'Your absorb: {absorb}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_absorb(surf, absorb):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Absorb')
    txt(surf, f'Enemy absorb: {absorb}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_regen(surf, regen):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Regen')
    txt(surf, f'Your regen: {regen}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_regen(surf, regen):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Regen')
    txt(surf, f'Enemy regen: {regen}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Poison')
    txt(surf, f'Your poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Poison')
    txt(surf, f'Enemy poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Bleed')
    txt(surf, f'Your bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Bleed')
    txt(surf, f'Enemy bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_burn(surf, burn):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Burn')
    txt(surf, f'Your burn: {burn}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_burn(surf, burn):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Burn')
    txt(surf, f'Enemy burn: {burn}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_freeze(surf, freeze):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Freeze')
    txt(surf, f'Your freeze: {freeze}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_freeze(surf, freeze):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Freeze')
    txt(surf, f'Enemy freeze: {freeze}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_shock(surf, shock):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Shock')
    txt(surf, f'Your shock: {shock}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_shock(surf, shock):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Shock')
    txt(surf, f'Enemy shock: {shock}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_curse(surf, curse):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Curse')
    txt(surf, f'Your curse: {curse}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_curse(surf, curse):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Curse')
    txt(surf, f'Enemy curse: {curse}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_bless(surf, bless):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Bless')
    txt(surf, f'Your bless: {bless}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_bless(surf, bless):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Bless')
    txt(surf, f'Enemy bless: {bless}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_haste(surf, haste):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Haste')
    txt(surf, f'Your haste: {haste}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_haste(surf, haste):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Haste')
    txt(surf, f'Enemy haste: {haste}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Slow')
    txt(surf, f'Your slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Slow')
    txt(surf, f'Enemy slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_confuse(surf, confuse):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Confuse')
    txt(surf, f'Your confuse: {confuse}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_confuse(surf, confuse):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Confuse')
    txt(surf, f'Enemy confuse: {confuse}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_charm(surf, charm):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Charm')
    txt(surf, f'Your charm: {charm}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_charm(surf, charm):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Charm')
    txt(surf, f'Enemy charm: {charm}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_blind(surf, blind):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Blind')
    txt(surf, f'Your blind: {blind}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_blind(surf, blind):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Blind')
    txt(surf, f'Enemy blind: {blind}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Poison')
    txt(surf, f'Your poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Poison')
    txt(surf, f'Enemy poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Bleed')
    txt(surf, f'Your bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Bleed')
    txt(surf, f'Enemy bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_stun(surf, stun):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Stun')
    txt(surf, f'Your stun: {stun}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_stun(surf, stun):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Stun')
    txt(surf, f'Enemy stun: {stun}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_sleep(surf, sleep):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Sleep')
    txt(surf, f'Your sleep: {sleep}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_sleep(surf, sleep):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Sleep')
    txt(surf, f'Enemy sleep: {sleep}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_paralyze(surf, paralyze):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Paralyze')
    txt(surf, f'Your paralyze: {paralyze}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_paralyze(surf, paralyze):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Paralyze')
    txt(surf, f'Enemy paralyze: {paralyze}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_fear(surf, fear):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Fear')
    txt(surf, f'Your fear: {fear}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_fear(surf, fear):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Fear')
    txt(surf, f'Enemy fear: {fear}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_silence(surf, silence):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Silence')
    txt(surf, f'Your silence: {silence}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_silence(surf, silence):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Silence')
    txt(surf, f'Enemy silence: {silence}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_root(surf, root):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Root')
    txt(surf, f'Your root: {root}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_root(surf, root):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Root')
    txt(surf, f'Enemy root: {root}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Slow')
    txt(surf, f'Your slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Slow')
    txt(surf, f'Enemy slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Poison')
    txt(surf, f'Your poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Poison')
    txt(surf, f'Enemy poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Bleed')
    txt(surf, f'Your bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Bleed')
    txt(surf, f'Enemy bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_dot(surf, dot):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Dot')
    txt(surf, f'Your dot: {dot}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_dot(surf, dot):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Dot')
    txt(surf, f'Enemy dot: {dot}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_hoT(surf, hoT):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player HoT')
    txt(surf, f'Your hot: {hoT}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_hoT(surf, hoT):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy HoT')
    txt(surf, f'Enemy hot: {hoT}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_shield(surf, shield):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Shield')
    txt(surf, f'Your shield: {shield}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_shield(surf, shield):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Shield')
    txt(surf, f'Enemy shield: {shield}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_absorb(surf, absorb):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Absorb')
    txt(surf, f'Your absorb: {absorb}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_absorb(surf, absorb):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Absorb')
    txt(surf, f'Enemy absorb: {absorb}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_barrier(surf, barrier):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Barrier')
    txt(surf, f'Your barrier: {barrier}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_barrier(surf, barrier):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Barrier')
    txt(surf, f'Enemy barrier: {barrier}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_invulnerable(surf, invulnerable):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Invulnerable')
    txt(surf, f'Your invulnerable: {invulnerable}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_invulnerable(surf, invulnerable):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Invulnerable')
    txt(surf, f'Enemy invulnerable: {invulnerable}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_stun(surf, stun):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Stun')
    txt(surf, f'Your stun: {stun}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_stun(surf, stun):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Stun')
    txt(surf, f'Enemy stun: {stun}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_sleep(surf, sleep):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Sleep')
    txt(surf, f'Your sleep: {sleep}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_sleep(surf, sleep):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Sleep')
    txt(surf, f'Enemy sleep: {sleep}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_confuse(surf, confuse):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Confuse')
    txt(surf, f'Your confuse: {confuse}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_confuse(surf, confuse):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Confuse')
    txt(surf, f'Enemy confuse: {confuse}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Slow')
    txt(surf, f'Your slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Slow')
    txt(surf, f'Enemy slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Bleed')
    txt(surf, f'Your bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_bleed(surf, bleed):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Bleed')
    txt(surf, f'Enemy bleed: {bleed}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Poison')
    txt(surf, f'Your poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_poison(surf, poison):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Poison')
    txt(surf, f'Enemy poison: {poison}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_dot(surf, dot):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Dot')
    txt(surf, f'Your dot: {dot}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_dot(surf, dot):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Dot')
    txt(surf, f'Enemy dot: {dot}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_hoT(surf, hoT):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player HoT')
    txt(surf, f'Your hot: {hoT}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_hoT(surf, hoT):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy HoT')
    txt(surf, f'Enemy hot: {hoT}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_shield(surf, shield):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Shield')
    txt(surf, f'Your shield: {shield}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_shield(surf, shield):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Shield')
    txt(surf, f'Enemy shield: {shield}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_absorb(surf, absorb):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Absorb')
    txt(surf, f'Your absorb: {absorb}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_absorb(surf, absorb):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Absorb')
    txt(surf, f'Enemy absorb: {absorb}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_reflect(surf, reflect):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Reflect')
    txt(surf, f'Your reflect: {reflect}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_reflect(surf, reflect):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Reflect')
    txt(surf, f'Enemy reflect: {reflect}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_taunt(surf, taunt):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Taunt')
    txt(surf, f'Your taunt: {taunt}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_taunt(surf, taunt):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Taunt')
    txt(surf, f'Enemy taunt: {taunt}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_stealth(surf, stealth):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Stealth')
    txt(surf, f'Your stealth: {stealth}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_stealth(surf, stealth):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Stealth')
    txt(surf, f'Enemy stealth: {stealth}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_invisibility(surf, invisibility):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Invisibility')
    txt(surf, f'Your invisibility: {invisibility}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_invisibility(surf, invisibility):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Invisibility')
    txt(surf, f'Enemy invisibility: {invisibility}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_blink(surf, blink):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Blink')
    txt(surf, f'Your blink: {blink}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_blink(surf, blink):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Blink')
    txt(surf, f'Enemy blink: {blink}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_teleport(surf, teleport):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Teleport')
    txt(surf, f'Your teleport: {teleport}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_teleport(surf, teleport):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Teleport')
    txt(surf, f'Enemy teleport: {teleport}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_root(surf, root):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Root')
    txt(surf, f'Your root: {root}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_root(surf, root):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Root')
    txt(surf, f'Enemy root: {root}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Slow')
    txt(surf, f'Your slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_slow(surf, slow):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Slow')
    txt(surf, f'Enemy slow: {slow}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_stun(surf, stun):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Stun')
    txt(surf, f'Your stun: {stun}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_stun(surf, stun):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Stun')
    txt(surf, f'Enemy stun: {stun}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_silence(surf, silence):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Silence')
    txt(surf, f'Your silence: {silence}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_silence(surf, silence):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Silence')
    txt(surf, f'Enemy silence: {silence}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_player_disarm(surf, disarm):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Player Disarm')
    txt(surf, f'Your disarm: {disarm}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn

def draw_enemy_disarm(surf, disarm):
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 90, 300, 180, 'Enemy Disarm')
    txt(surf, f'Enemy disarm: {disarm}', 20, 40, 24, (255, 255, 255))
    close_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 60, 280, 50, 'Close', (255, 0, 0), (255, 255, 255), 36)
    return close_btn
