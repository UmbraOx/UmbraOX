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

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (139, 69, 19),
    'forest': (34, 139, 34),
    'mountain': (139, 137, 137),
    'desert': (250, 235, 181),
    'water': (65, 105, 225),
    'snow': (255, 250, 240),
    'swamp': (32, 178, 170),
    'town': (255, 215, 0),
    'camp': (220, 20, 60),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'Capital'), (150, 150, 'Metropolis')]
BANDIT_CAMPS = [(20, 30), (70, 90), (140, 160)]
GOBLIN_CAMPS = [(30, 20), (90, 70), (160, 140)]
MINES = [(40, 50), (80, 100), (130, 150)]
WOODCUTS = [(60, 40), (110, 90), (170, 140)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choices(
                ['plains', 'forest', 'mountain', 'desert', 'water', 'snow', 'swamp'],
                weights=[15, 30, 10, 10, 5, 5, 5], k=1
            )[0]
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    tile_size = 8
    for x in range(25):
        for y in range(25):
            tx, ty = cam_x + x, cam_y + y
            if 0 <= tx < 200 and 0 <= ty < 200:
                biome = WORLD_MAP[tx][ty]
                color = BIOME_COL.get(biome, (0, 0, 0))
                pygame.draw.rect(surf, color, (x * tile_size, y * tile_size, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'unknown'

# ── CHARACTER MODULE ─────────────────────────────────────────────────────────

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (0, 255, 0), 'spd': 1.5, 'faction': 'Hostile'},
    {'name': 'Orc', 'hp': 40, 'atk': 8, 'def': 6, 'xp': 20, 'col': (255, 0, 0), 'spd': 1.0, 'faction': 'Hostile'},
    {'name': 'Troll', 'hp': 60, 'atk': 12, 'def': 9, 'xp': 30, 'col': (0, 0, 255), 'spd': 0.8, 'faction': 'Hostile'}
]

class Player:
    def __init__(self, cls):
        self.x = 0
        self.y = 0
        self.cls = cls
        self.max_hp = 100 if cls == 'Warrior' else (80 if cls == 'Mage' else 90)
        self.hp = self.max_hp
        self.max_mp = 50 if cls == 'Mage' else (30 if cls == 'Warrior' else 40)
        self.mp = self.max_mp
        self.max_sta = 100
        self.sta = self.max_sta
        self.str_ = 10 if cls == 'Warrior' else (6 if cls == 'Mage' else 8)
        self.dex = 8 if cls == 'Rogue' else (7 if cls == 'Warrior' else 5)
        self.int_ = 12 if cls == 'Mage' else (4 if cls == 'Warrior' else 6)
        self.luck = random.randint(1, 10)
        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 50
        self.speed = 2.0 if cls == 'Rogue' else (1.5 if cls == 'Warrior' else 1.0)
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = ['Fireball'] if cls == 'Mage' else []
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return self.str_ + (self.dex // 2) + (5 if self.equipped['weapon'] else 0)

    def def_power(self):
        return self.dex + (self.str_ // 2) + (10 if self.equipped['armor'] else 0)

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
        self.level += 1
        self.max_hp += random.randint(5, 10)
        self.hp = self.max_hp
        self.max_mp += random.randint(3, 6) if self.cls == 'Mage' else random.randint(2, 4)
        self.mp = self.max_mp
        self.str_ += random.randint(1, 2)
        self.dex += random.randint(1, 2)
        self.int_ += random.randint(1, 2) if self.cls == 'Mage' else 0
        self.xp_next *= 1.5

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.str_ / 10) * dt)
        self.mp = min(self.max_mp, self.mp + (self.int_ / 10) * dt if self.cls == 'Mage' else self.mp)
        self.sta = min(self.max_sta, self.sta + (self.dex / 10) * dt)

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
        self.x = tx
        self.y = ty

    def update(self, player, dt):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            self.x += (dx / dist) * self.spd * dt
            self.y += (dy / dist) * self.spd * dt

    def draw(self, surf, cx, cy):
        pass

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x = tx
        self.y = ty
        self.dialogue = []
        self.shop_stock = {}

        if job == 'Blacksmith':
            self.dialogue.append("Welcome to my forge!")
            self.shop_stock['Sword'] = {'price': 100, 'qty': 5}
            self.shop_stock['Shield'] = {'price': 80, 'qty': 3}
        elif job == 'Merchant':
            self.dialogue.append("Greetings, traveler!")
            self.shop_stock['Potion'] = {'price': 20, 'qty': 10}
            self.shop_stock['Scroll'] = {'price': 50, 'qty': 5}
        elif job == 'Healer':
            self.dialogue.append("May I heal your wounds?")
            self.shop_stock['Health Potion'] = {'price': 30, 'qty': 7}

# ── ITEM / DATA MODULE ───────────────────────────────────────────────────────
# Game Data Constants

WEAPONS = [
    {'name': 'Iron Sword', 'atk': 10, 'type': 'melee', 'val': 50, 'col': (200, 190, 140)},
    {'name': 'Bow', 'atk': 8, 'type': 'ranged', 'val': 30, 'col': (160, 82, 45)},
    {'name': 'Fire Staff', 'atk': 12, 'type': 'magic', 'val': 70, 'col': (255, 69, 0)},
    {'name': 'Dagger', 'atk': 6, 'type': 'melee', 'val': 20, 'col': (138, 43, 226)},
    {'name': 'Crossbow', 'atk': 10, 'type': 'ranged', 'val': 50, 'col': (165, 42, 42)},
    {'name': 'Ice Wand', 'atk': 9, 'type': 'magic', 'val': 60, 'col': (0, 255, 255)},
    {'name': 'Great Axe', 'atk': 15, 'type': 'melee', 'val': 80, 'col': (139, 69, 19)},
    {'name': 'Longbow', 'atk': 11, 'type': 'ranged', 'val': 40, 'col': (255, 140, 0)},
    {'name': 'Lightning Rod', 'atk': 13, 'type': 'magic', 'val': 75, 'col': (255, 215, 0)},
    {'name': 'Spear', 'atk': 9, 'type': 'melee', 'val': 45, 'col': (165, 42, 42)}
]

ARMOR_SETS = [
    {'name': 'Leather Armor', 'parts': ['Leather Helm', 'Leather Chestplate', 'Leather Greaves'], 'def': 8, 'val': 30},
    {'name': 'Iron Armor', 'parts': ['Iron Helm', 'Iron Chestplate', 'Iron Greaves'], 'def': 15, 'val': 70},
    {'name': 'Dragon Scale Mail', 'parts': ['Dragon Helm', 'Dragon Chestplate', 'Dragon Greaves'], 'def': 25, 'val': 150}
]

SPELLS = [
    {'name': 'Fireball', 'mp': 15, 'dmg': 20, 'col': (255, 69, 0), 'desc': 'A fiery projectile that burns enemies.'},
    {'name': 'Heal', 'mp': 10, 'dmg': -15, 'col': (0, 255, 0), 'desc': 'Restores health to an ally.'},
    {'name': 'Lightning Bolt', 'mp': 20, 'dmg': 30, 'col': (255, 215, 0), 'desc': 'A bolt of lightning that shocks enemies.'},
    {'name': 'Shield', 'mp': 10, 'dmg': 0, 'col': (173, 216, 230), 'desc': 'Raises a shield to block incoming damage.'},
    {'name': 'Ice Shard', 'mp': 15, 'dmg': 18, 'col': (0, 255, 255), 'desc': 'Fires shards of ice that freeze enemies.'},
    {'name': 'Mana Shield', 'mp': 25, 'dmg': 0, 'col': (138, 43, 226), 'desc': 'Creates a shield that absorbs magic damage.'},
    {'name': 'Earthquake', 'mp': 30, 'dmg': 25, 'col': (139, 69, 19), 'desc': 'Causes the ground to shake and damage enemies.'},
    {'name': 'Blizzard', 'mp': 20, 'dmg': 22, 'col': (173, 216, 230), 'desc': 'Summons a blizzard that damages all enemies.'},
    {'name': 'Meteor Shower', 'mp': 40, 'dmg': 35, 'col': (255, 69, 0), 'desc': 'Calls down meteors to rain fire upon enemies.'},
    {'name': 'Resurrection', 'mp': 50, 'dmg': -100, 'col': (0, 255, 0), 'desc': 'Brings a fallen ally back to life with full health.'}
]

MATERIALS = [
    'Iron Ore',
    'Leather Hide',
    'Dragon Scale',
    'Mana Crystal',
    'Wood',
    'Coal',
    'Herbs',
    'Gems',
    'Silk',
    'Steel'
]

QUESTS = [
    {'id': 1, 'name': 'Kill Goblins', 'desc': 'Eliminate 10 goblins in the forest.', 'target': 'goblin', 'need': 10, 'prog': 0, 'done': False, 'reward_gold': 50, 'reward_xp': 20},
    {'id': 2, 'name': 'Collect Herbs', 'desc': 'Gather 5 herbs from the forest.', 'target': 'mat:Herbs', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 30, 'reward_xp': 10},
    {'id': 3, 'name': 'Defend Village', 'desc': 'Protect the village from bandit attacks.', 'target': 'bandit', 'need': 5, 'prog': 0, 'done': False, 'reward_gold': 70, 'reward_xp': 30},
    {'id': 4, 'name': 'Craft Armor', 'desc': 'Create a set of Iron Armor.', 'target': 'Iron Armor', 'need': 1, 'prog': 0, 'done': False, 'reward_gold': 80, 'reward_xp': 25},
    {'id': 5, 'name': 'Discover Ancient Ruins', 'desc': 'Find the ancient ruins hidden in the mountains.', 'target': 'mat:Gems', 'need': 3, 'prog': 0, 'done': False, 'reward_gold': 100, 'reward_xp': 40}
]

FACTIONS = {
    'kingdom': {'rep': 0, 'name': 'Kingdom of Eldoria'},
    'bandit': {'rep': 0, 'name': 'Bandit Clan'},
    'goblin': {'rep': 0, 'name': 'Goblin Tribe'}
}

DIALOGUE_TREES = {
    'Merchant': [{'text': 'Welcome to my shop!', 'opts': ['Buy', 'Sell', 'Leave']}],
    'Guard': [{'text': 'Stay alert, stranger.', 'opts': ['Report Bandit Activity', 'Ask About Village News', 'Leave']}],
    'Blacksmith': [{'text': 'Need a weapon or armor?', 'opts': ['Craft Weapon', 'Craft Armor', 'Leave']}],
    'Farmer': [{'text': 'Hello! How can I help you?', 'opts': ['Buy Produce', 'Sell Materials', 'Leave']}],
    'default': [{'text': 'Greetings!', 'opts': ['Talk', 'Leave']}]
}

NPC_NAMES = [
    'Aldric',
    'Brynn',
    'Caelum',
    'Daria',
    'Eldrin',
    'Fiona',
    'Galen',
    'Hannah',
    'Igor',
    'Jenna',
    'Kael',
    'Lila',
    'Morgan',
    'Natalia',
    'Oscar',
    'Piper'
]

NPC_JOBS = ['Blacksmith', 'Merchant', 'Healer']

# ── MECHANIC MODULE ──────────────────────────────────────────────────────────
from collections import defaultdict

class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, px, py):
        self.x += (px - self.x) * 0.1
        self.y += (py - self.y) * 0.1

