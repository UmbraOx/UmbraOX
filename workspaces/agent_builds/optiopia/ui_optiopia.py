import pygame
from pygame.locals import *

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
    fill_w = int(w * min(1, max(0, val)))
    pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    pygame.draw.rect(surf, (200, 200, 200), (rx, ry, rw, rh), 1)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.Rect(rx + rw - 30, ry + 5, 20, 20)
    txt(surf, 'X', rx + rw - 27, ry + 8, 16, (255, 0, 0), True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    pygame.draw.rect(surf, (255, 255, 255), (x, y, w, h), 1)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp / player.max_hp, 0, (255, 0, 0), (50, 50, 50))
    bar(surf, 10, 40, 200, 20, player.mp / player.max_mp, 0, (0, 0, 255), (50, 50, 50))
    bar(surf, 10, 70, 200, 20, player.sta / player.max_sta, 0, (0, 255, 0), (50, 50, 50))
    txt(surf, f"Gold: {player.gold}", 10, 100, 24, (255, 255, 0))
    txt(surf, f"LvL: {player.level} XP: {player.xp}/{player.next_level_xp}", 10, 130, 24, (255, 255, 255))
    txt(surf, f"Equipped: {player.equipped}", 10, 160, 24, (255, 255, 255))
    txt(surf, f"Biome: {player.biome}", 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    minimap_surf = pygame.Surface((126, 126))
    for x in range(WORLD_MAP.width):
        for y in range(WORLD_MAP.height):
            biome = WORLD_MAP.get_biome(x, y)
            color = BIOME_COL[biome]
            pygame.draw.rect(minimap_surf, color, (x * 4, y * 4, 4, 4))
    for enemy in enemies:
        ex, ey = int(enemy.x / WORLD_MAP.width * 126), int(enemy.y / WORLD_MAP.height * 126)
        pygame.draw.circle(minimap_surf, (255, 0, 0), (ex, ey), 3)
    px, py = int(player.x / WORLD_MAP.width * 126), int(player.y / WORLD_MAP.height * 126)
    pygame.draw.circle(minimap_surf, (0, 255, 0), (px, py), 4)
    surf.blit(minimap_surf, (surf.get_width() - 136, 10))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    starfield = [(pygame.Color('white'), pygame.Rect(x, y, 2, 2)) for x in range(0, surf.get_width(), 20) for y in range(0, surf.get_height(), 20)]
    for color, rect in starfield:
        pygame.draw.rect(surf, color, rect)
    moon = pygame.Surface((100, 100), SRCALPHA)
    pygame.draw.circle(moon, (255, 255, 255, 128), (50, 50), 40)
    surf.blit(moon, (surf.get_width() - 150, 50))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 3, 64, (255, 255, 255), True)
    btns = [
        btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, "Start", (0, 128, 0), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 120, 200, 50, "Load", (0, 0, 128), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 190, 200, 50, "Exit", (128, 0, 0), (255, 255, 255), 32)
    ]
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    class_cards = [
        (surf.get_width() // 4 - 100, surf.get_height() // 3, 200, 200),
        (surf.get_width() // 2 - 100, surf.get_height() // 3, 200, 200),
        (surf.get_width() * 3 // 4 - 100, surf.get_height() // 3, 200, 200)
    ]
    for i, (x, y, w, h) in enumerate(class_cards):
        pygame.draw.rect(surf, (50, 50, 50), (x, y, w, h), 0)
        pygame.draw.rect(surf, (255, 255, 255), (x, y, w, h), 1)
        txt(surf, f"Class {i+1}", x + w // 2, y + 30, 32, (255, 255, 255), True)
    return class_cards

def draw_inventory(surf, player, selected):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, "Inventory")
    slots = []
    for i in range(10):
        x, y = 20 + (i % 5) * 76, 40 + (i // 5) * 76
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 70, 70), 0)
        pygame.draw.rect(surf, (255, 255, 255), (x, y, 70, 70), 1)
        slots.append(pygame.Rect(x, y, 70, 70))
    eq_btn = btn(surf, 340, 160, 60, 30, "Equip", (0, 128, 0), (255, 255, 255), 16)
    drop_btn = btn(surf, 340, 200, 60, 30, "Drop", (128, 0, 0), (255, 255, 255), 16)
    return panel_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((0, 0, 0))
    xbtn = panel(surf, 10, 10, 400, 380, "Quest Log")
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 20, 40 + i * 30, 24, (255, 255, 255))
    return xbtn

def draw_shop(surf, npc, player, selected):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, "Shop")
    buy_btns = []
    items = [(50 + (i % 2) * 190, 40 + (i // 2) * 60, f"Item {i+1}") for i in range(4)]
    for i, (x, y, name) in enumerate(items):
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 180, 50), 0)
        pygame.draw.rect(surf, (255, 255, 255), (x, y, 180, 50), 1)
        txt(surf, name, x + 90, y + 25, 24, (255, 255, 255), True)
        buy_btns.append(btn(surf, x + 130, y + 60, 50, 30, "Buy", (0, 128, 0), (255, 255, 255), 16))
    return panel_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, "Crafting")
    tab_btns = [
        btn(surf, 20, 40, 60, 30, "Weapons", (50, 50, 50), (255, 255, 255), 16),
        btn(surf, 90, 40, 60, 30, "Armor", (50, 50, 50), (255, 255, 255), 16),
        btn(surf, 160, 40, 60, 30, "Potions", (50, 50, 50), (255, 255, 255), 16)
    ]
    craft_btns = []
    for i, recipe in enumerate(recipes):
        x, y = 20 + (i % 3) * 120, 90 + (i // 3) * 70
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 110, 60), 0)
        pygame.draw.rect(surf, (255, 255, 255), (x, y, 110, 60), 1)
        txt(surf, recipe.name, x + 55, y + 30, 24, (255, 255, 255), True)
        craft_btns.append(btn(surf, x + 30, y + 65, 50, 30, "Craft", (0, 128, 0), (255, 255, 255), 16))
    return panel_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, "Dialogue")
    txt(surf, npc.dialogues[dial_idx], 20, 40, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options):
        btn_rect = btn(surf, 20, 100 + i * 30, 380, 30, option.text, (50, 50, 50), (255, 255, 255), 16)
        opt_btns.append(btn_rect)
    return panel_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, "Paused")
    pause_btns = [
        btn(surf, 20, 50, 380, 50, "Resume", (0, 128, 0), (255, 255, 255), 32),
        btn(surf, 20, 120, 380, 50, "Save & Exit", (0, 0, 128), (255, 255, 255), 32)
    ]
    return panel_rect, pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, f"{place_type} Panel")
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20 + (i % 2) * 190, 50 + (i // 2) * 60, 180, 50, building.name, (50, 50, 50), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return panel_rect, type_btns

def draw_world_map(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, "World Map")
    # Placeholder for world map drawing logic
    return panel_rect

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Game Over", surf.get_width() // 2, surf.get_height() // 2 - 50, 48, (255, 0, 0), True)
    btn_rect = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 30, 200, 50, "Restart", (0, 128, 0), (255, 255, 255), 32)
    return btn_rect

