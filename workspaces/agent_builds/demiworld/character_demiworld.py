import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (0, 255, 0), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orc', 'hp': 40, 'atk': 8, 'def': 6, 'xp': 20, 'col': (255, 0, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Troll', 'hp': 60, 'atk': 12, 'def': 9, 'xp': 30, 'col': (0, 0, 255), 'spd': 0.8, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.x = 0
        self.y = 0
        self.cls = cls
        self.max_hp = 100 if cls == 'Warrior' else 75 if cls == 'Mage' else 80
        self.hp = self.max_hp
        self.max_mp = 100 if cls == 'Mage' else 50 if cls == 'Warrior' else 60
        self.mp = self.max_mp
        self.max_sta = 100
        self.sta = self.max_sta
        self.str_ = 10 if cls == 'Warrior' else 5 if cls == 'Mage' else 7
        self.dex = 8 if cls == 'Rogue' else 6 if cls == 'Warrior' else 4
        self.int_ = 12 if cls == 'Mage' else 7 if cls == 'Rogue' else 5
        self.luck = random.randint(1, 10)
        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 100
        self.speed = 2.0 if cls == 'Rogue' else 1.5 if cls == 'Warrior' else 1.0
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = ['Fireball'] if cls == 'Mage' else []
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return (self.str_ + self.dex) / 2 * (1 + len(self.equipped['weapon']) / 10 if self.equipped['weapon'] else 1)

    def def_power(self):
        return self.dex + (self.equipped['armor'].get('defense', 0) if self.equipped['armor'] else 0)

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
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 10 if self.cls == 'Mage' else 5
        self.mp = self.max_mp
        self.str_ += 2 if self.cls == 'Warrior' else 1
        self.dex += 2 if self.cls == 'Rogue' else 1
        self.int_ += 2 if self.cls == 'Mage' else 1

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
            self.shop_stock = {'Sword': 100, 'Shield': 150}
        elif job == 'Merchant':
            self.dialogue.append("Greetings, traveler!")
            self.shop_stock = {'Potion': 30, 'Scroll': 50}
        elif job == 'Healer':
            self.dialogue.append("May I heal your wounds?")
            self.shop_stock = {'Health Potion': 40}