class FloatText:
    def __init__(self, text, x, y, col):
        self.text = text
        self.x = x
        self.y = y
        self.col = col
        self.alpha = 255
        self.font = pygame.font.Font(None, 36)

    def update(self):
        self.y -= 1
        self.alpha -= 5

    def draw(self, surf, cx, cy):
        if self.alpha > 0:
            txt_surf = self.font.render(self.text, True, (*self.col[:3], self.alpha))
            surf.blit(txt_surf, (int(self.x - cx), int(self.y - cy)))

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
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 5)

class Building:
    TYPES = {
        'House': {'col': (200, 160, 120), 'w': 3, 'h': 3, 'cost': {'wood': 10, 'stone': 5}},
        'Shop': {'col': (255, 215, 0), 'w': 4, 'h': 3, 'cost': {'wood': 15, 'stone': 7}},
        'Barracks': {'col': (165, 42, 42), 'w': 5, 'h': 4, 'cost': {'wood': 20, 'stone': 10}},
        'Farm': {'col': (34, 139, 34), 'w': 4, 'h': 4, 'cost': {'wood': 8, 'stone': 3}},
        'Tower': {'col': (255, 69, 0), 'w': 3, 'h': 5, 'cost': {'wood': 12, 'stone': 15}},
        'Warehouse': {'col': (210, 180, 140), 'w': 4, 'h': 4, 'cost': {'wood': 18, 'stone': 9}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.col = Building.TYPES[btype]['col']
        self.w = Building.TYPES[btype]['w']
        self.h = Building.TYPES[btype]['h']

    def draw(self, surf, cx, cy):
        x = (self.tx * 32) - cx
        y = (self.ty * 32) - cy
        pygame.draw.rect(surf, self.col, (x, y, self.w * 32, self.h * 32))
        pygame.draw.polygon(surf, (160, 82, 45), [(x + self.w * 16, y), (x, y - 16), (x + self.w * 32, y - 16)])
        pygame.draw.rect(surf, (0, 0, 0), (x + 10, y + self.h * 32 - 20, 12, 20))
        pygame.draw.rect(surf, (255, 255, 255), (x + self.w * 16 - 8, y + 10, 16, 16))

def save_game(player, buildings, filepath):
    data = {
        'player': player.__dict__,
        'buildings': [{'btype': b.btype, 'tx': b.tx, 'ty': b.ty} for b in buildings]
    }
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except Exception:
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
    except Exception:
        return False

# ── UI MODULE ────────────────────────────────────────────────────────────────

font_cache_dict = {}

def font_cache(sz):
    if sz not in font_cache_dict:
        font_cache_dict[sz] = pygame.font.Font(None, sz)
    return font_cache_dict[sz]

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

# ── QUEST MODULE ─────────────────────────────────────────────────────────────

WORLD_MAP = {}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
ENEMY_DEFS = {'bandit': {}, 'goblin': {}, 'orc': {}}
NPC_NAMES = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
NPC_JOBS = ['Merchant', 'Guard', 'Farmer', 'Miner', 'Blacksmith']

def spawn_entities(WORLD_MAP, TOWNS, CITIES, BANDIT_CAMPS, GOBLIN_CAMPS, ENEMY_DEFS, NPC_NAMES, NPC_JOBS):
    enemies = []
    npcs = []
    buildings = []

    for camp in BANDIT_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'bandit', 'name': f'Bandit_{random.choice(NPC_NAMES)}', 'location': camp})

    for camp in GOBLIN_CAMPS:
        for _ in range(4):
            enemies.append({'type': 'goblin', 'name': f'Goblin_{random.choice(NPC_NAMES)}', 'location': camp})
        enemies.append({'type': 'orc', 'name': f'Orc_{random.choice(NPC_NAMES)}', 'location': camp})

    for town in TOWNS:
        jobs = ['Merchant', 'Guard', 'Guard', 'Farmer', 'Farmer', 'Miner', 'Blacksmith']
        for job in jobs:
            npcs.append({'name': random.choice(NPC_NAMES), 'job': job, 'location': town})

    wild_locations = [loc for loc, biome in WORLD_MAP.items() if biome not in ['town', 'city', 'water']]
    for _ in range(30):
        location = random.choice(wild_locations)
        enemy_type = random.choices(['bandit', 'goblin'], weights=[2, 1], k=1)[0]
        enemies.append({'type': enemy_type, 'name': f'{enemy_type.capitalize()}_{random.choice(NPC_NAMES)}', 'location': location})

    return enemies, npcs, buildings

