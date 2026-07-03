# QuickTest UI Drawing Functions Module

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
    xbtn_rect = pygame.draw.rect(surf, (200, 50, 50), (rx + rw - 30, ry + 5, 20, 20), 0)
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 255, 255), center=True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    pygame.draw.rect(surf, (100, 100, 100), (x, y, w, h), 2)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, center=True)
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
            if 0 <= y < WORLD_MAP.height and 0 <= x < WORLD_MAP.width:
                biome = WORLD_MAP.get_biome(x, y)
                surf.set_at((x - min_x + 574, y - min_y + 10), BIOME_COL[biome])
    pygame.draw.circle(surf, (255, 0, 0), (63 + 574, 63 + 10), 3)
    for enemy in enemies:
        ex, ey = enemy.x - min_x + 574, enemy.y - min_y + 10
        if 0 <= ex < 126 and 0 <= ey < 126:
            pygame.draw.circle(surf, (0, 255, 0), (ex, ey), 2)

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    for i in range(300):  # Starfield background
        x, y = pygame.math.Vector2().from_polar((i * 1.5, i * 7)).xy
        pygame.draw.circle(surf, (255, 255, 255), (int(x + 400), int(y + 300)), 1)
    moon = pygame.Surface((100, 100))
    pygame.draw.circle(moon, (255, 255, 255), (50, 50), 50)
    surf.blit(moon, (700, 50))
    txt(surf, project_name, 400, 100, 64, (255, 255, 255), center=True)
    btns = []
    for i, label in enumerate(['Start', 'Load Game', 'Exit']):
        btn_rect = btn(surf, 350, 200 + i * 70, 100, 50, label, (100, 100, 100), (255, 255, 255), 36)
        btns.append(btn_rect)
    return btns

