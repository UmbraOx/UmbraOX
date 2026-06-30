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
__WORLD_CODE__

# ── CHARACTER MODULE ─────────────────────────────────────────────────────────
__CHAR_CODE__

# ── ITEM / DATA MODULE ───────────────────────────────────────────────────────
__ITEM_CODE__

# ── MECHANIC MODULE ──────────────────────────────────────────────────────────
__MECH_CODE__

# ── UI MODULE ────────────────────────────────────────────────────────────────
__UI_CODE__

# ── QUEST MODULE ─────────────────────────────────────────────────────────────
__QUEST_CODE__

# ── ECONOMY MODULE ───────────────────────────────────────────────────────────
__ECON_CODE__

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
    _menu_stars = [(random.randint(0,1280), random.randint(0,720), random.randint(1,3), random.random()*0.5+0.3) for _ in range(120)]
    def draw_main_menu(surf, project_name="__PROJECT_NAME__"):
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
        title = project_name if project_name else "__PROJECT_NAME__"
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

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GAME
# ═══════════════════════════════════════════════════════════════════════════

GAME_TITLE  = "__PROJECT_NAME__"
SAVE_PATH   = "__PROJ_SLUG___save.json"
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
GAME_TITLE = GAME_TITLE if "GAME_TITLE" in dir() else "__PROJECT_NAME__"
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