def draw_player_stats(surf, player):
    panel_rect = panel(surf, surf.get_width() - 220, 10, 210, 150, "Player Stats")
    txt(surf, f"HP: {player.hp}/{player.max_hp}", surf.get_width() - 210 + 10, 40, 24, (255, 0, 0))
    txt(surf, f"MP: {player.mp}/{player.max_mp}", surf.get_width() - 210 + 10, 70, 24, (0, 0, 255))
    txt(surf, f"XP: {player.xp}/{player.next_level_xp}", surf.get_width() - 210 + 10, 100, 24, (255, 255, 0))
    txt(surf, f"Lvl: {player.level}", surf.get_width() - 210 + 10, 130, 24, (255, 255, 255))

def draw_player_inventory(surf, player):
    panel_rect = panel(surf, surf.get_width() - 220, 170, 210, 220, "Inventory")
    for i in range(4):  # Assuming a simple grid of 4 items
        x, y = surf.get_width() - 210 + (i % 2) * 95, 180 + (i // 2) * 95
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 90, 90), 0)
        pygame.draw.rect(surf, (255, 255, 255), (x, y, 90, 90), 1)

def draw_player_equipment(surf, player):
    panel_rect = panel(surf, surf.get_width() - 220, 400, 210, 180, "Equipment")
    # Placeholder for equipment drawing logic