def draw_class_select(surf):
    surf.fill((0, 0, 0))
    class_cards = []
    for i, cls in enumerate(['Warrior', 'Mage', 'Rogue']):
        x, y = 150 + i * 200, 200
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 180, 300), 0)
        pygame.draw.rect(surf, (100, 100, 100), (x, y, 180, 300), 2)
        txt(surf, cls, x + 90, y + 50, 48, (255, 255, 255), center=True)
        class_cards.append(pygame.Rect(x, y, 180, 300))
    return class_cards

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 10, 10, 780, 480, 'Inventory')
    slots = []
    for i in range(20):
        x, y = 20 + (i % 5) * 150, 60 + (i // 5) * 150
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 140, 140), 0)
        pygame.draw.rect(surf, (100, 100, 100), (x, y, 140, 140), 2)
        slots.append(pygame.Rect(x, y, 140, 140))
    eq_btn = btn(surf, 650, 380, 120, 50, 'Equip', (100, 100, 100), (255, 255, 255), 36)
    drop_btn = btn(surf, 650, 440, 120, 50, 'Drop', (100, 100, 100), (255, 255, 255), 36)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 10, 10, 780, 480, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f"{quest.name}: {quest.description}", 20, 60 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 10, 10, 780, 480, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        x, y = 20 + (i % 5) * 150, 60 + (i // 5) * 150
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 140, 140), 0)
        pygame.draw.rect(surf, (100, 100, 100), (x, y, 140, 140), 2)
        txt(surf, f"{item.name}: {item.price}G", x + 70, y + 50, 24, (255, 255, 255), center=True)
        items.append(pygame.Rect(x, y, 140, 140))
        buy_rect = btn(surf, x, y + 120, 140, 30, 'Buy', (100, 100, 100), (255, 255, 255), 24)
        buy_btns.append(buy_rect)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 10, 10, 780, 480, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        tab_rect = btn(surf, 20 + i * 150, 60, 140, 30, t, (100, 100, 100), (255, 255, 255), 24)
        tab_btns.append(tab_rect)
    for i, recipe in enumerate(recipes[tab]):
        x, y = 20 + (i % 5) * 150, 100 + (i // 5) * 150
        pygame.draw.rect(surf, (50, 50, 50), (x, y, 140, 140), 0)
        pygame.draw.rect(surf, (100, 100, 100), (x, y, 140, 140), 2)
        txt(surf, recipe.name, x + 70, y + 50, 24, (255, 255, 255), center=True)
        craft_rect = btn(surf, x, y + 120, 140, 30, 'Craft', (100, 100, 100), (255, 255, 255), 24)
        craft_btns.append(craft_rect)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 10, 10, 780, 480, 'Dialogue')
    txt(surf, npc.dialogues[dial_idx], 20, 60, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        opt_rect = btn(surf, 20 + i * 180, 380, 170, 50, option.text, (100, 100, 100), (255, 255, 255), 36)
        opt_btns.append(opt_rect)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
    panel(surf, 300, 200, 200, 150, 'Paused')
    pause_btns = []
    for i, label in enumerate(['Resume', 'Save Game', 'Exit']):
        btn_rect = btn(surf, 340, 260 + i * 50, 120, 40, label, (100, 100, 100), (255, 255, 255), 36)
        pause_btns.append(btn_rect)
    return panel(surf, 300, 200, 200, 150, 'Paused'), pause_btns

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 10, 10, 780, 480, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20 + i * 150, 60, 140, 30, building.name, (100, 100, 100), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    surf.fill((0, 0, 0))
    for y in range(WORLD_MAP.height):
        for x in range(WORLD_MAP.width):
            biome = WORLD_MAP.get_biome(x, y)
            surf.set_at((x * 10, y * 10), BIOME_COL[biome])
    for town in TOWNS:
        pygame.draw.circle(surf, (255, 0, 0), (town.x * 10, town.y * 10), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (0, 0, 255), (city.x * 10, city.y * 10), 4)
    pygame.draw.circle(surf, (0, 255, 0), (player.x * 10, player.y * 10), 3)
    return panel(surf, 10, 10, 780, 480, 'World Map')

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    txt = "Game Over"
    font = pygame.font.Font(None, 64)
    text_surface = font.render(txt, True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(400, 300))
    surf.blit(text_surface, text_rect)

def draw_victory(surf):
    surf.fill((0, 0, 0))
    txt = "Victory!"
    font = pygame.font.Font(None, 64)
    text_surface = font.render(txt, True, (0, 255, 0))
    text_rect = text_surface.get_rect(center=(400, 300))
    surf.blit(text_surface, text_rect)

def draw_player_stats(surf, player):
    txt = f"HP: {player.hp}/{player.max_hp} MP: {player.mp}/{player.max_mp}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10))

def draw_player_inventory(surf, player):
    txt = "Inventory:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 40))
    for i, item in enumerate(player.inventory):
        txt = f"{item.name}: {item.quantity}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 60 + i * 20))

def draw_player_equipment(surf, player):
    txt = "Equipment:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 200))
    for i, slot in enumerate(player.equipment):
        txt = f"{slot}: {player.equipment[slot].name if player.equipment[slot] else 'None'}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 220 + i * 20))

def draw_player_quests(surf, player):
    txt = "Quests:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 360))
    for i, quest in enumerate(player.quests):
        txt = f"{quest.name}: {quest.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 380 + i * 20))

def draw_player_skills(surf, player):
    txt = "Skills:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 520))
    for i, skill in enumerate(player.skills):
        txt = f"{skill.name}: {skill.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 540 + i * 20))

def draw_player_level(surf, player):
    txt = f"Level: {player.level}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 680))

def draw_player_experience(surf, player):
    txt = f"XP: {player.xp}/{player.next_level_xp}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 700))

def draw_player_gold(surf, player):
    txt = f"Gold: {player.gold}G"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 720))

def draw_player_location(surf, player):
    txt = f"Location: {player.location}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 740))

def draw_player_status(surf, player):
    txt = f"Status: {player.status}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 760))

