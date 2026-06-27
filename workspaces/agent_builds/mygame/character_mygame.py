import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orc', 'hp': 30, 'atk': 7, 'def': 5, 'xp': 20, 'col': (128, 0, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Troll', 'hp': 40, 'atk': 9, 'def': 7, 'xp': 30, 'col': (0, 128, 0), 'spd': 0.5, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.x = 0
        self.y = 0
        self.cls = cls
        self.max_hp = 100 if cls == 'Warrior' else 80 if cls == 'Mage' else 90
        self.hp = self.max_hp
        self.max_mp = 120 if cls == 'Mage' else 60 if cls == 'Warrior' else 70
        self.mp = self.max_mp
        self.max_sta = 100
        self.sta = self.max_sta
        self.str_ = 10 if cls == 'Warrior' else 5 if cls == 'Mage' else 8
        self.dex = 8 if cls == 'Rogue' else 6 if cls == 'Warrior' else 7
        self.int_ = 12 if cls == 'Mage' else 4 if cls == 'Warrior' else 6
        self.luck = random.randint(5, 10)
        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 50
        self.speed = 2.0 if cls == 'Rogue' else 1.5 if cls == 'Mage' else 1.0
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Lightning']
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return (self.str_ + self.dex) / 2 * (1 + self.luck / 100)

    def def_power(self):
        return self.dex * (1 + self.luck / 100)

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
        self.max_mp += random.randint(5, 10) if self.cls == 'Mage' else random.randint(2, 5)
        self.mp = self.max_mp
        self.str_ += random.randint(1, 3)
        self.dex += random.randint(1, 3)
        self.int_ += random.randint(1, 3) if self.cls == 'Mage' else random.randint(0, 2)
        self.xp_next *= 1.5

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.str_ / 4) * dt)
        self.mp = min(self.max_mp, self.mp + (self.int_ / 4) * dt if self.cls == 'Mage' else self.mp)
        self.sta = min(self.max_sta, self.sta + (self.dex / 4) * dt)

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
        import pygame.draw
        pygame.draw.circle(surf, self.col, (int(cx + self.x), int(cy + self.y)), 10)

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
            self.shop_stock = {'Sword': 100, 'Shield': 150}
        elif job == 'Alchemist':
            self.dialogue.append("Greetings, traveler!")
            self.shop_stock = {'Potion': 30, 'Elixir': 60}
        elif job == 'Merchant':
            self.dialogue.append("Hello! Browse my wares.")
            self.shop_stock = {'Food': 10, 'Cloth': 20}