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
    surf.blit(txt_surf, rect.topleft)
    return rect

def bar(surf, x, y, w, h, val, mx, col, bg):
    pygame.draw.rect(surf, bg, (x, y, w, h), 0)
    fill_w = int(w * val / mx)
    if fill_w > 0:
        pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

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
    txt(surf, f'Lvl: {player.level} XP: {player.xp}/{player.next_level_xp}', 10, 130, 24, (255, 255, 255))
    txt(surf, f'Equipped: {player.equipped}', 10, 160, 24, (255, 255, 255))
    txt(surf, f'Biome: {player.biome}', 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    mini_surf = pygame.Surface((126, 126))
    for x in range(WORLD_MAP.width):
        for y in range(WORLD_MAP.height):
            biome = WORLD_MAP.get_biome(x, y)
            color = BIOME_COL[biome]
            pygame.draw.rect(mini_surf, color, (x * 4, y * 4, 4, 4), 0)
    for enemy in enemies:
        ex, ey = int(enemy.x / WORLD_MAP.width * 126), int(enemy.y / WORLD_MAP.height * 126)
        pygame.draw.circle(mini_surf, (255, 0, 0), (ex, ey), 2)
    px, py = int(player.x / WORLD_MAP.width * 126), int(player.y / WORLD_MAP.height * 126)
    pygame.draw.circle(mini_surf, (0, 255, 0), (px, py), 3)
    surf.blit(mini_surf, (surf.get_width() - 136, 10))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    starfield = [pygame.Rect(x, y, 2, 2) for x in range(0, surf.get_width(), 15) for y in range(0, surf.get_height(), 15)]
    for star in starfield:
        pygame.draw.rect(surf, (255, 255, 255), star)
    moon = pygame.Surface((64, 64))
    pygame.draw.circle(moon, (255, 255, 255), (32, 32), 30)
    surf.blit(moon, (surf.get_width() - 84, 10))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 64, (255, 255, 255), True)
    play_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Play', (0, 128, 0), (255, 255, 255), 36)
    load_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Load', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 140, 200, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return [play_btn, load_btn, quit_btn]

def draw_class_select(surf):
    class_cards = [
        {'name': 'Warrior', 'portrait': pygame.Surface((100, 100)), 'x': 100, 'y': 150},
        {'name': 'Mage', 'portrait': pygame.Surface((100, 100)), 'x': 300, 'y': 150},
        {'name': 'Rogue', 'portrait': pygame.Surface((100, 100)), 'x': 500, 'y': 150}
    ]
    for card in class_cards:
        pygame.draw.rect(surf, (50, 50, 50), (card['x'], card['y'], 200, 300), 0)
        pygame.draw.rect(surf, (100, 100, 100), (card['x'], card['y'], 200, 300), 2)
        surf.blit(card['portrait'], (card['x'] + 50, card['y'] + 20))
        txt(surf, card['name'], card['x'] + 100, card['y'] + 140, 36, (255, 255, 255), True)
    return [pygame.Rect(card['x'], card['y'], 200, 300) for card in class_cards]

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Inventory')
    slots = [pygame.Rect(20 + (i % 10) * 36, 40 + (i // 10) * 36, 32, 32) for i in range(player.inventory_size)]
    eq_btn = btn(surf, 10, 550, 190, 30, 'Equip', (0, 128, 0), (255, 255, 255), 24)
    drop_btn = btn(surf, 210, 550, 190, 30, 'Drop', (255, 0, 0), (255, 255, 255), 24)
    for i, slot in enumerate(slots):
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), slot, 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.name}: {quest.description}', 20, 40 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Shop')
    items = [pygame.Rect(20 + (i % 3) * 190, 40 + (i // 3) * 70, 180, 60) for i in range(len(npc.inventory))]
    buy_btns = []
    for i, item in enumerate(items):
        txt(surf, npc.inventory[i].name, item.x + 5, item.y + 5, 24, (255, 255, 255))
        txt(surf, f'Price: {npc.inventory[i].price}', item.x + 5, item.y + 30, 18, (255, 255, 255))
        buy_btn = btn(surf, item.right + 10, item.y + 10, 60, 40, 'Buy', (0, 128, 0), (255, 255, 255), 20)
        buy_btns.append(buy_btn)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Crafting')
    tab_btns = [btn(surf, 20 + i * 100, 40, 90, 30, t, (0, 128, 0), (255, 255, 255), 20) for i, t in enumerate(['Weapons', 'Armor', 'Potions'])]
    craft_btns = []
    recipes_displayed = [r for r in recipes if r.category == tab]
    for i, recipe in enumerate(recipes_displayed):
        txt(surf, recipe.name, 20, 80 + i * 60, 24, (255, 255, 255))
        craft_btn = btn(surf, 300, 80 + i * 60, 100, 40, 'Craft', (0, 128, 0), (255, 255, 255), 20)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 10, 10, 600, 300, 'Dialogue')
    txt(surf, f'{npc.name}: {npc.dialogues[dial_idx]}', 20, 40, 24, (255, 255, 255))
    opt_btns = [btn(surf, 20 + i * 150, 230, 140, 40, opt, (0, 128, 0), (255, 255, 255), 20) for i, opt in enumerate(npc.options[dial_idx])]
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
    panel_rect = pygame.Rect(surf.get_width() // 4, surf.get_height() // 3, surf.get_width() // 2, surf.get_height() // 3)
    pygame.draw.rect(surf, (50, 50, 50), panel_rect, 0)
    pygame.draw.rect(surf, (100, 100, 100), panel_rect, 2)
    txt(surf, 'Paused', surf.get_width() // 2, surf.get_height() // 3 + 20, 48, (255, 255, 255), True)
    resume_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 3 + 90, 200, 50, 'Resume', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 3 + 160, 200, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return panel_rect, [resume_btn, quit_btn]

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 10, 10, 400, 580, f'Build {place_type}')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = pygame.Rect(20 + (i % 3) * 120, 40 + (i // 3) * 70, 110, 60)
        txt(surf, building.name, btn_rect.x + 5, btn_rect.y + 5, 24, (255, 255, 255))
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf):
    # Placeholder for world map drawing logic
    pass

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Game Over', surf.get_width() // 2, surf.get_height() // 2 - 50, 72, (255, 0, 0), True)
    restart_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 30, 200, 50, 'Restart', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 100, 200, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return [restart_btn, quit_btn]

def draw_victory(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Victory!', surf.get_width() // 2, surf.get_height() // 2 - 50, 72, (0, 128, 0), True)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 30, 200, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return [quit_btn]

def draw_player_stats(surf, player):
    panel_rect = pygame.Rect(10, 10, 200, 180)
    pygame.draw.rect(surf, (50, 50, 50), panel_rect, 0)
    pygame.draw.rect(surf, (100, 100, 100), panel_rect, 2)
    txt(surf, f'HP: {player.hp}/{player.max_hp}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', 20, 60, 24, (255, 255, 255))
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 20, 90, 24, (255, 255, 255))
    txt(surf, f'Lvl: {player.level}', 20, 120, 24, (255, 255, 255))

def draw_minimap(surf, player, world_map):
    # Placeholder for minimap drawing logic
    pass

def draw_hud(surf, player, world_map):
    draw_player_stats(surf, player)
    draw_minimap(surf, player, world_map)

def txt(surface, text, x, y, size, color, center=False):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    if center:
        rect = text_surface.get_rect(center=(x, y))
    else:
        rect = text_surface.get_rect(topleft=(x, y))