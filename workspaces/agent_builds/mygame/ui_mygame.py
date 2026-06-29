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
    txt(surf, 'X', rx + rw - 28, ry + 7, 16, (255, 0, 0), True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (50, 50, 50))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (50, 50, 50))
    txt(surf, f"Gold: {player.gold}", 10, 70, 24, (255, 255, 0))
    txt(surf, f"LvL: {player.level} XP: {player.xp}/{player.next_level_xp}", 10, 100, 24, (255, 255, 255))
    txt(surf, f"Equipped: {player.equipped}", 10, 130, 24, (255, 255, 255))
    txt(surf, f"Biome: {player.biome}", 10, 160, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x, min_y = max(0, player.x - 63), max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < WORLD_MAP.height and 0 <= x < WORLD_MAP.width:
                biome = WORLD_MAP.get_biome(x, y)
                surf.set_at((x - min_x + surf.get_width() - 126, y - min_y), BIOME_COL[biome])
    for enemy in enemies:
        ex, ey = enemy.x - min_x, enemy.y - min_y
        if 0 <= ex < 126 and 0 <= ey < 126:
            surf.set_at((ex + surf.get_width() - 126, ey), (255, 0, 0))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, "Starfield Background", surf.get_width() // 2, surf.get_height() // 4, 36, (255, 255, 255), True)
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4 + 50, 72, (255, 215, 0), True)
    btns = [
        btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, "Start", (0, 128, 0), (255, 255, 255), 36),
        btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, "Load", (0, 128, 0), (255, 255, 255), 36),
        btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 140, 200, 50, "Exit", (255, 0, 0), (255, 255, 255), 36)
    ]
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    class_cards = [
        {'name': 'Warrior', 'portrait': pygame.Surface((100, 100)), 'rect': pygame.Rect(50, 50, 200, 300)},
        {'name': 'Mage', 'portrait': pygame.Surface((100, 100)), 'rect': pygame.Rect(300, 50, 200, 300)},
        {'name': 'Rogue', 'portrait': pygame.Surface((100, 100)), 'rect': pygame.Rect(550, 50, 200, 300)}
    ]
    for card in class_cards:
        pygame.draw.rect(surf, (50, 50, 50), card['rect'], 0)
        surf.blit(card['portrait'], (card['rect'].x + 50, card['rect'].y + 20))
        txt(surf, card['name'], card['rect'].centerx, card['rect'].centery + 100, 36, (255, 255, 255), True)
    return [card['rect'] for card in class_cards]

def draw_inventory(surf, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 400, "Inventory")
    slots = []
    eq_btn = btn(surf, 10, 420, 145, 50, "Equip", (0, 128, 0), (255, 255, 255), 36)
    drop_btn = btn(surf, 165, 420, 145, 50, "Drop", (255, 0, 0), (255, 255, 255), 36)
    for i in range(10):
        slot_rect = pygame.Rect(20 + (i % 5) * 55, 40 + (i // 5) * 55, 50, 50)
        slots.append(slot_rect)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), slot_rect, 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, "Quest Log")
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 20, 40 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, "Shop")
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        txt(surf, f"{item.name}: {item.price} Gold", 20, 40 + i * 30, 24, (255, 255, 255))
        buy_btn = btn(surf, 250, 40 + i * 30, 100, 25, "Buy", (0, 128, 0), (255, 255, 255), 24)
        buy_btns.append(buy_btn)
        items.append(item)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, "Crafting")
    tab_btns = [
        btn(surf, 20, 40, 100, 30, "Weapons", (0, 128, 0), (255, 255, 255), 24),
        btn(surf, 140, 40, 100, 30, "Armor", (0, 128, 0), (255, 255, 255), 24),
        btn(surf, 260, 40, 100, 30, "Potions", (0, 128, 0), (255, 255, 255), 24)
    ]
    craft_btns = []
    for i, recipe in enumerate(recipes[tab]):
        txt(surf, f"{recipe.name}: {recipe.cost} Gold", 20, 80 + i * 30, 24, (255, 255, 255))
        craft_btn = btn(surf, 250, 80 + i * 30, 100, 25, "Craft", (0, 128, 0), (255, 255, 255), 24)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, "Dialogue")
    txt(surf, f"{npc.name}: {npc.dialogues[dial_idx]}", 20, 40, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        opt_btn = btn(surf, 20, 80 + i * 30, 150, 25, option['text'], (0, 128, 0), (255, 255, 255), 24)
        opt_btns.append(opt_btn)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 250, "Paused")
    pause_btns = [
        btn(surf, 20, 40, 260, 50, "Resume", (0, 128, 0), (255, 255, 255), 36),
        btn(surf, 20, 100, 260, 50, "Save", (0, 128, 0), (255, 255, 255), 36),
        btn(surf, 20, 160, 260, 50, "Exit", (255, 0, 0), (255, 255, 255), 36)
    ]
    return xbtn_rect, pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, f"{place_type} Panel")
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20, 40 + i * 60, 360, 50, building['name'], (0, 128, 0), (255, 255, 255), 36)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 600, 450, "World Map")
    for town in TOWNS:
        pygame.draw.circle(surf, (255, 255, 0), (town.x, town.y), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (255, 165, 0), (city.x, city.y), 5)
    return xbtn_rect

def draw_gameover(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Game Over", surf.get_width() // 2, surf.get_height() // 3, 72, (255, 0, 0), True)
    btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, "Restart", (0, 128, 0), (255, 255, 255), 36)
    btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, "Exit", (255, 0, 0), (255, 255, 255), 36)

def draw_player_sprite(surf, player):
    # Placeholder for drawing the player sprite
    pygame.draw.rect(surf, (255, 0, 0), (player.x, player.y, 32, 32))

def draw_npc_sprite(surf, npc):
    # Placeholder for drawing an NPC sprite
    pygame.draw.rect(surf, (0, 0, 255), (npc.x, npc.y, 32, 32))

def draw_item_icon(surf, item, x, y):
    # Placeholder for drawing an item icon
    pygame.draw.circle(surf, (192, 192, 192), (x + 16, y + 16), 10)
    txt(surf, item.name[0], x + 8, y + 4, 24, (0, 0, 0))

def draw_ui_elements(surf, player):
    # Draw health bar
    pygame.draw.rect(surf, (255, 0, 0), (10, 10, 200 * (player.health / player.max_health), 30))
    pygame.draw.rect(surf, (255, 255, 255), (10, 10, 200, 30), 2)
    txt(surf, f"Health: {player.health}/{player.max_health}", 10, 45, 24, (255, 255, 255))

    # Draw mana bar
    pygame.draw.rect(surf, (0, 0, 255), (10, 70, 200 * (player.mana / player.max_mana), 30))
    pygame.draw.rect(surf, (255, 255, 255), (10, 70, 200, 30), 2)
    txt(surf, f"Mana: {player.mana}/{player.max_mana}", 10, 105, 24, (255, 255, 255))

    # Draw inventory icons
    for i in range(len(player.inventory)):
        draw_item_icon(surf, player.inventory[i], 10 + i * 36, 140)

def txt(surface, text, x, y, size, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)