def draw_minimap(surf, world_map, player_position):
    mini_map_size = (150, 150)
    mini_map_surface = pygame.Surface(mini_map_size)
    mini_map_surface.fill((0, 0, 0))
    # Draw the world map on a smaller scale
    for x in range(world_map.width):
        for y in range(world_map.height):
            tile_color = (255, 255, 255) if world_map.get_tile(x, y).walkable else (128, 128, 128)
            pygame.draw.rect(mini_map_surface, tile_color, (x * mini_map_size[0] // world_map.width, y * mini_map_size[1] // world_map.height, mini_map_size[0] // world_map.width, mini_map_size[1] // world_map.height), 0)
    # Draw the player position
    pygame.draw.circle(mini_map_surface, (255, 0, 0), (player_position.x * mini_map_size[0] // world_map.width, player_position.y * mini_map_size[1] // world_map.height), 3)
    surf.blit(mini_map_surface, (surf.get_width() - 160, surf.get_height() - 160))

def draw_player_health_bar(surf, player):
    bar_width = 200
    bar_height = 20
    x = 10
    y = 10
    pygame.draw.rect(surf, (255, 0, 0), (x, y, bar_width * player.hp / player.max_hp, bar_height))
    pygame.draw.rect(surf, (255, 255, 255), (x, y, bar_width, bar_height), 2)

def draw_player_mana_bar(surf, player):
    bar_width = 200
    bar_height = 20
    x = 10
    y = 40
    pygame.draw.rect(surf, (0, 0, 255), (x, y, bar_width * player.mp / player.max_mp, bar_height))
    pygame.draw.rect(surf, (255, 255, 255), (x, y, bar_width, bar_height), 2)

def draw_experience_bar(surf, player):
    bar_width = 200
    bar_height = 20
    x = 10
    y = 70
    pygame.draw.rect(surf, (255, 255, 0), (x, y, bar_width * player.xp / player.next_level_xp, bar_height))
    pygame.draw.rect(surf, (255, 255, 255), (x, y, bar_width, bar_height), 2)

def draw_level_indicator(surf, player):
    txt(surf, f"Lvl: {player.level}", 10, 100, 24, (255, 255, 255))

def draw_gold_counter(surf, player):
    txt(surf, f"Gold: {player.gold}", surf.get_width() - 100, 10, 24, (255, 255, 0), True)

def draw_quest_indicator(surf, player):
    txt(surf, f"Quests: {len(player.quests)}", surf.get_width() - 100, 40, 24, (255, 255, 255), True)

def draw_time_of_day(surf, time_of_day):
    txt(surf, f"Time: {time_of_day}", surf.get_width() // 2, 10, 24, (255, 255, 255), True)

def draw_weather_indicator(surf, weather):
    txt(surf, f"Weather: {weather}", surf.get_width() // 2, 40, 24, (255, 255, 255), True)

def draw_debug_info(surf, debug_info):
    y = 10
    for line in debug_info:
        txt(surf, line, 10, y, 20, (255, 255, 255))
        y += 20

def draw_game_ui(surf, player, world_map, time_of_day, weather, debug_info):
    draw_player_stats(surf, player)
    draw_player_inventory(surf, player)
    draw_player_equipment(surf, player)
    draw_minimap(surf, world_map, player.position)
    draw_player_health_bar(surf, player)
    draw_player_mana_bar(surf, player)
    draw_experience_bar(surf, player)
    draw_level_indicator(surf, player)
    draw_gold_counter(surf, player)
    draw_quest_indicator(surf, player)
    draw_time_of_day(surf, time_of_day)
    draw_weather_indicator(surf, weather)
    draw_debug_info(surf, debug_info)

def txt(surface, text, x, y, font_size=24, color=(255, 255, 255), center=False):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)

def btn(surface, x, y, width, height, text, bg_color=(50, 50, 50), text_color=(255, 255, 255)):
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    txt(surface, text, x + width // 2, y + height // 2, center=True)
    return pygame.Rect(x, y, width, height)

def panel(surface, x, y, width, height, title=""):
    pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
    txt(surface, title, x + 10, y + 5)
    return pygame.Rect(x, y, width, height)

def draw_world_map(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, 10, 400, 380, "World Map")
    # Placeholder for world map drawing logic
    return panel_rect

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Game Over", surf.get_width() // 2, surf.get_height() // 2 - 50, 48, (255, 0, 0), True)
    restart_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 30, 200, 50, "Restart", (0, 128, 0), (255, 255, 255))
    return restart_btn

def draw_pause_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Pause Menu")
    resume_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Resume", (0, 128, 0), (255, 255, 255))
    options_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Options", (0, 128, 0), (255, 255, 255))
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Quit", (255, 0, 0), (255, 255, 255))
    return panel_rect, resume_btn, options_btn, quit_btn

def draw_options_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Options")
    volume_slider = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Volume: 50%", (0, 128, 0), (255, 255, 255))
    fullscreen_toggle = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Fullscreen: Off", (0, 128, 0), (255, 255, 255))
    back_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Back", (0, 128, 0), (255, 255, 255))
    return panel_rect, volume_slider, fullscreen_toggle, back_btn

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Loading...", surf.get_width() // 2, surf.get_height() // 2, 48, (255, 255, 255), True)

def draw_main_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Main Menu")
    start_game_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Start Game", (0, 128, 0), (255, 255, 255))
    load_game_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Load Game", (0, 128, 0), (255, 255, 255))
    options_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Options", (0, 128, 0), (255, 255, 255))
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 105, 280, 50, "Quit", (255, 0, 0), (255, 255, 255))
    return panel_rect, start_game_btn, load_game_btn, options_btn, quit_btn

def draw_credits(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Credits", surf.get_width() // 2, surf.get_height() // 4, 48, (255, 255, 255), True)
    credits_text = [
        "Game Developer: John Doe",
        "Artist: Jane Smith",
        "Music Composer: Alex Johnson",
        "Sound Designer: Emily Davis"
    ]
    y = surf.get_height() // 3
    for line in credits_text:
        txt(surf, line, surf.get_width() // 2, y, 24, (255, 255, 255), True)
        y += 30
    back_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 150, 200, 50, "Back", (0, 128, 0), (255, 255, 255))
    return back_btn

def draw_inventory(surf, player):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Inventory")
    # Placeholder for inventory drawing logic
    return panel_rect

def draw_equipment(surf, player):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Equipment")
    # Placeholder for equipment drawing logic
    return panel_rect

def draw_quests(surf, player):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Quests")
    # Placeholder for quests drawing logic
    return panel_rect

def draw_shop(surf, shop_items):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Shop")
    # Placeholder for shop drawing logic
    return panel_rect

def draw_dialogue_box(surf, text):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() - 150, 400, 140, "Dialogue")
    txt(surf, text, surf.get_width() // 2, surf.get_height() - 130, 24, (255, 255, 255), True)
    continue_btn = btn(surf, surf.get_width() // 2 - 75, surf.get_height() - 80, 150, 50, "Continue", (0, 128, 0), (255, 255, 255))
    return panel_rect, continue_btn

def draw_combat_ui(surf, player, enemy):
    surf.fill((0, 0, 0))
    player_panel = panel(surf, 10, 10, 300, 100, "Player")
    txt(surf, f"HP: {player.hp}", 25, 40)
    txt(surf, f"MP: {player.mp}", 25, 70)

    enemy_panel = panel(surf, surf.get_width() - 310, 10, 300, 100, "Enemy")
    txt(surf, f"HP: {enemy.hp}", surf.get_width() - 285, 40)
    txt(surf, f"MP: {enemy.mp}", surf.get_width() - 285, 70)

    action_panel = panel(surf, surf.get_width() // 2 - 150, surf.get_height() - 150, 300, 140, "Actions")
    attack_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() - 130, 280, 50, "Attack", (0, 128, 0), (255, 255, 255))
    defend_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() - 75, 280, 50, "Defend", (0, 128, 0), (255, 255, 255))
    item_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() - 20, 280, 50, "Item", (0, 128, 0), (255, 255, 255))
    return player_panel, enemy_panel, action_panel, attack_btn, defend_btn, item_btn

def draw_minimap(surf, world_map):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() - 160, surf.get_height() - 160, 150, 150, "Minimap")
    # Placeholder for minimap drawing logic
    return panel_rect

def draw_status_effects(surf, player):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, 10, surf.get_height() - 160, 300, 150, "Status Effects")
    # Placeholder for status effects drawing logic
    return panel_rect

def draw_spellbook(surf, player):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Spellbook")
    # Placeholder for spellbook drawing logic
    return panel_rect

def draw_settings_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Settings")
    # Placeholder for settings menu drawing logic
    return panel_rect

def draw_tutorial(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Tutorial", surf.get_width() // 2, surf.get_height() // 4, 48, (255, 255, 255), True)
    tutorial_text = [
        "Welcome to the game!",
        "Use WASD or arrow keys to move.",
        "Press E to interact with objects.",
        "Press M to open the map.",
        "Press I to open your inventory."
    ]
    y = surf.get_height() // 3
    for line in tutorial_text:
        txt(surf, line, surf.get_width() // 2, y, 24, (255, 255, 255), True)
        y += 30
    continue_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 150, 200, 50, "Continue", (0, 128, 0), (255, 255, 255))
    return continue_btn

def draw_pause_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Pause Menu")
    resume_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Resume", (0, 128, 0), (255, 255, 255))
    options_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Options", (0, 128, 0), (255, 255, 255))
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Quit", (255, 0, 0), (255, 255, 255))
    return panel_rect, resume_btn, options_btn, quit_btn

def draw_options_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Options")
    volume_slider = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Volume: 50%", (0, 128, 0), (255, 255, 255))
    fullscreen_toggle = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Fullscreen: Off", (0, 128, 0), (255, 255, 255))
    back_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Back", (0, 128, 0), (255, 255, 255))
    return panel_rect, volume_slider, fullscreen_toggle, back_btn

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Loading...", surf.get_width() // 2, surf.get_height() // 2, 48, (255, 255, 255), True)

def draw_main_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Main Menu")
    start_game_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Start Game", (0, 128, 0), (255, 255, 255))
    load_game_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Load Game", (0, 128, 0), (255, 255, 255))
    options_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Options", (0, 128, 0), (255, 255, 255))
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 105, 280, 50, "Quit", (255, 0, 0), (255, 255, 255))
    return panel_rect, start_game_btn, load_game_btn, options_btn, quit_btn

def draw_credits(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Credits", surf.get_width() // 2, surf.get_height() // 4, 48, (255, 255, 255), True)
    credits_text = [
        "Game Developed by:",
        "John Doe",
        "Jane Smith",
        "Art by:",
        "Alice Johnson",
        "Music by:",
        "Bob Brown"
    ]
    y = surf.get_height() // 3
    for line in credits_text:
        txt(surf, line, surf.get_width() // 2, y, 24, (255, 255, 255), True)
        y += 30
    back_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 150, 200, 50, "Back", (0, 128, 0), (255, 255, 255))
    return back_btn

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Game Over", surf.get_width() // 2, surf.get_height() // 4, 48, (255, 0, 0), True)
    retry_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, "Retry", (0, 128, 0), (255, 255, 255))
    main_menu_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 105, 200, 50, "Main Menu", (0, 128, 0), (255, 255, 255))
    return retry_btn, main_menu_btn

def draw_victory(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Victory!", surf.get_width() // 2, surf.get_height() // 4, 48, (0, 255, 0), True)
    next_level_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, "Next Level", (0, 128, 0), (255, 255, 255))
    main_menu_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 105, 200, 50, "Main Menu", (0, 128, 0), (255, 255, 255))
    return next_level_btn, main_menu_btn

