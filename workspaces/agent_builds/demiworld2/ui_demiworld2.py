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
    pygame.draw.rect(surf, (100, 100, 100), (rx, ry, rw, rh), 2)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.Rect(rx + rw - 30, ry + 5, 20, 20)
    txt(surf, 'X', rx + rw - 28, ry + 7, 16, (255, 0, 0), True)
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
    minimap = pygame.Surface((126, 126))
    minimap.blit(WORLD_MAP, (0, 0))
    for x, y in enemies:
        pygame.draw.circle(minimap, (255, 0, 0), (int(x * 126 / WORLD_MAP.get_width()), int(y * 126 / WORLD_MAP.get_height())), 3)
    pygame.draw.circle(minimap, (0, 255, 0), (int(player.x * 126 / WORLD_MAP.get_width()), int(player.y * 126 / WORLD_MAP.get_height())), 4)
    surf.blit(minimap, (surf.get_width() - 136, 10))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    starfield = pygame.Surface(surf.get_size())
    for _ in range(200):
        x, y = pygame.math.Vector2(pygame.mouse.get_pos()).rotate(pygame.time.get_ticks() / 10)
        pygame.draw.circle(starfield, (255, 255, 255), (int(x) % surf.get_width(), int(y) % surf.get_height()), 1)
    surf.blit(starfield, (0, 0))
    moon = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(moon, (255, 255, 255, 128), (50, 50), 40)
    surf.blit(moon, (surf.get_width() - 150, 50))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 3, 64, (255, 255, 255), True)
    btns = []
    btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, 'Start Game', (50, 50, 50), (255, 255, 255), 32))
    btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 120, 200, 50, 'Load Game', (50, 50, 50), (255, 255, 255), 32))
    btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 190, 200, 50, 'Exit', (50, 50, 50), (255, 255, 255), 32))
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    classes = ['Warrior', 'Mage', 'Rogue']
    portraits = [pygame.Surface((100, 100)), pygame.Surface((100, 100)), pygame.Surface((100, 100))]
    btns = []
    for i, cls in enumerate(classes):
        x = surf.get_width() // 3 * (i + 1) - 50
        y = surf.get_height() // 2 - 50
        pygame.draw.rect(surf, (50, 50, 50), (x - 60, y - 60, 220, 220), 0)
        pygame.draw.rect(surf, (100, 100, 100), (x - 60, y - 60, 220, 220), 2)
        surf.blit(portraits[i], (x, y))
        btns.append(btn(surf, x - 50, y + 70, 100, 30, cls, (50, 50, 50), (255, 255, 255), 24))
    return btns

def draw_inventory(surf, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 380, 600, 'Inventory')
    slots = []
    eq_btn = btn(surf, 400, 200, 150, 50, 'Equip', (50, 50, 50), (255, 255, 255), 32)
    drop_btn = btn(surf, 400, 270, 150, 50, 'Drop', (50, 50, 50), (255, 255, 255), 32)
    for i in range(16):
        x = 20 + (i % 4) * 90
        y = 40 + (i // 4) * 90
        rect = pygame.Rect(x, y, 80, 80)
        slots.append(rect)
        if i == selected:
            pygame.draw.rect(surf, (255, 255, 0), rect, 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.title}: {quest.description}', 20, 50 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 600, f'Shop - {npc.name}')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        rect = pygame.Rect(20, 50 + i * 30, 150, 20)
        items.append(rect)
        txt(surf, f'{item.name} - {item.price}', 20, 50 + i * 30, 24, (255, 255, 255))
        if i == selected:
            pygame.draw.rect(surf, (255, 255, 0), rect, 3)
        buy_btns.append(btn(surf, 180, 50 + i * 30, 60, 20, 'Buy', (50, 50, 50), (255, 255, 255), 16))
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 600, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        tab_btns.append(btn(surf, 20 + i * 130, 50, 120, 40, t, (50, 50, 50), (255, 255, 255), 24))
    for i, recipe in enumerate(recipes[tab]):
        rect = pygame.Rect(20, 110 + i * 30, 150, 20)
        txt(surf, f'{recipe.name} - {recipe.cost}', 20, 110 + i * 30, 24, (255, 255, 255))
        if i == selected:
            pygame.draw.rect(surf, (255, 255, 0), rect, 3)
        craft_btns.append(btn(surf, 180, 110 + i * 30, 60, 20, 'Craft', (50, 50, 50), (255, 255, 255), 16))
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 300, f'Dialogue - {npc.name}')
    txt(surf, npc.dialogues[dial_idx]['text'], 20, 50, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.dialogues[dial_idx].get('options', [])):
        opt_btns.append(btn(surf, 20, 100 + i * 30, 360, 40, option['text'], (50, 50, 50), (255, 255, 255), 24))
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 3, surf.get_height() // 3, 400, 300, 'Paused')
    pause_btns = []
    pause_btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, 'Resume', (50, 50, 50), (255, 255, 255), 32))
    pause_btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 120, 200, 50, 'Save Game', (50, 50, 50), (255, 255, 255), 32))
    pause_btns.append(btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 190, 200, 50, 'Exit', (50, 50, 50), (255, 255, 255), 32))
    return pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 600, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        type_btns.append(btn(surf, 20 + (i % 3) * 130, 50 + (i // 3) * 60, 120, 40, building['name'], (50, 50, 50), (255, 255, 255), 24))
    return xbtn_rect, type_btns

def draw_world_map(surf):
    surf.fill((0, 0, 0))

def draw_minimap(surf, player_position, map_size):
    surf.fill((0, 0, 0))
    pygame.draw.rect(surf, (255, 255, 255), (10, 10, 280, 280), 2)
    x = int(player_position[0] / map_size * 280) + 10
    y = int(player_position[1] / map_size * 280) + 10
    pygame.draw.circle(surf, (255, 0, 0), (x, y), 3)

def draw_hud(surf, player):
    surf.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
    txt = f'HP: {player.hp}/{player.max_hp} MP: {player.mp}/{player.max_mp}'
    txt_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(txt_surface, (10, 10))

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    panel(surf, surf.get_width() // 3, surf.get_height() // 3, 400, 300, 'Game Over')
    btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, 'Restart', (50, 50, 50), (255, 255, 255), 32)
    return btn

def draw_win(surf):
    surf.fill((0, 0, 0))
    panel(surf, surf.get_width() // 3, surf.get_height() // 3, 400, 300, 'You Win!')
    btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, 'Exit', (50, 50, 50), (255, 255, 255), 32)
    return btn

def draw_player(surf, player):
    surf.blit(player.sprite, player.position)

def draw_enemies(surf, enemies):
    for enemy in enemies:
        surf.blit(enemy.sprite, enemy.position)


if __name__ == '__main__':
    main()