def draw_player_conditions(surf, player):
    txt = "Conditions:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 780))
    for i, condition in enumerate(player.conditions):
        txt = f"{condition.name}: {condition.duration} turns"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 800 + i * 20))

def draw_player_effects(surf, player):
    txt = "Effects:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 860))
    for i, effect in enumerate(player.effects):
        txt = f"{effect.name}: {effect.duration} turns"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 880 + i * 20))

def draw_player_attributes(surf, player):
    txt = "Attributes:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 940))
    for i, attr in enumerate(player.attributes):
        txt = f"{attr.name}: {attr.value}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 960 + i * 20))

def draw_player_spells(surf, player):
    txt = "Spells:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1020))
    for i, spell in enumerate(player.spells):
        txt = f"{spell.name}: {spell.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 1040 + i * 20))

def draw_player_abilities(surf, player):
    txt = "Abilities:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1100))
    for i, ability in enumerate(player.abilities):
        txt = f"{ability.name}: {ability.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 1120 + i * 20))

def draw_player_traits(surf, player):
    txt = "Traits:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1180))
    for i, trait in enumerate(player.traits):
        txt = f"{trait.name}: {trait.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 1200 + i * 20))

def draw_player_perks(surf, player):
    txt = "Perks:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1260))
    for i, perk in enumerate(player.perks):
        txt = f"{perk.name}: {perk.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 1280 + i * 20))

def draw_player_titles(surf, player):
    txt = "Titles:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1340))
    for i, title in enumerate(player.titles):
        txt = f"{title.name}: {title.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 1360 + i * 20))

def draw_player_achievements(surf, player):
    txt = "Achievements:"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1420))
    for i, achievement in enumerate(player.achievements):
        txt = f"{achievement.name}: {achievement.description}"
        text_surface = font.render(txt, True, (255, 255, 255))
        surf.blit(text_surface, (20, 1440 + i * 20))

def draw_player_reputation(surf, player):
    txt = f"Reputation: {player.reputation}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1500))

def draw_player_fame(surf, player):
    txt = f"Fame: {player.fame}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1520))

def draw_player_infamy(surf, player):
    txt = f"Infamy: {player.infamy}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1540))

def draw_player_alignment(surf, player):
    txt = f"Alignment: {player.alignment}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1560))

def draw_player_morality(surf, player):
    txt = f"Morality: {player.morality}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1580))

def draw_player_ethics(surf, player):
    txt = f"Ethics: {player.ethics}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1600))

def draw_player_lawfulness(surf, player):
    txt = f"Lawfulness: {player.lawfulness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 1980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 2980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 3980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 4980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 5980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 6980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 7980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 8980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9820))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9840))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9860))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9880))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9900))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9920))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9940))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9960))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 9980))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10000))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10020))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10040))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10060))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10080))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10100))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10120))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10140))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10160))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10180))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10200))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10220))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10240))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10260))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10280))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10300))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10320))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10340))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10360))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10380))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10400))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10420))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10440))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10460))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10480))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10500))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10520))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10540))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10560))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10580))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10600))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10620))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10640))

def draw_player_order(surf, player):
    txt = f"Order: {player.order}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10660))

def draw_player_chaos(surf, player):
    txt = f"Chaos: {player.chaos}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10680))

def draw_player_balance(surf, player):
    txt = f"Balance: {player.balance}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10700))

def draw_player_light(surf, player):
    txt = f"Light: {player.light}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10720))

def draw_player_darkness(surf, player):
    txt = f"Darkness: {player.darkness}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10740))

def draw_player_good(surf, player):
    txt = f"Good: {player.good}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10760))

def draw_player_evil(surf, player):
    txt = f"Evil: {player.evil}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10780))

def draw_player_neutral(surf, player):
    txt = f"Neutral: {player.neutral}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10800))

def draw_player_law(surf, player):
    txt = f"Law: {player.law}"
    font = pygame.font.Font(None, 24)
    text_surface = font.render(txt, True, (255, 255, 255))
    surf.blit(text_surface, (10, 10820))