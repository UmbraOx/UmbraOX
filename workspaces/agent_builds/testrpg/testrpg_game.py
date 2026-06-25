# game_skeleton.py — Umbra Game Skeleton Template v3.0
# Place at: C:\Umbra\core\assets\game_skeleton.py
# This file is the authoritative game template used by _stitch_game().
# Umbra replaces __PLACEHOLDERS__ with agent-generated code.
# DO NOT import this file — it is read as a text template by Umbra.

import pygame
import sys
import math
import random
import json
import os
import time

# ── INJECTED AGENT MODULES ──────────────────────────────────────────────────
# Each block below is replaced by Umbra with real agent output.
# If an agent returned nothing, the fallback code below keeps the game runnable.

# ── WORLD MODULE ─────────────────────────────────────────────────────────────

WORLD_MAP = [['plains'] * 200 for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (218, 165, 32),
    'water': (72, 202, 228),
    'snow': (255, 250, 250),
    'swamp': (94, 129, 162),
    'town': (255, 215, 0),
    'camp': (210, 180, 140),
    'mine': (128, 128, 128),
    'wood_area': (34, 93, 67),
    'road': (150, 150, 150)
}
TOWNS = [(random.randint(0, 199), random.randint(0, 199), 'Village') for _ in range(1)]
CITIES = [(random.randint(0, 199), random.randint(0, 199), f'City{i+1}') for i in range(2)]
BANDIT_CAMPS = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]
GOBLIN_CAMPS = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]
MINES = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]
WOODCUTS = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]

def gen_world():
    random.seed(42)
    biomes = list(BIOME_COL.keys())
    for x in range(200):
        for y in range(200):
            WORLD_MAP[x][y] = random.choice(biomes)

