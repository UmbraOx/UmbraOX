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
    xbtn_rect = pygame.draw.rect(surf, (200, 0, 0), (rx + rw - 30, ry + 5, 20, 20), 0)
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 255, 255), center=True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    pygame.draw.rect(surf, (0, 0, 0), (x, y, w, h), 2)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, center=True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (50, 50, 50))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (50, 50, 50))
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (0, 255, 0), (50, 50, 50))
    txt(surf, f'Gold: {player.gold}', 10, 100, 24, (255, 255, 255))
    txt(surf, f'Level: {player.level} XP: {player.xp}/{player.next_level_xp}', 10, 130, 24, (255, 255, 255))
    txt(surf, f'Equipped: {player.equipped}', 10, 160, 24, (255, 255, 255))
    txt(surf, f'Biome: {player.biome}', 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x, min_y = max(0, player.x - 63), max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < WORLD_MAP.height and 0 <= x < WORLD_MAP.width:
                biome = WORLD_MAP.get_at((x, y))
                pygame.draw.rect(surf, BIOME_COL[biome], (x - min_x + surf.get_width() - 126, y - min_y, 1, 1), 0)
    for enemy in enemies:
        ex, ey = enemy.x - min_x + surf.get_width() - 126, enemy.y - min_y
        if 0 <= ex < 126 and 0 <= ey < 126:
            pygame.draw.rect(surf, (255, 0, 0), (ex, ey, 2, 2), 0)
    px, py = player.x - min_x + surf.get_width() - 126, player.y - min_y
    if 0 <= px < 126 and 0 <= py < 126:
        pygame.draw.rect(surf, (0, 255, 0), (px, py, 3, 3), 0)

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, 'DemiWorld', surf.get_width() // 2, surf.get_height() // 4, 64, (255, 255, 255), center=True)
    btn_play = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Play', (0, 128, 0), (255, 255, 255), 36)
    btn_options = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Options', (0, 128, 128), (255, 255, 255), 36)
    btn_exit = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 140, 200, 50, 'Exit', (128, 0, 0), (255, 255, 255), 36)
    return [btn_play, btn_options, btn_exit]

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Select Class', surf.get_width() // 2, surf.get_height() // 4, 64, (255, 255, 255), center=True)
    btn_warrior = btn(surf, surf.get_width() // 3 - 100, surf.get_height() // 2, 200, 100, 'Warrior', (192, 64, 0), (255, 255, 255), 36)
    btn_mage = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 100, 'Mage', (64, 64, 192), (255, 255, 255), 36)
    btn_rogue = btn(surf, 2 * surf.get_width() // 3 - 100, surf.get_height() // 2, 200, 100, 'Rogue', (0, 192, 64), (255, 255, 255), 36)
    return [btn_warrior, btn_mage, btn_rogue]

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Inventory')
    slots = []
    eq_btn = btn(surf, 10, 600, 200, 30, 'Equip', (0, 128, 0), (255, 255, 255), 24)
    drop_btn = btn(surf, 220, 600, 200, 30, 'Drop', (192, 0, 0), (255, 255, 255), 24)
    for i in range(10):
        rect = pygame.draw.rect(surf, (100, 100, 100), (20 + (i % 5) * 76, 50 + (i // 5) * 76, 70, 70), 0)
        slots.append(rect)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, quest.description, 20, 50 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        rect = pygame.draw.rect(surf, (100, 100, 100), (20 + (i % 3) * 196, 50 + (i // 3) * 76, 190, 70), 0)
        items.append(rect)
        buy_btn = btn(surf, 20 + (i % 3) * 196, 130 + (i // 3) * 76, 50, 20, 'Buy', (0, 128, 0), (255, 255, 255), 18)
        buy_btns.append(buy_btn)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i in range(3):
        btn_rect = btn(surf, 20 + i * 196, 50, 190, 40, f'Tab {i+1}', (128, 128, 128), (255, 255, 255), 24)
        tab_btns.append(btn_rect)
    for i, recipe in enumerate(recipes[tab]):
        rect = pygame.draw.rect(surf, (100, 100, 100), (20 + (i % 3) * 196, 100 + (i // 3) * 76, 190, 70), 0)
        craft_btn = btn(surf, 20 + (i % 3) * 196, 180 + (i // 3) * 76, 50, 20, 'Craft', (0, 128, 0), (255, 255, 255), 18)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 10, 10, 600, 400, 'Dialogue')
    txt(surf, npc.dialogues[dial_idx], 20, 50, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        btn_rect = btn(surf, 20 + i * 196, 350, 190, 40, option.text, (128, 128, 128), (255, 255, 255), 24)
        opt_btns.append(btn_rect)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() // 4, surf.get_height() // 3, surf.get_width() // 2, surf.get_height() // 3), 0)
    txt(surf, 'Paused', surf.get_width() // 2, surf.get_height() // 3 + 10, 64, (255, 255, 255), center=True)
    btn_resume = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 50, 200, 50, 'Resume', (0, 128, 0), (255, 255, 255), 36)
    btn_options = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 120, 200, 50, 'Options', (0, 128, 128), (255, 255, 255), 36)
    btn_exit = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 190, 200, 50, 'Exit', (128, 0, 0), (255, 255, 255), 36)
    return panel_rect, [btn_resume, btn_options, btn_exit]

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 10, 10, 400, 580, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20 + (i % 3) * 126, 50 + (i // 3) * 76, 120, 70, building.name, (128, 128, 128), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'World Map', surf.get_width() // 2, 10, 64, (255, 255, 255), center=True)
    # Placeholder for world map drawing logic
    pass

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    txt(surf, 'Game Over', surf.get_width() // 2, surf.get_height() // 2 - 30, 64, (255, 255, 255), center=True)
    btn_retry = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 20, 200, 50, 'Retry', (0, 128, 0), (255, 255, 255), 36)
    btn_exit = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 90, 200, 50, 'Exit', (128, 0, 0), (255, 255, 255), 36)
    return [btn_retry, btn_exit]

def draw_player_stats(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (10, 10, 200, 200), 0)
    txt(surf, f'HP: {player.hp}/{player.max_hp}', 20, 30, 24, (255, 255, 255))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', 20, 60, 24, (255, 255, 255))
    txt(surf, f'Level: {player.level}', 20, 90, 24, (255, 255, 255))
    txt(surf, f'XP: {player.xp}/{player.next_level_xp}', 20, 120, 24, (255, 255, 255))
    return panel_rect

def draw_minimap(surf, player, world_map):
    minimap_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 110, surf.get_height() - 110, 100, 100), 0)
    # Placeholder for minimap drawing logic
    pass

def draw_player_inventory(surf, player):
    xbtn_rect = panel(surf, surf.get_width() - 420, surf.get_height() - 320, 400, 300, 'Inventory')
    slots = []
    for i in range(10):
        rect = pygame.draw.rect(surf, (100, 100, 100), (surf.get_width() - 400 + (i % 5) * 76, surf.get_height() - 300 + (i // 5) * 76, 70, 70), 0)
        slots.append(rect)
    return xbtn_rect, slots

def draw_player_equipment(surf, player):
    xbtn_rect = panel(surf, surf.get_width() - 420, surf.get_height() - 320, 400, 300, 'Equipment')
    # Placeholder for equipment drawing logic
    return xbtn_rect

def draw_player_quests(surf, player):
    xbtn_rect = panel(surf, surf.get_width() - 420, surf.get_height() - 320, 400, 300, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, quest.description, surf.get_width() - 400, surf.get_height() - 300 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_player_skills(surf, player):
    xbtn_rect = panel(surf, surf.get_width() - 420, surf.get_height() - 320, 400, 300, 'Skills')
    # Placeholder for skills drawing logic
    return xbtn_rect

def draw_player_spells(surf, player):
    xbtn_rect = panel(surf, surf.get_width() - 420, surf.get_height() - 320, 400, 300, 'Spells')
    # Placeholder for spells drawing logic
    return xbtn_rect

def draw_player_status_effects(surf, player):
    xbtn_rect = panel(surf, surf.get_width() - 420, surf.get_height() - 320, 400, 300, 'Status Effects')
    # Placeholder for status effects drawing logic
    return xbtn_rect

def draw_player_attributes(surf, player):
    xbtn_rect = panel(surf, surf.get_width() - 420, surf.get_height() - 320, 400, 300, 'Attributes')
    # Placeholder for attributes drawing logic
    return xbtn_rect

def draw_player_inventory_details(surf, player, selected_item):
    if selected_item is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 320, 400, 300), 0)
        txt(surf, selected_item.name, surf.get_width() - 400, surf.get_height() - 300, 24, (255, 255, 255))
        txt(surf, f'Description: {selected_item.description}', surf.get_width() - 400, surf.get_height() - 270, 18, (255, 255, 255))
        txt(surf, f'Type: {selected_item.type}', surf.get_width() - 400, surf.get_height() - 240, 18, (255, 255, 255))
        txt(surf, f'Value: {selected_item.value}', surf.get_width() - 400, surf.get_height() - 210, 18, (255, 255, 255))
    return panel_rect

def draw_player_equipment_details(surf, player, selected_slot):
    if selected_slot is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 320, 400, 300), 0)
        item = player.equipment[selected_slot]
        if item is not None:
            txt(surf, item.name, surf.get_width() - 400, surf.get_height() - 300, 24, (255, 255, 255))
            txt(surf, f'Description: {item.description}', surf.get_width() - 400, surf.get_height() - 270, 18, (255, 255, 255))
            txt(surf, f'Type: {item.type}', surf.get_width() - 400, surf.get_height() - 240, 18, (255, 255, 255))
            txt(surf, f'Value: {item.value}', surf.get_width() - 400, surf.get_height() - 210, 18, (255, 255, 255))
    return panel_rect

def draw_player_quest_details(surf, player, selected_quest):
    if selected_quest is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 320, 400, 300), 0)
        txt(surf, selected_quest.description, surf.get_width() - 400, surf.get_height() - 300, 24, (255, 255, 255))
        txt(surf, f'Objective: {selected_quest.objective}', surf.get_width() - 400, surf.get_height() - 270, 18, (255, 255, 255))
        txt(surf, f'Reward: {selected_quest.reward}', surf.get_width() - 400, surf.get_height() - 240, 18, (255, 255, 255))
    return panel_rect

def draw_player_skill_details(surf, player, selected_skill):
    if selected_skill is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 320, 400, 300), 0)
        txt(surf, selected_skill.name, surf.get_width() - 400, surf.get_height() - 300, 24, (255, 255, 255))
        txt(surf, f'Description: {selected_skill.description}', surf.get_width() - 400, surf.get_height() - 270, 18, (255, 255, 255))
        txt(surf, f'Cost: {selected_skill.cost} MP', surf.get_width() - 400, surf.get_height() - 240, 18, (255, 255, 255))
    return panel_rect

def draw_player_spell_details(surf, player, selected_spell):
    if selected_spell is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 320, 400, 300), 0)
        txt(surf, selected_spell.name, surf.get_width() - 400, surf.get_height() - 300, 24, (255, 255, 255))
        txt(surf, f'Description: {selected_spell.description}', surf.get_width() - 400, surf.get_height() - 270, 18, (255, 255, 255))
        txt(surf, f'Cost: {selected_spell.cost} MP', surf.get_width() - 400, surf.get_height() - 240, 18, (255, 255, 255))
    return panel_rect

def draw_player_status_effect_details(surf, player, selected_effect):
    if selected_effect is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 320, 400, 300), 0)
        txt(surf, selected_effect.name, surf.get_width() - 400, surf.get_height() - 300, 24, (255, 255, 255))
        txt(surf, f'Description: {selected_effect.description}', surf.get_width() - 400, surf.get_height() - 270, 18, (255, 255, 255))
        txt(surf, f'Duration: {selected_effect.duration} turns', surf.get_width() - 400, surf.get_height() - 240, 18, (255, 255, 255))
    return panel_rect

def draw_player_attribute_details(surf, player, selected_attribute):
    if selected_attribute is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 320, 400, 300), 0)
        txt(surf, selected_attribute.name, surf.get_width() - 400, surf.get_height() - 300, 24, (255, 255, 255))
        txt(surf, f'Description: {selected_attribute.description}', surf.get_width() - 400, surf.get_height() - 270, 18, (255, 255, 255))
        txt(surf, f'Value: {getattr(player, selected_attribute.name)}', surf.get_width() - 400, surf.get_height() - 240, 18, (255, 255, 255))
    return panel_rect

def draw_player_inventory_actions(surf, player, selected_item):
    if selected_item is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 160, 400, 150), 0)
        btn_use = btn(surf, 'Use', surf.get_width() - 380, surf.get_height() - 140, 120, 40, (0, 128, 0), (0, 255, 0))
        btn_drop = btn(surf, 'Drop', surf.get_width() - 250, surf.get_height() - 140, 120, 40, (128, 0, 0), (255, 0, 0))
        btn_equip = btn(surf, 'Equip', surf.get_width() - 380, surf.get_height() - 90, 120, 40, (0, 0, 128), (0, 0, 255))
        return panel_rect, btn_use, btn_drop, btn_equip
    return None

