import pygame
from collections import defaultdict

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
    if fill_w > 0:
        pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    pygame.draw.rect(surf, (100, 100, 100), (rx, ry, rw, rh), 2)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.Rect(rx + rw - 30, ry + 5, 20, 20)
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 0, 0), True)
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
    txt(surf, f"Gold: {player.gold}", 10, 100, 24, (255, 255, 255))
    txt(surf, f"LvL: {player.level} XP: {player.xp}/{player.next_level_xp}", 10, 130, 24, (255, 255, 255))
    txt(surf, f"Equipped: {player.equipped}", 10, 160, 24, (255, 255, 255))
    txt(surf, f"Biome: {player.biome}", 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x, min_y = max(0, player.x - 63), max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < len(WORLD_MAP) and 0 <= x < len(WORLD_MAP[y]):
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
    starfield = [(pygame.Color('white'), x, y) for x in range(0, surf.get_width(), 16) for y in range(0, surf.get_height(), 16)]
    for col, x, y in starfield:
        pygame.draw.circle(surf, col, (x, y), random.randint(1, 3))
    moon = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.circle(moon, (255, 255, 255, 128), (25, 25), 25)
    surf.blit(moon, (surf.get_width() - 70, 30))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 64, (255, 255, 255), True)
    btns = []
    for i, label in enumerate(['Start', 'Load Game', 'Exit']):
        b = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 4 + 100 + i * 60, 200, 50, label, (100, 100, 100), (255, 255, 255), 32)
        btns.append(b)
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    classes = ['Warrior', 'Mage', 'Rogue']
    btns = []
    for i, cls in enumerate(classes):
        x = surf.get_width() // 3 * (i % 3) + 50
        y = surf.get_height() // 4 * (i // 3) + 100
        pygame.draw.rect(surf, (100, 100, 100), (x, y, 200, 300), 0)
        txt(surf, cls, x + 100, y + 50, 48, (255, 255, 255), True)
        btns.append(pygame.Rect(x, y, 200, 300))
    return btns

def draw_inventory(surf, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Inventory')
    slots = []
    for i in range(20):
        x = 30 + (i % 5) * 75
        y = 60 + (i // 5) * 75
        pygame.draw.rect(surf, (100, 100, 100), (x, y, 70, 70), 2)
        slots.append(pygame.Rect(x, y, 70, 70))
    eq_btn = btn(surf, 350, 480, 150, 50, 'Equip', (100, 100, 100), (255, 255, 255), 32)
    drop_btn = btn(surf, 350, 540, 150, 50, 'Drop', (100, 100, 100), (255, 255, 255), 32)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 20, 60 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        txt(surf, f"{item.name}: {item.price} Gold", 20, 60 + i * 30, 24, (255, 255, 255))
        b = btn(surf, 250, 60 + i * 30, 100, 25, 'Buy', (100, 100, 100), (255, 255, 255), 24)
        buy_btns.append(b)
        items.append(item)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        b = btn(surf, 20 + i * 130, 60, 120, 50, t, (100, 100, 100), (255, 255, 255), 32)
        tab_btns.append(b)
    for i, recipe in enumerate(recipes[tab]):
        txt(surf, f"{recipe.name}: {recipe.cost} Gold", 20, 140 + i * 30, 24, (255, 255, 255))
        b = btn(surf, 250, 140 + i * 30, 100, 25, 'Craft', (100, 100, 100), (255, 255, 255), 24)
        craft_btns.append(b)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Dialogue')
    txt(surf, npc.dialogues[dial_idx], 20, 60, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        b = btn(surf, 20, 100 + i * 30, 360, 25, option['text'], (100, 100, 100), (255, 255, 255), 24)
        opt_btns.append(b)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0))
    panel(surf, 100, 100, 600, 380, 'Paused')
    pause_btns = []
    for i, label in enumerate(['Resume', 'Save Game', 'Exit']):
        b = btn(surf, 250, 180 + i * 60, 300, 50, label, (100, 100, 100), (255, 255, 255), 32)
        pause_btns.append(b)
    return panel(surf, 100, 100, 600, 380, 'Paused'), pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        b = btn(surf, 20 + i * 130, 60, 120, 50, building['name'], (100, 100, 100), (255, 255, 255), 32)
        type_btns.append(b)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 800, 600, 'World Map')
    for y in range(len(WORLD_MAP)):
        for x in range(len(WORLD_MAP[y])):
            pygame.draw.rect(surf, BIOME_COL[WORLD_MAP[y][x]], (x * 5, y * 5, 5, 5), 0)
    for town in TOWNS:
        pygame.draw.circle(surf, (255, 165, 0), (town.x * 5, town.y * 5), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (255, 0, 0), (city.x * 5, city.y * 5), 4)
    return xbtn_rect

def draw_gameover(surf):
    surf.fill((0, 0, 0))
    panel(surf, 100, 100, 600, 380, 'Game Over')
    btn(surf, 250, 240, 300, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)

def draw_player_sprite(surf, player):
    # Placeholder for drawing the player sprite
    pygame.draw.rect(surf, (255, 0, 0), (player.x, player.y, 32, 32))


if __name__ == '__main__':
    main()