def check_kill_quests(player, enemy_name):
    for quest in player['quests']:
        if quest['type'] == 'kill' and quest['target'] == enemy_name:
            quest['progress'] += 1
            if quest['progress'] >= quest['goal']:
                quest['completed'] = True

def check_item_quests(player, item_name, qty):
    for quest in player['quests']:
        if quest['type'] == 'collect' and quest['target'] == item_name:
            quest['progress'] += qty
            if quest['progress'] >= quest['goal']:
                quest['completed'] = True

def complete_ready_quests(player):
    completed_quests = []
    for quest in player['quests']:
        if quest['completed']:
            player['rewards'].append(quest['reward'])
            completed_quests.append(quest['name'])
    player['quests'] = [q for q in player['quests'] if not q['completed']]
    return completed_quests

def harvest_nearby(player, WORLD_MAP):
    location = player['location']
    biome = WORLD_MAP.get(location)
    if biome == 'forest':
        return 'chop'
    elif biome == 'mountain':
        return 'mine'
    elif biome in ['field', 'village']:
        return 'gather'
    else:
        return ''

# ── ECONOMY MODULE ───────────────────────────────────────────────────────────
# Economy and Crafting Module for DemiWorld

CRAFT_RECIPES = {
    'Fletching': [
        {'name': 'Arrow', 'cost': {'Feather': 1, 'Wood': 1}, 'out': {'Arrow': 5}},
        {'name': 'Quiver', 'cost': {'Leather': 2, 'String': 1}, 'out': {'Quiver': 1}},
        {'name': 'Crossbow Bolt', 'cost': {'Iron Ingot': 1, 'Wood': 1}, 'out': {'Crossbow Bolt': 5}},
        {'name': 'Bow', 'cost': {'Wood': 3, 'String': 2}, 'out': {'Bow': 1}}
    ],
    'Blacksmith': [
        {'name': 'Iron Sword', 'cost': {'Iron Ingot': 5, 'Steel': 2}, 'out': {'Iron Sword': 1}},
        {'name': 'Steel Shield', 'cost': {'Steel': 4, 'Leather': 2}, 'out': {'Steel Shield': 1}},
        {'name': 'Armor Plate', 'cost': {'Steel': 6, 'Iron Ingot': 3}, 'out': {'Armor Plate': 1}},
        {'name': 'Horse Shoe', 'cost': {'Iron Ingot': 2, 'Steel': 1}, 'out': {'Horse Shoe': 4}}
    ],
    'Alchemy': [
        {'name': 'Health Potion', 'cost': {'Herb': 3, 'Water Bottle': 1}, 'out': {'Health Potion': 5}},
        {'name': 'Mana Potion', 'cost': {'Crystal Dust': 2, 'Water Bottle': 1}, 'out': {'Mana Potion': 5}},
        {'name': 'Fire Scroll', 'cost': {'Sulfur': 3, 'Paper': 1}, 'out': {'Fire Scroll': 3}},
        {'name': 'Ice Scroll', 'cost': {'Snowflake Crystal': 2, 'Paper': 1}, 'out': {'Ice Scroll': 3}}
    ],
    'Building': [
        {'name': 'House', 'cost': {'Wood': 50, 'Stone': 20}, 'out': {'House': 1}},
        {'name': 'Shop', 'cost': {'Wood': 40, 'Iron Ingot': 10}, 'out': {'Shop': 1}},
        {'name': 'Barracks', 'cost': {'Stone': 60, 'Steel': 20}, 'out': {'Barracks': 1}},
        {'name': 'Farm', 'cost': {'Wood': 30, 'Soil': 40}, 'out': {'Farm': 1}}
    ]
}