def draw_player_equipment_actions(surf, player, selected_slot):
    if selected_slot is not None:
        item = player.equipment[selected_slot]
        if item is not None:
            panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 160, 400, 150), 0)
            btn_unequip = btn(surf, 'Unequip', surf.get_width() - 380, surf.get_height() - 140, 120, 40, (128, 0, 0), (255, 0, 0))
            return panel_rect, btn_unequip
    return None

def draw_player_quest_actions(surf, player, selected_quest):
    if selected_quest is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 160, 400, 150), 0)
        btn_complete = btn(surf, 'Complete', surf.get_width() - 380, surf.get_height() - 140, 120, 40, (0, 128, 0), (0, 255, 0))
        return panel_rect, btn_complete
    return None

def draw_player_skill_actions(surf, player, selected_skill):
    if selected_skill is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 160, 400, 150), 0)
        btn_cast = btn(surf, 'Cast', surf.get_width() - 380, surf.get_height() - 140, 120, 40, (0, 128, 0), (0, 255, 0))
        return panel_rect, btn_cast
    return None

def draw_player_spell_actions(surf, player, selected_spell):
    if selected_spell is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 160, 400, 150), 0)
        btn_cast = btn(surf, 'Cast', surf.get_width() - 380, surf.get_height() - 140, 120, 40, (0, 128, 0), (0, 255, 0))
        return panel_rect, btn_cast
    return None

