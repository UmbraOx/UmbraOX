"""
Optiopia - Complete RPG
Full pygame GUI, no terminal input.
Clickable class selection, inventory grid, shop, save/load, 3 enemy types,
health/mana bars, gear slots panel, all inside pygame window.
"""
import pygame
import json
import os
import random
import math

pygame.init()

W, H = 1024, 768
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Optiopia")
clock = pygame.time.Clock()

# ── Colors ──────────────────────────────────────────────────────────────────
BG       = (15, 15, 30)
PANEL    = (25, 25, 50)
ACCENT   = (80, 120, 200)
GREEN    = (50, 180, 80)
RED      = (200, 60, 60)
BLUE     = (60, 100, 200)
GOLD     = (220, 180, 40)
WHITE    = (240, 240, 240)
GRAY     = (120, 120, 140)
DARK     = (10, 10, 20)
PURPLE   = (140, 60, 200)
ORANGE   = (220, 140, 40)

font_lg  = pygame.font.SysFont("consolas", 28, bold=True)
font_md  = pygame.font.SysFont("consolas", 18)
font_sm  = pygame.font.SysFont("consolas", 14)

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "optiopia_save.json")

# ── Item Definitions ─────────────────────────────────────────────────────────
ITEMS = {
    "Iron Sword":    {"type":"weapon",  "atk":8,  "def":0,  "cost":50,  "color":GRAY},
    "Steel Sword":   {"type":"weapon",  "atk":15, "def":0,  "cost":120, "color":WHITE},
    "Iron Shield":   {"type":"armor",   "atk":0,  "def":6,  "cost":40,  "color":GRAY},
    "Chain Mail":    {"type":"armor",   "atk":0,  "def":10, "cost":100, "color":ACCENT},
    "Health Potion": {"type":"potion",  "hp":40,  "cost":20, "color":RED},
    "Mana Potion":   {"type":"potion",  "mp":30,  "cost":15, "color":BLUE},
    "Fire Staff":    {"type":"weapon",  "atk":20, "def":0,  "cost":200, "color":ORANGE},
    "Elven Bow":     {"type":"weapon",  "atk":12, "def":0,  "cost":150, "color":GREEN},
    "Plate Armor":   {"type":"armor",   "atk":0,  "def":18, "cost":250, "color":GOLD},
}

CLASS_DEFS = {
    "Warrior": {"hp":150,"mp":40,"atk":12,"def":8,"color":RED,"desc":"High HP and defense"},
    "Mage":    {"hp":80, "mp":120,"atk":20,"def":3,"color":PURPLE,"desc":"High magic power"},
    "Ranger":  {"hp":110,"mp":70, "atk":15,"def":5,"color":GREEN,"desc":"Balanced fighter"},
}

ENEMY_DEFS = [
    {"name":"Goblin",    "hp":40, "atk":8,  "def":2,  "xp":15, "gold":10, "color":(60,160,60),  "size":24},
    {"name":"Orc Warrior","hp":80,"atk":14, "def":6,  "xp":30, "gold":25, "color":(100,60,40),  "size":32},
    {"name":"Dark Mage", "hp":55, "atk":18, "def":3,  "xp":40, "gold":35, "color":(140,40,180), "size":28},
]