BUILDING_TYPES = {
    'House': {'col': (255, 228, 196), 'w': 5, 'h': 5, 'cost': {'Wood': 50, 'Stone': 20}},
    'Shop': {'col': (240, 230, 140), 'w': 6, 'h': 4, 'cost': {'Wood': 40, 'Iron Ingot': 10}},
    'Barracks': {'col': (192, 192, 192), 'w': 7, 'h': 5, 'cost': {'Stone': 60, 'Steel': 20}},
    'Farm': {'col': (144, 238, 144), 'w': 6, 'h': 6, 'cost': {'Wood': 30, 'Soil': 40}},
    'Tower': {'col': (173, 216, 230), 'w': 5, 'h': 8, 'cost': {'Stone': 80, 'Steel': 30}},
    'Warehouse': {'col': (255, 248, 220), 'w': 7, 'h': 6, 'cost': {'Wood': 60, 'Iron Ingot': 15}}
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

# --- Always-available helpers ---
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

# --- Fallback: UI ---
if 'draw_hud' not in dir():
    def draw_bar(surf, x, y, w, h, val, mx, col, bg=(20,20,28), label="", label_col=(220,220,220)):
        # Shadow
        pygame.draw.rect(surf, (0,0,0), (x+2, y+2, w, h))
        # Background
        pygame.draw.rect(surf, bg, (x, y, w, h))
        if mx > 0:
            ratio = max(0.0, min(1.0, val / max(1, mx)))
            fill_w = int(w * ratio)
            if fill_w > 0:
                # Gradient: bright centre strip
                pygame.draw.rect(surf, col, (x, y, fill_w, h))
                hi = tuple(min(255, c + 60) for c in col)
                pygame.draw.rect(surf, hi, (x, y, fill_w, max(1, h//3)))
        # Border
        pygame.draw.rect(surf, (80,80,100), (x, y, w, h), 1)
        # Inline label
        if label:
            lbl_s = font(10).render(label, True, label_col)
            surf.blit(lbl_s, (x + 4, y + (h - lbl_s.get_height())//2))
    def draw_x_button(surf, rx, ry, rw, rh):
        bx = rx + rw - 24; by = ry + 4
        r = pygame.Rect(bx, by, 20, 20)
        pygame.draw.rect(surf, (160,40,40), r)
        pygame.draw.rect(surf, (220,80,80), r, 2)
        xs = font(14).render("X", True, (255,255,255))
        surf.blit(xs, (bx+6, by+3))
        return r
    def draw_panel(surf, rx, ry, rw, rh, title=""):
        # Drop shadow
        pygame.draw.rect(surf, (0,0,0), (rx+4, ry+4, rw, rh))
        pygame.draw.rect(surf, (22,22,38), (rx, ry, rw, rh))
        pygame.draw.rect(surf, (70,70,140), (rx, ry, rw, 2))
        pygame.draw.rect(surf, (70,70,120), (rx, ry, rw, rh), 1)
        if title:
            txt(surf, title, rx+10, ry+8, 16, (180,180,255))
        return draw_x_button(surf, rx, ry, rw, rh)
    def draw_hud(surf, player):
        sw, sh = surf.get_size()
        PAD = 12
        BW, BH = 210, 14
        bx = PAD
        # Semi-transparent HUD backing
        hud_surf = pygame.Surface((BW + 230, 80), pygame.SRCALPHA)
        hud_surf.fill((0, 0, 0, 140))
        surf.blit(hud_surf, (0, sh - 90))
        # Stat bars with inline labels
        draw_bar(surf, bx, sh-84, BW, BH, player.hp,  player.max_hp,  (190,35,35),  label="HP  "+str(player.hp)+"/"+str(player.max_hp),  label_col=(255,200,200))
        draw_bar(surf, bx, sh-65, BW, BH, player.mp,  player.max_mp,  (35,70,200),  label="MP  "+str(player.mp)+"/"+str(player.max_mp),  label_col=(180,210,255))
        draw_bar(surf, bx, sh-46, BW, BH, player.sta, player.max_sta, (35,160,55),  label="STA "+str(player.sta)+"/"+str(player.max_sta), label_col=(180,255,180))
        xp_ratio = player.xp / max(1, player.xp_next)
        draw_bar(surf, bx, sh-27, BW, 8,  player.xp,  player.xp_next, (160,100,220), label="", label_col=(200,180,255))
        # Right-side info block
        ix = bx + BW + 12
        txt(surf, "Lv " + str(player.level) + " " + getattr(player,"cls","Hero"), ix, sh-86, 13, (220,210,160))
        txt(surf, "XP " + str(int(xp_ratio*100)) + "%", ix, sh-70, 11, (180,150,220))
        txt(surf, str(player.gold) + "g", ix, sh-54, 13, (255,210,0))
        weap  = player.equipped.get("weapon", None)
        armr  = player.equipped.get("armor",  None)
        if weap:  txt(surf, "[W] " + str(weap)[:14],  ix, sh-38, 11, (220,195,150))
        if armr:  txt(surf, "[A] " + str(armr)[:14],  ix, sh-24, 11, (170,170,220))
        # Spell hotbar (bottom-right)
        spells = getattr(player, "spells", []) or []
        for si, sp in enumerate(spells[:6]):
            sx2 = sw - 380 + si * 58
            sy2 = sh - 64
            active = (si == getattr(player, "current_spell", 0))
            bg_col = (70,70,120) if active else (30,30,50)
            border_col = (160,130,255) if active else (80,80,120)
            pygame.draw.rect(surf, bg_col, (sx2, sy2, 50, 50))
            pygame.draw.rect(surf, border_col, (sx2, sy2, 50, 50), 2)
            sdata = next((x for x in SPELLS if x.get("name") == sp), None)
            scol = sdata["col"] if sdata else (180,180,200)
            pygame.draw.circle(surf, scol, (sx2+25, sy2+20), 13)
            if active:
                pygame.draw.circle(surf, (255,255,200), (sx2+25, sy2+20), 13, 2)
            txt(surf, sp[:7], sx2+2, sy2+36, 9, (210,210,210))
            txt(surf, str(si+1), sx2+38, sy2+2, 9, (120,120,150))
    def draw_minimap(surf, player, enemies):
        sw, sh = surf.get_size()
        MS = 140
        mx = sw - MS - 10
        my = 10
        # Dark backing with border glow
        pygame.draw.rect(surf, (0,0,0),    (mx-2, my-2, MS+4, MS+4))
        pygame.draw.rect(surf, (12,12,25), (mx, my, MS, MS))
        pygame.draw.rect(surf, (60,60,110),(mx, my, MS, MS), 1)
        # Render world tiles (sampled)
        if "WORLD_MAP" in dir() and "BIOME_COL" in dir():
            wm = WORLD_MAP
            rows = len(wm); cols = len(wm[0]) if rows else 1
            cell = MS / max(rows, cols)
            for ty in range(rows):
                for tx in range(cols):
                    col = BIOME_COL.get(wm[ty][tx], (40,40,40))
                    dark = tuple(max(0, c//3) for c in col)
                    px3 = int(mx + tx * cell)
                    py3 = int(my + ty * cell)
                    cw = max(1, int(cell))
                    pygame.draw.rect(surf, dark, (px3, py3, cw, cw))
        # Enemies
        T = 32
        scale = MS / max(1, 200 * T)
        for e in enemies:
            if not getattr(e, "alive", True): continue
            ex2 = int(e.x * scale) + mx
            ey2 = int(e.y * scale) + my
            if mx <= ex2 < mx+MS and my <= ey2 < my+MS:
                pygame.draw.circle(surf, (220,50,50), (ex2, ey2), 2)
        # Player dot with glow
        px2 = max(mx+3, min(mx+MS-4, int(player.x * scale) + mx))
        py2 = max(my+3, min(my+MS-4, int(player.y * scale) + my))
        pygame.draw.circle(surf, (60,180,255),  (px2, py2), 5)
        pygame.draw.circle(surf, (200,240,255), (px2, py2), 3)
        # Label
        txt(surf, "MAP", mx+4, my+MS-16, 9, (80,80,130))
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
    _menu_stars = [(random.randint(0,1280), random.randint(0,720), random.randint(1,3), random.random()*0.5+0.3) for _ in range(120)]
    def draw_main_menu(surf, project_name):
        W, H = surf.get_size()
        # Gradient sky
        for y in range(H):
            t = y / H
            r2 = int(5  + t * 15)
            g2 = int(5  + t * 8)
            b2 = int(15 + t * 35)
            pygame.draw.line(surf, (r2, g2, b2), (0, y), (W, y))
        # Twinkling stars
        tick = pygame.time.get_ticks()
        for sx, sy, sr, spd in _menu_stars:
            bright = int(120 + 100 * abs(math.sin(tick * 0.001 * spd)))
            pygame.draw.circle(surf, (bright, bright, min(255, bright + 60)), (sx, sy), sr)
        # Moon
        moon_x, moon_y = W - 160, 110
        pygame.draw.circle(surf, (220, 220, 180), (moon_x, moon_y), 52)
        pygame.draw.circle(surf, (200, 200, 155), (moon_x, moon_y), 50)
        pygame.draw.circle(surf, (15, 12, 35),    (moon_x - 16, moon_y - 10), 42)
        # Silhouette hills
        hill_pts = [(0,H),(0,H-120),(80,H-180),(180,H-140),(280,H-210),(400,H-170),
                    (520,H-230),(640,H-190),(760,H-220),(900,H-160),(1050,H-200),
                    (1180,H-145),(1280,H-175),(1280,H)]
        pygame.draw.polygon(surf, (8, 12, 22), hill_pts)
        # Title glow
        title = project_name if project_name else "DemiWorld"
        for blur in range(4, 0, -1):
            gs = font(50 + blur).render(title, True, (80, 30, 120))
            surf.blit(gs, (W//2 - gs.get_width()//2, H//5 - blur))
        txt(surf, title, W//2, H//5, 50, (210, 160, 255), center=True)
        txt(surf, "An Umbra Game", W//2, H//5 + 60, 16, (140, 110, 190), center=True)
        # Buttons
        btns = {}
        btn_defs = [("New Game", (100,60,160), (180,100,255)),
                    ("Continue", (40,60,100),  (100,160,255)),
                    ("Quit",     (80,30,30),   (200,80,80))]
        for i, (lbl, bg, border) in enumerate(btn_defs):
            by = H//2 + 10 + i * 68
            bx = W//2 - 130
            r = pygame.Rect(bx, by, 260, 52)
            # Shadow
            pygame.draw.rect(surf, (0, 0, 0), r.move(3, 3))
            # Button body with gradient feel
            for dy in range(52):
                tt = dy / 52
                br = int(bg[0] + tt * 20)
                bg2 = int(bg[1] + tt * 20)
                bb  = int(bg[2] + tt * 20)
                pygame.draw.line(surf, (br, bg2, bb), (bx, by+dy), (bx+260, by+dy))
            pygame.draw.rect(surf, border, r, 2)
            txt(surf, lbl, W//2, by + 15, 20, (230, 210, 255), center=True)
            btns[lbl.lower().replace(" ", "_")] = r
        # Version tag
        txt(surf, "Powered by Umbra AI", W - 10, H - 18, 11, (60, 50, 90))
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

# --- Guaranteed fallback: draw_main_menu ---
# The block above only runs when the agent didn't supply draw_hud, which
# means draw_main_menu (and its helpers) can end up undefined whenever an
# agent DID supply its own draw_hud. Umbra strips any agent-authored
# draw_main_menu override, so without this independent guard the game has
# no draw_main_menu at all and crashes on launch (NameError). This block
# is self-contained (no dependency on draw_panel) so it always works.
if 'draw_main_menu' not in dir():
    _mm_stars = [(random.randint(0,1280), random.randint(0,720), random.randint(1,3),
                  random.random()*0.5+0.3) for _ in range(120)]
    def draw_main_menu(surf, project_name):
        W, H = surf.get_size()
        for y in range(H):
            t = y / H
            pygame.draw.line(surf, (int(5+t*15), int(5+t*8), int(15+t*35)), (0, y), (W, y))
        tick = pygame.time.get_ticks()
        for sx, sy, sr, spd in _mm_stars:
            b = int(120 + 100 * abs(math.sin(tick * 0.001 * spd)))
            pygame.draw.circle(surf, (b, b, min(255, b+60)), (sx, sy), sr)
        txt(surf, project_name, W//2, H//4, 56, (230,230,255), center=True)
        labels = ["New Game", "Load Game", "Settings", "Quit"]
        keys = ["new_game", "load_game", "settings", "quit"]
        btns = {}
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            bw, bh = 240, 48
            bx, by = W//2 - bw//2, H//2 + i*60
            r = pygame.Rect(bx, by, bw, bh)
            pygame.draw.rect(surf, (40,40,70), r)
            pygame.draw.rect(surf, (110,110,180), r, 2)
            txt(surf, lbl, bx+bw//2, by+bh//2-8, 18, (220,220,255), center=True)
            btns[key] = r
        return btns

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GAME
# ═══════════════════════════════════════════════════════════════════════════

GAME_TITLE  = "DemiWorld"
SAVE_PATH   = "demiworld_save.json"
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
GAME_TITLE = GAME_TITLE if "GAME_TITLE" in dir() else "DemiWorld"
pygame.display.set_caption(GAME_TITLE)
clock  = pygame.time.Clock()

project_name = 'DemiWorld'

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
                    btns = draw_main_menu(screen, project_name)  # get rects
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
            draw_main_menu(screen, project_name)

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


# UMBRA_PLAYER_PATCH
try:
    _op=Player.__init__
    def _np(self,*a,**kw):
        _op(self,*a,**kw)
        for _at,_dv in [('active_quests',{}),('completed_quests',[]),
                        ('inventory',{}),('equipped',{'weapon':None,'armor':None}),
                        ('spells',[]),('gold',50),('level',1),('xp',0),
                        ('xp_next',100),('float_texts',[]),('atk',10),
                        ('defense',5),('spd',180),('alive',True),
                        ('attack_cooldown',0.0),('regen_timer',0.0)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Player.__init__=_np
except Exception: pass
# UMBRA_ENEMY_PATCH
try:
    _oe=Enemy.__init__
    def _ne(self,edef,tx,ty,*a,**kw):
        if isinstance(edef,str):
            _n=edef
            edef={'name':_n,'hp':40,'atk':8,'def':3,'defense':3,'xp_val':15,'spd':90,'aggro':200}
        try:
            _oe(self,edef,tx,ty,*a,**kw)
        except (KeyError,TypeError,AttributeError):
            pass
        for _at,_dv in [('name',edef.get('name','Enemy')),
                        ('hp',edef.get('hp',40)),
                        ('max_hp',edef.get('hp',40)),
                        ('atk',edef.get('atk',8)),
                        ('defense',edef.get('defense',edef.get('def',3))),
                        ('def_',edef.get('def',edef.get('defense',3))),
                        ('xp_val',edef.get('xp_val',15)),
                        ('spd',edef.get('spd',90)),
                        ('aggro',edef.get('aggro',200)),
                        ('alive',True),('tx',tx),('ty',ty),
                        ('x',tx),('y',ty)]:
            if not hasattr(self,_at): setattr(self,_at,_dv)
    Enemy.__init__=_ne
except Exception: pass

if __name__ == '__main__':
    main()
# UMBRA_MENU_PATCH
try:
    _omm = draw_main_menu
    def draw_main_menu(surf, project_name=''):
        result = _omm(surf, project_name)
        if isinstance(result, dict):
            return result
        import pygame as _pg2
        W,H = surf.get_size()
        keys = ['new_game','load_game','settings','quit','start','play','continue','exit']
        if isinstance(result, (list, tuple)):
            out = {}
            for i,item in enumerate(result):
                k = keys[i] if i < len(keys) else 'btn_'+str(i)
                if isinstance(item, _pg2.Rect): out[k] = item
                elif isinstance(item, tuple) and len(item)==2 and isinstance(item[1],_pg2.Rect): out[k] = item[1]
            return out if out else {'new_game':_pg2.Rect(W//2-100,H//2-20,200,40)}
        return {'new_game':_pg2.Rect(W//2-100,H//2-20,200,40)}
except Exception: pass