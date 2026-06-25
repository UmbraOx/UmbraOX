import pygame

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
    surf.blit(txt_surf, rect)
    return rect

def bar(surf, x, y, w, h, val, mx, col, bg):
    pygame.draw.rect(surf, bg, (x, y, w, h), 0)
    fill_w = int(w * val / mx)
    pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.draw.rect(surf, (200, 0, 0), (rx + rw - 30, ry + 5, 20, 20), 0)
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 255, 255), center=True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, center=True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (100, 100, 100))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (100, 100, 100))
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (255, 165, 0), (100, 100, 100))
    txt(surf, f'Gold: {player.gold}', 10, 100, 24, (255, 255, 255))
    txt(surf, f'Lvl: {player.level} XP: {player.xp}/{player.next_level_xp}', 10, 130, 24, (255, 255, 255))
    txt(surf, f'Equipped: {player.equipped}', 10, 160, 24, (255, 255, 255))
    txt(surf, f'Biome: {player.biome}', 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x = max(0, player.x - 63)
    min_y = max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < WORLD_MAP.height and 0 <= x < WORLD_MAP.width:
                pygame.draw.rect(surf, BIOME_COL[WORLD_MAP.get_biome(x, y)], (x - min_x, y - min_y, 1, 1))
    for enemy in enemies:
        ex = max(0, min(125, enemy.x - min_x))
        ey = max(0, min(125, enemy.y - min_y))
        pygame.draw.rect(surf, (255, 0, 0), (ex, ey, 3, 3))
    px = player.x - min_x
    py = player.y - min_y
    pygame.draw.rect(surf, (0, 255, 0), (px, py, 3, 3))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 72, (255, 255, 255), center=True)
    start_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2, 200, 50, 'Start', (100, 100, 100), (255, 255, 255), 36)
    load_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 70, 200, 50, 'Load', (100, 100, 100), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 140, 200, 50, 'Quit', (100, 100, 100), (255, 255, 255), 36)
    return [start_btn, load_btn, quit_btn]

def draw_class_select(surf):
    class_cards = [
        {'name': 'Warrior', 'portrait': pygame.Surface((100, 100)), 'x': 100, 'y': 100},
        {'name': 'Mage', 'portrait': pygame.Surface((100, 100)), 'x': 300, 'y': 100},
        {'name': 'Rogue', 'portrait': pygame.Surface((100, 100)), 'x': 500, 'y': 100}
    ]
    for card in class_cards:
        pygame.draw.rect(surf, (150, 150, 150), (card['x'], card['y'], 200, 300))
        surf.blit(card['portrait'], (card['x'] + 50, card['y'] + 50))
        txt(surf, card['name'], card['x'] + 100, card['y'] + 260, 48, (0, 0, 0), center=True)
    return [pygame.Rect(card['x'], card['y'], 200, 300) for card in class_cards]

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Inventory')
    slots = []
    eq_btn = btn(surf, 20, 600, 190, 30, 'Equip', (100, 100, 100), (255, 255, 255), 24)
    drop_btn = btn(surf, 230, 600, 170, 30, 'Drop', (100, 100, 100), (255, 255, 255), 24)
    for i, item in enumerate(player.inventory):
        rect = pygame.draw.rect(surf, (200, 200, 200) if i == selected else (150, 150, 150), (20 + (i % 8) * 45, 60 + (i // 8) * 45, 40, 40))
        txt(surf, item.name[:3], rect.centerx, rect.centery, 24, (0, 0, 0), center=True)
        slots.append(rect)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.name}: {quest.description}', 20, 60 + i * 40, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        rect = pygame.draw.rect(surf, (200, 200, 200) if i == selected else (150, 150, 150), (20 + (i % 8) * 45, 60 + (i // 8) * 45, 40, 40))
        txt(surf, f'{item.name}: {item.price}', rect.centerx, rect.centery - 10, 18, (0, 0, 0), center=True)
        buy_btn = btn(surf, rect.right + 10, rect.top, 50, 30, 'Buy', (100, 100, 100), (255, 255, 255), 18)
        items.append(rect)
        buy_btns.append(buy_btn)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        tab_btn = btn(surf, 20 + i * 150, 60, 140, 30, t, (100, 100, 100) if i == tab else (150, 150, 150), (255, 255, 255), 24)
        tab_btns.append(tab_btn)
    for i, recipe in enumerate(recipes[tab]):
        rect = pygame.draw.rect(surf, (200, 200, 200) if i == selected else (150, 150, 150), (20 + (i % 8) * 45, 120 + (i // 8) * 45, 40, 40))
        txt(surf, recipe.name[:3], rect.centerx, rect.centery, 24, (0, 0, 0), center=True)
        craft_btn = btn(surf, rect.right + 10, rect.top, 60, 30, 'Craft', (100, 100, 100), (255, 255, 255), 18)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 10, 10, 600, 300, 'Dialogue')
    txt(surf, npc.dialogues[dial_idx], 20, 50, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        opt_btn = btn(surf, 20 + i * 160, 230, 150, 40, option['text'], (100, 100, 100), (255, 255, 255), 24)
        opt_btns.append(opt_btn)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 3, surf.get_height() // 4, 400, 300, 'Paused')
    resume_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Resume', (100, 100, 100), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Quit', (100, 100, 100), (255, 255, 255), 36)
    return [resume_btn, quit_btn]

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 10, 10, 400, 580, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20 + (i % 3) * 120, 60 + (i // 3) * 50, 100, 40, building['name'], (100, 100, 100), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'World Map')
    for town in TOWNS:
        pygame.draw.rect(surf, (255, 255, 0), (town.x - 3, town.y - 3, 6, 6))
    for city in CITIES:
        pygame.draw.rect(surf, (0, 255, 255), (city.x - 4, city.y - 4, 8, 8))
    return xbtn_rect

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    panel(surf, surf.get_width() // 3, surf.get_height() // 4, 400, 200, 'Game Over')
    restart_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Quit', (100, 100, 100), (255, 255, 255), 36)
    return [restart_btn, quit_btn]