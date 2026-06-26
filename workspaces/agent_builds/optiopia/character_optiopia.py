import random
import math

ENEMY_DEFS = [
    {'name': 'Goblins', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (0, 255, 0), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orcs', 'hp': 40, 'atk': 8, 'def': 6, 'xp': 20, 'col': (255, 0, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Trolls', 'hp': 60, 'atk': 10, 'def': 8, 'xp': 30, 'col': (0, 255, 255), 'spd': 0.75, 'faction': 'Enemy'},
    {'name': 'Dragons', 'hp': 100, 'atk': 15, 'def': 12, 'xp': 50, 'col': (255, 0, 255), 'spd': 0.5, 'faction': 'Enemy'},
    {'name': 'Goblins', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (0, 255, 0), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orcs', 'hp': 40, 'atk': 8, 'def': 6, 'xp': 20, 'col': (255, 0, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Trolls', 'hp': 60, 'atk': 10, 'def': 8, 'xp': 30, 'col': (0, 255, 255), 'spd': 0.75, 'faction': 'Enemy'},
    {'name': 'Dragons', 'hp': 100, 'atk': 15, 'def': 12, 'xp': 50, 'col': (255, 0, 255), 'spd': 0.5, 'faction': 'Enemy'},
    {'name': 'Goblins', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (0, 255, 0), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orcs', 'hp': 40, 'atk': 8, 'def': 6, 'xp': 20, 'col': (255, 0, 0), 'spd': 1.0, 'faction': 'Enemy'}
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
        self.equipped = {}
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Ice Shard']
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return self.str_ + (self.dex // 2) + (self.int_ // 3)

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
        self.xp_next *= 1.5
        self.max_hp += random.randint(10, 20)
        self.hp = self.max_hp
        self.max_mp += random.randint(5, 15) if self.cls == 'Mage' else random.randint(3, 10)
        self.mp = self.max_mp
        self.str_ += random.randint(1, 3)
        self.dex += random.randint(1, 2)
        self.int_ += random.randint(1, 2) if self.cls == 'Mage' else random.randint(0, 1)

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.str_ // 4) * dt)
        self.mp = min(self.max_mp, self.mp + (self.int_ // 6) * dt if self.cls == 'Mage' else self.mp)
        self.sta = min(self.max_sta, self.sta + (self.dex // 5) * dt)

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
            move_x = (dx / dist) * self.spd * dt
            move_y = (dy / dist) * self.spd * dt
            self.x += move_x
            self.y += move_y

    def draw(self, surf, cx, cy):
        import pygame
        rect = pygame.Rect(cx + self.x - 10, cy + self.y - 10, 20, 20)
        pygame.draw.rect(surf, self.col, rect)

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x = tx
        self.y = ty
        self.dialogue = []
        self.shop_stock = {}

        if job == 'Blacksmith':
            self.dialogue.append("Welcome to my forge! Need any weapons or armor?")
            self.shop_stock = {'Sword': 100, 'Shield': 150}
        elif job == 'Alchemist':
            self.dialogue.append("Greetings! I brew potions. What do you need?")
            self.shop_stock = {'Health Potion': 30, 'Mana Potion': 40}
        elif job == 'Merchant':
            self.dialogue.append("Hello traveler! Browse my wares.")
            self.shop_stock = {'Potion of Strength': 50, 'Potion of Agility': 60}
        elif job == 'Innkeeper':
            self.dialogue.append("Welcome to the inn. Rest up and regain your strength!")
            self.shop_stock = {'Room for Night': 20}