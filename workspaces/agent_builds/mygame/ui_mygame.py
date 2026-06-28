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
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 0, 0))
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
    txt(surf, f'Biom: {player.biome}', 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    minimap = pygame.Surface((126, 126))
    minimap.blit(WORLD_MAP, (0, 0))
    for x in range(126):
        for y in range(126):
            if minimap.get_at((x, y))[:3] == BIOME_COL:
                minimap.set_at((x, y), (minimap.get_at((x, y))[0], minimap.get_at((x, y))[1], minimap.get_at((x, y))[2], 150))
    pygame.draw.circle(minimap, (255, 0, 0), (int(player.x / player.world_size * 126), int(player.y / player.world_size * 126)), 3)
    for enemy in enemies:
        pygame.draw.circle(minimap, (0, 255, 0), (int(enemy.x / player.world_size * 126), int(enemy.y / player.world_size * 126)), 2)
    surf.blit(minimap, (surf.get_width() - 136, 10))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    pygame.draw.circle(surf, (50, 50, 50), (surf.get_width() // 2, surf.get_height() // 4), 100)
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 8, 64, (255, 255, 255), True)
    play_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Play', (0, 128, 0), (255, 255, 255), 36)
    load_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Load', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 140, 200, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return [play_btn, load_btn, quit_btn]

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    warrior_card = pygame.Rect(100, 100, 200, 300)
    mage_card = pygame.Rect(400, 100, 200, 300)
    rogue_card = pygame.Rect(700, 100, 200, 300)
    pygame.draw.rect(surf, (50, 50, 50), warrior_card, 0)
    pygame.draw.rect(surf, (50, 50, 50), mage_card, 0)
    pygame.draw.rect(surf, (50, 50, 50), rogue_card, 0)
    txt(surf, 'Warrior', warrior_card.centerx, warrior_card.y + 20, 36, (255, 255, 255), True)
    txt(surf, 'Mage', mage_card.centerx, mage_card.y + 20, 36, (255, 255, 255), True)
    txt(surf, 'Rogue', rogue_card.centerx, rogue_card.y + 20, 36, (255, 255, 255), True)
    return [warrior_card, mage_card, rogue_card]

def draw_inventory(surf, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 400, 'Inventory')
    slots = []
    eq_btn = btn(surf, 10, 420, 145, 50, 'Equip', (0, 128, 0), (255, 255, 255), 36)
    drop_btn = btn(surf, 165, 420, 145, 50, 'Drop', (255, 0, 0), (255, 255, 255), 36)
    for i in range(10):
        slot = pygame.Rect(20 + (i % 5) * 55, 40 + (i // 5) * 55, 50, 50)
        slots.append(slot)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), slot, 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.name}: {quest.description}', 20, 40 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.items):
        txt(surf, f'{item.name}: {item.price} Gold', 20, 40 + i * 30, 24, (255, 255, 255))
        buy_btn = btn(surf, 250, 40 + i * 30, 120, 25, 'Buy', (0, 128, 0), (255, 255, 255), 24)
        buy_btns.append(buy_btn)
        items.append(item)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        tab_btn = btn(surf, 20 + i * 130, 40, 120, 30, t, (50, 50, 50), (255, 255, 255), 24)
        tab_btns.append(tab_btn)
    for i, recipe in enumerate(recipes[tab]):
        txt(surf, f'{recipe.name}', 20, 80 + i * 30, 24, (255, 255, 255))
        craft_btn = btn(surf, 250, 80 + i * 30, 120, 25, 'Craft', (0, 128, 0), (255, 255, 255), 24)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 300, 'Dialogue')
    txt(surf, f'{npc.name}: {npc.dialogues[dial_idx]}', 20, 40, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        opt_btn = btn(surf, 20, 80 + i * 30, 360, 25, option.text, (50, 50, 50), (255, 255, 255), 24)
        opt_btns.append(opt_btn)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 300, 250, 'Paused')
    resume_btn = btn(surf, 20, 40, 260, 50, 'Resume', (0, 128, 0), (255, 255, 255), 36)
    save_btn = btn(surf, 20, 100, 260, 50, 'Save', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, 20, 160, 260, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return xbtn_rect, [resume_btn, save_btn, quit_btn]

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 400, 580, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20 + (i % 3) * 120, 40 + (i // 3) * 60, 100, 50, building.name, (50, 50, 50), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    surf.fill((0, 0, 0))
    xbtn_rect = panel(surf, 10, 10, 800, 600, 'World Map')
    surf.blit(WORLD_MAP, (20, 40))
    for town in TOWNS:
        pygame.draw.circle(surf, (0, 0, 255), (int(town.x / player.world_size * 780) + 20, int(town.y / player.world_size * 560) + 40), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (255, 0, 0), (int(city.x / player.world_size * 780) + 20, int(city.y / player.world_size * 560) + 40), 5)
    return xbtn_rect

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    panel(surf, 10, 10, 300, 200, 'Game Over')
    txt(surf, 'You have died.', 160, 80, 48, (255, 0, 0), True)
    restart_btn = btn(surf, 20, 140, 260, 50, 'Restart', (0, 128, 0), (255, 255, 255), 36)
    quit_btn = btn(surf, 20, 200, 260, 50, 'Quit', (255, 0, 0), (255, 255, 255), 36)
    return [restart_btn, quit_btn]

def draw_player_stats(surf, player):
    txt(surf, f'HP: {player.hp}/{player.max_hp}', 10, 10, 24, (255, 0, 0))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', 10, 35, 24, (0, 0, 255))
    txt(surf, f'Level: {player.level}', 10, 60, 24, (255, 255, 0))

def draw_player_inventory(surf, player):
    for i, item in enumerate(player.inventory[:10]):
        pygame.draw.rect(surf, (50, 50, 50), (10 + (i % 5) * 60, 720 - (i // 5) * 60, 50, 50))
        txt(surf, item.name[:3], 35 + (i % 5) * 60, 745 - (i // 5) * 60, 18, (255, 255, 255))

def draw_player_equipment(surf, player):
    txt(surf, 'Equipment:', 10, 600, 24, (255, 255, 255))
    if player.weapon:
        txt(surf, f'Weapon: {player.weapon.name}', 10, 630, 24, (255, 255, 255))
    else:
        txt(surf, 'Weapon: None', 10, 630, 24, (255, 255, 255))
    if player.armor:
        txt(surf, f'Armor: {player.armor.name}', 10, 660, 24, (255, 255, 255))
    else:
        txt(surf, 'Armor: None', 10, 660, 24, (255, 255, 255))

def draw_player_skills(surf, player):
    txt(surf, 'Skills:', 320, 600, 24, (255, 255, 255))
    for i, skill in enumerate(player.skills):
        txt(surf, f'{skill.name}: {skill.description}', 320, 630 + i * 30, 24, (255, 255, 255))

def draw_player_status_effects(surf, player):
    txt(surf, 'Status Effects:', 630, 600, 24, (255, 255, 255))
    for i, effect in enumerate(player.status_effects):
        txt(surf, f'{effect.name}: {effect.duration} turns', 630, 630 + i * 30, 24, (255, 255, 255))
