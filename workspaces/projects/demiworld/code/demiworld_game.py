"""
DemiWorld — Complete Fantasy RPG
Open world with crafting, city building, NPC hiring, shops, combat.
10 weapons, 3 armor sets, 10 spells, 10 enemy types.
WASD movement, ESC pause, I inventory, all menus have X close button.
"""
import pygame
import sys
import random
import json
import os
import math

pygame.init()
SCREEN_W, SCREEN_H = 1024, 768
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("DemiWorld")
clock = pygame.time.Clock()

# ── FONTS ──────────────────────────────────────────────────────────────────
font_lg = pygame.font.SysFont("consolas", 22, bold=True)
font_md = pygame.font.SysFont("consolas", 16)
font_sm = pygame.font.SysFont("consolas", 13)

# ── COLORS ─────────────────────────────────────────────────────────────────
C = {
    "bg": (15, 12, 25), "grass": (34, 85, 34), "dirt": (101, 67, 33),
    "water": (20, 60, 120), "stone": (80, 80, 90), "sand": (194, 178, 128),
    "forest": (20, 60, 20), "dungeon": (40, 20, 40),
    "white": (240, 240, 240), "black": (0, 0, 0), "red": (200, 50, 50),
    "green": (50, 200, 80), "blue": (60, 120, 220), "yellow": (220, 200, 50),
    "purple": (140, 60, 200), "orange": (220, 130, 40), "cyan": (60, 200, 200),
    "gold": (255, 215, 0), "gray": (120, 120, 130), "darkgray": (50, 50, 60),
    "panel": (20, 18, 35), "panel2": (30, 28, 50), "border": (80, 70, 120),
    "hp": (200, 50, 50), "mp": (50, 100, 220), "xp": (50, 180, 80),
    "highlight": (100, 90, 160), "btn": (60, 50, 100), "btn_hover": (90, 80, 140),
}

# ── WORLD DATA ──────────────────────────────────────────────────────────────
TILE_SIZE = 32
WORLD_W, WORLD_H = 80, 60

WEAPONS = [
    {"name": "Iron Sword", "dmg": 12, "type": "melee", "price": 50, "color": C["gray"]},
    {"name": "Steel Axe", "dmg": 18, "type": "melee", "price": 120, "color": C["blue"]},
    {"name": "Silver Dagger", "dmg": 8, "type": "melee", "price": 80, "color": C["white"]},
    {"name": "War Hammer", "dmg": 25, "type": "melee", "price": 200, "color": C["orange"]},
    {"name": "Elven Bow", "dmg": 15, "type": "ranged", "price": 150, "color": C["green"]},
    {"name": "Crossbow", "dmg": 20, "type": "ranged", "price": 180, "color": C["gray"]},
    {"name": "Fire Staff", "dmg": 22, "type": "magic", "price": 300, "color": C["red"]},
    {"name": "Frost Wand", "dmg": 17, "type": "magic", "price": 250, "color": C["cyan"]},
    {"name": "Thunder Spear", "dmg": 28, "type": "melee", "price": 350, "color": C["yellow"]},
    {"name": "Shadow Blade", "dmg": 30, "type": "melee", "price": 500, "color": C["purple"]},
]
ARMORS = [
    {"name": "Leather Armor", "defense": 5, "price": 60, "color": C["orange"]},
    {"name": "Iron Chainmail", "defense": 12, "price": 200, "color": C["gray"]},
    {"name": "Plate Armor", "defense": 22, "price": 500, "color": C["blue"]},
]
SPELLS = [
    {"name": "Fireball", "dmg": 25, "mp": 20, "color": C["red"]},
    {"name": "Ice Shard", "dmg": 18, "mp": 15, "color": C["cyan"]},
    {"name": "Lightning", "dmg": 30, "mp": 25, "color": C["yellow"]},
    {"name": "Heal", "dmg": -30, "mp": 20, "color": C["green"]},
    {"name": "Shield", "dmg": 0, "mp": 15, "color": C["blue"]},
    {"name": "Poison", "dmg": 10, "mp": 12, "color": C["purple"]},
    {"name": "Earthquake", "dmg": 35, "mp": 30, "color": C["orange"]},
    {"name": "Teleport", "dmg": 0, "mp": 25, "color": C["white"]},
    {"name": "Summon", "dmg": 20, "mp": 35, "color": C["gold"]},
    {"name": "Dark Nova", "dmg": 45, "mp": 40, "color": C["darkgray"]},
]
ENEMY_TYPES = [
    {"name": "Goblin", "hp": 30, "dmg": 6, "xp": 15, "gold": 5, "color": C["green"], "speed": 1.5},
    {"name": "Bandit", "hp": 50, "dmg": 10, "xp": 25, "gold": 15, "color": C["orange"], "speed": 1.2},
    {"name": "Wolf", "hp": 40, "dmg": 8, "xp": 20, "gold": 3, "color": C["gray"], "speed": 2.0},
    {"name": "Skeleton", "hp": 35, "dmg": 9, "xp": 22, "gold": 8, "color": C["white"], "speed": 1.0},
    {"name": "Troll", "hp": 80, "dmg": 15, "xp": 40, "gold": 20, "color": C["green"], "speed": 0.8},
    {"name": "Dark Mage", "hp": 45, "dmg": 18, "xp": 50, "gold": 30, "color": C["purple"], "speed": 1.0},
    {"name": "Orc", "hp": 70, "dmg": 14, "xp": 35, "gold": 18, "color": C["orange"], "speed": 1.0},
    {"name": "Vampire", "hp": 60, "dmg": 16, "xp": 45, "gold": 25, "color": C["red"], "speed": 1.8},
    {"name": "Dragon Whelp", "hp": 100, "dmg": 22, "xp": 80, "gold": 50, "color": C["red"], "speed": 1.2},
    {"name": "Demon", "hp": 120, "dmg": 28, "xp": 100, "gold": 80, "color": C["purple"], "speed": 1.5},
]
MATERIALS = ["Wood", "Stone", "Iron Ore", "Gold Ore", "Herbs", "Leather", "Silk", "Coal", "Crystal", "Bone"]
CRAFTABLE = [
    {"name": "Arrow Bundle", "mats": {"Wood": 3}, "type": "ammo"},
    {"name": "Health Potion", "mats": {"Herbs": 2}, "type": "consumable"},
    {"name": "Mana Potion", "mats": {"Crystal": 1, "Herbs": 1}, "type": "consumable"},
    {"name": "Iron Bar", "mats": {"Iron Ore": 2, "Coal": 1}, "type": "material"},
    {"name": "Throwing Star", "mats": {"Iron Ore": 1}, "type": "ammo"},
    {"name": "Wooden Cart", "mats": {"Wood": 10}, "type": "building"},
]

