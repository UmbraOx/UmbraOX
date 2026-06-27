# MyGame UI Drawing Functions Module

import pygame
from collections import defaultdict

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
    txt(surf, f"Gold: {player.gold}", 10, 100, 24, (255, 255, 0))
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
        pygame.draw.circle(surf, col, (x, y), 2)
    moon = pygame.Surface((50, 50))
    pygame.draw.circle(moon, (255, 255, 255), (25, 25), 25)
    surf.blit(moon, (surf.get_width() - 100, 50))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 64, (255, 255, 255), True)
    btns = [
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 - 50, 200, 50, 'Start Game', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 50, 200, 50, 'Load Game', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 150, 200, 50, 'Exit', (100, 100, 100), (255, 255, 255), 32)
    ]
    return btns

def draw_class_select(surf):
    class_cards = [
        {'name': 'Warrior', 'portrait': pygame.Surface((100, 100)), 'x': surf.get_width() // 4 - 50, 'y': surf.get_height() // 2 - 50},
        {'name': 'Mage', 'portrait': pygame.Surface((100, 100)), 'x': surf.get_width() // 2 - 50, 'y': surf.get_height() // 2 - 50},
        {'name': 'Rogue', 'portrait': pygame.Surface((100, 100)), 'x': surf.get_width() * 3 // 4 - 50, 'y': surf.get_height() // 2 - 50}
    ]
    for card in class_cards:
        pygame.draw.rect(surf, (100, 100, 100), (card['x'], card['y'], 100, 100), 0)
        txt(surf, card['name'], card['x'] + 50, card['y'] - 30, 24, (255, 255, 255), True)
    return [pygame.Rect(card['x'], card['y'], 100, 100) for card in class_cards]

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 50, 50, 300, 400, 'Inventory')
    slots = []
    eq_btn = btn(surf, 200, 460, 100, 30, 'Equip', (100, 100, 100), (255, 255, 255), 24)
    drop_btn = btn(surf, 310, 460, 100, 30, 'Drop', (100, 100, 100), (255, 255, 255), 24)
    for i, item in enumerate(player.inventory):
        rect = pygame.Rect(60, 80 + i * 30, 280, 25)
        txt(surf, f"{item.name} x{item.quantity}", rect.x, rect.y, 20, (255, 255, 255))
        slots.append(rect)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 50, 50, 300, 400, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 60, 80 + i * 30, 20, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 50, 50, 300, 400, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        rect = pygame.Rect(60, 80 + i * 30, 280, 25)
        txt(surf, f"{item.name} x{item.quantity} - {item.price} gold", rect.x, rect.y, 20, (255, 255, 255))
        items.append(rect)
        buy_btn = btn(surf, 60, 110 + i * 30, 80, 20, 'Buy', (100, 100, 100), (255, 255, 255), 16)
        buy_btns.append(buy_btn)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 50, 50, 300, 400, 'Crafting')
    tab_btns = [
        btn(surf, 60, 80, 100, 25, 'Weapons', (100, 100, 100), (255, 255, 255), 16),
        btn(surf, 170, 80, 100, 25, 'Armor', (100, 100, 100), (255, 255, 255), 16),
        btn(surf, 280, 80, 100, 25, 'Potions', (100, 100, 100), (255, 255, 255), 16)
    ]
    craft_btns = []
    for i, recipe in enumerate(recipes[tab]):
        rect = pygame.Rect(60, 120 + i * 30, 280, 25)
        txt(surf, f"{recipe.name} - {recipe.cost}", rect.x, rect.y, 20, (255, 255, 255))
        craft_btn = btn(surf, 60, 150 + i * 30, 80, 20, 'Craft', (100, 100, 100), (255, 255, 255), 16)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 50, 50, 300, 400, 'Dialogue')
    txt(surf, f"{npc.name}: {npc.dialogues[dial_idx]}", 60, 80, 20, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options):
        btn_rect = btn(surf, 60, 120 + i * 30, 280, 25, option.text, (100, 100, 100), (255, 255, 255), 16)
        opt_btns.append(btn_rect)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 4, surf.get_height() // 3, surf.get_width() // 2, surf.get_height() // 3, 'Paused')
    pause_btns = [
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 - 50, 200, 50, 'Resume', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 50, 200, 50, 'Save Game', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 150, 200, 50, 'Exit', (100, 100, 100), (255, 255, 255), 32)
    ]
    return panel(surf, surf.get_width() // 4, surf.get_height() // 3, surf.get_width() // 2, surf.get_height() // 3, 'Paused'), pause_btns

def draw_city_map(surf):
    # Placeholder for city map drawing logic
    pass

def draw_world_map(surf):
    # Placeholder for world map drawing logic
    pass

def draw_character_screen(surf, player):
    panel(surf, 50, 50, 300, 400, 'Character')
    txt(surf, f"Name: {player.name}", 60, 80, 20, (255, 255, 255))
    txt(surf, f"Level: {player.level}", 60, 110, 20, (255, 255, 255))
    txt(surf, f"Health: {player.health}/{player.max_health}", 60, 140, 20, (255, 255, 255))
    txt(surf, f"Mana: {player.mana}/{player.max_mana}", 60, 170, 20, (255, 255, 255))
    txt(surf, f"Experience: {player.experience}/{player.next_level_exp}", 60, 200, 20, (255, 255, 255))
    txt(surf, f"Gold: {player.gold}", 60, 230, 20, (255, 255, 255))

def draw_game_over_screen(surf):
    surf.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 4, surf.get_height() // 3, surf.get_width() // 2, surf.get_height() // 3, 'Game Over')
    txt(surf, "You have been defeated.", surf.get_width() // 2 - 100, surf.get_height() // 2 - 50, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 50, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_victory_screen(surf):
    surf.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 4, surf.get_height() // 3, surf.get_width() // 2, surf.get_height() // 3, 'Victory')
    txt(surf, "Congratulations! You have won!", surf.get_width() // 2 - 150, surf.get_height() // 2 - 50, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 50, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Loading...", surf.get_width() // 2 - 50, surf.get_height() // 2, 24, (255, 255, 255), True)

def draw_settings_screen(surf):
    panel(surf, 50, 50, 300, 400, 'Settings')
    txt(surf, "Volume: 100%", 60, 80, 20, (255, 255, 255))
    txt(surf, "Fullscreen: Off", 60, 110, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 140, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_help_screen(surf):
    panel(surf, 50, 50, 300, 400, 'Help')
    txt(surf, "Controls:", 60, 80, 20, (255, 255, 255))
    txt(surf, "WASD - Move", 60, 110, 20, (255, 255, 255))
    txt(surf, "E - Interact", 60, 140, 20, (255, 255, 255))
    txt(surf, "I - Inventory", 60, 170, 20, (255, 255, 255))
    txt(surf, "Q - Quest Log", 60, 200, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 230, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_achievement_screen(surf):
    panel(surf, 50, 50, 300, 400, 'Achievements')
    txt(surf, "Unlock achievements as you play!", 60, 80, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 110, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_tutorial_screen(surf):
    panel(surf, 50, 50, 300, 400, 'Tutorial')
    txt(surf, "Welcome to the game!", 60, 80, 20, (255, 255, 255))
    txt(surf, "Explore the world, complete quests, and become stronger.", 60, 110, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 140, 80, 20, 'Start', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_credits_screen(surf):
    panel(surf, 50, 50, 300, 400, 'Credits')
    txt(surf, "Developed by:", 60, 80, 20, (255, 255, 255))
    txt(surf, "Your Name", 60, 110, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 140, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_debug_screen(surf):
    panel(surf, 50, 50, 300, 400, 'Debug')
    txt(surf, "Debug Information:", 60, 80, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 110, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_main_menu(surf):
    surf.fill((0, 0, 0))
    txt(surf, "My RPG Game", surf.get_width() // 2 - 75, surf.get_height() // 3, 48, (255, 255, 255), True)
    btn_rects = [
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 - 100, 200, 50, 'Start', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 - 40, 200, 50, 'Load', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 20, 200, 50, 'Settings', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 80, 200, 50, 'Help', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 140, 200, 50, 'Credits', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 200, 200, 50, 'Exit', (100, 100, 100), (255, 255, 255), 32)
    ]
    return btn_rects

def draw_game_screen(surf, player):
    # Placeholder for game screen drawing logic
    pass

def draw_battle_screen(surf, player, enemy):
    panel(surf, 50, 50, 300, 400, 'Battle')
    txt(surf, f"Player: {player.name}", 60, 80, 20, (255, 255, 255))
    txt(surf, f"Health: {player.health}/{player.max_health}", 60, 110, 20, (255, 255, 255))
    txt(surf, f"Mana: {player.mana}/{player.max_mana}", 60, 140, 20, (255, 255, 255))
    txt(surf, f"Enemy: {enemy.name}", 60, 180, 20, (255, 255, 255))
    txt(surf, f"Health: {enemy.health}/{enemy.max_health}", 60, 210, 20, (255, 255, 255))
    btn_rects = [
        btn(surf, 60, 250, 80, 20, 'Attack', (100, 100, 100), (255, 255, 255), 16),
        btn(surf, 60, 280, 80, 20, 'Defend', (100, 100, 100), (255, 255, 255), 16),
        btn(surf, 60, 310, 80, 20, 'Magic', (100, 100, 100), (255, 255, 255), 16),
        btn(surf, 60, 340, 80, 20, 'Run', (100, 100, 100), (255, 255, 255), 16)
    ]
    return btn_rects

def draw_inventory_screen(surf, player):
    panel(surf, 50, 50, 300, 400, 'Inventory')
    txt(surf, "Items:", 60, 80, 20, (255, 255, 255))
    for i, item in enumerate(player.inventory):
        txt(surf, f"{item.name} - {item.description}", 60, 110 + i * 30, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 400, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_spellbook_screen(surf, player):
    panel(surf, 50, 50, 300, 400, 'Spellbook')
    txt(surf, "Spells:", 60, 80, 20, (255, 255, 255))
    for i, spell in enumerate(player.spellbook):
        txt(surf, f"{spell.name} - {spell.description}", 60, 110 + i * 30, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 400, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_shop_screen(surf, player, shop):
    panel(surf, 50, 50, 300, 400, 'Shop')
    txt(surf, "Items for Sale:", 60, 80, 20, (255, 255, 255))
    btn_rects = []
    for i, item in enumerate(shop.items):
        txt(surf, f"{item.name} - {item.price} gold", 60, 110 + i * 30, 20, (255, 255, 255))
        btn_rect = btn(surf, 200, 110 + i * 30, 80, 20, f'Buy', (100, 100, 100), (255, 255, 255), 16)
        btn_rects.append(btn_rect)
    back_btn_rect = btn(surf, 60, 400, 80, 20, 'Back', (100, 100, 100), (255, 255, 255), 16)
    return btn_rects, back_btn_rect

def draw_npc_dialogue_screen(surf, npc):
    panel(surf, 50, 50, 300, 400, f'Dialogue - {npc.name}')
    txt(surf, npc.dialogue, 60, 80, 20, (255, 255, 255))
    btn_rect = btn(surf, 60, 370, 80, 20, 'Continue', (100, 100, 100), (255, 255, 255), 16)
    return btn_rect

def draw_achievement_unlocked_screen(surf, achievement):
    surf.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 4, surf.get_height() // 3, surf.get_width() // 2, surf.get_height() // 3, 'Achievement Unlocked')
    txt(surf, f"Congratulations!", surf.get_width() // 2 - 75, surf.get_height() // 3 + 20, 24, (255, 255, 255), True)
    txt(surf, f"{achievement.name}", surf.get_width() // 2 - len(achievement.name) * 6, surf.get_height() // 3 + 70, 20, (255, 255, 255))
    txt(surf, f"{achievement.description}", surf.get_width() // 2 - len(achievement.description) * 6, surf.get_height() // 3 + 100, 16, (255, 255, 255))
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 80, 200, 50, 'Continue', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Loading...', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 255, 255), True)

def draw_error_screen(surf, error_message):
    surf.fill((0, 0, 0))
    txt(surf, 'Error:', surf.get_width() // 2 - 30, surf.get_height() // 2 - 40, 24, (255, 0, 0), True)
    txt(surf, error_message, surf.get_width() // 2 - len(error_message) * 6, surf.get_height() // 2 - 10, 20, (255, 0, 0))
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 40, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_save_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Save Game', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 40, 200, 50, 'Save', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_load_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Load Game', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 40, 200, 50, 'Load', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_pause_screen(surf):
    surf.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    txt(surf, 'Paused', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 255, 255), True)
    btn_rects = [
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 40, 200, 50, 'Resume', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 100, 200, 50, 'Save', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 160, 200, 50, 'Load', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 220, 200, 50, 'Exit', (100, 100, 100), (255, 255, 255), 32)
    ]
    return btn_rects

def draw_game_over_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Game Over', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 0, 0), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 40, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_win_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'You Win!', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (0, 255, 0), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 40, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_settings_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Settings', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 255, 255), True)
    btn_rects = [
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 40, 200, 50, 'Graphics', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 100, 200, 50, 'Audio', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 160, 200, 50, 'Controls', (100, 100, 100), (255, 255, 255), 32),
        btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 220, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    ]
    return btn_rects

def draw_help_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Help', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 255, 255), True)
    txt(surf, 'Controls:', surf.get_width() // 3, surf.get_height() // 2 + 40, 20, (255, 255, 255))
    txt(surf, 'WASD - Move', surf.get_width() // 3, surf.get_height() // 2 + 70, 16, (255, 255, 255))
    txt(surf, 'Space - Attack', surf.get_width() // 3, surf.get_height() // 2 + 90, 16, (255, 255, 255))
    txt(surf, 'E - Interact', surf.get_width() // 3, surf.get_height() // 2 + 110, 16, (255, 255, 255))
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 180, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_credits_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Credits', surf.get_width() // 2 - 40, surf.get_height() // 2 - 10, 24, (255, 255, 255), True)
    txt(surf, 'Developed by:', surf.get_width() // 3, surf.get_height() // 2 + 40, 20, (255, 255, 255))
    txt(surf, 'Your Name', surf.get_width() // 3, surf.get_height() // 2 + 70, 16, (255, 255, 255))
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 180, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_inventory_screen(surf, inventory):
    surf.fill((0, 0, 0))
    txt(surf, 'Inventory', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for item in inventory:
        txt(surf, f'{item.name}: {item.quantity}', surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_spellbook_screen(surf, spells):
    surf.fill((0, 0, 0))
    txt(surf, 'Spellbook', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for spell in spells:
        txt(surf, f'{spell.name}: {spell.description}', surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_character_screen(surf, character):
    surf.fill((0, 0, 0))
    txt(surf, 'Character', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    txt(surf, f'Name: {character.name}', surf.get_width() // 3, 60, 16, (255, 255, 255))
    txt(surf, f'Level: {character.level}', surf.get_width() // 3, 90, 16, (255, 255, 255))
    txt(surf, f'Health: {character.health}/{character.max_health}', surf.get_width() // 3, 120, 16, (255, 255, 255))
    txt(surf, f'Mana: {character.mana}/{character.max_mana}', surf.get_width() // 3, 150, 16, (255, 255, 255))
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_map_screen(surf, map_data):
    surf.fill((0, 0, 0))
    txt(surf, 'Map', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for row in map_data:
        txt(surf, ''.join(row), surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_dialogue_screen(surf, dialogue):
    surf.fill((0, 0, 0))
    txt(surf, 'Dialogue', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for line in dialogue:
        txt(surf, line, surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Continue', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_shop_screen(surf, items):
    surf.fill((0, 0, 0))
    txt(surf, 'Shop', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for item in items:
        txt(surf, f'{item.name}: {item.price} gold', surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_achievement_screen(surf, achievements):
    surf.fill((0, 0, 0))
    txt(surf, 'Achievements', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for achievement in achievements:
        txt(surf, f'{achievement.name}: {achievement.description}', surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_minimap_screen(surf, minimap_data):
    surf.fill((0, 0, 0))
    txt(surf, 'Minimap', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for row in minimap_data:
        txt(surf, ''.join(row), surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_log_screen(surf, log_entries):
    surf.fill((0, 0, 0))
    txt(surf, 'Log', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for entry in log_entries:
        txt(surf, entry, surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_settings_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Settings', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_main_menu_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Main Menu', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Start Game', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_pause_menu_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Pause Menu', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Resume', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_game_over_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Game Over', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_victory_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Victory!', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Main Menu', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Loading...', surf.get_width() // 2 - 40, surf.get_height() // 2, 24, (255, 255, 255), True)

def draw_transition_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Transitioning...', surf.get_width() // 2 - 40, surf.get_height() // 2, 24, (255, 255, 255), True)

def draw_debug_screen(surf, debug_info):
    surf.fill((0, 0, 0))
    txt(surf, 'Debug Info', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for info in debug_info:
        txt(surf, info, surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30

def draw_help_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Help', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_tutorial_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Tutorial', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_credits_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Credits', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_highscores_screen(surf, highscores):
    surf.fill((0, 0, 0))
    txt(surf, 'Highscores', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    y_offset = 60
    for score in highscores:
        txt(surf, f'{score.name}: {score.score}', surf.get_width() // 3, y_offset, 16, (255, 255, 255))
        y_offset += 30
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_options_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Options', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_customization_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Customization', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_multiplayer_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Multiplayer', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_singleplayer_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Singleplayer', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_campaign_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Campaign', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_survival_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Survival', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_challenge_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Challenge', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_leaderboard_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Leaderboard', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_achievements_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Achievements', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_inventory_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Inventory', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_equipment_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Equipment', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_spellbook_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Spellbook', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_map_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Map', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_journal_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Journal', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_dialogue_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Dialogue', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Continue', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_cutscene_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Cutscene', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Skip', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_minimap_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Minimap', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Close', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_status_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Status', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_settings_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Settings', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_controls_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Controls', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_audio_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Audio', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_video_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Video', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_network_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Network', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_about_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'About', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_exit_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Exit', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Confirm', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_pause_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Pause', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Resume', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_game_over_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Game Over', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_win_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'You Win!', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Next Level', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Loading...', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    return

def draw_error_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Error', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Retry', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_debug_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Debug', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_help_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Help', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_tutorial_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Tutorial', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Start', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_credits_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Credits', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_highscores_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'High Scores', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_shop_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Shop', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_inventory_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Inventory', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_character_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Character', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_quests_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Quests', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_map_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Map', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Close', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_dialogue_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Dialogue', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Next', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_notification_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Notification', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Close', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_chat_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Chat', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Close', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_achievement_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Achievements', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_leaderboard_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Leaderboard', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_ranking_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Ranking', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_settings_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Settings', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_options_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Options', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Back', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_main_menu_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Main Menu', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Start', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_pause_menu_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Pause Menu', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Resume', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_game_over_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Game Over', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_victory_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Victory', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    btn_rect = btn(surf, surf.get_width() // 3, surf.get_height() - 80, 200, 50, 'Next Level', (100, 100, 100), (255, 255, 255), 32)
    return btn_rect

def draw_loading_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Loading...', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    return None

def draw_transition_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Transition', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    return None

def draw_fade_in_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Fade In', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    return None

def draw_fade_out_screen(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Fade Out', surf.get_width() // 2 - 40, 10, 24, (255, 255, 255), True)
    return None

def draw_black_screen(surf):
    surf.fill((0, 0, 0))
    return None

def draw_white_screen(surf):
    surf.fill((255, 255, 255))
    return None

def draw_red_screen(surf):
    surf.fill((255, 0, 0))
    return None

def draw_green_screen(surf):
    surf.fill((0, 255, 0))
    return None

def draw_blue_screen(surf):
    surf.fill((0, 0, 255))
    return None

def draw_yellow_screen(surf):
    surf.fill((255, 255, 0))
    return None

def draw_cyan_screen(surf):
    surf.fill((0, 255, 255))
    return None

def draw_magenta_screen(surf):
    surf.fill((255, 0, 255))
    return None

def draw_gray_screen(surf):
    surf.fill((128, 128, 128))
    return None

def draw_light_gray_screen(surf):
    surf.fill((192, 192, 192))
    return None

def draw_dark_gray_screen(surf):
    surf.fill((64, 64, 64))
    return None

def draw_brown_screen(surf):
    surf.fill((165, 42, 42))
    return None

def draw_orange_screen(surf):
    surf.fill((255, 165, 0))
    return None

def draw_purple_screen(surf):
    surf.fill((128, 0, 128))
    return None

def draw_pink_screen(surf):
    surf.fill((255, 192, 203))
    return None

def draw_lime_screen(surf):
    surf.fill((0, 255, 0))
    return None

def draw_teal_screen(surf):
    surf.fill((0, 128, 128))
    return None

def draw_maroon_screen(surf):
    surf.fill((128, 0, 0))
    return None

def draw_olive_screen(surf):
    surf.fill((128, 128, 0))
    return None

def draw_navy_screen(surf):
    surf.fill((0, 0, 128))
    return None

def draw_silver_screen(surf):
    surf.fill((192, 192, 192))
    return None

def draw_gold_screen(surf):
    surf.fill((255, 215, 0))
    return None

def draw_brass_screen(surf):
    surf.fill((205, 173, 0))
    return None

def draw_bronze_screen(surf):
    surf.fill((205, 127, 50))
    return None

def draw_copper_screen(surf):
    surf.fill((184, 115, 51))
    return None

def draw_tin_screen(surf):
    surf.fill((192, 192, 192))
    return None

def draw_steel_screen(surf):
    surf.fill((169, 169, 169))
    return None

def draw_aluminum_screen(surf):
    surf.fill((238, 232, 170))
    return None

def draw_nickel_screen(surf):
    surf.fill((224, 224, 224))
    return None

def draw_zinc_screen(surf):
    surf.fill((255, 250, 205))
    return None

def draw_platinum_screen(surf):
    surf.fill((238, 236, 236))
    return None

def draw_silver_screen(surf):
    surf.fill((192, 192, 192))
    return None

def draw_gold_screen(surf):
    surf.fill((255, 215, 0))
    return None

def draw_brass_screen(surf):
    surf.fill((205, 173, 0))
    return None

def draw_bronze_screen(surf):
    surf.fill((205, 127, 50))
    return None

def draw_copper_screen(surf):
    surf.fill((184, 115, 51))
    return None

def draw_tin_screen(surf):
    surf.fill((192, 192, 192))
    return None

def draw_steel_screen(surf):
    surf.fill((169, 169, 169))
    return None

def draw_aluminum_screen(surf):
    surf.fill((238, 232, 170))
    return None

def draw_nickel_screen(surf):
    surf.fill((224, 224, 224))
    return None

def draw_zinc_screen(surf):
    surf.fill((255, 250, 205))
    return None

def draw_platinum_screen(surf):
    surf.fill((238, 236, 236))
    return None

# Helper function to draw text
def txt(surface, text, x, y, size, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Helper function to create a button
def btn(surface, x, y, width, height, color, hover_color, text, text_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))

    txt(surface, text, x + (width / 2 - len(text) * 3), y + (height / 2 - size / 2), size, text_color)
    return pygame.Rect(x, y, width, height)

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_main_menu_screen(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()