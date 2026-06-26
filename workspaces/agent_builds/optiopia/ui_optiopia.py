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
    pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

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
    mini_surf = pygame.Surface((126, 126))
    for x in range(WORLD_MAP.width):
        for y in range(WORLD_MAP.height):
            biome = WORLD_MAP.get_biome(x, y)
            color = BIOME_COL[biome]
            pygame.draw.rect(mini_surf, color, (x * 4, y * 4, 4, 4), 0)
    for enemy in enemies:
        ex, ey = enemy.pos
        pygame.draw.circle(mini_surf, (255, 0, 0), (ex // 16 * 4, ey // 16 * 4), 2)
    px, py = player.pos
    pygame.draw.circle(mini_surf, (0, 255, 0), (px // 16 * 4, py // 16 * 4), 3)
    surf.blit(mini_surf, (surf.get_width() - 136, 10))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 72, (255, 255, 255), True)
    btns = []
    btns.append(btn(surf, surf.get_width() // 3, surf.get_height() // 2 - 60, 200, 40, "Start", (100, 100, 100), (255, 255, 255), 24))
    btns.append(btn(surf, surf.get_width() // 3, surf.get_height() // 2, 200, 40, "Load", (100, 100, 100), (255, 255, 255), 24))
    btns.append(btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 60, 200, 40, "Exit", (100, 100, 100), (255, 255, 255), 24))
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    btns = []
    btns.append(btn(surf, 50, 100, 200, 300, "Warrior", (100, 100, 100), (255, 255, 255), 24))
    btns.append(btn(surf, 300, 100, 200, 300, "Mage", (100, 100, 100), (255, 255, 255), 24))
    btns.append(btn(surf, 550, 100, 200, 300, "Rogue", (100, 100, 100), (255, 255, 255), 24))
    return btns

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 50, 50, 700, 600, "Inventory")
    slots = []
    eq_btn = btn(surf, 300, 450, 100, 50, "Equip", (100, 100, 100), (255, 255, 255), 24)
    drop_btn = btn(surf, 450, 450, 100, 50, "Drop", (100, 100, 100), (255, 255, 255), 24)
    for i in range(len(player.inventory)):
        slots.append(btn(surf, 60 + (i % 8) * 70, 80 + (i // 8) * 70, 60, 60, player.inventory[i].name[:5], (100, 100, 100), (255, 255, 255), 18))
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 50, 50, 700, 600, "Quest Log")
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 60, 80 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 50, 50, 700, 600, "Shop")
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        btn_rect = btn(surf, 60 + (i % 4) * 180, 80 + (i // 4) * 70, 150, 50, f"Buy {item.name} - {item.price}", (100, 100, 100), (255, 255, 255), 20)
        buy_btns.append(btn_rect)
        items.append(item)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 50, 50, 700, 600, "Crafting")
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(["Weapons", "Armor", "Potions"]):
        tab_btns.append(btn(surf, 100 + i * 200, 80, 150, 40, t, (100, 100, 100), (255, 255, 255), 24))
    for i, recipe in enumerate(recipes[tab]):
        craft_btns.append(btn(surf, 60 + (i % 3) * 200, 150 + (i // 3) * 70, 180, 50, f"Craft {recipe.name}", (100, 100, 100), (255, 255, 255), 24))
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 50, 50, 700, 600, "Dialogue")
    txt(surf, f"{npc.name}: {npc.dialogues[dial_idx]}", 100, 80, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        opt_btns.append(btn(surf, 100 + i * 200, 300 + i * 40, 180, 40, option.text, (100, 100, 100), (255, 255, 255), 24))
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
    panel(surf, 300, 200, 200, 200, "Paused")
    pause_btns = []
    pause_btns.append(btn(surf, 350, 260, 100, 40, "Resume", (100, 100, 100), (255, 255, 255), 24))
    pause_btns.append(btn(surf, 350, 320, 100, 40, "Menu", (100, 100, 100), (255, 255, 255), 24))
    pause_btns.append(btn(surf, 350, 380, 100, 40, "Exit", (100, 100, 100), (255, 255, 255), 24))
    return panel(surf, 300, 200, 200, 200, "Paused"), pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 50, 50, 700, 600, f"{place_type} Panel")
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        type_btns.append(btn(surf, 100 + (i % 4) * 180, 80 + (i // 4) * 70, 150, 50, building.name, (100, 100, 100), (255, 255, 255), 24))
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    mini_surf = pygame.Surface((WORLD_MAP.width * 16, WORLD_MAP.height * 16))
    for x in range(WORLD_MAP.width):
        for y in range(WORLD_MAP.height):
            biome = WORLD_MAP.get_biome(x, y)
            color = BIOME_COL[biome]
            pygame.draw.rect(mini_surf, color, (x * 16, y * 16, 16, 16), 0)
    for town in TOWNS:
        tx, ty = town.pos
        pygame.draw.circle(mini_surf, (255, 255, 0), (tx * 16 + 8, ty * 16 + 8), 4)
    for city in CITIES:
        cx, cy = city.pos
        pygame.draw.circle(mini_surf, (0, 255, 255), (cx * 16 + 8, cy * 16 + 8), 6)
    px, py = player.pos
    pygame.draw.circle(mini_surf, (0, 255, 0), (px // 16 * 16 + 8, py // 16 * 16 + 8), 3)
    surf.blit(mini_surf, (surf.get_width() // 2 - WORLD_MAP.width * 8, surf.get_height() // 2 - WORLD_MAP.height * 8))
    return panel(surf, surf.get_width() // 2 - WORLD_MAP.width * 8, surf.get_height() // 2 - WORLD_MAP.height * 8 - 50, WORLD_MAP.width * 16, 40, "World Map")

def draw_gameover(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Game Over", surf.get_width() // 2, surf.get_height() // 3, 72, (255, 255, 255))
    btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, "Restart", (100, 100, 100), (255, 255, 255), 36)

def draw_player(surf, player):
    # Placeholder for drawing the player
    pygame.draw.circle(surf, (255, 0, 0), (player.x, player.y), 10)

def draw_npc(surf, npc):
    # Placeholder for drawing an NPC
    pygame.draw.circle(surf, (0, 0, 255), (npc.x, npc.y), 8)

def draw_item(surf, item):
    # Placeholder for drawing an item
    pygame.draw.rect(surf, (0, 255, 0), (item.x, item.y, 16, 16))

# Example usage:
# import pygame
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# player = Player(400, 300)
# draw_player(screen, player)
# pygame.display.flip()