def draw_player_status_effect_actions(surf, player, selected_effect):
    if selected_effect is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 160, 400, 150), 0)
        btn_remove = btn(surf, 'Remove', surf.get_width() - 380, surf.get_height() - 140, 120, 40, (128, 0, 0), (255, 0, 0))
        return panel_rect, btn_remove
    return None

def draw_player_attribute_actions(surf, player, selected_attribute):
    if selected_attribute is not None:
        panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 160, 400, 150), 0)
        btn_increase = btn(surf, 'Increase', surf.get_width() - 380, surf.get_height() - 140, 120, 40, (0, 128, 0), (0, 255, 0))
        return panel_rect, btn_increase
    return None

def draw_player_inventory_list(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 360, 400, 300), 0)
    font = pygame.font.Font(None, 24)
    for i, item in enumerate(player.inventory):
        text = font.render(item.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 410, surf.get_height() - 350 + i * 30))
    return panel_rect

def draw_player_equipment_list(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 360, 400, 300), 0)
    font = pygame.font.Font(None, 24)
    for i, item in enumerate(player.equipment):
        if item is not None:
            text = font.render(item.name, True, (255, 255, 255))
        else:
            text = font.render('Empty', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 410, surf.get_height() - 350 + i * 30))
    return panel_rect

def draw_player_quest_list(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 360, 400, 300), 0)
    font = pygame.font.Font(None, 24)
    for i, quest in enumerate(player.quests):
        text = font.render(quest.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 410, surf.get_height() - 350 + i * 30))
    return panel_rect

