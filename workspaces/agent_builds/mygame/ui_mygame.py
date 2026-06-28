# MyGame UI Drawing Functions Module

import pygame
from pygame.locals import *

font_cache = {}

def font_cache(sz):
    if sz not in font_cache:
        font_cache[sz] = pygame.font.Font(None, sz)
    return font_cache[sz]

def txt(surf, text, x, y, sz, col, center=False):
    fnt = font_cache(sz)
    txt_surf = fnt.render(text, True, col)
    if center:
        rect = txt_surf.get_rect(center=(x, y))
    else:
        rect = txt_surf.get_rect(topleft=(x, y))
    surf.blit(txt_surf, rect.topleft)
    return rect

def bar(surf, x, y, w, h, val, mx, col, bg):
    pygame.draw.rect(surf, bg, (x, y, w, h), 0)
    fill_w = int(w * val / mx)
    pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    pygame.draw.rect(surf, (100, 100, 100), (rx, ry, rw, rh), 2)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.draw.rect(surf, (200, 50, 50), (rx + rw - 30, ry + 5, 20, 20), 0)
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 255, 255), center=True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    pygame.draw.rect(surf, (100, 100, 100), (x, y, w, h), 2)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, center=True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp / player.max_hp, player.max_hp, (255, 0, 0), (50, 50, 50))
    bar(surf, 10, 40, 200, 20, player.mp / player.max_mp, player.max_mp, (0, 0, 255), (50, 50, 50))
    bar(surf, 10, 70, 200, 20, player.sta / player.max_sta, player.max_sta, (255, 255, 0), (50, 50, 50))
    txt(surf, f"Gold: {player.gold}", 10, 100, 24, (255, 255, 255))
    txt(surf, f"LvL: {player.level}", 10, 130, 24, (255, 255, 255))
    txt(surf, f"XP: {player.xp}/{player.next_level_xp}", 10, 160, 24, (255, 255, 255))
    txt(surf, f"Equipped: {player.equipped}", 10, 190, 24, (255, 255, 255))
    txt(surf, f"Biome: {player.biome}", 10, 220, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x, min_y = max(0, player.x - 63), max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < len(WORLD_MAP) and 0 <= x < len(WORLD_MAP[0]):
                pygame.draw.rect(surf, BIOME_COL[WORLD_MAP[y][x]], (x - min_x + surf.get_width() - 126, y - min_y, 1, 1))
    for enemy in enemies:
        ex, ey = enemy.x - min_x + surf.get_width() - 126, enemy.y - min_y
        if 0 <= ex < 126 and 0 <= ey < 126:
            pygame.draw.rect(surf, (255, 0, 0), (ex, ey, 2, 2))
    px, py = player.x - min_x + surf.get_width() - 126, player.y - min_y
    if 0 <= px < 126 and 0 <= py < 126:
        pygame.draw.rect(surf, (0, 255, 0), (px, py, 3, 3))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    starfield = [(pygame.Color(255, 255, 255) if i % 10 == 0 else pygame.Color(180, 180, 180)) for i in range(100)]
    for _ in range(100):
        x, y = pygame.math.Vector2(surf.get_width(), surf.get_height()).elementwise() * pygame.math.Vector2.random()
        pygame.draw.circle(surf, starfield.pop(), (int(x), int(y)), 1)
    moon_rect = pygame.Rect(surf.get_width() - 100, 50, 80, 80)
    pygame.draw.ellipse(surf, (200, 200, 200), moon_rect)
    txt(surf, project_name, surf.get_width() // 2, 100, 48, (255, 255, 255), center=True)
    btns = []
    for i, label in enumerate(['Start', 'Load Game', 'Exit']):
        b = btn(surf, surf.get_width() // 2 - 100, 200 + i * 60, 200, 40, label, (50, 50, 50), (255, 255, 255), 32)
        btns.append(b)
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    classes = ['Warrior', 'Mage', 'Rogue']
    portraits = [pygame.Surface((100, 100)) for _ in range(3)]
    for i, (cls, portrait) in enumerate(zip(classes, portraits)):
        pygame.draw.rect(portrait, (255, 0, 0), (0, 0, 100, 100))
        txt(surf, cls, surf.get_width() // 3 * i + 50, 200, 32, (255, 255, 255), center=True)
        surf.blit(portrait, (surf.get_width() // 3 * i, 100))
    return [pygame.Rect(surf.get_width() // 3 * i, 100, 100, 100) for i in range(3)]

def draw_inventory(surf, player, selected):
    surf.fill((50, 50, 50))
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Inventory')
    slots = [pygame.Rect(20 + i % 8 * 45, 50 + i // 8 * 45, 40, 40) for i in range(len(player.inventory))]
    eq_btn = btn(surf, 10, 620, 190, 30, 'Equip', (50, 50, 50), (255, 255, 255), 24)
    drop_btn = btn(surf, 210, 620, 190, 30, 'Drop', (50, 50, 50), (255, 255, 255), 24)
    for i, slot in enumerate(slots):
        pygame.draw.rect(surf, (100, 100, 100), slot, 2)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), slot, 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((50, 50, 50))
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 20, 50 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    surf.fill((50, 50, 50))
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Shop')
    items = [pygame.Rect(20 + i % 8 * 45, 50 + i // 8 * 45, 40, 40) for i in range(len(npc.inventory))]
    buy_btns = []
    for i, item in enumerate(items):
        pygame.draw.rect(surf, (100, 100, 100), item, 2)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), item, 3)
        b = btn(surf, item.x + item.width + 10, item.y, 80, 40, f'Buy {npc.inventory[i].price}', (50, 50, 50), (255, 255, 255), 20)
        buy_btns.append(b)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((50, 50, 50))
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Crafting')
    tab_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        b = btn(surf, 20 + i * 135, 50, 130, 40, t, (50, 50, 50), (255, 255, 255), 24)
        tab_btns.append(b)
    craft_btns = []
    for i, recipe in enumerate(recipes[tab]):
        rect = pygame.Rect(20 + i % 8 * 130, 100 + i // 8 * 60, 120, 50)
        pygame.draw.rect(surf, (100, 100, 100), rect, 2)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), rect, 3)
        txt(surf, recipe.name, rect.x + 10, rect.y + 10, 24, (255, 255, 255))
        b = btn(surf, rect.x + rect.width + 10, rect.y, 80, 50, 'Craft', (50, 50, 50), (255, 255, 255), 24)
        craft_btns.append(b)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((50, 50, 50))
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Dialogue')
    txt(surf, npc.dialogues[dial_idx], 20, 50, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        b = btn(surf, 20 + i % 3 * 130, 500 + i // 3 * 40, 120, 30, option.text, (50, 50, 50), (255, 255, 255), 20)
        opt_btns.append(b)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), special_flags=BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 4, surf.get_height() // 4, surf.get_width() // 2, surf.get_height() // 2, 'Paused')
    pause_btns = []
    for i, label in enumerate(['Resume', 'Save Game', 'Exit']):
        b = btn(surf, surf.get_width() // 3 * (i + 1) - 75, surf.get_height() // 2 + i * 60 - 90, 150, 40, label, (50, 50, 50), (255, 255, 255), 32)
        pause_btns.append(b)
    return panel(surf, surf.get_width() // 4, surf.get_height() // 4, surf.get_width() // 2, surf.get_height() // 2, 'Paused'), pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((50, 50, 50))
    xbtn_rect = panel(surf, 10, 10, 400, 600, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        b = btn(surf, 20 + i % 3 * 130, 50 + i // 3 * 60, 120, 50, building.name, (50, 50, 50), (255, 255, 255), 24)
        type_btns.append(b)
    return xbtn_rect, type_btns

def draw_world_map(surf):
    surf.fill((0, 128, 0))
    txt(surf, 'World Map', surf.get_width() // 2, 20, 36, (255, 255, 255), center=True)

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    panel(surf, surf.get_width() // 4, surf.get_height() // 4, surf.get_width() // 2, surf.get_height() // 2, 'Game Over')
    btns = []
    for i, label in enumerate(['Restart', 'Exit']):
        b = btn(surf, surf.get_width() // 3 * (i + 1) - 75, surf.get_height() // 2 + i * 60 - 90, 150, 40, label, (50, 50, 50), (255, 255, 255), 32)
        btns.append(b)
    return panel(surf, surf.get_width() // 4, surf.get_height() // 4, surf.get_width() // 2, surf.get_height() // 2, 'Game Over'), btns

def draw_main_menu(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Main Menu', surf.get_width() // 2, 100, 48, (255, 255, 255), center=True)
    btns = []
    for i, label in enumerate(['Start Game', 'Load Game', 'Exit']):
        b = btn(surf, surf.get_width() // 2 - 100, 200 + i * 60, 200, 40, label, (50, 50, 50), (255, 255, 255), 32)
        btns.append(b)
    return btns

def draw_settings(surf):
    surf.fill((50, 50, 50))
    panel(surf, 10, 10, 400, 600, 'Settings')
    txt(surf, 'Volume:', 20, 50, 32, (255, 255, 255))
    volume_slider = pygame.Rect(100, 50, 280, 40)
    pygame.draw.rect(surf, (100, 100, 100), volume_slider, 2)
    txt(surf, 'Graphics:', 20, 120, 32, (255, 255, 255))
    graphics_options = ['Low', 'Medium', 'High']
    for i, option in enumerate(graphics_options):
        b = btn(surf, 20 + i * 130, 160, 120, 40, option, (50, 50, 50), (255, 255, 255), 24)
        surf.blit(b, (20 + i * 130, 160))
    return panel(surf, 10, 10, 400, 600, 'Settings'), volume_slider

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Loading...', surf.get_width() // 2, surf.get_height() // 2, 36, (255, 255, 255), center=True)

def draw_minimap(surf, player_pos, map_size):
    mini_map = pygame.Surface((100, 100))
    mini_map.fill((0, 128, 0))
    x, y = int(player_pos[0] / map_size * 100), int(player_pos[1] / map_size * 100)
    pygame.draw.circle(mini_map, (255, 0, 0), (x, y), 3)
    surf.blit(mini_map, (surf.get_width() - 110, 10))

def draw_health_bar(surf, player):
    health_bar = pygame.Rect(10, 10, player.health / player.max_health * 200, 20)
    pygame.draw.rect(surf, (255, 0, 0), health_bar)
    pygame.draw.rect(surf, (255, 255, 255), health_bar, 2)

def draw_mana_bar(surf, player):
    mana_bar = pygame.Rect(10, 40, player.mana / player.max_mana * 200, 20)
    pygame.draw.rect(surf, (0, 0, 255), mana_bar)
    pygame.draw.rect(surf, (255, 255, 255), mana_bar, 2)

def draw_experience_bar(surf, player):
    exp_bar = pygame.Rect(10, 70, player.exp / player.next_level_exp * 200, 20)
    pygame.draw.rect(surf, (255, 255, 0), exp_bar)
    pygame.draw.rect(surf, (255, 255, 255), exp_bar, 2)

def draw_status_effects(surf, player):
    for i, effect in enumerate(player.status_effects):
        txt(surf, f'{effect.name}: {effect.duration}', 10, 100 + i * 30, 24, (255, 255, 255))

def draw_target_indicator(surf, target_pos):
    pygame.draw.circle(surf, (255, 0, 0), (int(target_pos[0]), int(target_pos[1])), 5)

def draw_debug_info(surf, debug_data):
    txt(surf, f'FPS: {debug_data["fps"]:.2f}', 10, surf.get_height() - 30, 24, (255, 255, 255))
    txt(surf, f'Delta Time: {debug_data["delta_time"]:.4f}s', 10, surf.get_height() - 60, 24, (255, 255, 255))

def draw_tooltip(surf, tooltip_text, pos):
    txt(surf, tooltip_text, pos[0], pos[1] - 30, 24, (255, 255, 255), bg_color=(0, 0, 0))