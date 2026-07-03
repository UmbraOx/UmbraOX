import random
import math

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