# ── Button Helper ─────────────────────────────────────────────────────────────
class Button:
    def __init__(self, x, y, w, h, text, color=ACCENT, text_color=WHITE, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = font or font_md
        self.hovered = False

    def draw(self, surf):
        c = tuple(min(255, v+30) for v in self.color) if self.hovered else self.color
        pygame.draw.rect(surf, c, self.rect, border_radius=6)
        pygame.draw.rect(surf, WHITE, self.rect, 1, border_radius=6)
        t = self.font.render(self.text, True, self.text_color)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def update(self, mx, my):
        self.hovered = self.rect.collidepoint(mx, my)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_bar(surf, x, y, w, h, val, max_val, color, label=""):
    pygame.draw.rect(surf, DARK, (x, y, w, h), border_radius=4)
    filled = int(w * max(0, val) / max(1, max_val))
    if filled > 0:
        pygame.draw.rect(surf, color, (x, y, filled, h), border_radius=4)
    pygame.draw.rect(surf, WHITE, (x, y, w, h), 1, border_radius=4)
    if label:
        t = font_sm.render(f"{label}: {val}/{max_val}", True, WHITE)
        surf.blit(t, (x + 4, y + 1))


def draw_text(surf, text, x, y, color=WHITE, font=None):
    f = font or font_md
    surf.blit(f.render(text, True, color), (x, y))


# ── Enemy ────────────────────────────────────────────────────────────────────
class Enemy:
    def __init__(self, etype_idx, x, y):
        d = ENEMY_DEFS[etype_idx % len(ENEMY_DEFS)]
        self.name  = d["name"]
        self.hp    = d["hp"] + random.randint(0, 20)
        self.maxhp = self.hp
        self.atk   = d["atk"]
        self.def_  = d["def"]
        self.xp    = d["xp"]
        self.gold  = d["gold"]
        self.color = d["color"]
        self.size  = d["size"]
        self.x, self.y = float(x), float(y)
        self.alive = True
        self.atk_timer = 0

    def move_toward(self, px, py, dt):
        dx, dy = px - self.x, py - self.y
        dist = math.hypot(dx, dy)
        if dist > 40:
            speed = 60 * dt
            self.x += (dx/dist) * speed
            self.y += (dy/dist) * speed

    def draw(self, surf):
        if not self.alive:
            return
        s = self.size
        pygame.draw.rect(surf, self.color, (int(self.x)-s//2, int(self.y)-s//2, s, s), border_radius=4)
        pygame.draw.rect(surf, WHITE, (int(self.x)-s//2, int(self.y)-s//2, s, s), 1, border_radius=4)
        draw_bar(surf, int(self.x)-s//2, int(self.y)-s//2-10, s, 6, self.hp, self.maxhp, RED)
        t = font_sm.render(self.name[0], True, WHITE)
        surf.blit(t, t.get_rect(center=(int(self.x), int(self.y))))


# ── Player ───────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, class_name):
        d = CLASS_DEFS[class_name]
        self.class_name = class_name
        self.name  = "Hero"
        self.hp    = d["hp"]
        self.maxhp = d["hp"]
        self.mp    = d["mp"]
        self.maxmp = d["mp"]
        self.base_atk = d["atk"]
        self.base_def = d["def"]
        self.color = d["color"]
        self.gold  = 100
        self.xp    = 0
        self.level = 1
        self.xp_next = 50
        self.x, self.y = 300.0, 350.0
        self.speed = 150
        self.atk_cooldown = 0
        self.inv_items = []   # list of item name strings
        self.equipped  = {"weapon": None, "armor": None}

    @property
    def atk(self):
        bonus = ITEMS[self.equipped["weapon"]]["atk"] if self.equipped["weapon"] else 0
        return self.base_atk + bonus

    @property
    def def_(self):
        bonus = ITEMS[self.equipped["armor"]]["def"] if self.equipped["armor"] else 0
        return self.base_def + bonus

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.xp_next = int(self.xp_next * 1.4)
            self.maxhp  += 15
            self.maxmp  += 10
            self.base_atk += 2
            self.base_def += 1
            self.hp = self.maxhp
            self.mp = self.maxmp

    def use_potion(self, item_name):
        if item_name not in self.inv_items:
            return False
        d = ITEMS[item_name]
        if d["type"] != "potion":
            return False
        self.inv_items.remove(item_name)
        if "hp" in d:
            self.hp = min(self.maxhp, self.hp + d["hp"])
        if "mp" in d:
            self.mp = min(self.maxmp, self.mp + d["mp"])
        return True

    def equip(self, item_name):
        if item_name not in self.inv_items:
            return
        d = ITEMS[item_name]
        slot = "weapon" if d["type"] == "weapon" else "armor"
        if self.equipped[slot]:
            self.inv_items.append(self.equipped[slot])
        self.equipped[slot] = item_name
        self.inv_items.remove(item_name)

    def to_dict(self):
        return {
            "class_name": self.class_name,
            "hp": self.hp, "maxhp": self.maxhp,
            "mp": self.mp, "maxmp": self.maxmp,
            "base_atk": self.base_atk, "base_def": self.base_def,
            "gold": self.gold, "xp": self.xp,
            "level": self.level, "xp_next": self.xp_next,
            "x": self.x, "y": self.y,
            "inv_items": self.inv_items,
            "equipped": self.equipped,
        }

    @classmethod
    def from_dict(cls, d):
        p = cls(d["class_name"])
        for k, v in d.items():
            setattr(p, k, v)
        return p


# ── Game States ───────────────────────────────────────────────────────────────
STATE_CLASS_SELECT = "class_select"
STATE_PLAY         = "play"
STATE_INVENTORY    = "inventory"
STATE_SHOP         = "shop"
STATE_GAME_OVER    = "game_over"

class Game:
    def __init__(self):
        self.state   = STATE_CLASS_SELECT
        self.player  = None
        self.enemies = []
        self.spawn_timer = 0
        self.wave    = 1
        self.message = ""
        self.msg_timer = 0
        self.class_btns = []
        self.action_btns = {}
        self._build_class_btns()
        self._build_action_btns()

    def _build_class_btns(self):
        names = list(CLASS_DEFS.keys())
        for i, cn in enumerate(names):
            bx = W//2 - 120 + (i-1) * 260
            self.class_btns.append(Button(bx-100, 340, 200, 60, cn,
                                          color=CLASS_DEFS[cn]["color"]))

    def _build_action_btns(self):
        self.action_btns = {
            "inventory": Button(650, 10, 110, 32, "Inventory", ACCENT),
            "shop":      Button(770, 10, 80,  32, "Shop",      GOLD,   DARK),
            "save":      Button(860, 10, 70,  32, "Save",      GREEN,  DARK),
            "load":      Button(940, 10, 70,  32, "Load",      GRAY),
            "back":      Button(10,  10, 70,  32, "Back",      RED),
        }

    def show_message(self, msg, duration=2.5):
        self.message   = msg
        self.msg_timer = duration

    def spawn_enemies(self):
        count = 2 + self.wave
        for _ in range(count):
            ex = random.choice([random.randint(580, 620), random.randint(0, 30)])
            ey = random.randint(60, H-60)
            etype = random.randint(0, min(self.wave - 1, 2))
            self.enemies.append(Enemy(etype, ex, ey))

    def save(self):
        if not self.player:
            return
        data = {"player": self.player.to_dict(), "wave": self.wave}
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        self.show_message("Game Saved!")

    def load(self):
        if not os.path.isfile(SAVE_FILE):
            self.show_message("No save file found.")
            return
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        self.player = Player.from_dict(data["player"])
        self.wave   = data.get("wave", 1)
        self.enemies = []
        self.spawn_enemies()
        self.state  = STATE_PLAY
        self.show_message("Game Loaded!")

    def update(self, dt, events):
        mx, my = pygame.mouse.get_pos()

        if self.msg_timer > 0:
            self.msg_timer -= dt

        if self.state == STATE_CLASS_SELECT:
            for btn in self.class_btns:
                btn.update(mx, my)
            for event in events:
                for btn in self.class_btns:
                    if btn.clicked(event):
                        self.player = Player(btn.text)
                        self.enemies = []
                        self.spawn_enemies()
                        self.state = STATE_PLAY
                        self.show_message(f"Welcome, {btn.text}! Survive the waves!")

        elif self.state == STATE_PLAY:
            for btn in self.action_btns.values():
                btn.update(mx, my)
            for event in events:
                if self.action_btns["inventory"].clicked(event):
                    self.state = STATE_INVENTORY
                if self.action_btns["shop"].clicked(event):
                    self.state = STATE_SHOP
                if self.action_btns["save"].clicked(event):
                    self.save()
                if self.action_btns["load"].clicked(event):
                    self.load()

            keys = pygame.key.get_pressed()
            p = self.player
            spd = p.speed * dt
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                p.y = max(50, p.y - spd)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                p.y = min(H - 20, p.y + spd)
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                p.x = max(20, p.x - spd)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                p.x = min(580, p.x + spd)

            if p.atk_cooldown > 0:
                p.atk_cooldown -= dt

            if keys[pygame.K_SPACE] and p.atk_cooldown <= 0:
                p.atk_cooldown = 0.5
                for e in self.enemies:
                    if e.alive and math.hypot(e.x - p.x, e.y - p.y) < 80:
                        dmg = max(1, p.atk - e.def_ + random.randint(-3, 3))
                        e.hp -= dmg
                        if e.hp <= 0:
                            e.alive = False
                            p.gain_xp(e.xp)
                            p.gold += e.gold
                            self.show_message(f"+{e.xp} XP +{e.gold} Gold")

            for e in self.enemies:
                if not e.alive:
                    continue
                e.move_toward(p.x, p.y, dt)
                e.atk_timer += dt
                if e.atk_timer >= 1.2 and math.hypot(e.x - p.x, e.y - p.y) < 44:
                    e.atk_timer = 0
                    dmg = max(1, e.atk - p.def_ + random.randint(-2, 2))
                    p.hp -= dmg

            self.enemies = [e for e in self.enemies if e.alive]
            if not self.enemies:
                self.wave += 1
                self.spawn_timer += dt
                if self.spawn_timer >= 2:
                    self.spawn_timer = 0
                    self.spawn_enemies()
                    self.show_message(f"Wave {self.wave}!")

            if p.hp <= 0:
                p.hp = 0
                self.state = STATE_GAME_OVER

        elif self.state in (STATE_INVENTORY, STATE_SHOP):
            self.action_btns["back"].update(mx, my)
            for event in events:
                if self.action_btns["back"].clicked(event):
                    self.state = STATE_PLAY

        elif self.state == STATE_GAME_OVER:
            for event in events:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.__init__()

    def draw_hud(self):
        p = self.player
        # Left panel background
        pygame.draw.rect(screen, PANEL, (0, 0, 640, 50))
        draw_bar(screen, 10, 10, 200, 14, p.hp, p.maxhp, RED, "HP")
        draw_bar(screen, 10, 28, 200, 14, p.mp, p.maxmp, BLUE, "MP")
        draw_bar(screen, 215, 10, 150, 14, p.xp, p.xp_next, GOLD)
        draw_text(screen, f"XP to lv{p.level+1}", 215, 12, GOLD, font_sm)
        draw_text(screen, f"Lv{p.level}", 215, 26, WHITE, font_sm)
        draw_text(screen, f"Gold: {p.gold}", 370, 10, GOLD, font_md)
        draw_text(screen, f"Wave: {self.wave}", 370, 28, WHITE, font_sm)
        draw_text(screen, f"ATK:{p.atk} DEF:{p.def_}", 460, 10, WHITE, font_sm)
        draw_text(screen, "WASD/Arrows=Move  SPACE=Attack", 10, H-20, GRAY, font_sm)

        for btn in self.action_btns.values():
            if btn.text not in ("back",):
                btn.draw(screen)

    def draw_side_panel(self):
        p = self.player
        pygame.draw.rect(screen, PANEL, (640, 0, 384, H))
        pygame.draw.line(screen, ACCENT, (640, 0), (640, H), 2)
        draw_text(screen, "GEAR SLOTS", 660, 10, ACCENT, font_md)
        slots = [("Weapon", p.equipped["weapon"]), ("Armor", p.equipped["armor"])]
        for i, (slot_name, item_name) in enumerate(slots):
            y = 40 + i * 70
            pygame.draw.rect(screen, DARK, (655, y, 350, 60), border_radius=6)
            pygame.draw.rect(screen, ACCENT, (655, y, 350, 60), 1, border_radius=6)
            draw_text(screen, slot_name + ":", 665, y+5, GRAY, font_sm)
            if item_name:
                col = ITEMS[item_name]["color"]
                draw_text(screen, item_name, 665, y+22, col, font_md)
                d = ITEMS[item_name]
                stat = f"ATK+{d['atk']}" if d.get('atk') else f"DEF+{d.get('def',0)}"
                draw_text(screen, stat, 665, y+40, GOLD, font_sm)
            else:
                draw_text(screen, "(empty)", 665, y+22, GRAY, font_md)

        draw_text(screen, "MINIMAP", 660, 200, ACCENT, font_md)
        pygame.draw.rect(screen, DARK, (655, 220, 350, 200), border_radius=4)
        pygame.draw.rect(screen, ACCENT, (655, 220, 350, 200), 1, border_radius=4)
        scale = 350/640
        pygame.draw.circle(screen, p.color,
            (655 + int(p.x*scale), 220 + int((p.y-50)/H*200)), 5)
        for e in self.enemies:
            if e.alive:
                pygame.draw.circle(screen, e.color,
                    (655 + int(e.x*scale), 220 + int((e.y-50)/H*200)), 3)

        draw_text(screen, f"Class: {p.class_name}", 660, 435, p.color, font_md)
        draw_text(screen, f"Level: {p.level}", 660, 455, WHITE, font_sm)
        draw_text(screen, f"Enemies: {len([e for e in self.enemies if e.alive])}", 660, 475, RED, font_sm)
        draw_text(screen, f"Inventory: {len(p.inv_items)} items", 660, 495, WHITE, font_sm)

    def draw_inventory(self):
        screen.fill(BG)
        draw_text(screen, "INVENTORY", W//2-80, 20, ACCENT, font_lg)
        self.action_btns["back"].draw(screen)
        p = self.player

        cols, rows = 6, 4
        iw, ih = 130, 80
        ox, oy = 40, 70
        mx, my = pygame.mouse.get_pos()

        all_items = p.inv_items[:]

        for idx in range(cols * rows):
            x = ox + (idx % cols) * (iw + 8)
            y = oy + (idx // cols) * (ih + 8)
            pygame.draw.rect(screen, DARK, (x, y, iw, ih), border_radius=6)
            pygame.draw.rect(screen, GRAY, (x, y, iw, ih), 1, border_radius=6)

            if idx < len(all_items):
                iname = all_items[idx]
                idata = ITEMS[iname]
                col   = idata["color"]
                draw_text(screen, iname[:12], x+5, y+5, col, font_sm)
                if idata["type"] == "potion":
                    hp_val = idata.get("hp", 0)
                    mp_val = idata.get("mp", 0)
                    if hp_val:
                        draw_text(screen, f"+{hp_val} HP", x+5, y+25, RED, font_sm)
                    if mp_val:
                        draw_text(screen, f"+{mp_val} MP", x+5, y+25, BLUE, font_sm)
                    # Use button
                    if pygame.Rect(x+5, y+48, 55, 22).collidepoint(mx, my):
                        pygame.draw.rect(screen, GREEN, (x+5, y+48, 55, 22), border_radius=4)
                    else:
                        pygame.draw.rect(screen, (30,100,30), (x+5, y+48, 55, 22), border_radius=4)
                    draw_text(screen, "USE", x+18, y+50, WHITE, font_sm)
                    if (pygame.mouse.get_pressed()[0] and
                            pygame.Rect(x+5, y+48, 55, 22).collidepoint(mx, my)):
                        p.use_potion(iname)
                        self.show_message(f"Used {iname}")
                else:
                    stat = f"ATK+{idata.get('atk',0)}" if idata.get('atk') else f"DEF+{idata.get('def',0)}"
                    draw_text(screen, stat, x+5, y+25, GOLD, font_sm)
                    # Equip button
                    if pygame.Rect(x+5, y+48, 60, 22).collidepoint(mx, my):
                        pygame.draw.rect(screen, ACCENT, (x+5, y+48, 60, 22), border_radius=4)
                    else:
                        pygame.draw.rect(screen, (30,50,120), (x+5, y+48, 60, 22), border_radius=4)
                    draw_text(screen, "EQUIP", x+8, y+50, WHITE, font_sm)
                    if (pygame.mouse.get_pressed()[0] and
                            pygame.Rect(x+5, y+48, 60, 22).collidepoint(mx, my)):
                        p.equip(iname)
                        self.show_message(f"Equipped {iname}")

        y2 = oy + rows * (ih + 8) + 10
        draw_text(screen, "EQUIPPED:", 40, y2, ACCENT, font_md)
        draw_text(screen, f"Weapon: {p.equipped['weapon'] or 'None'}", 40, y2+25, WHITE, font_sm)
        draw_text(screen, f"Armor:  {p.equipped['armor'] or 'None'}", 40, y2+45, WHITE, font_sm)
        draw_text(screen, f"Gold: {p.gold}", 40, y2+65, GOLD, font_md)

    def draw_shop(self):
        screen.fill(BG)
        draw_text(screen, "SHOP", W//2-40, 20, GOLD, font_lg)
        draw_text(screen, f"Your Gold: {self.player.gold}", W-200, 20, GOLD, font_md)
        self.action_btns["back"].draw(screen)

        mx, my = pygame.mouse.get_pos()
        shop_items = list(ITEMS.keys())
        cols = 3
        iw, ih = 200, 100
        ox, oy = 60, 70

        for idx, iname in enumerate(shop_items):
            x = ox + (idx % cols) * (iw + 20)
            y = oy + (idx // cols) * (ih + 10)
            idata = ITEMS[iname]
            hover = pygame.Rect(x, y, iw, ih).collidepoint(mx, my)
            bg_col = (40, 40, 60) if hover else DARK
            pygame.draw.rect(screen, bg_col, (x, y, iw, ih), border_radius=8)
            pygame.draw.rect(screen, idata["color"], (x, y, iw, ih), 2, border_radius=8)
            draw_text(screen, iname, x+8, y+6, idata["color"], font_sm)
            t = idata["type"].upper()
            draw_text(screen, t, x+8, y+24, GRAY, font_sm)
            if idata["type"] != "potion":
                stat = f"ATK+{idata.get('atk',0)}" if idata.get('atk') else f"DEF+{idata.get('def',0)}"
                draw_text(screen, stat, x+8, y+42, WHITE, font_sm)
            else:
                val = f"HP+{idata.get('hp',0)}" if idata.get('hp') else f"MP+{idata.get('mp',0)}"
                draw_text(screen, val, x+8, y+42, WHITE, font_sm)
            cost = idata["cost"]
            can_afford = self.player.gold >= cost
            draw_text(screen, f"{cost} Gold", x+8, y+60, GOLD if can_afford else RED, font_sm)
            # Buy button
            btn_col = (30,130,30) if can_afford else (80,30,30)
            if hover and can_afford:
                btn_col = GREEN
            pygame.draw.rect(screen, btn_col, (x+8, y+76, 80, 18), border_radius=4)
            draw_text(screen, "BUY", x+28, y+77, WHITE, font_sm)

            if (pygame.mouse.get_pressed()[0] and
                    pygame.Rect(x+8, y+76, 80, 18).collidepoint(mx, my) and can_afford):
                self.player.gold -= cost
                self.player.inv_items.append(iname)
                self.show_message(f"Bought {iname}!")

    def draw(self):
        if self.state == STATE_CLASS_SELECT:
            screen.fill(BG)
            draw_text(screen, "OPTIOPIA", W//2-120, 80, ACCENT, font_lg)
            draw_text(screen, "Choose Your Class", W//2-120, 140, WHITE, font_md)
            for btn in self.class_btns:
                btn.draw(screen)
                # Class description
                d = CLASS_DEFS[btn.text]
                draw_text(screen, d["desc"], btn.rect.x, btn.rect.y + 70, GRAY, font_sm)
                draw_text(screen, f"HP:{d['hp']} MP:{d['mp']} ATK:{d['atk']} DEF:{d['def']}",
                         btn.rect.x, btn.rect.y + 88, d["color"], font_sm)

        elif self.state == STATE_PLAY:
            # Game area
            screen.fill(BG)
            # Ground grid
            for gx in range(0, 640, 60):
                pygame.draw.line(screen, (20,20,40), (gx,50), (gx,H), 1)
            for gy in range(50, H, 60):
                pygame.draw.line(screen, (20,20,40), (0,gy), (640,gy), 1)

            # Player
            p = self.player
            pygame.draw.rect(screen, p.color,
                (int(p.x)-15, int(p.y)-15, 30, 30), border_radius=5)
            pygame.draw.rect(screen, WHITE,
                (int(p.x)-15, int(p.y)-15, 30, 30), 1, border_radius=5)
            draw_bar(screen, int(p.x)-20, int(p.y)-30, 40, 6, p.hp, p.maxhp, RED)

            for e in self.enemies:
                e.draw(screen)

            self.draw_hud()
            self.draw_side_panel()

        elif self.state == STATE_INVENTORY:
            self.draw_inventory()

        elif self.state == STATE_SHOP:
            self.draw_shop()

        elif self.state == STATE_GAME_OVER:
            screen.fill(BG)
            draw_text(screen, "GAME OVER", W//2-120, H//2-60, RED, font_lg)
            draw_text(screen, f"Reached Wave {self.wave}", W//2-100, H//2, WHITE, font_md)
            draw_text(screen, "Click or press any key to restart", W//2-160, H//2+40, GRAY, font_md)

        # Message overlay
        if self.msg_timer > 0 and self.message:
            alpha = min(255, int(self.msg_timer * 200))
            t = font_md.render(self.message, True, GOLD)
            tr = t.get_rect(center=(W//2, H-60))
            pygame.draw.rect(screen, (0,0,0,180), tr.inflate(20,10), border_radius=6)
            screen.blit(t, tr)

        pygame.display.flip()


def main():
    game = Game()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        game.update(dt, events)
        game.draw()

    pygame.quit()


if __name__ == "__main__":
    main()