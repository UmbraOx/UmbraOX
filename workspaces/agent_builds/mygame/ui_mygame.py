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
    inner_w = int(w * val / mx)
    pygame.draw.rect(surf, col, (x, y, inner_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.Rect(rx + rw - 30, ry + 5, 20, 20)
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 0, 0))
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (100, 0, 0))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (0, 0, 100))
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (0, 255, 0), (0, 100, 0))
    txt(surf, f"Gold: {player.gold}", 10, 100, 24, (255, 255, 255))
    txt(surf, f"LvL: {player.level} XP: {player.xp}/{player.next_level_xp}", 10, 130, 24, (255, 255, 255))
    txt(surf, f"Equipped: {player.equipped}", 10, 160, 24, (255, 255, 255))
    txt(surf, f"Biome: {player.biome}", 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x = max(0, player.x - 63)
    min_y = max(0, player.y - 63)
    sub_map = WORLD_MAP[min_y:min_y+126, min_x:min_x+126]
    for y in range(sub_map.shape[0]):
        for x in range(sub_map.shape[1]):
            pygame.draw.rect(surf, BIOME_COL[sub_map[y, x]], (x + surf.get_width() - 126, y, 1, 1))
    pygame.draw.circle(surf, (255, 0, 0), (surf.get_width() - 63 + player.x % 126, 63 + player.y % 126), 3)
    for enemy in enemies:
        ex = surf.get_width() - 63 + (enemy.x - min_x) % 126
        ey = 63 + (enemy.y - min_y) % 126
        pygame.draw.circle(surf, (0, 255, 0), (ex, ey), 2)

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 64, (255, 255, 255), True)
    pygame.draw.circle(surf, (193, 217, 230), (surf.get_width() // 2, surf.get_height() // 2 - 100), 50)
    btns = []
    y_offset = surf.get_height() // 2 + 50
    for label in ['Start', 'Load Game', 'Exit']:
        b = btn(surf, surf.get_width() // 2 - 100, y_offset, 200, 40, label, (50, 50, 50), (255, 255, 255), 32)
        btns.append(b)
        y_offset += 60
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    class_cards = [(100, 100, 200, 200), (400, 100, 200, 200), (700, 100, 200, 200)]
    for card in class_cards:
        pygame.draw.rect(surf, (50, 50, 50), card, 0)
    return [pygame.Rect(card) for card in class_cards]

def draw_inventory(surf, player, selected):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 300, 580, 'Inventory')
    slots = []
    eq_btn = btn(surf, 10, 600, 140, 40, 'Equip', (50, 50, 50), (255, 255, 255), 32)
    drop_btn = btn(surf, 160, 600, 140, 40, 'Drop', (50, 50, 50), (255, 255, 255), 32)
    for i in range(10):
        slots.append(pygame.Rect(20 + (i % 5) * 60, 40 + (i // 5) * 60, 50, 50))
        pygame.draw.rect(surf, (70, 70, 70), slots[-1], 0)
    if selected is not None:
        pygame.draw.rect(surf, (255, 255, 0), slots[selected], 3)
    return xbtn, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 300, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 20, 40 + i * 30, 24, (255, 255, 255))
    return xbtn

def draw_shop(surf, npc, player, selected):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 300, 580, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.items):
        txt(surf, f"{item.name}: {item.price} Gold", 20, 40 + i * 30, 24, (255, 255, 255))
        b = btn(surf, 180, 40 + i * 30, 100, 24, 'Buy', (50, 50, 50), (255, 255, 255), 24)
        buy_btns.append(b)
        items.append(item)
    if selected is not None:
        pygame.draw.rect(surf, (255, 255, 0), buy_btns[selected], 3)
    return xbtn, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 300, 580, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        b = btn(surf, 20 + i * 90, 40, 80, 30, t, (50, 50, 50), (255, 255, 255), 24)
        tab_btns.append(b)
    for i, recipe in enumerate(recipes[tab]):
        txt(surf, f"{recipe.name}", 20, 80 + i * 30, 24, (255, 255, 255))
        b = btn(surf, 180, 80 + i * 30, 100, 24, 'Craft', (50, 50, 50), (255, 255, 255), 24)
        craft_btns.append(b)
    if selected is not None:
        pygame.draw.rect(surf, (255, 255, 0), craft_btns[selected], 3)
    return xbtn, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 300, 580, 'Dialogue')
    txt(surf, f"{npc.name}: {npc.dialogues[dial_idx]}", 20, 40, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options):
        b = btn(surf, 20, 80 + i * 30, 260, 24, option.text, (50, 50, 50), (255, 255, 255), 24)
        opt_btns.append(b)
    return xbtn, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 300, 580, 'Paused')
    pause_btns = []
    for i, label in enumerate(['Resume', 'Save Game', 'Exit']):
        b = btn(surf, 20, 40 + i * 60, 260, 50, label, (50, 50, 50), (255, 255, 255), 32)
        pause_btns.append(b)
    return xbtn, pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 300, 580, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        b = btn(surf, 20, 40 + i * 60, 260, 50, building.name, (50, 50, 50), (255, 255, 255), 32)
        type_btns.append(b)
    return xbtn, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 800, 600, 'World Map')
    for y in range(WORLD_MAP.shape[0]):
        for x in range(WORLD_MAP.shape[1]):
            pygame.draw.rect(surf, BIOME_COL[WORLD_MAP[y, x]], (x * 2, y * 2, 2, 2))
    for town in TOWNS:
        pygame.draw.circle(surf, (255, 0, 0), (town.x * 2, town.y * 2), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (0, 0, 255), (city.x * 2, city.y * 2), 4)
    return xbtn

def draw_gameover(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Game Over', surf.get_width() // 2, surf.get_height() // 2 - 50, 64, (255, 0, 0), True)
    btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 40, 'Restart', (50, 50, 50), (255, 255, 255), 32)

def draw_player_sprite(surf, sx, sy, cls, crouching):
    if crouching:
        sprite = pygame.image.load(f'sprites/{cls}_crouch.png')
    else:
        sprite = pygame.image.load(f'sprites/{cls}.png')
    surf.blit(sprite, (sx - sprite.get_width() // 2, sy - sprite.get_height()))

def draw_enemy_sprite(surf, sx, sy, edef):
    sprite = pygame.image.load(f'enemies/{edef.name}.png')
    surf.blit(sprite, (sx - sprite.get_width() // 2, sy - sprite.get_height()))

def draw_npc_sprite(surf, sx, sy, job):
    sprite = pygame.image.load(f'npcs/{job}.png')