def draw_world(surf, cam_x, cam_y):
    tile_size = 10
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            x = cam_x + dx
            y = cam_y + dy
            if 0 <= x < 200 and 0 <= y < 200:
                biome = WORLD_MAP[x][y]
                color = BIOME_COL[biome]
                pygame.draw.rect(surf, color, (dx * tile_size, dy * tile_size, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'plains'

# ── CHARACTER MODULE ─────────────────────────────────────────────────────────

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls="Warrior"):
        self.cls = cls
        self.name = "Hero"
        self.x, self.y = 512.0, 512.0
        self.w = self.h = 28
        self.col = (100, 160, 240)
        self.max_hp, self.hp = 100, 100
        self.max_mp, self.mp = 50, 50
        self.max_sta, self.sta = 100, 100
        self.str_, self.dex, self.int_, self.luck = 10, 10, 10, 10
        self.atk = 10
        self.defense = 5
        self.spd = 180
        self.level, self.xp, self.xp_next = 1, 0, 100
        self.gold = 50
        self.speed = 5
        self.vx = self.vy = 0.0
        self.inventory = {}
        self.equipped = {"weapon": None, "armor": None}
        self.spells = []
        self.current_spell = 0
        self.active_quests = {}
        self.completed_quests = []
        self.kills = {}
        self.quests = []
        self.crouching = False
        self.sprint = False
        self.alive = True
        self.regen_timer = 0.0
        self.attack_cooldown = 0.0
        self.float_texts = []
        # Apply class bonuses
        bases = {
            "Warrior":  dict(max_hp=130, max_mp=30,  max_sta=100, atk=14, defense=8,  col=(200, 80, 80)),
            "Mage":     dict(max_hp=70,  max_mp=120, max_sta=60,  atk=8,  defense=3,  col=(80,  80, 200)),
            "Rogue":    dict(max_hp=90,  max_mp=50,  max_sta=90,  atk=12, defense=5,  col=(80,  180, 80)),
            "Ranger":   dict(max_hp=100, max_mp=60,  max_sta=80,  atk=11, defense=6,  col=(160, 120, 40)),
            "Paladin":  dict(max_hp=120, max_mp=70,  max_sta=90,  atk=13, defense=10, col=(230, 200, 60)),
        }
        b = bases.get(cls, bases["Warrior"])
        for k, v in b.items():
            setattr(self, k, v)
            base = k.replace("max_", "")
            if base in ("hp", "mp", "sta"):
                setattr(self, base, v)

    def atk_power(self):
        return self.str_ + (self.dex // 2)

    def def_power(self):
        return self.dex + (self.str_ // 2)

    def add_item(self, name, qty):
        if name in self.inventory:
            self.inventory[name] += qty
        else:
            self.inventory[name] = qty

    def gain_xp(self, amt):
        self.xp += amt
        while self.xp >= self.xp_next:
            self.level_up()

    def level_up(self):
        self.xp -= self.xp_next
        self.xp_next = int(self.xp_next * 1.5)
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5
        self.mp = self.max_mp
        self.max_sta += 5
        self.sta = self.max_sta
        self.str_ += 2
        self.dex += 2
        self.int_ += 1
        self.luck += 1

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.max_hp * 0.01 * dt))
        self.mp = min(self.max_mp, self.mp + (self.max_mp * 0.01 * dt))
        self.sta = min(self.max_sta, self.sta + (self.max_sta * 0.01 * dt))

class Enemy:
    def __init__(self, edef, tx, ty):
        self.name = edef['name']
        self.hp = edef['hp']
        self.atk = edef['atk']
        self.def_ = edef['def']
        self.xp = edef['xp']
        self.col = edef['col']
        self.spd = edef['spd']
        self.faction = edef['faction']
        self.tx, self.ty = tx, ty
        self.path = [(tx, ty)]
        self.patrol_index = 0

    def update(self, player, dt):
        if self.hp <= 0:
            return
        target_x, target_y = self.path[self.patrol_index]
        dx, dy = target_x - self.tx, target_y - self.ty
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 1:
            move_speed = self.spd * dt
            angle = math.atan2(dy, dx)
            self.tx += move_speed * math.cos(angle)
            self.ty += move_speed * math.sin(angle)
        else:
            self.patrol_index = (self.patrol_index + 1) % len(self.path)

    def draw(self, surf, cx, cy):
        pygame.draw.circle(surf, self.col, (int(cx + self.tx), int(cy + self.ty)), 10)

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x, self.y = tx, ty
        self.dialogue = []
        self.shop_stock = {}

# END OF CODE

# ── ITEM / DATA MODULE ───────────────────────────────────────────────────────
# Game Data Constants

WEAPONS = [
    {'name': 'Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (255, 69, 0)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 40, 'col': (139, 69, 19)},
    {'name': 'Staff', 'atk': 7, 'type': 'magic', 'val': 35, 'col': (255, 218, 185)},
    {'name': 'Axe', 'atk': 12, 'type': 'melee', 'val': 60, 'col': (139, 0, 0)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 50, 'col': (165, 42, 42)},
    {'name': 'Wand', 'atk': 9, 'type': 'magic', 'val': 45, 'col': (255, 182, 193)},
    {'name': 'Dagger', 'atk': 6, 'type': 'melee', 'val': 30, 'col': (255, 140, 0)},
    {'name': 'Spear', 'atk': 9, 'type': 'ranged', 'val': 45, 'col': (255, 69, 0)},
    {'name': 'Orb', 'atk': 8, 'type': 'magic', 'val': 40, 'col': (135, 206, 250)},
    {'name': 'Hammer', 'atk': 11, 'type': 'melee', 'val': 55, 'col': (165, 42, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helmet', 'Leather Chestplate', 'Leather Boots'], 'def': 5, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Iron Helmet', 'Iron Chestplate', 'Iron Boots'], 'def': 10, 'val': 60},
    {'name': 'Steel Armor', 'parts': ['Steel Helmet', 'Steel Chestplate', 'Steel Boots'], 'def': 15, 'val': 90}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 20, 'dmg': 15, 'col': (255, 69, 0), 'desc': 'A basic fire spell'},
    {'name': 'Heal', 'mp': 15, 'dmg': -10, 'col': (34, 139, 34), 'desc': 'Restores health to the target'},
    {'name': 'Lightning Bolt', 'mp': 25, 'dmg': 20, 'col': (255, 255, 0), 'desc': 'A powerful electric spell'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (65, 105, 225), 'desc': 'Creates a protective shield'},
    {'name': 'Ice Shard', 'mp': 18, 'dmg': 12, 'col': (0, 191, 255), 'desc': 'Throws an icy shard at the enemy'},
    {'name': 'Thunderclap', 'mp': 30, 'dmg': 25, 'col': (255, 69, 0), 'desc': 'A thunderous clap that damages enemies'},
    {'name': 'Poison Arrow', 'mp': 12, 'dmg': 8, 'col': (34, 139, 34), 'desc': 'Fires an arrow coated in poison'},
    {'name': 'Earthquake', 'mp': 35, 'dmg': 30, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake and damage enemies'},
    {'name': 'Frost Nova', 'mp': 22, 'dmg': 18, 'col': (0, 191, 255), 'desc': 'Freezes nearby enemies in ice'},
    {'name': 'Meteor Shower', 'mp': 40, 'dmg': 35, 'col': (255, 69, 0), 'desc': 'Summons meteors to rain down on enemies'}
]

MATERIALS = [
    'Iron Ore',
    'Steel Ingot',
    'Leather Hide',
    'Magic Crystal',
    'Wood Plank',
    'Mana Stone',
    'Goblin Horn',
    'Dragon Scale',
    'Phoenix Feather',
    'Elixir of Life'
]

QUESTS = [
    {'id': 1, 'name': 'Kill Goblins', 'desc': 'Eliminate 5 goblins in the forest.', 'target': 'goblin', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Iron Ore', 'desc': 'Gather 10 pieces of iron ore from the mines.', 'target': 'mat:Iron Ore', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 10},
    {'id': 3, 'name': 'Defeat Bandit Leader', 'desc': 'Find and defeat the bandit leader in the mountains.', 'target': 'Bandit Leader', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 200, 'reward_xp': 50},
    {'id': 4, 'name': 'Craft Steel Armor', 'desc': 'Create a set of steel armor.', 'target': 'Steel Armor', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 150, 'reward_xp': 30},
    {'id': 5, 'name': 'Rescue Princess', 'desc': 'Save the princess from the dragon.', 'target': 'Dragon', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 500, 'reward_xp': 100}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Gang'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Greetings! How can I assist you?', 'opts': ['Report a crime', 'Ask about quests', 'Leave']}],
    'Blacksmith': [{'text': 'Need weapons or armor? Come in!', 'opts': ['Order weapon', 'Order armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How are you today?', 'opts': ['Buy produce', 'Chat', 'Leave']}],
    'default': [{'text': 'Hi there.', 'opts': ['Talk', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caelum',
    'Daria',
    'Elian',
    'Fiona',
    'Galen',
    'Hannah',
    'Igor',
    'Jenna',
    'Kael',
    'Lila',
    'Morgan',
    'Nora',
    'Oscar',
    'Piper'
]

NPC_JOBS = ['Blacksmith']

# ── MECHANIC MODULE ──────────────────────────────────────────────────────────
# Game Mechanic Helpers Module


class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, px, py, speed=0.1):
        self.x += (px - self.x) * speed
        self.y += (py - self.y) * speed

class FloatText:
    def __init__(self, text, x, y, col=(255, 255, 255), lifespan=60, fade_rate=1):
        self.text = text
        self.x = x
        self.y = y
        self.col = col
        self.lifespan = lifespan
        self.fade_rate = fade_rate

    def update(self):
        if self.lifespan > 0:
            self.y -= 0.5
            self.lifespan -= self.fade_rate
            self.col = (self.col[0], self.col[1], self.col[2], max(0, int(self.col[3] - self.fade_rate * 4)))

    def draw(self, surf, cx, cy, font):
        if self.lifespan > 0:
            text_surface = font.render(self.text, True, self.col)
            surf.blit(text_surface, (self.x - cx, self.y - cy))

class Projectile:
    def __init__(self, x, y, tx, ty, dmg, col, spd=9):
        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty
        self.dmg = dmg
        self.col = col
        self.spd = spd
        angle = math.atan2(ty - y, tx - x)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surf, cx, cy):
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 3)

class Building:
    TYPES = {
        'House': {'col': (165, 42, 42), 'w': 2, 'h': 2, 'cost': {'wood': 10, 'stone': 5}},
        'Shop': {'col': (255, 182, 193), 'w': 3, 'h': 2, 'cost': {'wood': 15, 'stone': 7}},
        'Barracks': {'col': (100, 149, 237), 'w': 4, 'h': 3, 'cost': {'wood': 20, 'stone': 10}},
        'Farm': {'col': (34, 139, 34), 'w': 3, 'h': 2, 'cost': {'wood': 8, 'stone': 3}},
        'Tower': {'col': (165, 42, 42), 'w': 2, 'h': 3, 'cost': {'wood': 12, 'stone': 8}},
        'Warehouse': {'col': (210, 105, 30), 'w': 3, 'h': 3, 'cost': {'wood': 18, 'stone': 9}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.col = Building.TYPES[btype]['col']
        self.w = Building.TYPES[btype]['w']
        self.h = Building.TYPES[btype]['h']

    def draw(self, surf, cx, cy, tile_size):
        x = (self.tx * tile_size) - cx
        y = (self.ty * tile_size) - cy
        pygame.draw.rect(surf, self.col, (x, y, self.w * tile_size, self.h * tile_size))
        pygame.draw.polygon(surf, (105, 105, 105), [(x + self.w * tile_size / 2, y),
                                                   (x, y - tile_size / 2),
                                                   (x + self.w * tile_size, y - tile_size / 2)])
        pygame.draw.rect(surf, (0, 0, 0), (x + tile_size // 4, y + self.h * tile_size - tile_size // 4, tile_size // 2, tile_size // 4))
        pygame.draw.rect(surf, (255, 255, 255), (x + tile_size // 2, y + tile_size // 2, tile_size // 8, tile_size // 8))

def save_game(player, buildings, filepath):
    try:
        data = {
            'player': player.__dict__,
            'buildings': [{'btype': b.btype, 'tx': b.tx, 'ty': b.ty} for b in buildings]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(e)
        return False

def load_game(player, buildings, filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        player.__dict__.update(data['player'])
        buildings.clear()
        for b in data['buildings']:
            buildings.append(Building(b['btype'], b['tx'], b['ty']))
        return True
    except Exception as e:
        print(e)
        return False

# ── UI MODULE ────────────────────────────────────────────────────────────────

font_cache = {}
def font_cache(sz):
    if sz not in font_cache:
        font_cache[sz] = pygame.font.Font(None, sz)
    return font_cache[sz]

def txt(surf, text, x, y, sz, col, center=False):
    fnt = font_cache(sz)
    txt_surf = fnt.render(text, True, col)
    if center:
        rect = txt_surf.get_rect(center=(x, y))
    else:
        rect = txt_surf.get_rect(topleft=(x, y))
    surf.blit(txt_surf, rect)
    return rect

def bar(surf, x, y, w, h, val, mx, col, bg):
    pygame.draw.rect(surf, bg, (x, y, w, h), 0)
    fill_w = int(w * val / mx)
    pygame.draw.rect(surf, col, (x, y, fill_w, h), 0)

def panel(surf, rx, ry, rw, rh, title):
    pygame.draw.rect(surf, (50, 50, 50), (rx, ry, rw, rh), 0)
    txt(surf, title, rx + 10, ry + 5, 24, (255, 255, 255))
    xbtn_rect = pygame.draw.rect(surf, (200, 0, 0), (rx + rw - 30, ry + 5, 20, 20), 0)
    txt(surf, 'X', rx + rw - 25, ry + 10, 24, (255, 255, 255), center=True)
    return xbtn_rect

def btn(surf, x, y, w, h, label, col, tcol, sz):
    pygame.draw.rect(surf, col, (x, y, w, h), 0)
    txt(surf, label, x + w // 2, y + h // 2, sz, tcol, center=True)
    return pygame.Rect(x, y, w, h)

def draw_hud(surf, player):
    bar(surf, 10, 10, 200, 20, player.hp, player.max_hp, (255, 0, 0), (100, 100, 100))
    bar(surf, 10, 40, 200, 20, player.mp, player.max_mp, (0, 0, 255), (100, 100, 100))
    bar(surf, 10, 70, 200, 20, player.sta, player.max_sta, (255, 165, 0), (100, 100, 100))
    txt(surf, f'Gold: {player.gold}', 10, 100, 24, (255, 255, 255))
    txt(surf, f'Lvl: {player.level} XP: {player.xp}/{player.next_level_xp}', 10, 130, 24, (255, 255, 255))
    txt(surf, f'Equipped: {player.equipped}', 10, 160, 24, (255, 255, 255))
    txt(surf, f'Biome: {player.biome}', 10, 190, 24, (255, 255, 255))

def draw_minimap(surf, player, enemies, WORLD_MAP, BIOME_COL):
    min_x = max(0, player.x - 63)
    min_y = max(0, player.y - 63)
    for y in range(min_y, min_y + 126):
        for x in range(min_x, min_x + 126):
            if 0 <= y < WORLD_MAP.height and 0 <= x < WORLD_MAP.width:
                pygame.draw.rect(surf, BIOME_COL[WORLD_MAP.get_biome(x, y)], (x - min_x, y - min_y, 1, 1))
    for enemy in enemies:
        ex = max(0, min(125, enemy.x - min_x))
        ey = max(0, min(125, enemy.y - min_y))
        pygame.draw.rect(surf, (255, 0, 0), (ex, ey, 3, 3))
    px = player.x - min_x
    py = player.y - min_y
    pygame.draw.rect(surf, (0, 255, 0), (px, py, 3, 3))

def draw_main_menu(surf, project_name):
    surf.fill((0, 0, 0))
    txt(surf, project_name, surf.get_width() // 2, surf.get_height() // 4, 72, (255, 255, 255), center=True)
    start_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2, 200, 50, 'Start', (100, 100, 100), (255, 255, 255), 36)
    load_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 70, 200, 50, 'Load', (100, 100, 100), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 3, surf.get_height() // 2 + 140, 200, 50, 'Quit', (100, 100, 100), (255, 255, 255), 36)
    return [start_btn, load_btn, quit_btn]

def draw_class_select(surf):
    class_cards = [
        {'name': 'Warrior', 'portrait': pygame.Surface((100, 100)), 'x': 100, 'y': 100},
        {'name': 'Mage', 'portrait': pygame.Surface((100, 100)), 'x': 300, 'y': 100},
        {'name': 'Rogue', 'portrait': pygame.Surface((100, 100)), 'x': 500, 'y': 100}
    ]
    for card in class_cards:
        pygame.draw.rect(surf, (150, 150, 150), (card['x'], card['y'], 200, 300))
        surf.blit(card['portrait'], (card['x'] + 50, card['y'] + 50))
        txt(surf, card['name'], card['x'] + 100, card['y'] + 260, 48, (0, 0, 0), center=True)
    return [pygame.Rect(card['x'], card['y'], 200, 300) for card in class_cards]

def draw_inventory(surf, player, selected):
    xbtn_rect = panel(surf, 10, 10, 400, 580, 'Inventory')
    slots = []
    eq_btn = btn(surf, 20, 600, 190, 30, 'Equip', (100, 100, 100), (255, 255, 255), 24)
    drop_btn = btn(surf, 230, 600, 170, 30, 'Drop', (100, 100, 100), (255, 255, 255), 24)
    for i, item in enumerate(player.inventory):
        rect = pygame.draw.rect(surf, (200, 200, 200) if i == selected else (150, 150, 150), (20 + (i % 8) * 45, 60 + (i // 8) * 45, 40, 40))
        txt(surf, item.name[:3], rect.centerx, rect.centery, 24, (0, 0, 0), center=True)
        slots.append(rect)
    return xbtn_rect, slots, eq_btn, drop_btn

def draw_quest_log(surf, player):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Quest Log')
    for i, quest in enumerate(player.quests):
        txt(surf, f'{quest.name}: {quest.description}', 20, 60 + i * 40, 24, (255, 255, 255))
    return xbtn_rect

def draw_shop(surf, npc, player, selected):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Shop')
    buy_btns = []
    items = []
    for i, item in enumerate(npc.inventory):
        rect = pygame.draw.rect(surf, (200, 200, 200) if i == selected else (150, 150, 150), (20 + (i % 8) * 45, 60 + (i // 8) * 45, 40, 40))
        txt(surf, f'{item.name}: {item.price}', rect.centerx, rect.centery - 10, 18, (0, 0, 0), center=True)
        buy_btn = btn(surf, rect.right + 10, rect.top, 50, 30, 'Buy', (100, 100, 100), (255, 255, 255), 18)
        items.append(rect)
        buy_btns.append(buy_btn)
    return xbtn_rect, buy_btns, items

def draw_crafting(surf, player, tab, selected, recipes):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'Crafting')
    tab_btns = []
    craft_btns = []
    for i, t in enumerate(['Weapons', 'Armor', 'Potions']):
        tab_btn = btn(surf, 20 + i * 150, 60, 140, 30, t, (100, 100, 100) if i == tab else (150, 150, 150), (255, 255, 255), 24)
        tab_btns.append(tab_btn)
    for i, recipe in enumerate(recipes[tab]):
        rect = pygame.draw.rect(surf, (200, 200, 200) if i == selected else (150, 150, 150), (20 + (i % 8) * 45, 120 + (i // 8) * 45, 40, 40))
        txt(surf, recipe.name[:3], rect.centerx, rect.centery, 24, (0, 0, 0), center=True)
        craft_btn = btn(surf, rect.right + 10, rect.top, 60, 30, 'Craft', (100, 100, 100), (255, 255, 255), 18)
        craft_btns.append(craft_btn)
    return xbtn_rect, tab_btns, craft_btns

def draw_dialogue(surf, npc, dial_idx):
    xbtn_rect = panel(surf, 10, 10, 600, 300, 'Dialogue')
    txt(surf, npc.dialogues[dial_idx], 20, 50, 24, (255, 255, 255))
    opt_btns = []
    for i, option in enumerate(npc.options[dial_idx]):
        opt_btn = btn(surf, 20 + i * 160, 230, 150, 40, option['text'], (100, 100, 100), (255, 255, 255), 24)
        opt_btns.append(opt_btn)
    return xbtn_rect, opt_btns

def draw_pause(surf):
    surf.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
    panel(surf, surf.get_width() // 3, surf.get_height() // 4, 400, 300, 'Paused')
    resume_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Resume', (100, 100, 100), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Quit', (100, 100, 100), (255, 255, 255), 36)
    return [resume_btn, quit_btn]

def draw_city_panel(surf, place_type, BUILDING_TYPES):
    xbtn_rect = panel(surf, 10, 10, 400, 580, f'{place_type} Panel')
    type_btns = []
    for i, building in enumerate(BUILDING_TYPES):
        btn_rect = btn(surf, 20 + (i % 3) * 120, 60 + (i // 3) * 50, 100, 40, building['name'], (100, 100, 100), (255, 255, 255), 24)
        type_btns.append(btn_rect)
    return xbtn_rect, type_btns

def draw_world_map(surf, player, TOWNS, CITIES, WORLD_MAP, BIOME_COL):
    xbtn_rect = panel(surf, 10, 10, 600, 580, 'World Map')
    for town in TOWNS:
        pygame.draw.rect(surf, (255, 255, 0), (town.x - 3, town.y - 3, 6, 6))
    for city in CITIES:
        pygame.draw.rect(surf, (0, 255, 255), (city.x - 4, city.y - 4, 8, 8))
    return xbtn_rect

def draw_game_over(surf):
    surf.fill((0, 0, 0))
    panel(surf, surf.get_width() // 3, surf.get_height() // 4, 400, 200, 'Game Over')
    restart_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2, 200, 50, 'Restart', (100, 100, 100), (255, 255, 255), 36)
    quit_btn = btn(surf, surf.get_width() // 2 - 100, surf.get_height() // 2 + 70, 200, 50, 'Quit', (100, 100, 100), (255, 255, 255), 36)
    return [restart_btn, quit_btn]

# ── QUEST MODULE ─────────────────────────────────────────────────────────────

WORLD_MAP = {}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
ENEMY_DEFS = {}
NPC_NAMES = []
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']
PLAYER_QUESTS = []

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Bandit', 'position': camp['position'], **ENEMY_DEFS['Bandit']})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'name': 'Goblin', 'position': camp['position'], **ENEMY_DEFS['Goblin']})
        enemies.append({'name': 'Orc', 'position': camp['position'], **ENEMY_DEFS['Orc']})

    wild_positions = [pos for pos, tile in WORLD_MAP.items() if tile not in ['Town', 'City', 'Water']]
    random.shuffle(wild_positions)
    for _ in range(30):
        position = wild_positions.pop()
        enemy_type = random.choice(['Goblin', 'Bandit'])
        enemies.append({'name': enemy_type, 'position': position, **ENEMY_DEFS[enemy_type]})

    for town in TOWNS:
        buildings.append({'type': 'Town', 'position': town['position']})
        npc_positions = [pos for pos, tile in WORLD_MAP.items() if tile == 'Town' and pos != town['position']]
        random.shuffle(npc_positions)
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            position = npc_positions.pop()
            name = random.choice(NPC_NAMES)
            npcs.append({'name': name, 'job': job, 'position': position})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'kill' and quest['target'] == enemy_name and not quest['completed']:
            quest['progress'] += 1
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def check_item_quests(player, item_name, qty):
    for quest in PLAYER_QUESTS:
        if quest['type'] == 'item' and quest['target'] == item_name and not quest['completed']:
            quest['progress'] += qty
            if quest['progress'] >= quest['required']:
                quest['completed'] = True

def complete_ready_quests(player):
    completed_quests = []
    for quest in PLAYER_QUESTS:
        if quest['completed']:
            player['gold'] += quest.get('reward', 0)
            completed_quests.append(quest['name'])
    PLAYER_QUESTS[:] = [quest for quest in PLAYER_QUESTS if not quest['completed']]
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    position = player['position']
    tile_type = WORLD_MAP.get(position)
    if tile_type == 'Forest':
        return 'Chopped wood'
    elif tile_type == 'Mountain':
        return 'Mined ore'
    elif tile_type == 'Field':
        return 'Gathered crops'
    else:
        return 'Nothing to harvest'

# ── ECONOMY MODULE ───────────────────────────────────────────────────────────
# TestRPG Economy and Crafting Module

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron': 1, 'Wood': 1}, 'out': {'Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron': 5, 'Coal': 2}, 'out': {'Sword': 1}},
        {'name': 'Steel Armor', 'cost': {'Steel': 8, 'Leather': 3}, 'out': {'Armor': 1}},
        {'name': 'Axe', 'cost': {'Iron': 4, 'Wood': 2}, 'out': {'Axe': 1}},
        {'name': 'Shield', 'cost': {'Wood': 5, 'Leather': 3}, 'out': {'Shield': 1}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 2, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Mana Potion', 'cost': {'Crystal': 1, 'Water': 1}, 'out': {'Potion': 1}},
        {'name': 'Poison', 'cost': {'Venom': 2, 'Herb': 1}, 'out': {'Poison': 1}},
        {'name': 'Fire Potion', 'cost': {'Sulfur': 3, 'Water': 1}, 'out': {'Potion': 1}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 20, 'Stone': 15}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 30, 'Iron': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Steel': 25, 'Stone': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 15, 'Soil': 30}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 228, 196), 'w': 4, 'h': 4, 'cost': {'Wood': 20, 'Stone': 15}},
    'Shop': {'col': (238, 232, 170), 'w': 5, 'h': 5, 'cost': {'Wood': 30, 'Iron': 10}},
    'Barracks': {'col': (196, 228, 255), 'w': 6, 'h': 6, 'cost': {'Steel': 25, 'Stone': 20}},
    'Farm': {'col': (173, 255, 47), 'w': 5, 'h': 5, 'cost': {'Wood': 15, 'Soil': 30}},
    'Tower': {'col': (169, 169, 169), 'w': 8, 'h': 8, 'cost': {'Steel': 40, 'Stone': 30}},
    'Warehouse': {'col': (255, 228, 181), 'w': 7, 'h': 7, 'cost': {'Wood': 40, 'Iron': 20}}
}

def buy_item(player, npc, item_name):
    if item_name in npc.inventory and player.gold >= npc.prices[item_name]:
        player.gold -= npc.prices[item_name]
        player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
        npc.inventory[item_name] -= 1
        return True, 'Item bought successfully'
    else:
        return False, 'Not enough gold or item not available'

def sell_item(player, npc, item_name):
    if item_name in player.inventory and player.inventory[item_name] > 0:
        player.gold += npc.prices[item_name]
        player.inventory[item_name] -= 1
        npc.inventory[item_name] = npc.inventory.get(item_name, 0) + 1
        return True, 'Item sold successfully'
    else:
        return False, 'Item not in inventory'

def craft_item(player, recipe):
    if all(player.inventory.get(mat, 0) >= qty for mat, qty in recipe['cost'].items()):
        for mat, qty in recipe['cost'].items():
            player.inventory[mat] -= qty
        for item, qty in recipe['out'].items():
            player.inventory[item] = player.inventory.get(item, 0) + qty
        return True, 'Item crafted successfully'
    else:
        return False, 'Not enough materials'

# ── FALLBACK DEFINITIONS (only used if agents returned nothing) ──────────────

# --- Fallback: World ---
if 'WORLD_MAP' not in dir():
    _W, _H = 200, 200
    _BIOMES = ["GRASS","GRASS","GRASS","FOREST","FOREST","MOUNTAIN","WATER","DESERT","SNOW","SWAMP"]
    WORLD_MAP = [[random.choice(_BIOMES) for _ in range(_W)] for _ in range(_H)]
    BIOME_COL = {
        "GRASS":   (80, 160, 60),
        "FOREST":  (30, 100, 30),
        "MOUNTAIN":(120,120,120),
        "WATER":   (40,  80,200),
        "DESERT":  (210,190,100),
        "SNOW":    (230,240,255),
        "SWAMP":   (60, 100, 60),
        "DIRT":    (160,130, 80),
        "ROAD":    (180,160,120),
        "TOWN":    (200,180,140),
    }
    TOWNS  = [(20,20,"Stonehaven"),(60,40,"Rivergate"),(100,80,"Duskmill")]
    CITIES = [(30,30,"Iron City"),(80,60,"Ashport")]
    BANDIT_CAMPS = [(45,55),(90,30),(130,70)]
    GOBLIN_CAMPS = [(25,75),(70,90),(110,50)]
    MINES  = [(35,45),(85,65)]
    WOODCUTS = [(50,50),(95,75)]
    def gen_world():
        global WORLD_MAP
        for ty in range(_H):
            for tx in range(_W):
                WORLD_MAP[ty][tx] = random.choice(_BIOMES)
        for tx,ty,_ in TOWNS:
            for dy in range(-2,3):
                for dx in range(-2,3):
                    ny,nx = ty+dy, tx+dx
                    if 0<=ny<_H and 0<=nx<_W:
                        WORLD_MAP[ny][nx] = "TOWN"
    def draw_world(surf, cam_x, cam_y):
        T = 32
        sx,sy = surf.get_size()
        tiles_x = sx//T + 2
        tiles_y = sy//T + 2
        start_tx = max(0, int(cam_x)//T)
        start_ty = max(0, int(cam_y)//T)
        for row in range(tiles_y):
            for col in range(tiles_x):
                tx = start_tx + col
                ty = start_ty + row
                if 0<=ty<_H and 0<=tx<_W:
                    biome = WORLD_MAP[ty][tx]
                    col_rgb = BIOME_COL.get(biome, (100,100,100))
                    px = col*T - int(cam_x)%T
                    py = row*T - int(cam_y)%T
                    pygame.draw.rect(surf, col_rgb, (px, py, T, T))
                    pygame.draw.rect(surf, (0,0,0,30), (px, py, T, T), 1)
    def get_tile(tx, ty):
        if 0<=ty<_H and 0<=tx<_W:
            return WORLD_MAP[ty][tx]
        return "WATER"

# --- Fallback: Entity / Player / Enemy / NPC ---
if 'Player' not in dir():
    TILE = 32
    class Entity:
        def __init__(self):
            self.x = self.y = 100.0
            self.col = (200,200,200)
            self.w = self.h = 28
        def draw(self, surf, cam_x, cam_y):
            sx = int(self.x - cam_x)
            sy = int(self.y - cam_y)
            # Head (circle)
            pygame.draw.circle(surf, self.col, (sx+14, sy+8), 9)
            # Eyes
            pygame.draw.circle(surf, (255,255,255), (sx+10, sy+7), 3)
            pygame.draw.circle(surf, (255,255,255), (sx+18, sy+7), 3)
            pygame.draw.circle(surf, (30,30,30),   (sx+10, sy+7), 1)
            pygame.draw.circle(surf, (30,30,30),   (sx+18, sy+7), 1)
            # Body
            pygame.draw.rect(surf, self.col, (sx+8, sy+17, 12, 13))
            # Arms
            pygame.draw.line(surf, self.col, (sx+8,  sy+19), (sx+2,  sy+28), 3)
            pygame.draw.line(surf, self.col, (sx+20, sy+19), (sx+26, sy+28), 3)
            # Legs
            pygame.draw.line(surf, self.col, (sx+11, sy+30), (sx+8,  sy+42), 3)
            pygame.draw.line(surf, self.col, (sx+17, sy+30), (sx+20, sy+42), 3)

    class Player(Entity):
        def __init__(self, cls="Warrior"):
            super().__init__()
            self.cls = cls
            self.name = "Hero"
            self.col = (100, 160, 240)
            self.x = self.y = 512.0
            self.hp = self.max_hp = 100
            self.mp = self.max_mp = 60
            self.sta = self.max_sta = 80
            self.gold = 50
            self.level = 1
            self.xp = 0
            self.xp_next = 100
            self.atk = 10
            self.defense = 5
            self.spd = 180
            self.inventory = {}
            self.equipped = {"weapon": None, "armor": None}
            self.spells = []
            self.active_quests = {}
            self.completed_quests = []
            self.kills = {}
            self.current_spell = 0
            self.alive = True
            self.sprint = False
            self.crouch = False
            self.regen_timer = 0.0
            self.attack_cooldown = 0.0
            self.float_texts = []
            self.vx = self.vy = 0.0
            bases = {
                "Warrior":  dict(hp=130, mp=30,  sta=100, atk=14, defense=8,  col=(200, 80, 80)),
                "Mage":     dict(hp=70,  mp=120, sta=60,  atk=8,  defense=3,  col=(80,  80, 200)),
                "Rogue":    dict(hp=90,  mp=50,  sta=90,  atk=12, defense=5,  col=(80,  180, 80)),
                "Ranger":   dict(hp=100, mp=60,  sta=80,  atk=11, defense=6,  col=(160, 120, 40)),
                "Paladin":  dict(hp=120, mp=70,  sta=90,  atk=13, defense=10, col=(230, 200, 60)),
            }
            b = bases.get(cls, bases["Warrior"])
            for k,v in b.items():
                setattr(self, k, v)
                if k in ("hp","mp","sta"):
                    setattr(self, "max_"+k, v)
        def atk_power(self):
            bonus = 0
            if self.equipped.get("weapon"):
                w = next((x for x in WEAPONS if x["name"]==self.equipped["weapon"]), None)
                if w: bonus = w.get("atk", 0)
            return self.atk + bonus
        def def_power(self):
            bonus = 0
            if self.equipped.get("armor"):
                a = next((x for x in ARMOR_SETS if x["name"]==self.equipped["armor"]), None)
                if a: bonus = a.get("def", 0)
            return self.defense + bonus
        def gain_xp(self, amount):
            self.xp += amount
            while self.xp >= self.xp_next:
                self.xp -= self.xp_next
                self.level += 1
                self.xp_next = int(self.xp_next * 1.4)
                self.max_hp  += 10; self.hp  = self.max_hp
                self.max_mp  += 5;  self.mp  = self.max_mp
                self.atk     += 2
                self.defense += 1
                self.float_texts.append(("LEVEL UP! " + str(self.level), (255,220,0)))
        def add_item(self, name, qty=1):
            self.inventory[name] = self.inventory.get(name, 0) + qty
        def regen(self, dt):
            self.regen_timer += dt
            if self.regen_timer >= 3.0:
                self.regen_timer = 0.0
                if self.hp < self.max_hp: self.hp = min(self.max_hp, self.hp + 2)
                if self.mp < self.max_mp: self.mp = min(self.max_mp, self.mp + 3)
                if self.sta < self.max_sta: self.sta = min(self.max_sta, self.sta + 5)

    class Enemy(Entity):
        def __init__(self, name="Goblin", x=200, y=200):
            super().__init__()
            defs = {d["name"]:d for d in ENEMY_DEFS} if 'ENEMY_DEFS' in dir() else {}
            d = defs.get(name, {"hp":30,"atk":6,"defense":2,"xp_val":15,"spd":70,"col":(180,60,60)})
            self.name   = name
            self.x      = float(x)
            self.y      = float(y)
            self.max_hp = d.get("hp", 30)
            self.hp     = self.max_hp
            self.atk    = d.get("atk", 6)
            self.defense= d.get("defense", 2)
            self.xp_val = d.get("xp_val", 15)
            self.spd    = d.get("spd", 70)
            self.col    = d.get("col", (180,60,60))
            self.alive  = True
            self.aggro  = False
            self.state  = "patrol"
            self.patrol_timer = 0.0
            self.patrol_dx  = random.uniform(-1,1)
            self.patrol_dy  = random.uniform(-1,1)
            self.gold_drop  = random.randint(1,8)
        def update(self, player, dt):
            if not self.alive: return
            dist = math.hypot(player.x - self.x, player.y - self.y)
            if dist < 220:
                self.aggro = True
            if dist > 400:
                self.aggro = False
            if self.aggro and dist > 30:
                dx = player.x - self.x
                dy = player.y - self.y
                d  = math.hypot(dx, dy) or 1
                self.x += (dx/d) * self.spd * dt
                self.y += (dy/d) * self.spd * dt
        def draw(self, surf, cam_x, cam_y):
            if not self.alive: return
            sx = int(self.x - cam_x)
            sy = int(self.y - cam_y)
            W,H = surf.get_size()
            if sx < -40 or sx > W+40 or sy < -40 or sy > H+40: return
            pygame.draw.rect(surf, self.col, (sx, sy, 28, 28))
            pygame.draw.circle(surf,(255,255,255),(sx+8,sy+8),4)
            pygame.draw.circle(surf,(255,255,255),(sx+20,sy+8),4)
            pygame.draw.circle(surf,(200,0,0),(sx+8,sy+8),2)
            pygame.draw.circle(surf,(200,0,0),(sx+20,sy+8),2)
            # HP bar
            if self.hp < self.max_hp:
                bw = 28
                ratio = max(0, self.hp/self.max_hp)
                pygame.draw.rect(surf,(60,0,0),(sx,sy-8,bw,5))
                pygame.draw.rect(surf,(220,30,30),(sx,sy-8,int(bw*ratio),5))

    class NPC(Entity):
        def __init__(self, name="Guard", x=300, y=300, job="Guard"):
            super().__init__()
            self.name = name
            self.x = float(x)
            self.y = float(y)
            self.job = job
            self.col = (200, 180, 100)
            self.shop_stock = {}
            self.dialogue = ["Hello, traveller.", "Safe travels.", "Watch yourself out there."]
            if job == "Merchant":
                self.col = (220, 160, 40)
                self.dialogue = ["Buy something or get out.", "Best prices in town!", "What'll it be?"]
            elif job == "Blacksmith":
                self.col = (160, 100, 60)
                self.dialogue = ["Need a weapon sharpened?", "Fine steel, made right here.", "Blades and armor — I do both."]

# --- Fallback: Items data ---
if 'WEAPONS' not in dir():
    WEAPONS = [
        {"name":"Iron Sword","atk":8,"type":"sword","val":30,"mat":"Iron","qty":1},
        {"name":"Steel Axe","atk":12,"type":"axe","val":55,"mat":"Steel","qty":1},
        {"name":"Shadow Dagger","atk":10,"type":"dagger","val":45,"mat":"Iron","qty":1},
        {"name":"Oak Bow","atk":9,"type":"bow","val":40,"mat":"Wood","qty":1},
        {"name":"Flame Staff","atk":14,"type":"staff","val":80,"mat":"Ash","qty":1},
        {"name":"Frost Wand","atk":11,"type":"wand","val":65,"mat":"Ice","qty":1},
        {"name":"Battle Hammer","atk":15,"type":"hammer","val":90,"mat":"Steel","qty":1},
        {"name":"Silver Spear","atk":13,"type":"spear","val":70,"mat":"Silver","qty":1},
        {"name":"Throwing Stars","atk":7,"type":"thrown","val":25,"mat":"Iron","qty":5},
        {"name":"Death Scythe","atk":18,"type":"scythe","val":150,"mat":"Obsidian","qty":1},
    ]
    ARMOR_SETS = [
        {"name":"Iron Set",  "def":6, "val":50, "mat":"Iron",    "parts":["Helmet","Chest","Legs","Boots"]},
        {"name":"Steel Set", "def":10,"val":100,"mat":"Steel",   "parts":["Helmet","Chest","Legs","Boots"]},
        {"name":"Shadow Set","def":8, "val":80, "mat":"Obsidian","parts":["Hood","Tunic","Pants","Shoes"]},
    ]
    SPELLS = [
        {"name":"Fireball",   "mp":15,"dmg":25,"col":(255,100,0),  "desc":"Hurls a ball of fire"},
        {"name":"Ice Spike",  "mp":12,"dmg":20,"col":(100,200,255),"desc":"Shoots an ice spike"},
        {"name":"Lightning",  "mp":18,"dmg":30,"col":(255,255,0),  "desc":"Calls down lightning"},
        {"name":"Heal",       "mp":20,"dmg":-30,"col":(0,255,100), "desc":"Restores 30 HP"},
        {"name":"Shield",     "mp":15,"dmg":0, "col":(100,100,255),"desc":"Blocks next hit"},
        {"name":"Teleport",   "mp":25,"dmg":0, "col":(200,0,255), "desc":"Blink forward"},
        {"name":"Summon Wolf","mp":30,"dmg":0, "col":(180,140,80),"desc":"Summons a wolf ally"},
        {"name":"Earthquake", "mp":35,"dmg":40,"col":(160,100,40),"desc":"Area damage around you"},
        {"name":"Drain Life", "mp":22,"dmg":20,"col":(100,0,100), "desc":"Steal HP from enemy"},
        {"name":"Time Slow",  "mp":40,"dmg":0, "col":(0,200,200),"desc":"Slows all enemies"},
    ]
    ENEMY_DEFS = [
        {"name":"Goblin",      "hp":30, "atk":6, "defense":2, "xp_val":15,"spd":80, "col":(80,160,60)},
        {"name":"Bandit",      "hp":50, "atk":10,"defense":4, "xp_val":25,"spd":75, "col":(160,100,60)},
        {"name":"Orc",         "hp":80, "atk":14,"defense":6, "xp_val":40,"spd":60, "col":(100,140,80)},
        {"name":"Skeleton",    "hp":40, "atk":9, "defense":3, "xp_val":20,"spd":65, "col":(220,220,200)},
        {"name":"Wolf",        "hp":35, "atk":8, "defense":2, "xp_val":18,"spd":100,"col":(120,100,80)},
        {"name":"Dark Mage",   "hp":55, "atk":16,"defense":3, "xp_val":50,"spd":55, "col":(80, 40,140)},
        {"name":"Troll",       "hp":120,"atk":18,"defense":8, "xp_val":70,"spd":45, "col":(100,140,60)},
        {"name":"Spider",      "hp":28, "atk":7, "defense":1, "xp_val":12,"spd":90, "col":(60, 30, 60)},
        {"name":"Dragon Spawn","hp":200,"atk":25,"defense":12,"xp_val":150,"spd":70,"col":(200,60, 30)},
        {"name":"Mimic",       "hp":60, "atk":13,"defense":5, "xp_val":60,"spd":50, "col":(180,140,60)},
    ]
    QUESTS = [
        {"id":"q1","name":"Goblin Problem","desc":"Kill 5 Goblins near Stonehaven",
         "target":"kill","enemy":"Goblin","need":5,"reward_gold":40,"reward_xp":80},
        {"id":"q2","name":"Iron Shortage","desc":"Collect 10 Iron Ore for the Blacksmith",
         "target":"item","item":"Iron Ore","need":10,"reward_gold":60,"reward_xp":50},
        {"id":"q3","name":"Bandit Raid","desc":"Eliminate 3 Bandits terrorizing the road",
         "target":"kill","enemy":"Bandit","need":3,"reward_gold":80,"reward_xp":100},
        {"id":"q4","name":"Merchant Supply","desc":"Gather 5 Wood for the Merchant",
         "target":"item","item":"Wood","need":5,"reward_gold":30,"reward_xp":40},
        {"id":"q5","name":"Dark Ruins","desc":"Slay the Dark Mage in the ruins",
         "target":"kill","enemy":"Dark Mage","need":1,"reward_gold":150,"reward_xp":200},
    ]
    FACTIONS = {"Warriors Guild":{"rep":0},"Thieves Guild":{"rep":0},"Mages Circle":{"rep":0}}
    DIALOGUE_TREES = {
        "Merchant":  ["Welcome! Buy or sell?","Got fresh stock today.","Come back anytime!"],
        "Guard":     ["Move along.","Keep the peace.","The city's safe on my watch."],
        "Blacksmith":["Need gear?","I can sharpen that.","Steel's the best."],
        "default":   ["Hello.","Nice weather.","Safe travels."],
    }
    MATERIALS = ["Iron Ore","Wood","Stone","Leather","Herb","Coal","Silver","Gold Ore","Obsidian","Crystal"]
    CRAFT_RECIPES = {
        "Iron Sword": {"Iron Ore":3,"Wood":1},
        "Steel Axe":  {"Iron Ore":5,"Coal":2},
        "Health Potion": {"Herb":3},
        "Arrows": {"Wood":2,"Iron Ore":1},
        "Torch": {"Wood":1,"Coal":1},
    }

# --- Fallback: Camera ---
if 'Camera' not in dir():
    class Camera:
        def __init__(self):
            self.x = self.y = 0.0
        def update(self, player, sw=1280, sh=720):
            tx = player.x - sw//2
            ty = player.y - sh//2
            self.x += (tx - self.x) * 0.12
            self.y += (ty - self.y) * 0.12

# --- Fallback: FloatText / Projectile / Building ---
if 'FloatText' not in dir():
    class FloatText:
        def __init__(self, text, x, y, col=(255,220,0)):
            self.text = text; self.x = x; self.y = y
            self.col  = col;  self.life = 1.8; self.vy = -40.0
        def update(self, dt):
            self.life -= dt
            self.y    += self.vy * dt
        def draw(self, surf, cam_x, cam_y):
            if self.life <= 0: return
            f = pygame.font.SysFont("Arial", 14, bold=True)
            alpha = max(0, min(255, int(self.life * 160)))
            s = f.render(self.text, True, self.col)
            s.set_alpha(alpha)
            surf.blit(s, (int(self.x - cam_x), int(self.y - cam_y)))
    class Projectile:
        def __init__(self, x, y, tx, ty, dmg=10, col=(255,100,0)):
            self.x = float(x); self.y = float(y)
            d = math.hypot(tx-x, ty-y) or 1
            spd = 320
            self.vx = (tx-x)/d*spd; self.vy = (ty-y)/d*spd
            self.dmg = dmg; self.col = col; self.alive = True; self.life = 2.0
        def update(self, dt):
            self.x += self.vx*dt; self.y += self.vy*dt
            self.life -= dt
            if self.life <= 0: self.alive = False
        def draw(self, surf, cam_x, cam_y):
            if not self.alive: return
            pygame.draw.circle(surf, self.col,
                (int(self.x - cam_x), int(self.y - cam_y)), 6)
    BTYPE_COLS = {"House":(160,130,100),"Shop":(200,160,80),"Barracks":(100,120,160),
                  "Farm":(160,200,80),"Tower":(130,130,150),"Warehouse":(170,140,110)}
    class Building:
        TYPES = {"House":{"w":64,"h":48},"Shop":{"w":72,"h":56},"Barracks":{"w":96,"h":64},
                 "Farm":{"w":80,"h":48},"Tower":{"w":48,"h":80},"Warehouse":{"w":80,"h":60}}
        def __init__(self, btype="House", tx=10, ty=10):
            self.btype = btype; self.tx = tx; self.ty = ty
            d = self.TYPES.get(btype, {"w":64,"h":48})
            self.w = d["w"]; self.h = d["h"]
            self.built = True
        def draw(self, surf, cam_x, cam_y):
            T = 32
            sx = self.tx*T - int(cam_x); sy = self.ty*T - int(cam_y)
            col = BTYPE_COLS.get(self.btype, (150,150,150))
            pygame.draw.rect(surf, col, (sx, sy, self.w, self.h))
            pygame.draw.rect(surf, (50,30,20), (sx, sy, self.w, self.h), 2)
            f = pygame.font.SysFont("Arial", 10)
            lbl = f.render(self.btype, True, (255,255,255))
            surf.blit(lbl, (sx+2, sy+2))

# --- Fallback: save / load ---
if 'save_game' not in dir():
    def save_game(player, buildings, filepath="save.json"):
        try:
            data = {
                "name":player.name,"cls":player.cls,"level":player.level,
                "hp":player.hp,"mp":player.mp,"sta":player.sta,"gold":player.gold,
                "xp":player.xp,"xp_next":player.xp_next,
                "atk":player.atk,"defense":player.defense,
                "x":player.x,"y":player.y,
                "inventory":player.inventory,"equipped":player.equipped,
                "active_quests":player.active_quests,
                "completed_quests":player.completed_quests,
                "buildings":[{"btype":b.btype,"tx":b.tx,"ty":b.ty} for b in buildings],
            }
            with open(filepath,"w") as f: json.dump(data,f,indent=2)
            return True
        except Exception: return False
    def load_game(player, buildings, filepath="save.json"):
        try:
            with open(filepath,"r") as f: data = json.load(f)
            for k in ("name","cls","level","hp","mp","sta","gold","xp","xp_next",
                      "atk","defense","x","y","inventory","equipped",
                      "active_quests","completed_quests"):
                if k in data: setattr(player, k, data[k])
            buildings.clear()
            for bd in data.get("buildings",[]):
                buildings.append(Building(bd["btype"],bd["tx"],bd["ty"]))
            return True
        except Exception: return False

# --- Fallback: spawn world entities ---
if 'spawn_world_entities' not in dir():
    def spawn_world_entities(world_map, towns, cities, bandit_camps, goblin_camps, enemy_defs, npc_names=None):
        enemies = []
        npcs    = []
        buildings = []
        T = 32
        npc_names = npc_names or ["Gareth","Mira","Torin","Elara","Bron","Sylva"]
        jobs = ["Merchant","Guard","Blacksmith","Farmer","Miner","Alchemist"]
        ei = 0
        for bx,by in bandit_camps:
            for _ in range(random.randint(3,6)):
                ex = bx*T + random.randint(-2,2)*T
                ey = by*T + random.randint(-2,2)*T
                enemies.append(Enemy("Bandit",ex,ey))
                ei+=1
        for gx,gy in goblin_camps:
            for _ in range(random.randint(4,7)):
                ex = gx*T + random.randint(-2,2)*T
                ey = gy*T + random.randint(-2,2)*T
                enemies.append(Enemy("Goblin",ex,ey))
        for tx,ty,tname in towns:
            for i,job in enumerate(jobs):
                nx = tx*T + (i%3)*40
                ny = ty*T + (i//3)*40
                name = random.choice(npc_names)
                npcs.append(NPC(name, nx, ny, job))
            for btype in ["House","House","Shop","Barracks"]:
                btx = tx + random.randint(-2,2)
                bty = ty + random.randint(-2,2)
                buildings.append(Building(btype, btx, bty))
        return enemies, npcs, buildings

# --- Fallback: quest helpers ---
if 'check_quest_kill' not in dir():
    def check_quest_kill(player, enemy_name):
        for qid, prog in player.active_quests.items():
            q = next((x for x in QUESTS if x["id"]==qid), None)
            if q and q.get("target")=="kill" and q.get("enemy")==enemy_name:
                player.active_quests[qid] = prog + 1
    def check_quest_item(player, item_name, qty):
        for qid, prog in player.active_quests.items():
            q = next((x for x in QUESTS if x["id"]==qid), None)
            if q and q.get("target")=="item" and q.get("item")==item_name:
                player.active_quests[qid] = prog + qty
    def complete_ready_quests(player):
        done = []
        for qid, prog in list(player.active_quests.items()):
            q = next((x for x in QUESTS if x["id"]==qid), None)
            if q and prog >= q.get("need",1):
                player.gold += q.get("reward_gold",0)
                player.gain_xp(q.get("reward_xp",0))
                del player.active_quests[qid]
                player.completed_quests.append(qid)
                done.append(q["name"])
        return done
    def harvest_nearby(player, world_map):
        T = 32
        tx, ty = int(player.x)//T, int(player.y)//T
        tile = get_tile(tx, ty)
        if tile == "FOREST":
            player.add_item("Wood", random.randint(1,3))
            return "Gathered Wood"
        elif tile == "MOUNTAIN":
            player.add_item("Iron Ore", random.randint(1,2))
            return "Gathered Iron Ore"
        elif tile == "GRASS":
            player.add_item("Herb", random.randint(1,2))
            return "Gathered Herb"
        elif tile == "SWAMP":
            player.add_item("Crystal", 1)
            return "Found Crystal"
        return "Nothing to harvest here"

# --- Fallback: economy ---
if 'buy_item' not in dir():
    def buy_item(player, npc, item_name):
        stock = npc.shop_stock
        if item_name not in stock: return False, "Not in stock"
        price = stock[item_name].get("price", 999)
        if player.gold < price: return False, "Not enough gold"
        player.gold -= price
        player.add_item(item_name, 1)
        return True, "Bought " + item_name
    def sell_item(player, npc, item_name):
        if player.inventory.get(item_name,0) <= 0: return False, "Don't have that"
        price = 5
        for w in WEAPONS:
            if w["name"]==item_name: price = w["val"]//2; break
        player.gold += price
        player.inventory[item_name] -= 1
        if player.inventory[item_name] <= 0: del player.inventory[item_name]
        return True, "Sold " + item_name + " for " + str(price) + "g"
    def craft_item(player, recipe_name):
        recipe = CRAFT_RECIPES.get(recipe_name)
        if not recipe: return False, "Unknown recipe"
        for mat, qty in recipe.items():
            if player.inventory.get(mat,0) < qty:
                return False, "Need " + str(qty) + " " + mat
        for mat, qty in recipe.items():
            player.inventory[mat] -= qty
        player.add_item(recipe_name, 1)
        return True, "Crafted " + recipe_name

# --- Fallback: UI ---
if 'draw_hud' not in dir():
    _FONT_CACHE = {}
    def font(size):
        if size not in _FONT_CACHE:
            _FONT_CACHE[size] = pygame.font.SysFont("Arial", size)
        return _FONT_CACHE[size]
    def txt(surf, text, x, y, size=16, col=(255,255,255), center=False):
        f = font(size)
        s = f.render(str(text), True, col)
        if center: x -= s.get_width()//2
        surf.blit(s, (x, y))
    def draw_bar(surf, x, y, w, h, val, mx, col, bg=(40,40,40)):
        pygame.draw.rect(surf, bg, (x, y, w, h))
        if mx > 0:
            ratio = max(0, min(1, val/mx))
            pygame.draw.rect(surf, col, (x, y, int(w*ratio), h))
        pygame.draw.rect(surf, (100,100,100), (x, y, w, h), 1)
    def draw_x_button(surf, rx, ry, rw, rh):
        bx = rx + rw - 24; by = ry + 4
        r = pygame.Rect(bx, by, 20, 20)
        pygame.draw.rect(surf, (160,40,40), r)
        pygame.draw.rect(surf, (220,80,80), r, 2)
        f = font(14)
        xs = f.render("X", True, (255,255,255))
        surf.blit(xs, (bx+6, by+3))
        return r
    def draw_panel(surf, rx, ry, rw, rh, title=""):
        pygame.draw.rect(surf, (30,30,45), (rx, ry, rw, rh))
        pygame.draw.rect(surf, (80,80,130), (rx, ry, rw, rh), 2)
        if title:
            txt(surf, title, rx+10, ry+8, 18, (200,200,255))
        return draw_x_button(surf, rx, ry, rw, rh)
    def draw_hud(surf, player):
        sw, sh = surf.get_size()
        # Bars
        draw_bar(surf, 10, sh-90, 200, 16, player.hp,  player.max_hp,  (200,40,40))
        draw_bar(surf, 10, sh-68, 200, 16, player.mp,  player.max_mp,  (40,80,200))
        draw_bar(surf, 10, sh-46, 200, 16, player.sta, player.max_sta, (40,180,60))
        txt(surf, "HP " + str(player.hp)+"/"+str(player.max_hp), 10, sh-92, 12, (255,180,180))
        txt(surf, "MP " + str(player.mp)+"/"+str(player.max_mp), 10, sh-70, 12, (160,200,255))
        txt(surf, "STA "+str(player.sta)+"/"+str(player.max_sta),10, sh-48, 12, (160,255,160))
        txt(surf, "Gold: " + str(player.gold),  10, sh-26, 14, (255,220,0))
        txt(surf, "Lv " + str(player.level) + "  " + player.cls, 220, sh-90, 14, (200,200,200))
        xp_pct = int(100 * player.xp / max(1, player.xp_next))
        txt(surf, "XP: " + str(player.xp)+"/"+str(player.xp_next)+" ("+str(xp_pct)+"%)",220, sh-72, 12, (180,220,180))
        weap = player.equipped.get("weapon","---")
        armor = player.equipped.get("armor","---")
        txt(surf, "W: " + (weap or "---"), 220, sh-52, 12, (220,200,160))
        txt(surf, "A: " + (armor or "---"), 220, sh-36, 12, (180,180,220))
        # Spell bar
        spells = player.spells or []
        for si, sp in enumerate(spells[:5]):
            sx2 = sw - 280 + si*56
            sy2 = sh - 60
            col = (60,60,80) if si != player.current_spell else (80,80,150)
            pygame.draw.rect(surf, col, (sx2, sy2, 48, 48))
            pygame.draw.rect(surf, (120,120,200), (sx2, sy2, 48, 48), 2)
            sdata = next((x for x in SPELLS if x["name"]==sp), None)
            scol = sdata["col"] if sdata else (200,200,200)
            pygame.draw.circle(surf, scol, (sx2+24, sy2+20), 12)
            txt(surf, sp[:6], sx2+2, sy2+34, 10, (200,200,200))
    def draw_minimap(surf, player, enemies):
        sw, sh = surf.get_size()
        ms = 120
        mx = sw - ms - 10; my = 10
        pygame.draw.rect(surf, (20,20,30), (mx, my, ms, ms))
        pygame.draw.rect(surf, (80,80,120), (mx, my, ms, ms), 2)
        T = 32
        scale = ms / (200*T)
        for e in enemies:
            if not e.alive: continue
            ex2 = int(e.x * scale) + mx
            ey2 = int(e.y * scale) + my
            if mx<=ex2<mx+ms and my<=ey2<my+ms:
                pygame.draw.circle(surf, (200,40,40), (ex2, ey2), 2)
        px2 = int(player.x * scale) + mx
        py2 = int(player.y * scale) + my
        px2 = max(mx, min(mx+ms-3, px2))
        py2 = max(my, min(my+ms-3, py2))
        pygame.draw.circle(surf, (100,200,255), (px2, py2), 4)
    def draw_inventory(surf, player, selected=0):
        W,H = surf.get_size()
        rx,ry,rw,rh = W//4, H//8, W//2, H*3//4
        xbtn = draw_panel(surf, rx, ry, rw, rh, "INVENTORY")
        items = list(player.inventory.items())
        slot_btns = []
        for i,(name,qty) in enumerate(items):
            iy = ry+40+i*28
            if iy > ry+rh-80: break
            col = (80,100,140) if i==selected else (50,50,70)
            r = pygame.Rect(rx+10, iy, rw-20, 24)
            pygame.draw.rect(surf, col, r)
            txt(surf, name + "  x"+str(qty), rx+15, iy+4, 14, (220,220,220))
            slot_btns.append(r)
        eby = ry+rh-64
        equip_btn = pygame.Rect(rx+10, eby, 100, 28)
        drop_btn  = pygame.Rect(rx+120,eby, 100, 28)
        pygame.draw.rect(surf,(60,100,60),equip_btn)
        pygame.draw.rect(surf,(100,60,60),drop_btn)
        txt(surf,"Equip",rx+28,eby+6,14,(200,255,200))
        txt(surf,"Drop",rx+140,eby+6,14,(255,200,200))
        return xbtn, slot_btns, equip_btn, drop_btn
    def draw_quest_log(surf, player):
        W,H = surf.get_size()
        rx,ry,rw,rh = W//4, H//8, W//2, H*3//4
        xbtn = draw_panel(surf, rx, ry, rw, rh, "QUEST LOG")
        y = ry+40
        for qid,prog in player.active_quests.items():
            q = next((x for x in QUESTS if x["id"]==qid), None)
            if not q: continue
            txt(surf, q["name"], rx+14, y, 15, (255,220,80)); y+=20
            txt(surf, q["desc"], rx+18, y, 12, (180,180,180)); y+=16
            txt(surf, "Progress: "+str(prog)+"/"+str(q.get("need",1)), rx+18, y, 12,(100,220,100)); y+=22
        if not player.active_quests:
            txt(surf, "No active quests. Talk to NPCs!", rx+14, y, 14, (160,160,160))
        return xbtn
    def draw_dialogue(surf, npc, dial_idx=0):
        W,H = surf.get_size()
        rx,ry,rw,rh = W//6, H*2//3, W*2//3, H//4
        xbtn = draw_panel(surf, rx, ry, rw, rh, npc.name+" ("+npc.job+")")
        lines = npc.dialogue
        line = lines[dial_idx % len(lines)] if lines else "..."
        txt(surf, line, rx+14, ry+36, 15, (220,220,200))
        btns = []
        if any(q.get("id") not in player_ref.active_quests and q.get("id") not in player_ref.completed_quests
               for q in QUESTS) if 'player_ref' in dir() else False:
            rb = pygame.Rect(rx+14, ry+rh-36, 120, 24)
            pygame.draw.rect(surf,(60,100,60),rb)
            txt(surf,"Accept Quest",rx+18,ry+rh-32,12,(200,255,200))
            btns.append(("accept",rb))
        nb = pygame.Rect(rx+rw-110, ry+rh-36, 90, 24)
        pygame.draw.rect(surf,(60,60,100),nb)
        txt(surf,"Next",rx+rw-90,ry+rh-32,14,(200,200,255))
        btns.append(("next",nb))
        return xbtn, btns
    def draw_shop(surf, npc, player, selected=0):
        W,H = surf.get_size()
        rx,ry,rw,rh = W//5, H//8, W*3//5, H*3//4
        xbtn = draw_panel(surf, rx, ry, rw, rh, npc.name+"'s Shop")
        txt(surf,"Gold: "+str(player.gold), rx+14, ry+36, 14, (255,220,0))
        items = list(npc.shop_stock.items())
        buy_btns=[]
        for i,(name,info) in enumerate(items):
            iy = ry+60+i*30
            if iy > ry+rh-60: break
            r = pygame.Rect(rx+10,iy,rw-20,26)
            pygame.draw.rect(surf,(50+(i==selected)*30,50,70),r)
            txt(surf,name+"   "+str(info.get("price",0))+"g",rx+14,iy+5,13,(220,220,200))
            bb = pygame.Rect(rx+rw-80,iy+2,68,22)
            pygame.draw.rect(surf,(60,100,60),bb)
            txt(surf,"Buy",rx+rw-64,iy+5,13,(200,255,200))
            buy_btns.append((name,bb))
        return xbtn, buy_btns, items
    def draw_pause(surf):
        W,H = surf.get_size()
        overlay = pygame.Surface((W,H), pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        surf.blit(overlay,(0,0))
        rx,ry,rw,rh = W//3, H//4, W//3, H//2
        xbtn = draw_panel(surf, rx, ry, rw, rh, "PAUSED")
        labels=["Resume","Save Game","Load Game","Settings","Quit"]
        btns={}
        for i,lbl in enumerate(labels):
            by2 = ry+50+i*52
            r = pygame.Rect(rx+30, by2, rw-60, 40)
            pygame.draw.rect(surf,(60,60,90),r)
            pygame.draw.rect(surf,(100,100,160),r,2)
            txt(surf, lbl, rx+rw//2, by2+10, 16, (220,220,255), center=True)
            btns[lbl.lower().replace(" ","_")] = r
        return xbtn, btns
    def draw_main_menu(surf):
        W,H = surf.get_size()
        surf.fill((10,10,20))
        for i in range(20):
            pygame.draw.circle(surf,(20,20,60),(random.randint(0,W),random.randint(0,H)),random.randint(1,3))
        txt(surf, "TestRPG", W//2, H//5, 48, (180,120,255), center=True)
        txt(surf, "An Umbra-Generated RPG", W//2, H//5+55, 18, (120,100,180), center=True)
        lbls = ["New Game","Continue","Quit"]
        btns = {}
        for i,lbl in enumerate(lbls):
            by = H//2+i*70
            r = pygame.Rect(W//2-120, by, 240, 50)
            pygame.draw.rect(surf,(40,30,60),r)
            pygame.draw.rect(surf,(130,80,200),r,2)
            txt(surf, lbl, W//2, by+14, 20, (220,200,255), center=True)
            btns[lbl.lower().replace(" ","_")] = r
        return btns
    def draw_class_select(surf):
        W,H = surf.get_size()
        surf.fill((10,10,20))
        txt(surf,"Choose Your Class",W//2,60,36,(200,180,255),center=True)
        classes = [
            ("Warrior","Strong melee fighter",(200,80,80)),
            ("Mage","Powerful spell caster",(80,80,200)),
            ("Rogue","Fast and stealthy",(80,180,80)),
            ("Ranger","Ranged bow master",(160,120,40)),
            ("Paladin","Holy warrior",(230,200,60)),
        ]
        btns={}
        for i,(cls,desc,col) in enumerate(classes):
            bx = W//2-200+i*100; by=H//3
            r = pygame.Rect(bx-35, by, 80, 100)
            pygame.draw.rect(surf,col,r)
            pygame.draw.rect(surf,(200,200,200),r,2)
            txt(surf,cls,bx,by+105,13,(220,220,255),center=True)
            txt(surf,desc,bx,by+120,10,(160,160,200),center=True)
            btns[cls]=r
        return btns
    def draw_crafting(surf, player, tab="Blacksmith", selected=0):
        W,H = surf.get_size()
        rx,ry,rw,rh = W//4, H//8, W//2, H*3//4
        xbtn = draw_panel(surf, rx, ry, rw, rh, "CRAFTING — "+tab)
        tabs=["Blacksmith","Alchemy","Fletcher"]
        tab_btns=[]
        for i,t in enumerate(tabs):
            r=pygame.Rect(rx+10+i*110,ry+32,100,24)
            col=(70,70,110) if t==tab else (40,40,70)
            pygame.draw.rect(surf,col,r)
            txt(surf,t,r.x+10,r.y+5,12,(200,200,255))
            tab_btns.append((t,r))
        recipes=[k for k in CRAFT_RECIPES]
        craft_btns=[]
        for i,name in enumerate(recipes):
            iy=ry+70+i*30
            if iy>ry+rh-50: break
            r=pygame.Rect(rx+10,iy,rw-20,26)
            col=(80,100,80) if i==selected else (50,65,50)
            pygame.draw.rect(surf,col,r)
            mats=CRAFT_RECIPES[name]
            mat_str=", ".join(str(q)+" "+m for m,q in mats.items())
            txt(surf,name+" ("+mat_str+")",rx+14,iy+5,12,(200,220,200))
            cb=pygame.Rect(rx+rw-80,iy+2,68,22)
            pygame.draw.rect(surf,(60,90,60),cb)
            txt(surf,"Craft",rx+rw-68,iy+5,12,(180,255,180))
            craft_btns.append((name,cb))
        return xbtn, tab_btns, craft_btns
    def draw_city_build(surf, player, buildings, place_type="House"):
        W,H = surf.get_size()
        rx,ry,rw,rh = 0, H-130, W, 130
        pygame.draw.rect(surf,(20,20,35),(rx,ry,rw,rh))
        pygame.draw.rect(surf,(60,60,100),(rx,ry,rw,rh),2)
        txt(surf,"CITY BUILDER — Gold: "+str(player.gold)+"g",rx+10,ry+8,14,(255,220,0))
        btypes=list(Building.TYPES.keys())
        type_btns=[]
        for i,bt in enumerate(btypes):
            r=pygame.Rect(rx+10+i*110, ry+34, 100, 40)
            col=(60,80,110) if bt==place_type else (40,50,70)
            pygame.draw.rect(surf,col,r)
            pygame.draw.rect(surf,(80,100,160),r,2)
            txt(surf,bt,r.x+10,r.y+12,13,(200,220,255))
            type_btns.append((bt,r))
        xbtn=draw_x_button(surf,rx,ry,rw,rh)
        return xbtn, type_btns
    def draw_world_map(surf, player, towns, cities):
        W,H=surf.get_size()
        rx,ry,rw,rh=W//8,H//8,W*3//4,H*3//4
        xbtn=draw_panel(surf,rx,ry,rw,rh,"WORLD MAP")
        T=32
        scale=min(rw,rh)/(200*T)*0.9
        for tx2,ty2,name in towns:
            sx2=int(tx2*T*scale)+rx+20
            sy2=int(ty2*T*scale)+ry+40
            pygame.draw.circle(surf,(200,180,100),(sx2,sy2),6)
            txt(surf,name,sx2+8,sy2-6,10,(220,200,160))
        for tx2,ty2,name in cities:
            sx2=int(tx2*T*scale)+rx+20
            sy2=int(ty2*T*scale)+ry+40
            pygame.draw.circle(surf,(255,220,80),(sx2,sy2),9)
            txt(surf,name,sx2+10,sy2-8,11,(255,230,100))
        px2=int(player.x*scale)+rx+20
        py2=int(player.y*scale)+ry+40
        pygame.draw.circle(surf,(100,200,255),(px2,py2),5)
        txt(surf,"You",px2+6,py2-6,10,(100,200,255))
        return xbtn
    def draw_gameover(surf):
        W,H=surf.get_size()
        overlay=pygame.Surface((W,H),pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        surf.blit(overlay,(0,0))
        txt(surf,"GAME OVER",W//2,H//3,64,(220,40,40),center=True)
        txt(surf,"Press R to restart or ESC to quit",W//2,H//2,18,(180,180,180),center=True)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GAME
# ═══════════════════════════════════════════════════════════════════════════

GAME_TITLE  = "TestRPG"
SAVE_PATH   = "testrpg_save.json"
SCREEN_W    = 1280
SCREEN_H    = 720
FPS         = 60

# Game states
ST_MENU        = "MENU"
ST_CLASS       = "CLASS_SELECT"
ST_PLAY        = "PLAY"
ST_INVENTORY   = "INVENTORY"
ST_QUEST       = "QUEST"
ST_DIALOGUE    = "DIALOGUE"
ST_SHOP        = "SHOP"
ST_CRAFT       = "CRAFTING"
ST_PAUSE       = "PAUSE"
ST_CITY        = "CITY_BUILD"
ST_MAP         = "WORLD_MAP"
ST_GAMEOVER    = "GAME_OVER"

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption(GAME_TITLE)
clock  = pygame.time.Clock()

def main():
    global player_ref

    # ─── World generation ────────────────────────────────────────────────
    if 'gen_world' in dir():
        gen_world()

    player    = Player("Warrior")
    player_ref = player   # used by draw_dialogue for quest acceptance
    camera    = Camera()

    enemies, npcs, buildings = spawn_world_entities(
        WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS
    )

    # Give all NPCs shop stock
    for npc in npcs:
        if npc.job == "Merchant":
            npc.shop_stock = {w["name"]:{"price":w["val"],"qty":10} for w in WEAPONS[:5]}
        elif npc.job == "Blacksmith":
            npc.shop_stock = {a["name"]:{"price":100,"qty":3} for a in ARMOR_SETS}
            npc.shop_stock.update({w["name"]:{"price":w["val"],"qty":5} for w in WEAPONS[5:]})

    # Accept first quest automatically so log isn't empty
    if QUESTS:
        player.active_quests[QUESTS[0]["id"]] = 0

    projectiles   = []
    float_texts   = []
    state         = ST_MENU
    sel_inv       = 0
    sel_shop      = 0
    sel_craft     = 0
    craft_tab     = "Blacksmith"
    active_npc    = None
    dial_idx      = 0
    place_type    = "House"
    attack_flash  = 0.0
    notification  = ""
    notif_timer   = 0.0
    keys_held     = set()
    running       = True
    dt            = 0.0

    def notify(msg, dur=2.5):
        nonlocal notification, notif_timer
        notification = msg
        notif_timer  = dur

    def add_float(text, x, y, col=(255,220,0)):
        float_texts.append(FloatText(text, x, y, col))

    def attack_nearest():
        nonlocal attack_flash
        if player.attack_cooldown > 0: return
        player.attack_cooldown = 0.5
        attack_flash = 0.15
        best = None; bd = 180
        for e in enemies:
            if not e.alive: continue
            d = math.hypot(e.x - player.x, e.y - player.y)
            if d < bd:
                bd = d; best = e
        if best:
            dmg = max(1, player.atk_power() - best.defense + random.randint(-2,3))
            best.hp -= dmg
            add_float("-"+str(dmg), best.x, best.y-20, (255,80,80))
            if best.hp <= 0:
                best.alive = False
                check_quest_kill(player, best.name)
                done = complete_ready_quests(player)
                for qn in done:
                    notify("Quest Complete: " + qn)
                player.gain_xp(best.xp_val)
                player.gold += best.gold_drop
                add_float("+"+str(best.xp_val)+"xp", player.x, player.y-40, (100,255,100))
                add_float("+"+str(best.gold_drop)+"g", player.x, player.y-60, (255,220,0))

    def cast_spell(mx, my):
        if not player.spells: return
        spell_name = player.spells[player.current_spell % len(player.spells)]
        sdata = next((x for x in SPELLS if x["name"]==spell_name), None)
        if not sdata: return
        if player.mp < sdata["mp"]:
            notify("Not enough MP!")
            return
        player.mp -= sdata["mp"]
        wx = mx + camera.x; wy = my + camera.y
        if sdata["dmg"] < 0:
            player.hp = min(player.max_hp, player.hp + abs(sdata["dmg"]))
            add_float("Heal +"+str(abs(sdata["dmg"])), player.x, player.y-30, (0,255,100))
        elif sdata["dmg"] > 0:
            proj = Projectile(player.x+14, player.y+14, wx, wy, sdata["dmg"], sdata["col"])
            projectiles.append(proj)
        notify(spell_name + " cast!")

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        # ─── Events ─────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                keys_held.add(event.key)

                if state == ST_MENU:
                    pass  # handled by mouse

                elif state == ST_PLAY:
                    if event.key == pygame.K_ESCAPE:
                        state = ST_PAUSE
                    elif event.key == pygame.K_i:
                        state = ST_INVENTORY; sel_inv = 0
                    elif event.key == pygame.K_q:
                        state = ST_QUEST
                    elif event.key == pygame.K_k:
                        state = ST_CRAFT; craft_tab = "Blacksmith"
                    elif event.key == pygame.K_b:
                        state = ST_CITY
                    elif event.key == pygame.K_m:
                        state = ST_MAP
                    elif event.key == pygame.K_e:
                        # Interact with nearest NPC
                        closest = None; cd = 80
                        for npc in npcs:
                            d = math.hypot(npc.x - player.x, npc.y - player.y)
                            if d < cd:
                                cd = d; closest = npc
                        if closest:
                            active_npc = closest; dial_idx = 0
                            state = ST_DIALOGUE
                    elif event.key == pygame.K_f:
                        harvest_result = harvest_nearby(player, WORLD_MAP)
                        notify(harvest_result)
                        check_quest_item(player, "Wood", player.inventory.get("Wood",0))
                        check_quest_item(player, "Iron Ore", player.inventory.get("Iron Ore",0))
                        done = complete_ready_quests(player)
                        for qn in done: notify("Quest Complete: " + qn)
                    elif event.key == pygame.K_SPACE:
                        attack_nearest()
                    elif event.key == pygame.K_TAB:
                        if player.spells:
                            player.current_spell = (player.current_spell+1) % len(player.spells)
                    elif event.key == pygame.K_F5:
                        if save_game(player, buildings, SAVE_PATH):
                            notify("Game Saved!")
                    elif event.key == pygame.K_F9:
                        if load_game(player, buildings, SAVE_PATH):
                            notify("Game Loaded!")
                    elif event.key == pygame.K_1:
                        player.equipped["weapon"] = WEAPONS[0]["name"]
                        notify("Equipped: " + WEAPONS[0]["name"])

                elif state == ST_INVENTORY:
                    items = list(player.inventory.items())
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                        state = ST_PLAY
                    elif event.key == pygame.K_DOWN:
                        sel_inv = min(sel_inv+1, max(0,len(items)-1))
                    elif event.key == pygame.K_UP:
                        sel_inv = max(0, sel_inv-1)
                    elif event.key == pygame.K_RETURN:
                        if items:
                            name,_ = items[sel_inv]
                            w = next((x for x in WEAPONS if x["name"]==name), None)
                            a = next((x for x in ARMOR_SETS if x["name"]==name), None)
                            if w:
                                player.equipped["weapon"] = name
                                notify("Equipped weapon: "+name)
                            elif a:
                                player.equipped["armor"] = name
                                notify("Equipped armor: "+name)
                            sp = next((x for x in SPELLS if x["name"]==name),None)
                            if sp and name not in player.spells:
                                player.spells.append(name)
                                notify("Learned spell: "+name)

                elif state == ST_QUEST:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        state = ST_PLAY

                elif state == ST_PAUSE:
                    if event.key == pygame.K_ESCAPE:
                        state = ST_PLAY

                elif state == ST_DIALOGUE:
                    if event.key == pygame.K_ESCAPE:
                        state = ST_PLAY
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if active_npc:
                            dial_idx += 1
                        if active_npc and active_npc.shop_stock:
                            state = ST_SHOP; sel_shop = 0

                elif state == ST_SHOP:
                    if event.key == pygame.K_ESCAPE:
                        state = ST_PLAY
                    elif event.key == pygame.K_DOWN:
                        sel_shop = min(sel_shop+1, max(0,len(active_npc.shop_stock)-1))
                    elif event.key == pygame.K_UP:
                        sel_shop = max(0, sel_shop-1)
                    elif event.key == pygame.K_RETURN:
                        if active_npc:
                            items_list = list(active_npc.shop_stock.keys())
                            if 0<=sel_shop<len(items_list):
                                ok,msg = buy_item(player, active_npc, items_list[sel_shop])
                                notify(msg)

                elif state == ST_CRAFT:
                    if event.key == pygame.K_ESCAPE:
                        state = ST_PLAY
                    elif event.key == pygame.K_DOWN:
                        sel_craft = min(sel_craft+1, max(0,len(CRAFT_RECIPES)-1))
                    elif event.key == pygame.K_UP:
                        sel_craft = max(0, sel_craft-1)
                    elif event.key == pygame.K_RETURN:
                        rnames = list(CRAFT_RECIPES.keys())
                        if 0<=sel_craft<len(rnames):
                            ok,msg = craft_item(player, rnames[sel_craft])
                            notify(msg)

                elif state == ST_CITY:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                        state = ST_PLAY

                elif state == ST_MAP:
                    if event.key in (pygame.K_ESCAPE, pygame.K_m):
                        state = ST_PLAY

                elif state == ST_GAMEOVER:
                    if event.key == pygame.K_r:
                        return main()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            elif event.type == pygame.KEYUP:
                keys_held.discard(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if state == ST_MENU:
                    btns = draw_main_menu(screen)  # get rects
                    if btns.get("new_game") and btns["new_game"].collidepoint(mx,my):
                        state = ST_CLASS
                    elif btns.get("continue") and btns["continue"].collidepoint(mx,my):
                        if os.path.exists(SAVE_PATH):
                            load_game(player, buildings, SAVE_PATH)
                            state = ST_PLAY
                            notify("Save loaded!")
                        else:
                            notify("No save file found.")
                    elif btns.get("quit") and btns["quit"].collidepoint(mx,my):
                        running = False

                elif state == ST_CLASS:
                    btns = draw_class_select(screen)
                    for cls, r in btns.items():
                        if r.collidepoint(mx,my):
                            player = Player(cls)
                            player_ref = player
                            notify("Playing as " + cls)
                            state = ST_PLAY
                            break

                elif state == ST_PLAY:
                    if event.button == 3:  # Right click: cast spell
                        cast_spell(mx, my)
                    elif event.button == 1:  # Left click: attack
                        attack_nearest()

                elif state == ST_INVENTORY:
                    xbtn, slot_btns, equip_btn, drop_btn = draw_inventory(screen, player, sel_inv)
                    if xbtn.collidepoint(mx,my):
                        state = ST_PLAY
                    else:
                        for i,r in enumerate(slot_btns):
                            if r.collidepoint(mx,my): sel_inv=i; break
                        if equip_btn.collidepoint(mx,my):
                            items_list = list(player.inventory.items())
                            if 0<=sel_inv<len(items_list):
                                name,_ = items_list[sel_inv]
                                w = next((x for x in WEAPONS if x["name"]==name),None)
                                a = next((x for x in ARMOR_SETS if x["name"]==name),None)
                                if w: player.equipped["weapon"]=name; notify("Equipped: "+name)
                                elif a: player.equipped["armor"]=name; notify("Equipped: "+name)
                        elif drop_btn.collidepoint(mx,my):
                            items_list = list(player.inventory.items())
                            if 0<=sel_inv<len(items_list):
                                name,_ = items_list[sel_inv]
                                del player.inventory[name]
                                notify("Dropped "+name)
                                sel_inv = max(0,sel_inv-1)

                elif state == ST_PAUSE:
                    xbtn, btns = draw_pause(screen)
                    if xbtn.collidepoint(mx,my) or btns.get("resume","").collidepoint(mx,my):
                        state = ST_PLAY
                    elif btns.get("save_game") and btns["save_game"].collidepoint(mx,my):
                        save_game(player, buildings, SAVE_PATH)
                        notify("Saved!")
                    elif btns.get("load_game") and btns["load_game"].collidepoint(mx,my):
                        load_game(player, buildings, SAVE_PATH)
                        notify("Loaded!")
                    elif btns.get("quit") and btns["quit"].collidepoint(mx,my):
                        running = False

                elif state == ST_SHOP:
                    if active_npc:
                        xbtn, buy_btns, _ = draw_shop(screen, active_npc, player, sel_shop)
                        if xbtn.collidepoint(mx,my):
                            state = ST_PLAY
                        else:
                            for name, r in buy_btns:
                                if r.collidepoint(mx,my):
                                    ok,msg = buy_item(player, active_npc, name)
                                    notify(msg)

                elif state == ST_CRAFT:
                    xbtn, tab_btns, craft_btns = draw_crafting(screen, player, craft_tab, sel_craft)
                    if xbtn.collidepoint(mx,my):
                        state = ST_PLAY
                    for t, r in tab_btns:
                        if r.collidepoint(mx,my): craft_tab=t; break
                    for name, r in craft_btns:
                        if r.collidepoint(mx,my):
                            ok,msg = craft_item(player, name)
                            notify(msg)

                elif state == ST_CITY:
                    xbtn, type_btns = draw_city_build(screen, player, buildings, place_type)
                    if xbtn.collidepoint(mx,my):
                        state = ST_PLAY
                    for bt, r in type_btns:
                        if r.collidepoint(mx,my):
                            place_type = bt; break
                    # Click on world = place building there
                    if event.button == 1 and my < SCREEN_H-130:
                        T=32
                        btx = int((mx+camera.x)//T)
                        bty = int((my+camera.y)//T)
                        cost = 50
                        if player.gold >= cost:
                            player.gold -= cost
                            buildings.append(Building(place_type, btx, bty))
                            notify("Built "+place_type)
                        else:
                            notify("Need 50 gold to build")

                elif state == ST_MAP:
                    xbtn = draw_world_map(screen, player, TOWNS, CITIES)
                    if xbtn.collidepoint(mx,my):
                        state = ST_MAP
                        state = ST_PLAY

                elif state == ST_DIALOGUE:
                    if active_npc:
                        xbtn, btns = draw_dialogue(screen, active_npc, dial_idx)
                        if xbtn.collidepoint(mx,my):
                            state = ST_PLAY
                        for action, r in btns:
                            if r.collidepoint(mx,my):
                                if action == "next":
                                    dial_idx += 1
                                    if active_npc.shop_stock and dial_idx >= len(active_npc.dialogue):
                                        state = ST_SHOP; sel_shop=0
                                elif action == "accept":
                                    avail = [q for q in QUESTS
                                             if q["id"] not in player.active_quests
                                             and q["id"] not in player.completed_quests]
                                    if avail:
                                        player.active_quests[avail[0]["id"]] = 0
                                        notify("Quest Accepted: "+avail[0]["name"])
                                    else:
                                        notify("No more quests available!")

        # ─── Update (PLAY state only) ───────────────────────────────────
        if state == ST_PLAY:
            # Movement
            spd = player.spd
            if pygame.K_LSHIFT in keys_held and player.sta > 0:
                spd *= 1.8
                player.sta = max(0, player.sta - 30*dt)
            if pygame.K_LCTRL in keys_held:
                spd *= 0.5

            dx = dy = 0
            if pygame.K_w in keys_held or pygame.K_UP    in keys_held: dy -= 1
            if pygame.K_s in keys_held or pygame.K_DOWN  in keys_held: dy += 1
            if pygame.K_a in keys_held or pygame.K_LEFT  in keys_held: dx -= 1
            if pygame.K_d in keys_held or pygame.K_RIGHT in keys_held: dx += 1
            if dx != 0 and dy != 0:
                dx *= 0.707; dy *= 0.707
            player.x += dx * spd * dt
            player.y += dy * spd * dt
            player.x = max(0, min(player.x, 200*32-32))
            player.y = max(0, min(player.y, 200*32-32))

            player.regen(dt)
            if player.attack_cooldown > 0:
                player.attack_cooldown -= dt

            camera.update(player, SCREEN_W, SCREEN_H)

            for e in enemies:
                e.update(player, dt)
                # Enemy attacks player
                if e.alive and math.hypot(e.x-player.x, e.y-player.y) < 35:
                    if random.random() < 0.3*dt:
                        dmg = max(1, e.atk - player.def_power() + random.randint(-2,2))
                        player.hp -= dmg
                        add_float("-"+str(dmg)+" HP", player.x, player.y-20, (255,80,80))

            for p in projectiles:
                p.update(dt)
                if p.alive:
                    for e in enemies:
                        if e.alive and math.hypot(e.x-p.x, e.y-p.y) < 25:
                            e.hp -= p.dmg
                            add_float("-"+str(p.dmg), e.x, e.y-20, (255,160,0))
                            p.alive = False
                            if e.hp <= 0:
                                e.alive = False
                                check_quest_kill(player, e.name)
                                player.gain_xp(e.xp_val)
                                player.gold += e.gold_drop
                                add_float("+"+str(e.xp_val)+"xp", e.x, e.y-40,(100,255,100))
            projectiles = [p for p in projectiles if p.alive]

            for ft in float_texts:
                ft.update(dt)
            float_texts = [ft for ft in float_texts if ft.life > 0]
            for ft in player.float_texts:
                float_texts.append(FloatText(ft[0], player.x, player.y-50, ft[1]))
            player.float_texts.clear()

            if notif_timer > 0:
                notif_timer -= dt

            if attack_flash > 0:
                attack_flash -= dt

            if player.hp <= 0:
                state = ST_GAMEOVER

        # ─── Draw ───────────────────────────────────────────────────────
        screen.fill((10,10,20))

        if state == ST_MENU:
            draw_main_menu(screen)

        elif state == ST_CLASS:
            draw_class_select(screen)

        elif state in (ST_PLAY, ST_INVENTORY, ST_QUEST, ST_DIALOGUE,
                       ST_SHOP, ST_CRAFT, ST_PAUSE, ST_CITY, ST_MAP):
            # World
            draw_world(screen, int(camera.x), int(camera.y))

            # Buildings
            for b in buildings:
                b.draw(screen, int(camera.x), int(camera.y))

            # Enemies
            for e in enemies:
                e.draw(screen, int(camera.x), int(camera.y))

            # NPCs
            for npc in npcs:
                npc.draw(screen, int(camera.x), int(camera.y))

            # Projectiles
            for p in projectiles:
                p.draw(screen, int(camera.x), int(camera.y))

            # Player
            if attack_flash > 0:
                pygame.draw.rect(screen, (255,200,100),
                    (int(player.x-camera.x)-4, int(player.y-camera.y)-4, 36,36))
            player.draw(screen, int(camera.x), int(camera.y))

            # Float texts
            for ft in float_texts:
                ft.draw(screen, int(camera.x), int(camera.y))

            # HUD
            draw_hud(screen, player)
            draw_minimap(screen, player, enemies)

            # Controls hint
            txt(screen, "WASD:Move  SPACE:Attack  RClick:Spell  E:Talk  F:Harvest  I:Inv  Q:Quests  K:Craft  B:Build  M:Map  F5:Save  ESC:Pause",
                10, 4, 11, (140,140,160))

            # Notification
            if notif_timer > 0 and notification:
                alpha = min(255, int(notif_timer * 200))
                ns = font(16).render(notification, True, (255,240,150))
                ns.set_alpha(alpha)
                screen.blit(ns, (SCREEN_W//2 - ns.get_width()//2, 40))

            # Overlays
            if state == ST_INVENTORY:
                draw_inventory(screen, player, sel_inv)
            elif state == ST_QUEST:
                draw_quest_log(screen, player)
            elif state == ST_DIALOGUE and active_npc:
                draw_dialogue(screen, active_npc, dial_idx)
            elif state == ST_SHOP and active_npc:
                draw_shop(screen, active_npc, player, sel_shop)
            elif state == ST_CRAFT:
                draw_crafting(screen, player, craft_tab, sel_craft)
            elif state == ST_PAUSE:
                draw_pause(screen)
            elif state == ST_CITY:
                draw_city_build(screen, player, buildings, place_type)
            elif state == ST_MAP:
                draw_world_map(screen, player, TOWNS, CITIES)

        elif state == ST_GAMEOVER:
            draw_gameover(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()