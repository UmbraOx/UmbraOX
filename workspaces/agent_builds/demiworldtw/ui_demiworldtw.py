import pygame

def font(size):
    return pygame.font.Font(None, size)

def txt(surf, text, x, y, size, col, center=False):
    f = font(size)
    t = f.render(text, True, col)
    if center:
        rect = t.get_rect(center=(x, y))
    else:
        rect = t.get_rect(topleft=(x, y))
    surf.blit(t, rect)

def draw_bar(surf, x, y, w, h, val, mx, col, bg):
    pygame.draw.rect(surf, bg, (x, y, w, h), 0)
    inner_width = int(w * min(1, max(0, val / mx)))
    pygame.draw.rect(surf, col, (x, y, inner_width, h), 0)

def draw_x_button(surf, rx, ry, rw, rh):
    pygame.draw.rect(surf, (255, 0, 0), (rx, ry, rw, rh))
    txt(surf, 'X', rx + rw // 2, ry + rh // 2, 24, (255, 255, 255), True)
    return pygame.Rect(rx, ry, rw, rh)

def draw_panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (30, 30, 30), (rx, ry, rw, rh))
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    return draw_x_button(surf, rx + rw - 30, ry, 25, 25)

def draw_hud(surf, player):
    x = 10
    y = 10
    txt(surf, f'HP: {player.hp}/{player.max_hp}', x, y, 24, (255, 0, 0))
    draw_bar(surf, x + 80, y + 3, 200, 20, player.hp, player.max_hp, (255, 0, 0), (100, 0, 0))
    txt(surf, f'MP: {player.mp}/{player.max_mp}', x, y + 30, 24, (0, 0, 255))
    draw_bar(surf, x + 80, y + 33, 200, 20, player.mp, player.max_mp, (0, 0, 255), (0, 0, 100))
    txt(surf, f'STA: {player.sta}/{player.max_sta}', x, y + 60, 24, (255, 165, 0))
    draw_bar(surf, x + 80, y + 63, 200, 20, player.sta, player.max_sta, (255, 165, 0), (100, 84, 0))
    txt(surf, f'Gold: {player.gold}', x, y + 90, 24, (255, 215, 0))
    txt(surf, f'Lvl: {player.level} XP: {player.xp}/{player.next_level_xp}', x, y + 120, 24, (255, 255, 255))
    txt(surf, 'Equipped:', x, y + 150, 24, (255, 255, 255))
    for i, item in enumerate(player.equipped):
        txt(surf, f'{item.name}', x, y + 180 + i * 30, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies):
    pygame.draw.rect(surf, (0, 0, 0), (surf.get_width() - 130, 10, 120, 120))
    txt(surf, 'Minimap', surf.get_width() - 65, 15, 24, (255, 255, 255), True)
    pygame.draw.circle(surf, (0, 255, 0), (surf.get_width() - 70 + player.x // 10, 70 + player.y // 10), 3)
    for enemy in enemies:
        pygame.draw.circle(surf, (255, 0, 0), (surf.get_width() - 70 + enemy.x // 10, 70 + enemy.y // 10), 2)

def draw_inventory(surf, player, selected):
    xbtn = draw_panel(surf, 100, 100, 600, 400, 'Inventory')
    slot_btns = []
    equip_btn = pygame.Rect(500, 300, 80, 30)
    drop_btn = pygame.Rect(590, 300, 80, 30)
    for i, item in enumerate(player.inventory):
        btn = pygame.Rect(120 + (i % 4) * 120, 140 + (i // 4) * 60, 100, 50)
        slot_btns.append(btn)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), btn, 3)
        txt(surf, item.name, btn.x + 5, btn.y + 5, 18, (255, 255, 255))
    pygame.draw.rect(surf, (0, 255, 0) if selected is not None else (100, 100, 100), equip_btn)
    txt(surf, 'Equip', equip_btn.x + 10, equip_btn.y + 5, 18, (255, 255, 255))
    pygame.draw.rect(surf, (255, 0, 0) if selected is not None else (100, 100, 100), drop_btn)
    txt(surf, 'Drop', drop_btn.x + 10, drop_btn.y + 5, 18, (255, 255, 255))
    return xbtn, slot_btns, equip_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn = draw_panel(surf, 100, 100, 600, 400, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.name}: {quest.description}', 120, 140 + i * 30, 18, (255, 255, 255))
    return xbtn

def draw_shop(surf, npc, player, selected):
    xbtn = draw_panel(surf, 100, 100, 600, 400, f'Shop - {npc.name}')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        btn = pygame.Rect(120 + (i % 3) * 180, 140 + (i // 3) * 60, 150, 50)
        buy_btns.append(btn)
        items.append(item)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), btn, 3)
        txt(surf, f'{item.name} - {item.price}', btn.x + 5, btn.y + 5, 18, (255, 255, 255))
    return xbtn, buy_btns, items

def draw_crafting(surf, player, tab, selected):
    xbtn = draw_panel(surf, 100, 100, 600, 400, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        btn = pygame.Rect(120 + i * 150, 140, 130, 30)
        tab_btns.append(btn)
        if tab == i:
            pygame.draw.rect(surf, (255, 255, 0), btn, 3)
        txt(surf, t, btn.x + 5, btn.y + 5, 18, (255, 255, 255))
    recipes = player.crafting_recipes[tab]
    for i, recipe in enumerate(recipes):
        btn = pygame.Rect(120 + (i % 3) * 180, 190 + (i // 3) * 60, 150, 50)
        craft_btns.append(btn)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), btn, 3)
        txt(surf, recipe.name, btn.x + 5, btn.y + 5, 18, (255, 255, 255))
    return xbtn, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn = draw_panel(surf, 100, 100, 600, 400, f'Dialogue - {npc.name}')
    opt_btns = []
    options = npc.dialogues[dial_idx].options
    for i, option in enumerate(options):
        btn = pygame.Rect(120, 140 + i * 50, 560, 40)
        opt_btns.append(btn)
        txt(surf, option.text, btn.x + 5, btn.y + 5, 18, (255, 255, 255))
    return xbtn, opt_btns

def draw_pause(surf):
    pygame.draw.rect(surf, (0, 0, 0, 128), (0, 0, surf.get_width(), surf.get_height()))
    panel = pygame.Rect(100, 100, 600, 400)
    pygame.draw.rect(surf, (30, 30, 30), panel)
    txt(surf, 'Paused', panel.x + 300, panel.y + 20, 36, (255, 255, 255), True)
    pause_btns = []
    for i, text in enumerate(['Resume', 'Save Game', 'Load Game', 'Main Menu']):
        btn = pygame.Rect(panel.x + 150, panel.y + 80 + i * 60, 300, 40)
        pause_btns.append(btn)
        txt(surf, text, btn.x + 10, btn.y + 5, 24, (255, 255, 255))
    xbtn = draw_x_button(surf, panel.right - 30, panel.top, 25, 25)
    return xbtn, pause_btns

def draw_main_menu(surf):
    pygame.draw.rect(surf, (0, 0, 0), (0, 0, surf.get_width(), surf.get_height()))
    txt(surf, 'DemiWorldTw', surf.get_width() // 2, surf.get_height() // 4, 72, (255, 255, 255), True)
    btns = {}
    for i, text in enumerate(['New Game', 'Load Game', 'Exit']):
        btn = pygame.Rect(surf.get_width() // 3, surf.get_height() // 2 + i * 60, surf.get_width() // 3, 40)
        btns[text] = btn
        txt(surf, text, btn.x + 10, btn.y + 5, 24, (255, 255, 255))
    return btns

def draw_class_select(surf):
    pygame.draw.rect(surf, (0, 0, 0), (0, 0, surf.get_width(), surf.get_height()))
    txt(surf, 'Select Class', surf.get_width() // 2, surf.get_height() // 4, 72, (255, 255, 255), True)
    btns = {}
    for i, text in enumerate(['Warrior', 'Mage', 'Rogue']):
        btn = pygame.Rect(surf.get_width() // 3, surf.get_height() // 2 + i * 60, surf.get_width() // 3, 40)
        btns[text] = btn
        txt(surf, text, btn.x + 10, btn.y + 5, 24, (255, 255, 255))
    return btns

def draw_city_build(surf, player, buildings, place_type):
    xbtn = draw_panel(surf, 100, 100, 600, 400, 'City Build')
    type_btns = []
    for i, btype in enumerate(['House', 'Shop', 'Barracks']):
        btn = pygame.Rect(120 + i * 150, 140, 130, 30)
        type_btns.append(btn)
        if place_type == btype:
            pygame.draw.rect(surf, (255, 255, 0), btn, 3)
        txt(surf, btype, btn.x + 5, btn.y + 5, 18, (255, 255, 255))
    return xbtn, type_btns

def draw_world_map(surf, player, towns, cities):
    pygame.draw.rect(surf, (0, 0, 0), (0, 0, surf.get_width(), surf.get_height()))
    txt(surf, 'World Map', surf.get_width() // 2, 50, 72, (255, 255, 255), True)
    for town in towns:
        pygame.draw.circle(surf, (0, 255, 0), (town.x, town.y), 5)
        txt(surf, town.name, town.x + 10, town.y - 10, 18, (255, 255, 255))
    for city in cities:
        pygame.draw.circle(surf, (0, 0, 255), (city.x, city.y), 7)
        txt(surf, city.name, city.x + 10, city.y - 10, 18, (255, 255, 255))
    pygame.draw.circle(surf, (255, 255, 0), (player.x, player.y), 3)
    xbtn = draw_x_button(surf, surf.get_width() - 30, 30, 25, 25)
    return xbtn

def draw_game_over(surf):
    pygame.draw.rect(surf, (0, 0, 0, 128), (0, 0, surf.get_width(), surf.get_height()))
    txt(surf, 'Game Over', surf.get_width() // 2, surf.get_height() // 3, 72, (255, 255, 255), True)
    btn = pygame.Rect(surf.get_width() // 3, surf.get_height() // 2, surf.get_width() // 3, 40)
    txt(surf, 'Main Menu', btn.x + 10, btn.y + 5, 24, (255, 255, 255))
    return btn

def draw_victory(surf):
    pygame.draw.rect(surf, (0, 0, 0, 128), (0, 0, surf.get_width(), surf.get_height()))
    txt(surf, 'Victory!', surf.get_width() // 2, surf.get_height() // 3, 72, (255, 255, 255), True)
    btn = pygame.Rect(surf.get_width() // 3, surf.get_height() // 2, surf.get_width() // 3, 40)
    txt(surf, 'Main Menu', btn.x + 10, btn.y + 5, 24, (255, 255, 255))
    return btn

def draw_inventory(surf, player):
    xbtn = draw_panel(surf, 100, 100, 600, 400, 'Inventory')
    for i, item in enumerate(player.inventory):
        txt(surf, f'{item.name} - {item.quantity}', 120, 140 + i * 30, 18, (255, 255, 255))
    return xbtn

def draw_stats(surf, player):
    xbtn = draw_panel(surf, 100, 100, 600, 400, 'Stats')
    txt(surf, f'Level: {player.level}', 120, 140, 18, (255, 255, 255))
    txt(surf, f'Experience: {player.experience}/{player.next_level_exp}', 120, 170, 18, (255, 255, 255))
    txt(surf, f'Health: {player.health}/{player.max_health}', 120, 200, 18, (255, 255, 255))
    txt(surf, f'Mana: {player.mana}/{player.max_mana}', 120, 230, 18, (255, 255, 255))
    txt(surf, f'Attack: {player.attack}', 120, 260, 18, (255, 255, 255))
    txt(surf, f'Defense: {player.defense}', 120, 290, 18, (255, 255, 255))
    return xbtn

def draw_map(surf, player, tiles):
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            color = (255, 255, 255) if tile.walkable else (100, 100, 100)
            pygame.draw.rect(surf, color, (x * 32, y * 32, 32, 32))
    pygame.draw.circle(surf, (255, 0, 0), (player.x * 32 + 16, player.y * 32 + 16), 8)

def draw_minimap(surf, player, tiles):
    mini_surf = pygame.Surface((100, 100))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            color = (255, 255, 255) if tile.walkable else (100, 100, 100)
            pygame.draw.rect(mini_surf, color, ((x / len(tiles[0])) * 100, (y / len(tiles)) * 100, 100 / len(tiles[0]), 100 / len(tiles)))
    pygame.draw.circle(mini_surf, (255, 0, 0), ((player.x / len(tiles[0])) * 100 + 5, (player.y / len(tiles)) * 100 + 5), 3)
    surf.blit(pygame.transform.scale(mini_surf, (200, 200)), (surf.get_width() - 205, 5))

def draw_health_bar(surf, player):
    pygame.draw.rect(surf, (255, 0, 0), (10, 10, player.health / player.max_health * 200, 30))
    pygame.draw.rect(surf, (255, 255, 255), (10, 10, 200, 30), 2)

def draw_mana_bar(surf, player):
    pygame.draw.rect(surf, (0, 0, 255), (10, 50, player.mana / player.max_mana * 200, 30))
    pygame.draw.rect(surf, (255, 255, 255), (10, 50, 200, 30), 2)

def draw_experience_bar(surf, player):
    pygame.draw.rect(surf, (255, 255, 0), (10, 90, player.experience / player.next_level_exp * 200, 30))
    pygame.draw.rect(surf, (255, 255, 255), (10, 90, 200, 30), 2)


if __name__ == '__main__':
    main()