def draw_inventory(surf, player):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Inventory")
    # Placeholder for inventory drawing logic
    return panel_rect

def draw_shop(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Shop")
    # Placeholder for shop drawing logic
    return panel_rect

def draw_achievement_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Achievements", surf.get_width() // 2, surf.get_height() // 4, 48, (255, 255, 255), True)
    # Placeholder for achievement screen drawing logic
    back_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 150, 200, 50, "Back", (0, 128, 0), (255, 255, 255))
    return back_btn

def draw_character_screen(surf, player):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 200, surf.get_height() // 2 - 150, 400, 300, "Character")
    txt(surf, f"Name: {player.name}", surf.get_width() // 2, surf.get_height() // 2 - 100)
    txt(surf, f"Level: {player.level}", surf.get_width() // 2, surf.get_height() // 2 - 75)
    txt(surf, f"XP: {player.xp}/{player.next_level_xp}", surf.get_width() // 2, surf.get_height() // 2 - 50)
    txt(surf, f"HP: {player.hp}/{player.max_hp}", surf.get_width() // 2, surf.get_height() // 2 - 25)
    txt(surf, f"MP: {player.mp}/{player.max_mp}", surf.get_width() // 2, surf.get_height() // 2)
    back_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, "Back", (0, 128, 0), (255, 255, 255))
    return panel_rect, back_btn

def draw_world_map(surf, world_map):
    surf.fill((0, 0, 0))
    # Placeholder for world map drawing logic
    return

def draw_dialogue_box(surf, text):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 300, surf.get_height() - 150, 600, 140, "Dialogue")
    txt(surf, text, surf.get_width() // 2, surf.get_height() - 120)
    continue_btn = btn(surf, surf.get_width() // 2 - 75, surf.get_height() - 80, 150, 50, "Continue", (0, 128, 0), (255, 255, 255))
    return panel_rect, continue_btn

def draw_skill_tree(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 300, surf.get_height() // 2 - 150, 600, 300, "Skill Tree")
    # Placeholder for skill tree drawing logic
    back_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 150, 200, 50, "Back", (0, 128, 0), (255, 255, 255))
    return panel_rect, back_btn

def draw_settings_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Settings")
    volume_slider = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Volume: 50%", (0, 128, 0), (255, 255, 255))
    fullscreen_toggle = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Fullscreen: Off", (0, 128, 0), (255, 255, 255))
    back_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Back", (0, 128, 0), (255, 255, 255))
    return panel_rect, volume_slider, fullscreen_toggle, back_btn

def draw_pause_menu(surf):
    surf.fill((0, 0, 0))
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() // 2 - 100, 300, 200, "Pause Menu")
    resume_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 60, 280, 50, "Resume", (0, 128, 0), (255, 255, 255))
    settings_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 - 5, 280, 50, "Settings", (0, 128, 0), (255, 255, 255))
    main_menu_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 50, 280, 50, "Main Menu", (0, 128, 0), (255, 255, 255))
    quit_btn = btn(surf, surf.get_width() // 2 - 140, surf.get_height() // 2 + 105, 280, 50, "Quit", (255, 0, 0), (255, 255, 255))
    return panel_rect, resume_btn, settings_btn, main_menu_btn, quit_btn

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Loading...", surf.get_width() // 2, surf.get_height() // 2)
    # Placeholder for loading screen drawing logic
    return

def draw_notification(surf, message):
    panel_rect = panel(surf, surf.get_width() // 2 - 150, surf.get_height() - 100, 300, 80, "Notification")
    txt(surf, message, surf.get_width() // 2, surf.get_height() - 75)
    return panel_rect

def draw_debug_info(surf, debug_info):
    y = 20
    for info in debug_info:
        txt(surf, info, 10, y)
        y += 20
    return

# Example usage of the functions
if __name__ == "__main__":
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Example of drawing the main menu
        panel_rect, start_game_btn, load_game_btn, options_btn, quit_btn = draw_main_menu(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

### Explanation:

1. **Initialization**: The script initializes Pygame and sets up a window with dimensions 800x600.

2. **Main Loop**: The main loop handles events, such as quitting the game when the user closes the window.

3. **Drawing Functions**: Each function is designed to draw a specific UI element or screen. For example:
   - `draw_main_menu` draws the main menu with buttons for starting the game, loading a save, accessing options, and quitting.
   - `draw_pause_menu` provides options to resume gameplay, access settings, return to the main menu, or quit.

4. **Utility Functions**: Functions like `txt`, `btn`, and `panel` are used to draw text, buttons, and panels respectively. These functions handle positioning and rendering of UI elements.

5. **Example Usage**: The script includes an example usage section that demonstrates how to use the drawing functions within a Pygame loop.