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
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (255, 165, 0), (100, 84, 0))
    txt(surf, f"Gold: {player.gold}", 10, 100, 24, (255, 255, 0))
    txt(surf, f"LvL: {player.level} XP: {player.xp}/{player.next_level_xp}", 10, 130, 24, (255, 255, 255))
    txt(surf, f"Equipped: {player.equipped}", 10, 160, 24, (255, 255, 255))
    txt(surf, f"Biome: {player.biome}", 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x, min_y = max(0, player.x - 63), max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < WORLD_MAP.height and 0 <= x < WORLD_MAP.width:
                biome = WORLD_MAP.get_at((x, y))
                surf.set_at((x - min_x + surf.get_width() - 126, y - min_y), BIOME_COL[biome])
    pygame.draw.circle(surf, (255, 0, 0), (surf.get_width() - 63, 63), 4)
    for enemy in enemies:
        ex, ey = enemy.x - min_x + surf.get_width() - 126, enemy.y - min_y
        if 0 <= ex < 126 and 0 <= ey < 126:
            pygame.draw.circle(surf, (0, 255, 0), (ex, ey), 3)

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 72, (255, 255, 255), True)
    start_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2, 200, 50, "Start", (100, 149, 237), (255, 255, 255), 36)
    load_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 70, 200, 50, "Load", (100, 149, 237), (255, 255, 255), 36)
    exit_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 140, 200, 50, "Exit", (100, 149, 237), (255, 255, 255), 36)
    return [start_btn, load_btn, exit_btn]

def draw_class_select(surf):
    class_cards = [
        {'name': 'Warrior', 'portrait': pygame.Surface((100, 100)), 'rect': pygame.Rect(50, 50, 200, 300)},
        {'name': 'Mage', 'portrait': pygame.Surface((100, 100)), 'rect': pygame.Rect(300, 50, 200, 300)},
        {'name': 'Rogue', 'portrait': pygame.Surface((100, 100)), 'rect': pygame.Rect(550, 50, 200, 300)}
    ]
    for card in class_cards:
        pygame.draw.rect(surf, (100, 149, 237), card['rect'], 0)
        txt(surf, card['name'], card['rect'].x + 50, card['rect'].y + 10, 36, (255, 255, 255), True)
    return [card['rect'] for card in class_cards]

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 50, 50, 700, 400, "Inventory")
    slots = []
    eq_btn = btn(surf, 325, 460, 100, 30, "Equip", (100, 149, 237), (255, 255, 255), 24)
    drop_btn = btn(surf, 450, 460, 100, 30, "Drop", (100, 149, 237), (255, 255, 255), 24)
    for i in range(10):
        slot_rect = pygame.Rect(60 + i * 65, 80, 50, 50)
        slots.append(slot_rect)
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), slot_rect, 3)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 50, 50, 700, 400, "Quest Log")
    for i, quest in enumerate(player.quests):
        txt(surf, quest.title, 60, 80 + i * 30, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 50, 50, 700, 400, "Shop")
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        txt(surf, f"{item.name} - {item.price}g", 60, 80 + i * 30, 24, (255, 255, 255))
        items.append(pygame.Rect(60, 75 + i * 30, 200, 30))
        buy_btn = btn(surf, 300, 80 + i * 30, 100, 30, "Buy", (100, 149, 237), (255, 255, 255), 24)
        buy_btns.append(buy_btn)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 50, 50, 700, 400, "Crafting")
    tab_btns = []
    craft_btns = []
    for i, recipe in enumerate(recipes[tab]):
        txt(surf, f"{recipe.name}", 60, 80 + i * 30, 24, (255, 255, 255))
        if selected == i:
            pygame.draw.rect(surf, (255, 255, 0), pygame.Rect(60, 75 + i * 30, 200, 30), 3)
        craft_btn = btn(surf, 300, 80 + i * 30, 100, 30, "Craft", (100, 149, 237), (255, 255, 255), 24)
        craft_btns.append(craft_btn)
    for i, tab_name in enumerate(recipes.keys()):
        tab_btn = btn(surf, 60 + i * 120, 460, 100, 30, tab_name, (100, 149, 237), (255, 255, 255), 24)
        tab_btns.append(tab_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 50, 50, 700, 400, "Dialogue")
    txt(surf, npc.dialogues[dial_idx]['text'], 60, 80, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.dialogues[dial_idx].get('options', [])):
        opt_btn = btn(surf, 60, 120 + i * 30, 200, 30, option['text'], (100, 149, 237), (255, 255, 255), 24)
        opt_btns.append(opt_btn)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
    panel(surf, 300, 200, 200, 200, "Paused")
    resume_btn = btn(surf, 350, 260, 100, 40, "Resume", (100, 149, 237), (255, 255, 255), 24)
    menu_btn = btn(surf, 350, 320, 100, 40, "Menu", (100, 149, 237), (255, 255, 255), 24)
    exit_btn = btn(surf, 350, 380, 100, 40, "Exit", (100, 149, 237), (255, 255, 255), 24)
    return panel(surf, 300, 200, 200, 200, "Paused"), [resume_btn, menu_btn, exit_btn]

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 50, 50, 700, 400, f"{place_type} Panel")
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 60 + i * 120, 80, 100, 50, building['name'], (100, 149, 237), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    surf.fill((0, 0, 0))
    for y in range(WORLD_MAP.height):
        for x in range(WORLD_MAP.width):
            biome = WORLD_MAP.get_at((x, y))
            surf.set_at((x, y), BIOME_COL[biome])
    for town in TOWNS:
        pygame.draw.circle(surf, (255, 0, 0), (town.x, town.y), 3)
    for city in CITIES:
        pygame.draw.circle(surf, (0, 0, 255), (city.x, city.y), 4)
    xbtn_rect = panel(surf, surf.get_width() - 260, 10, 250, 50, "World Map")
    return xbtn_rect

