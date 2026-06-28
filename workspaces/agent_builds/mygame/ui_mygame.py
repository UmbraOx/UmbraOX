# MyGame UI Drawing Functions Module

import pygame
from pygame.locals import *

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
    fill_w = int(w * min(val / mx, 1))
    pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.draw.rect(surf, (200, 50, 50), (rx + rw - 30, ry + 5, 20, 20), 0)
    txt(surf, 'X', rx + rw - 25, ry + 10, 16, (255, 255, 255))
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (100, 0, 0))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (0, 0, 100))
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (0, 255, 0), (0, 100, 0))
    txt(surf, f'Gold: {player.gold}', 10, 100, 24, (255, 255, 255))
    txt(surf, f'Level: {player.level}', 10, 130, 24, (255, 255, 255))
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 10, 160, 24, (255, 255, 255))
    txt(surf, f'Equipped: {player.equipped}', 10, 190, 24, (255, 255, 255))
    txt(surf, f'Biome: {player.biome}', 10, 220, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x, min_y = max(player.x - 63, 0), max(player.y - 63, 0)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < len(WORLD_MAP) and 0 <= x < len(WORLD_MAP[y]):
                pygame.draw.rect(surf, BIOME_COL[WORLD_MAP[y][x]], (x - min_x + surf.get_width() - 126, y - min_y, 1, 1))
    pygame.draw.circle(surf, (255, 0, 0), (surf.get_width() - 63, 63), 4)
    for enemy in enemies:
        ex, ey = enemy.x - min_x + surf.get_width() - 126, enemy.y - min_y
        if 0 <= ex < 126 and 0 <= ey < 126:
            pygame.draw.circle(surf, (0, 255, 0), (ex, ey), 3)

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    starfield = [(pygame.Color('white'), (x, y)) for x in range(0, surf.get_width(), 16) for y in range(0, surf.get_height(), 16)]
    pygame.draw.circle(surf, (255, 255, 255), (surf.get_width() // 2, surf.get_height() // 4), 50)
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 8, 64, (255, 255, 255), True)
    btns = []
    btns.append(btn(surf, surf.get_width() // 3, surf.get_height() * 3 // 4 - 100, 200, 50, 'Start', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, surf.get_width() // 3, surf.get_height() * 3 // 4 - 40, 200, 50, 'Load', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, surf.get_width() // 3, surf.get_height() * 3 // 4 + 20, 200, 50, 'Exit', (50, 50, 50), (255, 255, 255), 24))
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    btns = []
    btns.append(btn(surf, 100, 100, 200, 300, 'Warrior', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, 400, 100, 200, 300, 'Mage', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, 700, 100, 200, 300, 'Rogue', (50, 50, 50), (255, 255, 255), 24))
    return btns

def draw_inventory(surf, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 600, 'Inventory')
    slots = [pygame.Rect(20 + (i % 5) * 50, 40 + (i // 5) * 50, 40, 40) for i in range(len(player.inventory))]
    eq_btn = btn(surf, 10, 620, 140, 30, 'Equip', (50, 50, 50), (255, 255, 255), 24)
    drop_btn = btn(surf, 160, 620, 140, 30, 'Drop', (50, 50, 50), (255, 255, 255), 24)
    for i, slot in enumerate(slots):
        pygame.draw.rect(surf, (100, 100, 100) if selected == i else (50, 50, 50), slot, 0)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 600, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, quest.title, 20, 40 + i * 50, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 600, 'Shop')
    items = [pygame.Rect(20 + (i % 5) * 50, 40 + (i // 5) * 50, 40, 40) for i in range(len(npc.items))]
    buy_btns = []
    for i, item in enumerate(items):
        pygame.draw.rect(surf, (100, 100, 100) if selected == i else (50, 50, 50), item, 0)
        txt(surf, str(npc.items[i].price), item.x, item.y + 40, 16, (255, 255, 255))
        buy_btns.append(btn(surf, item.x, item.y + 60, 40, 30, 'Buy', (50, 50, 50), (255, 255, 255), 16))
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 600, 'Crafting')
    tab_btns = []
    for i in range(len(recipes)):
        tab_btns.append(btn(surf, 20 + i * 80, 40, 75, 30, recipes[i].name, (50, 50, 50), (255, 255, 255), 16))
    craft_btns = []
    for i, recipe in enumerate(recipes):
        if tab == i:
            slots = [pygame.Rect(20 + j * 40, 80, 30, 30) for j in range(len(recipe.ingredients))]
            for j, slot in enumerate(slots):
                pygame.draw.rect(surf, (100, 100, 100) if selected == j else (50, 50, 50), slot, 0)
            craft_btns.append(btn(surf, 20 + len(recipe.ingredients) * 40, 80, 75, 30, 'Craft', (50, 50, 50), (255, 255, 255), 16))
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 400, 'Dialogue')
    txt(surf, npc.dialogues[dial_idx].text, 20, 40, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.dialogues[dial_idx].options):
        opt_btns.append(btn(surf, 20, 100 + i * 50, 260, 40, option.text, (50, 50, 50), (255, 255, 255), 24))
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 600, 'Paused')
    pause_btns = []
    pause_btns.append(btn(surf, 20, 40, 260, 50, 'Resume', (50, 50, 50), (255, 255, 255), 24))
    pause_btns.append(btn(surf, 20, 100, 260, 50, 'Save', (50, 50, 50), (255, 255, 255), 24))
    pause_btns.append(btn(surf, 20, 160, 260, 50, 'Load', (50, 50, 50), (255, 255, 255), 24))
    pause_btns.append(btn(surf, 20, 220, 260, 50, 'Exit', (50, 50, 50), (255, 255, 255), 24))
    return xbtn_rect, pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 600, f'{place_type} Panel')
    type_btns = []
    for i in range(len(BUILDING_TYPES)):
        type_btns.append(btn(surf, 20 + i * 80, 40, 75, 30, BUILDING_TYPES[i], (50, 50, 50), (255, 255, 255), 16))
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 600, 'World Map')
    for i in range(len(WORLD_MAP)):
        for j in range(len(WORLD_MAP[i])):
            pygame.draw.rect(surf, BIOME_COL[WORLD_MAP[i][j]], (20 + j * 5, 40 + i * 5, 5, 5), 0)
    for town in TOWNS:
        pygame.draw.circle(surf, (255, 0, 0), (20 + town.x * 5, 40 + town.y * 5), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (0, 0, 255), (20 + city.x * 5, 40 + city.y * 5), 3)
    return xbtn_rect

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    panel(surf, 10, 10, 300, 600, 'Game Over')
    txt(surf, 'You have been defeated.', 20, 40, 24, (255, 255, 255))
    btn(surf, 20, 100, 260, 50, 'Restart', (50, 50, 50), (255, 255, 255), 24)
    btn(surf, 20, 160, 260, 50, 'Exit', (50, 50, 50), (255, 255, 255), 24)

def draw_player_stats(surf, player):
    txt(surf, f'HP: {player.hp}/{player.max_hp}', 10, 10, 24, (255, 0, 0))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', 10, 40, 24, (0, 0, 255))
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 10, 70, 24, (255, 255, 0))
    txt(surf, f'Lvl: {player.level}', 10, 100, 24, (255, 255, 255))

def draw_player_inventory(surf, player):
    for i in range(len(player.inventory)):
        pygame.draw.rect(surf, (100, 100, 100), (10 + i * 30, 600, 20, 20), 0)

def draw_player_equipment(surf, player):
    for i in range(len(player.equipment)):
        pygame.draw.rect(surf, (150, 150, 150), (10 + i * 30, 630, 20, 20), 0)

def draw_player_skills(surf, player):
    for i in range(len(player.skills)):
        pygame.draw.rect(surf, (200, 200, 200), (10 + i * 30, 660, 20, 20), 0)

def draw_player_status_effects(surf, player):
    for i in range(len(player.status_effects)):
        pygame.draw.rect(surf, (255, 0, 255), (10 + i * 30, 690, 20, 20), 0)

def draw_player_gold(surf, player):
    txt(surf, f'Gold: {player.gold}', 10, 720, 24, (255, 215, 0))