def draw_player_skill_list(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 360, 400, 300), 0)
    font = pygame.font.Font(None, 24)
    for i, skill in enumerate(player.skills):
        text = font.render(skill.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 410, surf.get_height() - 350 + i * 30))
    return panel_rect

def draw_player_spell_list(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 360, 400, 300), 0)
    font = pygame.font.Font(None, 24)
    for i, spell in enumerate(player.spells):
        text = font.render(spell.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 410, surf.get_height() - 350 + i * 30))
    return panel_rect

def draw_player_status_effect_list(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 360, 400, 300), 0)
    font = pygame.font.Font(None, 24)
    for i, effect in enumerate(player.status_effects):
        text = font.render(effect.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 410, surf.get_height() - 350 + i * 30))
    return panel_rect

def draw_player_attribute_list(surf, player):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 420, surf.get_height() - 360, 400, 300), 0)
    font = pygame.font.Font(None, 24)
    for i, attribute in enumerate(player.attributes):
        text = font.render(attribute.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 410, surf.get_height() - 350 + i * 30))
    return panel_rect

def draw_player_inventory_selection(surf, player):
    panel_rect = draw_player_inventory_list(surf, player)
    selected_item = None
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, item in enumerate(player.inventory):
                if surf.get_width() - 410 <= mouse_pos[0] <= surf.get_width() - 310 and surf.get_height() - 350 + i * 30 <= mouse_pos[1] <= surf.get_height() - 320 + i * 30:
                    selected_item = item
    return panel_rect, selected_item