def draw_gameover(surf):
    surf.fill((0, 0, 0))
    txt(surf, "Game Over", surf.get_width() // 2, surf.get_height() // 3, 72, (255, 0, 0), True)
    restart_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2, 200, 50, "Restart", (100, 149, 237), (255, 255, 255), 24)
    menu_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 60, 200, 50, "Menu", (100, 149, 237), (255, 255, 255), 24)
    return restart_btn, menu_btn

def draw_player_sprite(surf, player):
    # Placeholder for drawing the player sprite
    pygame.draw.circle(surf, (0, 128, 255), (player.x, player.y), 10)

def draw_npc_sprite(surf, npc):
    # Placeholder for drawing an NPC sprite
    pygame.draw.rect(surf, (255, 0, 0), (npc.x - 5, npc.y - 5, 10, 10))

def draw_item_icon(surf, item, x, y):
    # Placeholder for drawing an item icon
    pygame.draw.circle(surf, (0, 255, 0), (x + 5, y + 5), 5)

def draw_ui_elements(surf, player, inventory_open, quest_log_open, shop_open, crafting_open, dialogue_open):
    if inventory_open:
        xbtn_rect, slots, eq_btn, drop_btn = draw_inventory(surf, player, player.selected_item)
    if quest_log_open:
        xbtn_rect = draw_quest_log(surf, player)
    if shop_open:
        xbtn_rect, buy_btns, items = draw_shop(surf, player.current_npc, player, player.selected_item)
    if crafting_open:
        xbtn_rect, tab_btns, craft_btns = draw_crafting(surf, player, player.crafting_tab, player.selected_recipe, player.recipes)
    if dialogue_open:
        xbtn_rect, opt_btns = draw_dialogue(surf, player.current_npc, player.dialogue_index)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Example player object
    class Player:
        def __init__(self):
            self.x, self.y = 400, 300
            self.selected_item = None
            self.quests = []
            self.current_npc = None
            self.dialogue_index = 0
            self.crafting_tab = 'Weapons'
            self.recipes = {'Weapons': [], 'Armor': []}

    player = Player()

    running = True
    inventory_open = False
    quest_log_open = False
    shop_open = False
    crafting_open = False
    dialogue_open = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory_open = not inventory_open
                elif event.key == pygame.K_q:
                    quest_log_open = not quest_log_open
                elif event.key == pygame.K_s:
                    shop_open = not shop_open
                elif event.key == pygame.K_c:
                    crafting_open = not crafting_open
                elif event.key == pygame.K_d:
                    dialogue_open = not dialogue_open

        screen.fill((0, 0, 0))
        draw_player_sprite(screen, player)
        # Draw other game elements here...

        draw_ui_elements(screen, player, inventory_open, quest_log_open, shop_open, crafting_open, dialogue_open)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
