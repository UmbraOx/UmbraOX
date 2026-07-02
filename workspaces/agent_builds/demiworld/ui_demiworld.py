import pygame

font_cache_dict = {}

def font_cache(sz):
    if sz not in font_cache_dict:
        font_cache_dict[sz] = pygame.font.Font(None, sz)
    return font_cache_dict[sz]

def txt(surf, text, x, y, sz, col, center=False):
    font = font_cache(sz)
    txt_surf = font.render(text, True, col)
    if center:
        rect = txt_surf.get_rect(center=(x, y))
    else:
        rect = txt_surf.get_rect(topleft=(x, y))
    surf.blit(txt_surf, rect)
    return rect

def bar(surf, x, y, w, h, val, mx, col, bg):
    pygame.draw.rect(surf, bg, (x, y, w, h), 0)
    inner_w = int(w * min(1, max(0, val / mx)))
    pygame.draw.rect(surf, col, (x, y, inner_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    pygame.draw.rect(surf, (100, 100, 100), (rx, ry, rw, rh), 2)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.Rect(rx + rw - 30, ry + 5, 20, 20)
    txt(surf, 'X', rx + rw - 27, ry + 8, 16, (255, 0, 0), True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    pygame.draw.rect(surf, (255, 255, 255), (x, y, w, h), 2)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (50, 50, 50))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (50, 50, 50))
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (0, 255, 0), (50, 50, 50))
    txt(surf, f'Gold: {player.gold}', 10, 100, 24, (255, 255, 0))
    txt(surf, f'Level: {player.level}', 10, 130, 24, (255, 255, 255))
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 10, 160, 24, (255, 255, 255))
    txt(surf, f'Equipped: {player.equipped}', 10, 190, 24, (255, 255, 255))
    txt(surf, f'Biome: {player.biome}', 10, 220, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    mini_surf = pygame.Surface((126, 126))
    for y in range(len(WORLD_MAP)):
        for x in range(len(WORLD_MAP[y])):
            pygame.draw.rect(mini_surf, BIOME_COL[WORLD_MAP[y][x]], (x * 4, y * 4, 4, 4), 0)
    for enemy in enemies:
        ex, ey = int(enemy.x / 16), int(enemy.y / 16)
        pygame.draw.circle(mini_surf, (255, 0, 0), (ex * 4 + 2, ey * 4 + 2), 2)
    px, py = int(player.x / 16), int(player.y / 16)
    pygame.draw.circle(mini_surf, (0, 255, 0), (px * 4 + 2, py * 4 + 2), 3)
    surf.blit(mini_surf, (surf.get_width() - 136, 10))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 72, (255, 255, 255), True)
    btns = []
    btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 30, 200, 40, 'Start Game', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 80, 200, 40, 'Load Game', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 130, 200, 40, 'Exit', (50, 50, 50), (255, 255, 255), 24))
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    btns = []
    btns.append(btn(surf, 100, 100, 200, 300, 'Warrior', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, 400, 100, 200, 300, 'Mage', (50, 50, 50), (255, 255, 255), 24))
    btns.append(btn(surf, 700, 100, 200, 300, 'Rogue', (50, 50, 50), (255, 255, 255), 24))
    return btns

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 10, 10, 300, 600, 'Inventory')
    slots = []
    eq_btn = btn(surf, 10, 520, 140, 80, 'Equip', (50, 50, 50), (255, 255, 255), 24)
    drop_btn = btn(surf, 160, 520, 140, 80, 'Drop', (50, 50, 50), (255, 255, 255), 24)
    for i in range(len(player.inventory)):
        rect = pygame.Rect(10 + (i % 6) * 45, 40 + (i // 6) * 45, 40, 40)
        slots.append(rect)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), rect, 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.name}: {quest.description}', 20, 50 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 10, 10, 600, 600, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        rect = pygame.Rect(20 + (i % 3) * 180, 50 + (i // 3) * 40, 170, 30)
        txt(surf, f'{item.name} - {item.price}g', rect.x, rect.y, 24, (255, 255, 255))
        items.append(rect)
        buy_btn = btn(surf, rect.x, rect.y + 30, 170, 30, 'Buy', (50, 50, 50), (255, 255, 255), 24)
        buy_btns.append(buy_btn)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 10, 10, 600, 600, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        btn_rect = btn(surf, 20 + i * 180, 50, 170, 30, t, (50, 50, 50), (255, 255, 255), 24)
        tab_btns.append(btn_rect)
    for i, recipe in enumerate(recipes[tab]):
        rect = pygame.Rect(20 + (i % 3) * 180, 90 + (i // 3) * 60, 170, 50)
        txt(surf, f'{recipe.name}', rect.x, rect.y, 24, (255, 255, 255))
        craft_btn = btn(surf, rect.x, rect.y + 30, 170, 30, 'Craft', (50, 50, 50), (255, 255, 255), 24)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 10, 10, 600, 300, 'Dialogue')
    txt(surf, f'{npc.name}: {npc.dialogues[dial_idx]}', 20, 50, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        btn_rect = btn(surf, 20 + i * 180, 90 + i * 30, 170, 30, option['text'], (50, 50, 50), (255, 255, 255), 24)
        opt_btns.append(btn_rect)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'Paused')
    pause_btns = []
    pause_btns.append(btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 50, 280, 40, 'Resume', (50, 50, 50), (255, 255, 255), 24))
    pause_btns.append(btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 0, 280, 40, 'Save Game', (50, 50, 50), (255, 255, 255), 24))
    pause_btns.append(btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 40, 'Exit', (50, 50, 50), (255, 255, 255), 24))
    return pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 10, 10, 600, 300, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20 + (i % 3) * 180, 50 + (i // 3) * 60, 170, 50, building['name'], (50, 50, 50), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    xbtn_rect = panel(surf, surf.get_width() // 2 - 300, surf.get_height() // 2 - 300, 600, 600, 'World Map')
    mini_surf = pygame.Surface((128, 128))
    for y in range(len(WORLD_MAP)):
        for x in range(len(WORLD_MAP[y])):
            pygame.draw.rect(mini_surf, BIOME_COL[WORLD_MAP[y][x]], (x * 1, y * 1, 1, 1), 0)
    surf.blit(pygame.transform.scale(mini_surf, (600, 600)), (surf.get_width() // 2 - 300 + 5, surf.get_height() // 2 - 300 + 5))
    for town in TOWNS:
        pygame.draw.circle(surf, (255, 140, 0), (int(town['x'] / 8) + surf.get_width() // 2 - 300 + 5, int(town['y'] / 8) + surf.get_height() // 2 - 300 + 5), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (173, 216, 230), (int(city['x'] / 8) + surf.get_width() // 2 - 300 + 5, int(city['y'] / 8) + surf.get_height() // 2 - 300 + 5), 4)
    return xbtn_rect

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'Game Over')
    btn_rect = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 50, 280, 40, 'Restart', (50, 50, 50), (255, 255, 255), 24)
    return btn_rect

def draw_game_win(surf):
    surf.fill((0, 0, 0))
    panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, 'You Win!')
    btn_rect = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 50, 280, 40, 'Restart', (50, 50, 50), (255, 255, 255), 24)
    return btn_rect

def draw_player_stats(surf, player):
    panel(surf, 10, 10, 300, 150, 'Player Stats')
    txt(surf, f'Health: {player.health}/{player.max_health}', 20, 40, 24, (255, 255, 255))
    txt(surf, f'Mana: {player.mana}/{player.max_mana}', 20, 70, 24, (255, 255, 255))
    txt(surf, f'Level: {player.level}', 20, 100, 24, (255, 255, 255))

def draw_minimap(surf, player, WORLD_MAP, BIOME_COL):
    mini_surf = pygame.Surface((128, 128))
    for y in range(len(WORLD_MAP)):
        for x in range(len(WORLD_MAP[y])):
            pygame.draw.rect(mini_surf, BIOME_COL[WORLD_MAP[y][x]], (x * 1, y * 1, 1, 1), 0)
    surf.blit(pygame.transform.scale(mini_surf, (256, 256)), (surf.get_width() - 270, 10))
    pygame.draw.circle(surf, (255, 0, 0), (int(player.x / 8) + surf.get_width() - 270, int(player.y / 8) + 10), 3)

def draw_health_bar(surf, player):
    bar_length = 200
    bar_height = 20
    fill = (player.health / player.max_health) * bar_length
    outline_rect = pygame.Rect(10, surf.get_height() - 40, bar_length, bar_height)
    fill_rect = pygame.Rect(10, surf.get_height() - 40, fill, bar_height)
    pygame.draw.rect(surf, (255, 0, 0), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def draw_mana_bar(surf, player):
    bar_length = 200
    bar_height = 20
    fill = (player.mana / player.max_mana) * bar_length
    outline_rect = pygame.Rect(10, surf.get_height() - 70, bar_length, bar_height)
    fill_rect = pygame.Rect(10, surf.get_height() - 70, fill, bar_height)
    pygame.draw.rect(surf, (0, 0, 255), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def draw_experience_bar(surf, player):
    bar_length = 200
    bar_height = 20
    fill = (player.experience / player.next_level_exp) * bar_length
    outline_rect = pygame.Rect(10, surf.get_height() - 100, bar_length, bar_height)
    fill_rect = pygame.Rect(10, surf.get_height() - 100, fill, bar_height)
    pygame.draw.rect(surf, (255, 215, 0), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)