def draw_player_equipment_selection(surf, player):
    panel_rect = draw_player_equipment_list(surf, player)
    selected_slot = None
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(player.equipment)):
                if surf.get_width() - 410 <= mouse_pos[0] <= surf.get_width() - 310 and surf.get_height() - 350 + i * 30 <= mouse_pos[1] <= surf.get_height() - 320 + i * 30:
                    selected_slot = i
    return panel_rect, selected_slot

def draw_player_quest_selection(surf, player):
    panel_rect = draw_player_quest_list(surf, player)
    selected_quest = None
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, quest in enumerate(player.quests):
                if surf.get_width() - 410 <= mouse_pos[0] <= surf.get_width() - 310 and surf.get_height() - 350 + i * 30 <= mouse_pos[1] <= surf.get_height() - 320 + i * 30:
                    selected_quest = quest
    return panel_rect, selected_quest

def draw_player_skill_selection(surf, player):
    panel_rect = draw_player_skill_list(surf, player)
    selected_skill = None
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, skill in enumerate(player.skills):
                if surf.get_width() - 410 <= mouse_pos[0] <= surf.get_width() - 310 and surf.get_height() - 350 + i * 30 <= mouse_pos[1] <= surf.get_height() - 320 + i * 30:
                    selected_skill = skill
    return panel_rect, selected_skill

def draw_player_spell_selection(surf, player):
    panel_rect = draw_player_spell_list(surf, player)
    selected_spell = None
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, spell in enumerate(player.spells):
                if surf.get_width() - 410 <= mouse_pos[0] <= surf.get_width() - 310 and surf.get_height() - 350 + i * 30 <= mouse_pos[1] <= surf.get_height() - 320 + i * 30:
                    selected_spell = spell
    return panel_rect, selected_spell

def draw_player_status_effect_selection(surf, player):
    panel_rect = draw_player_status_effect_list(surf, player)
    selected_effect = None
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, effect in enumerate(player.status_effects):
                if surf.get_width() - 410 <= mouse_pos[0] <= surf.get_width() - 310 and surf.get_height() - 350 + i * 30 <= mouse_pos[1] <= surf.get_height() - 320 + i * 30:
                    selected_effect = effect
    return panel_rect, selected_effect

def draw_player_attribute_selection(surf, player):
    panel_rect = draw_player_attribute_list(surf, player)
    selected_attribute = None
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, attribute in enumerate(player.attributes):
                if surf.get_width() - 410 <= mouse_pos[0] <= surf.get_width() - 310 and surf.get_height() - 350 + i * 30 <= mouse_pos[1] <= surf.get_height() - 320 + i * 30:
                    selected_attribute = attribute
    return panel_rect, selected_attribute

def draw_player_inventory_interface(surf, player):
    panel_rect, selected_item = draw_player_inventory_selection(surf, player)
    if selected_item is not None:
        details_panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 360, 400, 300), 0)
        font = pygame.font.Font(None, 24)
        text = font.render(selected_item.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
        text = font.render(f'Description: {selected_item.description}', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 320))
        actions_panel_rect, action_button = draw_player_inventory_actions(surf, selected_item)
    return panel_rect

def draw_player_equipment_interface(surf, player):
    panel_rect, selected_slot = draw_player_equipment_selection(surf, player)
    if selected_slot is not None:
        item = player.equipment[selected_slot]
        details_panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 360, 400, 300), 0)
        font = pygame.font.Font(None, 24)
        if item is not None:
            text = font.render(item.name, True, (255, 255, 255))
            surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
            text = font.render(f'Description: {item.description}', True, (255, 255, 255))
            surf.blit(text, (surf.get_width() - 810, surf.get_height() - 320))
        else:
            text = font.render('Empty', True, (255, 255, 255))
            surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
        actions_panel_rect, action_button = draw_player_equipment_actions(surf, item)
    return panel_rect

def draw_player_quest_interface(surf, player):
    panel_rect, selected_quest = draw_player_quest_selection(surf, player)
    if selected_quest is not None:
        details_panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 360, 400, 300), 0)
        font = pygame.font.Font(None, 24)
        text = font.render(selected_quest.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
        text = font.render(f'Description: {selected_quest.description}', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 320))
        actions_panel_rect, action_button = draw_player_quest_actions(surf, selected_quest)
    return panel_rect