# ── WORLD GENERATION ────────────────────────────────────────────────────────
def gen_world():
    world = []
    for y in range(WORLD_H):
        row = []
        for x in range(WORLD_W):
            r = random.random()
            if x < 3 or x >= WORLD_W-3 or y < 3 or y >= WORLD_H-3:
                row.append("water")
            elif r < 0.05:
                row.append("water")
            elif r < 0.15:
                row.append("forest")
            elif r < 0.22:
                row.append("stone")
            elif r < 0.26:
                row.append("sand")
            elif r < 0.28:
                row.append("dungeon")
            else:
                row.append("grass")
        world.append(row)
    # Towns
    for _ in range(4):
        tx, ty = random.randint(10, WORLD_W-15), random.randint(10, WORLD_H-15)
        for dy in range(4):
            for dx in range(5):
                world[ty+dy][tx+dx] = "dirt"
    return world

WORLD = gen_world()
TILE_COLOR = {
    "grass": C["grass"], "dirt": C["dirt"], "water": C["water"],
    "stone": C["stone"], "sand": C["sand"], "forest": C["forest"], "dungeon": C["dungeon"]
}

# ── ENTITIES ────────────────────────────────────────────────────────────────
class Player:
    def __init__(self):
        self.x, self.y = 20 * TILE_SIZE, 20 * TILE_SIZE
        self.hp = self.max_hp = 100
        self.mp = self.max_mp = 80
        self.xp = 0
        self.level = 1
        self.xp_next = 100
        self.gold = 200
        self.speed = 3
        self.weapon = WEAPONS[0].copy()
        self.armor = None
        self.spells = [SPELLS[0].copy(), SPELLS[3].copy()]
        self.inventory = {m: 0 for m in MATERIALS}
        self.inventory.update({"Health Potion": 3, "Mana Potion": 2})
        self.hired_npcs = []
        self.attack_cd = 0
        self.spell_cd = 0
        self.shield = 0
        self.msg = []

    def add_msg(self, text, color=None):
        self.msg.append({"text": text, "color": color or C["white"], "t": 180})

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.max_hp += 15
            self.max_mp += 10
            self.hp = self.max_hp
            self.mp = self.max_mp
            self.xp_next = int(self.xp_next * 1.4)
            self.add_msg("Level Up! Now level " + str(self.level), C["gold"])

    def take_damage(self, dmg):
        defense = (self.armor["defense"] if self.armor else 0) + self.shield
        actual = max(1, dmg - defense)
        self.hp = max(0, self.hp - actual)
        return actual

    def move(self, dx, dy):
        nx = self.x + dx * self.speed
        ny = self.y + dy * self.speed
        tx, ty = int(nx // TILE_SIZE), int(ny // TILE_SIZE)
        if 0 <= tx < WORLD_W and 0 <= ty < WORLD_H:
            tile = WORLD[ty][tx]
            if tile != "water":
                # Gather materials from tiles
                if tile == "forest" and random.random() < 0.002:
                    self.inventory["Wood"] = self.inventory.get("Wood", 0) + 1
                    self.add_msg("+1 Wood", C["green"])
                elif tile == "stone" and random.random() < 0.002:
                    self.inventory["Stone"] = self.inventory.get("Stone", 0) + 1
                    self.add_msg("+1 Stone", C["gray"])
                self.x, self.y = nx, ny

    def attack(self, enemies):
        if self.attack_cd > 0:
            return
        self.attack_cd = 30
        range_ = 80 if self.weapon["type"] == "ranged" else 50
        for e in enemies:
            dist = math.hypot(e.x - self.x, e.y - self.y)
            if dist < range_:
                dmg = self.weapon["dmg"] + random.randint(0, 5)
                e.hp -= dmg
                self.add_msg("Hit " + e.name + " for " + str(dmg), C["yellow"])
                return

    def cast_spell(self, spell_idx, enemies):
        if self.spell_cd > 0 or spell_idx >= len(self.spells):
            return
        spell = self.spells[spell_idx]
        if self.mp < spell["mp"]:
            self.add_msg("Not enough MP!", C["red"])
            return
        self.mp -= spell["mp"]
        self.spell_cd = 45
        if spell["name"] == "Heal":
            heal = abs(spell["dmg"])
            self.hp = min(self.max_hp, self.hp + heal)
            self.add_msg("Healed " + str(heal) + " HP", C["green"])
        elif spell["name"] == "Shield":
            self.shield = 15
            self.add_msg("Shield activated!", C["blue"])
        elif spell["name"] == "Teleport":
            self.x = random.randint(10, WORLD_W-10) * TILE_SIZE
            self.y = random.randint(10, WORLD_H-10) * TILE_SIZE
            self.add_msg("Teleported!", C["purple"])
        else:
            for e in enemies[:3]:
                dist = math.hypot(e.x - self.x, e.y - self.y)
                if dist < 150:
                    e.hp -= spell["dmg"]
                    self.add_msg(spell["name"] + " hit " + e.name, spell["color"])


class Enemy:
    def __init__(self, etype, x, y):
        d = ENEMY_TYPES[etype].copy()
        self.name = d["name"]
        self.hp = self.max_hp = d["hp"]
        self.dmg = d["dmg"]
        self.xp = d["xp"]
        self.gold = d["gold"]
        self.color = d["color"]
        self.speed = d["speed"]
        self.x = float(x)
        self.y = float(y)
        self.attack_cd = 0

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist < 300 and dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        if dist < 35 and self.attack_cd <= 0:
            self.attack_cd = 60
            dmg = player.take_damage(self.dmg + random.randint(0, 4))
            player.add_msg(self.name + " hit you for " + str(dmg), C["red"])
        if self.attack_cd > 0:
            self.attack_cd -= 1


class NPC:
    def __init__(self, name, role, x, y):
        self.name = name
        self.role = role
        self.x = x
        self.y = y
        self.dialogue_idx = 0
        DIALOGUES = {
            "merchant": ["Welcome traveler! Buy something?", "Fine goods, cheap prices!", "Come back soon!"],
            "guard": ["Halt! State your business.", "Move along, citizen.", "Stay out of trouble."],
            "peasant": ["Hard times...", "The crops are poor this year.", "Have you heard the news?"],
            "blacksmith": ["Need weapons or armor?", "I can forge anything from iron!", "Bring me ore and I'll make you gear."],
        }
        self.lines = DIALOGUES.get(role, ["Hello there."])
        self.hire_cost = random.randint(50, 200)
        self.hired = False

    def get_line(self):
        line = self.lines[self.dialogue_idx % len(self.lines)]
        self.dialogue_idx += 1
        return line


# ── SPAWN SYSTEMS ────────────────────────────────────────────────────────────
def spawn_enemies(count=20):
    enemies = []
    for _ in range(count):
        etype = random.randint(0, len(ENEMY_TYPES)-1)
        # Spawn near camps (dungeon/stone tiles)
        for attempt in range(50):
            ex = random.randint(5, WORLD_W-5) * TILE_SIZE
            ey = random.randint(5, WORLD_H-5) * TILE_SIZE
            tx, ty = ex // TILE_SIZE, ey // TILE_SIZE
            tile = WORLD[ty][tx]
            if tile in ("dungeon", "stone", "grass", "forest"):
                enemies.append(Enemy(etype, ex, ey))
                break
    return enemies

def spawn_npcs():
    npcs = []
    roles = ["merchant", "guard", "blacksmith", "peasant"]
    names = ["Aldric", "Brenna", "Cedric", "Dara", "Erwin", "Fiona", "Gareth", "Hilda"]
    for i, name in enumerate(names):
        role = roles[i % len(roles)]
        tx = random.randint(12, WORLD_W-12)
        ty = random.randint(12, WORLD_H-12)
        while WORLD[ty][tx] != "dirt":
            tx = random.randint(12, WORLD_W-12)
            ty = random.randint(12, WORLD_H-12)
        npcs.append(NPC(name, role, tx * TILE_SIZE, ty * TILE_SIZE))
    return npcs

# ── UI HELPERS ───────────────────────────────────────────────────────────────
def draw_panel(surf, x, y, w, h, title=None, alpha=220):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((*C["panel"], alpha))
    surf.blit(s, (x, y))
    pygame.draw.rect(surf, C["border"], (x, y, w, h), 2)
    if title:
        t = font_md.render(title, True, C["gold"])
        surf.blit(t, (x + w//2 - t.get_width()//2, y + 8))
    return pygame.Rect(x, y, w, h)

def draw_x_button(surf, px, py, pw):
    """Draw X close button in top-right of panel."""
    bx, by = px + pw - 24, py + 6
    pygame.draw.rect(surf, C["red"], (bx, by, 18, 18), border_radius=3)
    xt = font_sm.render("X", True, C["white"])
    surf.blit(xt, (bx + 4, by + 2))
    return pygame.Rect(bx, by, 18, 18)

def draw_bar(surf, x, y, w, h, val, maxval, color, bg=C["darkgray"]):
    pygame.draw.rect(surf, bg, (x, y, w, h))
    if maxval > 0:
        fill = int(w * val / maxval)
        pygame.draw.rect(surf, color, (x, y, fill, h))
    pygame.draw.rect(surf, C["border"], (x, y, w, h), 1)

def draw_button(surf, x, y, w, h, text, hover=False):
    color = C["btn_hover"] if hover else C["btn"]
    pygame.draw.rect(surf, color, (x, y, w, h), border_radius=4)
    pygame.draw.rect(surf, C["border"], (x, y, w, h), 1, border_radius=4)
    t = font_sm.render(text, True, C["white"])
    surf.blit(t, (x + w//2 - t.get_width()//2, y + h//2 - t.get_height()//2))
    return pygame.Rect(x, y, w, h)

# ── SCREENS ──────────────────────────────────────────────────────────────────
def draw_hud(surf, player):
    # HP bar
    draw_bar(surf, 10, 10, 160, 16, player.hp, player.max_hp, C["hp"])
    surf.blit(font_sm.render("HP " + str(player.hp) + "/" + str(player.max_hp), True, C["white"]), (12, 11))
    # MP bar
    draw_bar(surf, 10, 30, 160, 16, player.mp, player.max_mp, C["mp"])
    surf.blit(font_sm.render("MP " + str(player.mp) + "/" + str(player.max_mp), True, C["white"]), (12, 31))
    # XP bar
    draw_bar(surf, 10, 50, 160, 10, player.xp, player.xp_next, C["xp"])
    surf.blit(font_sm.render("Lv " + str(player.level), True, C["gold"]), (12, 62))
    # Gold
    surf.blit(font_sm.render("Gold: " + str(player.gold), True, C["gold"]), (10, 78))
    # Weapon
    surf.blit(font_sm.render(player.weapon["name"], True, player.weapon["color"]), (10, 94))
    # Messages
    y_msg = SCREEN_H - 20
    for msg_data in list(reversed(player.msg[-5:])):
        if msg_data["t"] > 0:
            alpha = min(255, msg_data["t"] * 3)
            t = font_sm.render(msg_data["text"], True, msg_data["color"])
            ts = pygame.Surface(t.get_size(), pygame.SRCALPHA)
            ts.fill((0,0,0,0))
            ts.blit(t, (0,0))
            ts.set_alpha(alpha)
            surf.blit(ts, (10, y_msg))
            y_msg -= 18
    # Spells
    for i, sp in enumerate(player.spells[:4]):
        sx = SCREEN_W - 140
        sy = 10 + i * 36
        pygame.draw.rect(surf, C["darkgray"], (sx, sy, 130, 30), border_radius=3)
        pygame.draw.rect(surf, sp["color"], (sx, sy, 130, 30), 2, border_radius=3)
        surf.blit(font_sm.render(str(i+1) + ":" + sp["name"], True, sp["color"]), (sx+4, sy+8))
    # Cooldowns
    if player.attack_cd > 0:
        surf.blit(font_sm.render("ATK CD", True, C["red"]), (SCREEN_W//2 - 30, 5))
    # Minimap
    mm_x, mm_y, mm_w, mm_h = SCREEN_W - 130, SCREEN_H - 110, 120, 100
    pygame.draw.rect(surf, C["black"], (mm_x, mm_y, mm_w, mm_h))
    for ty in range(0, WORLD_H, 2):
        for tx in range(0, WORLD_W, 2):
            tc = TILE_COLOR.get(WORLD[ty][tx], C["grass"])
            pygame.draw.rect(surf, tc, (mm_x + tx//2 * mm_w//(WORLD_W//2), mm_y + ty//2 * mm_h//(WORLD_H//2), 2, 2))
    px = mm_x + int(player.x / TILE_SIZE / WORLD_W * mm_w)
    py2 = mm_y + int(player.y / TILE_SIZE / WORLD_H * mm_h)
    pygame.draw.rect(surf, C["white"], (px-1, py2-1, 3, 3))
    pygame.draw.rect(surf, C["border"], (mm_x, mm_y, mm_w, mm_h), 1)


def draw_inventory(surf, player, mx, my):
    pw, ph = 500, 500
    px, py = SCREEN_W//2 - pw//2, SCREEN_H//2 - ph//2
    draw_panel(surf, px, py, pw, ph, "INVENTORY")
    x_btn = draw_x_button(surf, px, py, pw)
    # Equipped
    surf.blit(font_md.render("Weapon: " + player.weapon["name"], True, player.weapon["color"]), (px+20, py+40))
    armor_name = player.armor["name"] if player.armor else "None"
    surf.blit(font_md.render("Armor:  " + armor_name, True, C["white"]), (px+20, py+62))
    # Materials
    surf.blit(font_md.render("Materials:", True, C["gold"]), (px+20, py+95))
    cols = 2
    items = [(k, v) for k, v in player.inventory.items() if v > 0]
    for i, (name, qty) in enumerate(items[:20]):
        row, col = i // cols, i % cols
        surf.blit(font_sm.render(name + ": " + str(qty), True, C["white"]),
                  (px+20 + col*220, py+115 + row*20))
    # Gold
    surf.blit(font_md.render("Gold: " + str(player.gold), True, C["gold"]), (px+20, py+ph-60))
    # Level info
    surf.blit(font_md.render("Level " + str(player.level) + " — XP: " + str(player.xp) + "/" + str(player.xp_next), True, C["xp"]), (px+20, py+ph-40))
    return x_btn

def draw_shop(surf, player, mx, my):
    pw, ph = 600, 520
    px, py = SCREEN_W//2 - pw//2, SCREEN_H//2 - ph//2
    draw_panel(surf, px, py, pw, ph, "SHOP — Gold: " + str(player.gold))
    x_btn = draw_x_button(surf, px, py, pw)
    surf.blit(font_md.render("WEAPONS", True, C["gold"]), (px+20, py+40))
    btns = []
    for i, w in enumerate(WEAPONS):
        col, row = i % 2, i // 2
        bx = px + 20 + col * 270
        by = py + 65 + row * 35
        hov = pygame.Rect(bx, by, 260, 28).collidepoint(mx, my)
        b = draw_button(surf, bx, by, 260, 28, w["name"] + " " + str(w["dmg"]) + "dmg $" + str(w["price"]), hov)
        btns.append(("weapon", i, b))
    surf.blit(font_md.render("ARMORS", True, C["gold"]), (px+20, py+275))
    for i, a in enumerate(ARMORS):
        bx = px + 20 + i * 185
        by = py + 300
        hov = pygame.Rect(bx, by, 175, 28).collidepoint(mx, my)
        b = draw_button(surf, bx, by, 175, 28, a["name"] + " " + str(a["defense"]) + "def $" + str(a["price"]), hov)
        btns.append(("armor", i, b))
    surf.blit(font_md.render("SPELLS", True, C["gold"]), (px+20, py+350))
    for i, sp in enumerate(SPELLS):
        col, row = i % 2, i // 2
        bx = px + 20 + col * 270
        by = py + 375 + row * 35
        hov = pygame.Rect(bx, by, 260, 28).collidepoint(mx, my)
        b = draw_button(surf, bx, by, 260, 28, sp["name"] + " " + str(sp["dmg"]) + "dmg " + str(sp["mp"]) + "mp $" + str(sp["dmg"]*8+50), hov)
        btns.append(("spell", i, b))
    return x_btn, btns

def draw_craft(surf, player, mx, my):
    pw, ph = 480, 400
    px, py = SCREEN_W//2 - pw//2, SCREEN_H//2 - ph//2
    draw_panel(surf, px, py, pw, ph, "CRAFTING")
    x_btn = draw_x_button(surf, px, py, pw)
    btns = []
    for i, recipe in enumerate(CRAFTABLE):
        by = py + 50 + i * 52
        can_craft = all(player.inventory.get(k, 0) >= v for k, v in recipe["mats"].items())
        mat_str = ", ".join(k + "×" + str(v) for k, v in recipe["mats"].items())
        surf.blit(font_md.render(recipe["name"] + " (" + recipe["type"] + ")", True, C["gold"] if can_craft else C["gray"]), (px+20, by))
        surf.blit(font_sm.render("Needs: " + mat_str, True, C["white"]), (px+20, by+18))
        hov = pygame.Rect(px+pw-120, by, 100, 28).collidepoint(mx, my)
        b = draw_button(surf, px+pw-120, by, 100, 28, "Craft", hov and can_craft)
        btns.append((i, b, can_craft))
    return x_btn, btns

def draw_npc_dialog(surf, npc, player, mx, my):
    pw, ph = 500, 220
    px, py = SCREEN_W//2 - pw//2, SCREEN_H - ph - 20
    draw_panel(surf, px, py, pw, ph, npc.name + " (" + npc.role + ")")
    x_btn = draw_x_button(surf, px, py, pw)
    surf.blit(font_md.render('"' + npc.get_line() + '"', True, C["white"]), (px+20, py+45))
    hire_txt = "Hired!" if npc.hired else "Hire ($" + str(npc.hire_cost) + ")"
    hov_h = pygame.Rect(px+20, py+ph-60, 150, 32).collidepoint(mx, my)
    btn_hire = draw_button(surf, px+20, py+ph-60, 150, 32, hire_txt, hov_h)
    hov_s = pygame.Rect(px+200, py+ph-60, 100, 32).collidepoint(mx, my)
    btn_shop = draw_button(surf, px+200, py+ph-60, 100, 32, "Shop", hov_s)
    return x_btn, btn_hire, btn_shop

def draw_pause(surf, mx, my):
    draw_panel(surf, SCREEN_W//2-150, SCREEN_H//2-200, 300, 400, "PAUSED")
    btns = []
    labels = ["Resume", "Save Game", "Load Game", "Quit"]
    for i, label in enumerate(labels):
        bx, by = SCREEN_W//2-100, SCREEN_H//2-120+i*70
        hov = pygame.Rect(bx, by, 200, 50).collidepoint(mx, my)
        b = draw_button(surf, bx, by, 200, 50, label, hov)
        btns.append((label, b))
    return btns

# ── SAVE / LOAD ──────────────────────────────────────────────────────────────
SAVE_FILE = os.path.join(os.path.dirname(__file__), "demiworld_save.json")

def save_game(player):
    data = {
        "x": player.x, "y": player.y,
        "hp": player.hp, "mp": player.mp,
        "level": player.level, "xp": player.xp, "xp_next": player.xp_next,
        "gold": player.gold, "inventory": player.inventory,
        "weapon_idx": next((i for i, w in enumerate(WEAPONS) if w["name"] == player.weapon["name"]), 0),
        "armor_idx": next((i for i, a in enumerate(ARMORS) if player.armor and a["name"] == player.armor["name"]), -1),
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    return True

def load_game(player):
    if not os.path.exists(SAVE_FILE):
        return False
    try:
        with open(SAVE_FILE) as f:
            data = json.load(f)
        player.x, player.y = data["x"], data["y"]
        player.hp, player.mp = data["hp"], data["mp"]
        player.level, player.xp, player.xp_next = data["level"], data["xp"], data["xp_next"]
        player.gold = data["gold"]
        player.inventory = data.get("inventory", player.inventory)
        player.weapon = WEAPONS[data.get("weapon_idx", 0)].copy()
        ai = data.get("armor_idx", -1)
        player.armor = ARMORS[ai].copy() if ai >= 0 else None
        return True
    except Exception:
        return False

# ── MAIN GAME ────────────────────────────────────────────────────────────────
def main():
    player = Player()
    enemies = spawn_enemies(25)
    npcs = spawn_npcs()
    cam_x = cam_y = 0

    STATE = "play"
    active_npc = None
    show_inv = False
    show_shop = False
    show_craft = False
    shop_btns = []

    respawn_timer = 0

    while True:
        mx, my = pygame.mouse.get_pos()
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if show_inv or show_shop or show_craft or active_npc:
                        show_inv = show_shop = show_craft = False
                        active_npc = None
                    elif STATE == "pause":
                        STATE = "play"
                    else:
                        STATE = "pause"
                if STATE == "play" and not show_inv and not show_shop and not show_craft and not active_npc:
                    if e.key == pygame.K_i:
                        show_inv = not show_inv
                    if e.key == pygame.K_c:
                        show_craft = not show_craft
                    if e.key == pygame.K_SPACE:
                        player.attack(enemies)
                    for ki, kv in enumerate([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]):
                        if e.key == kv:
                            player.cast_spell(ki, enemies)
                    if e.key == pygame.K_f:
                        # Use health potion
                        if player.inventory.get("Health Potion", 0) > 0:
                            player.inventory["Health Potion"] -= 1
                            heal = 40
                            player.hp = min(player.max_hp, player.hp + heal)
                            player.add_msg("Used Health Potion (+"+str(heal)+"HP)", C["green"])

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if STATE == "pause":
                    pause_btns = draw_pause(screen, mx, my)
                    for label, btn in pause_btns:
                        if btn.collidepoint(mx, my):
                            if label == "Resume": STATE = "play"
                            elif label == "Save Game":
                                save_game(player)
                                player.add_msg("Game saved!", C["green"])
                                STATE = "play"
                            elif label == "Load Game":
                                if load_game(player):
                                    player.add_msg("Game loaded!", C["green"])
                                STATE = "play"
                            elif label == "Quit":
                                pygame.quit(); sys.exit()

                elif show_inv:
                    x_btn = draw_inventory(screen, player, mx, my)
                    if x_btn.collidepoint(mx, my):
                        show_inv = False

                elif show_shop:
                    x_btn, btns = draw_shop(screen, player, mx, my)
                    if x_btn.collidepoint(mx, my):
                        show_shop = False
                    for btype, bidx, brect in btns:
                        if brect.collidepoint(mx, my):
                            if btype == "weapon":
                                w = WEAPONS[bidx]
                                if player.gold >= w["price"]:
                                    player.gold -= w["price"]
                                    player.weapon = w.copy()
                                    player.add_msg("Bought " + w["name"], C["green"])
                            elif btype == "armor":
                                a = ARMORS[bidx]
                                if player.gold >= a["price"]:
                                    player.gold -= a["price"]
                                    player.armor = a.copy()
                                    player.add_msg("Bought " + a["name"], C["green"])
                            elif btype == "spell":
                                sp = SPELLS[bidx]
                                cost = sp["dmg"] * 8 + 50
                                if player.gold >= cost:
                                    player.gold -= cost
                                    if sp not in player.spells:
                                        player.spells.append(sp.copy())
                                    player.add_msg("Learned " + sp["name"], sp["color"])

                elif show_craft:
                    x_btn, btns = draw_craft(screen, player, mx, my)
                    if x_btn.collidepoint(mx, my):
                        show_craft = False
                    for ridx, brect, can in btns:
                        if brect.collidepoint(mx, my) and can:
                            recipe = CRAFTABLE[ridx]
                            for mat, qty in recipe["mats"].items():
                                player.inventory[mat] = player.inventory.get(mat, 0) - qty
                            player.inventory[recipe["name"]] = player.inventory.get(recipe["name"], 0) + 1
                            player.add_msg("Crafted " + recipe["name"], C["green"])

                elif active_npc:
                    x_btn, btn_hire, btn_shop = draw_npc_dialog(screen, active_npc, player, mx, my)
                    if x_btn.collidepoint(mx, my):
                        active_npc = None
                    elif btn_hire.collidepoint(mx, my) and not active_npc.hired:
                        if player.gold >= active_npc.hire_cost:
                            player.gold -= active_npc.hire_cost
                            active_npc.hired = True
                            player.hired_npcs.append(active_npc)
                            player.add_msg("Hired " + active_npc.name + "!", C["gold"])
                    elif btn_shop.collidepoint(mx, my):
                        show_shop = True
                        active_npc = None

                elif STATE == "play":
                    # Check NPC interaction
                    for npc in npcs:
                        nx_s = npc.x - cam_x
                        ny_s = npc.y - cam_y
                        if abs(mx - nx_s) < 24 and abs(my - ny_s) < 24:
                            dist = math.hypot(npc.x - player.x, npc.y - player.y)
                            if dist < 80:
                                active_npc = npc
                                break
                    # Open shop shortcut
                    if my < 200 and mx > SCREEN_W - 200:
                        show_shop = True

        # ── UPDATE ──────────────────────────────────────────────────────────
        if STATE == "play" and not show_inv and not show_shop and not show_craft and not active_npc:
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_d] - keys[pygame.K_a])
            dy = (keys[pygame.K_s] - keys[pygame.K_w])
            if dx != 0 or dy != 0:
                player.move(dx, dy)

            # Update enemies
            dead = []
            for en in enemies:
                en.update(player)
                if en.hp <= 0:
                    dead.append(en)
                    player.gain_xp(en.xp)
                    player.gold += en.gold
                    # Random material drop
                    if random.random() < 0.3:
                        mat = random.choice(MATERIALS[:5])
                        player.inventory[mat] = player.inventory.get(mat, 0) + 1
                        player.add_msg(en.name + " dropped " + mat, C["cyan"])
                    player.add_msg(en.name + " defeated! +" + str(en.xp) + "xp +" + str(en.gold) + "g", C["yellow"])
            for d in dead:
                enemies.remove(d)

            # Respawn
            respawn_timer += 1
            if respawn_timer > 300 and len(enemies) < 20:
                respawn_timer = 0
                etype = random.randint(0, len(ENEMY_TYPES)-1)
                ex = random.randint(5, WORLD_W-5) * TILE_SIZE
                ey = random.randint(5, WORLD_H-5) * TILE_SIZE
                enemies.append(Enemy(etype, ex, ey))

            # Cooldowns
            if player.attack_cd > 0: player.attack_cd -= 1
            if player.spell_cd > 0: player.spell_cd -= 1
            if player.shield > 0: player.shield -= 0.05

            # Update messages
            for msg_data in player.msg:
                msg_data["t"] -= 1
            player.msg = [m for m in player.msg if m["t"] > 0]

            # Regen
            if random.random() < 0.005:
                player.hp = min(player.max_hp, player.hp + 1)
                player.mp = min(player.max_mp, player.mp + 1)

            # Death
            if player.hp <= 0:
                player.hp = player.max_hp // 2
                player.mp = player.max_mp // 2
                player.x, player.y = 20 * TILE_SIZE, 20 * TILE_SIZE
                player.gold = max(0, player.gold - 50)
                player.add_msg("You died! Respawned. Lost 50 gold.", C["red"])

        # Camera
        cam_x = int(player.x - SCREEN_W // 2)
        cam_y = int(player.y - SCREEN_H // 2)
        cam_x = max(0, min(cam_x, WORLD_W * TILE_SIZE - SCREEN_W))
        cam_y = max(0, min(cam_y, WORLD_H * TILE_SIZE - SCREEN_H))

        # ── DRAW ────────────────────────────────────────────────────────────
        screen.fill(C["bg"])

        # World tiles
        start_tx = cam_x // TILE_SIZE
        start_ty = cam_y // TILE_SIZE
        for ty in range(start_ty, min(start_ty + SCREEN_H // TILE_SIZE + 2, WORLD_H)):
            for tx in range(start_tx, min(start_tx + SCREEN_W // TILE_SIZE + 2, WORLD_W)):
                tile = WORLD[ty][tx]
                color = TILE_COLOR.get(tile, C["grass"])
                pygame.draw.rect(screen, color,
                    (tx * TILE_SIZE - cam_x, ty * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE))
                # Tile details
                if tile == "forest":
                    pygame.draw.circle(screen, (15, 50, 15),
                        (tx * TILE_SIZE - cam_x + 16, ty * TILE_SIZE - cam_y + 16), 10)
                elif tile == "stone":
                    pygame.draw.rect(screen, (60, 60, 70),
                        (tx * TILE_SIZE - cam_x + 8, ty * TILE_SIZE - cam_y + 8, 16, 16))

        # NPCs
        for npc in npcs:
            nx_s = npc.x - cam_x
            ny_s = npc.y - cam_y
            if -32 < nx_s < SCREEN_W + 32 and -32 < ny_s < SCREEN_H + 32:
                col = C["gold"] if npc.role == "merchant" else C["blue"] if npc.role == "guard" else C["orange"] if npc.role == "blacksmith" else C["white"]
                pygame.draw.circle(screen, col, (int(nx_s), int(ny_s)), 12)
                pygame.draw.circle(screen, C["black"], (int(nx_s), int(ny_s)), 12, 2)
                name_t = font_sm.render(npc.name, True, col)
                screen.blit(name_t, (int(nx_s) - name_t.get_width()//2, int(ny_s) - 28))
                if npc.hired:
                    screen.blit(font_sm.render("★", True, C["gold"]), (int(nx_s)+10, int(ny_s)-28))

        # Enemies
        for en in enemies:
            ex_s = int(en.x - cam_x)
            ey_s = int(en.y - cam_y)
            if -32 < ex_s < SCREEN_W + 32 and -32 < ey_s < SCREEN_H + 32:
                pygame.draw.rect(screen, en.color, (ex_s - 10, ey_s - 10, 20, 20))
                pygame.draw.rect(screen, C["black"], (ex_s - 10, ey_s - 10, 20, 20), 1)
                # HP bar above
                draw_bar(screen, ex_s - 15, ey_s - 18, 30, 5, en.hp, en.max_hp, C["red"])
                name_t = font_sm.render(en.name, True, en.color)
                screen.blit(name_t, (ex_s - name_t.get_width()//2, ey_s - 30))

        # Player
        px_s = int(player.x - cam_x)
        py_s = int(player.y - cam_y)
        pygame.draw.circle(screen, C["blue"], (px_s, py_s), 14)
        pygame.draw.circle(screen, C["white"], (px_s, py_s), 14, 2)
        pygame.draw.rect(screen, player.weapon["color"], (px_s + 10, py_s - 6, 16, 5))

        # HUD
        draw_hud(screen, player)

        # Controls hint
        hints = "WASD:move  SPACE:attack  1-4:spell  I:inventory  C:craft  F:potion  ESC:pause"
        screen.blit(font_sm.render(hints, True, C["gray"]), (SCREEN_W//2 - 280, SCREEN_H - 16))

        # Overlays
        if STATE == "pause":
            s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            s.fill((0, 0, 0, 140))
            screen.blit(s, (0, 0))
            draw_pause(screen, mx, my)

        if show_inv:
            s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            s.fill((0, 0, 0, 120))
            screen.blit(s, (0, 0))
            draw_inventory(screen, player, mx, my)

        if show_shop:
            s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            s.fill((0, 0, 0, 120))
            screen.blit(s, (0, 0))
            draw_shop(screen, player, mx, my)

        if show_craft:
            s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            s.fill((0, 0, 0, 120))
            screen.blit(s, (0, 0))
            draw_craft(screen, player, mx, my)

        if active_npc:
            draw_npc_dialog(screen, active_npc, player, mx, my)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()