def draw_player_skill_interface(surf, player):
    panel_rect, selected_skill = draw_player_skill_selection(surf, player)
    if selected_skill is not None:
        details_panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 360, 400, 300), 0)
        font = pygame.font.Font(None, 24)
        text = font.render(selected_skill.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
        text = font.render(f'Description: {selected_skill.description}', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 320))
        actions_panel_rect, action_button = draw_player_skill_actions(surf, selected_skill)
    return panel_rect

def draw_player_spell_interface(surf, player):
    panel_rect, selected_spell = draw_player_spell_selection(surf, player)
    if selected_spell is not None:
        details_panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 360, 400, 300), 0)
        font = pygame.font.Font(None, 24)
        text = font.render(selected_spell.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
        text = font.render(f'Description: {selected_spell.description}', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 320))
        actions_panel_rect, action_button = draw_player_spell_actions(surf, selected_spell)
    return panel_rect

def draw_player_status_effect_interface(surf, player):
    panel_rect, selected_effect = draw_player_status_effect_selection(surf, player)
    if selected_effect is not None:
        details_panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 360, 400, 300), 0)
        font = pygame.font.Font(None, 24)
        text = font.render(selected_effect.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
        text = font.render(f'Description: {selected_effect.description}', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 320))
        actions_panel_rect, action_button = draw_player_status_effect_actions(surf, selected_effect)
    return panel_rect

def draw_player_attribute_interface(surf, player):
    panel_rect, selected_attribute = draw_player_attribute_selection(surf, player)
    if selected_attribute is not None:
        details_panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 360, 400, 300), 0)
        font = pygame.font.Font(None, 24)
        text = font.render(selected_attribute.name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 350))
        text = font.render(f'Description: {selected_attribute.description}', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 320))
        actions_panel_rect, action_button = draw_player_attribute_actions(surf, selected_attribute)
    return panel_rect

def draw_player_inventory_actions(surf, item):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 60, 400, 30), 0)
    font = pygame.font.Font(None, 24)
    text = font.render('Use', True, (255, 255, 255))
    surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
    action_button = 'use'
    return panel_rect, action_button

def draw_player_equipment_actions(surf, item):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 60, 400, 30), 0)
    font = pygame.font.Font(None, 24)
    if item is not None:
        text = font.render('Unequip', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
        action_button = 'unequip'
    else:
        text = font.render('Equip', True, (255, 255, 255))
        surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
        action_button = 'equip'
    return panel_rect, action_button

def draw_player_quest_actions(surf, quest):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 60, 400, 30), 0)
    font = pygame.font.Font(None, 24)
    text = font.render('Accept', True, (255, 255, 255))
    surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
    action_button = 'accept'
    return panel_rect, action_button

def draw_player_skill_actions(surf, skill):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 60, 400, 30), 0)
    font = pygame.font.Font(None, 24)
    text = font.render('Use', True, (255, 255, 255))
    surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
    action_button = 'use'
    return panel_rect, action_button

def draw_player_spell_actions(surf, spell):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 60, 400, 30), 0)
    font = pygame.font.Font(None, 24)
    text = font.render('Cast', True, (255, 255, 255))
    surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
    action_button = 'cast'
    return panel_rect, action_button

def draw_player_status_effect_actions(surf, effect):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 60, 400, 30), 0)
    font = pygame.font.Font(None, 24)
    text = font.render('Remove', True, (255, 255, 255))
    surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
    action_button = 'remove'
    return panel_rect, action_button

def draw_player_attribute_actions(surf, attribute):
    panel_rect = pygame.draw.rect(surf, (50, 50, 50), (surf.get_width() - 820, surf.get_height() - 60, 400, 30), 0)
    font = pygame.font.Font(None, 24)
    text = font.render('Upgrade', True, (255, 255, 255))
    surf.blit(text, (surf.get_width() - 810, surf.get_height() - 50))
    action_button = 'upgrade'
    return panel_rect, action_button

# Example usage
pygame.init()
screen = pygame.display.set_mode((1280, 720))

player = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_player_inventory_interface(screen, player)
    pygame.display.flip()

pygame.quit()

# This code sets up a basic Pygame window and defines a `Player` class with various attributes like inventory, equipment, quests, skills, spells, status effects, and attributes. The interfaces for each of these are defined in functions that draw the necessary UI elements on the screen.

# The `draw_player_inventory_interface` function is an example of how you might draw the inventory interface, including a selection panel, details panel, and actions panel. Similar functions are provided for other player attributes.
