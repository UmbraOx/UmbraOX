import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Bandit', 'hp': 30, 'atk': 7, 'def': 4, 'xp': 15, 'col': (128, 0, 0), 'spd': 1.2, 'faction': 'Enemy'},
    {'name': 'Orc', 'hp': 40, 'atk': 9, 'def': 6, 'xp': 20, 'col': (0, 128, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Skeleton', 'hp': 25, 'atk': 4, 'def': 2, 'xp': 12, 'col': (255, 255, 255), 'spd': 1.3, 'faction': 'Enemy'},
    {'name': 'Wolf', 'hp': 35, 'atk': 6, 'def': 3, 'xp': 14, 'col': (192, 192, 192), 'spd': 1.8, 'faction': 'Enemy'},
    {'name': 'Dark Mage', 'hp': 50, 'atk': 10, 'def': 5, 'xp': 25, 'col': (64, 0, 128), 'spd': 0.8, 'faction': 'Enemy'},
    {'name': 'Troll', 'hp': 70, 'atk': 12, 'def': 8, 'xp': 30, 'col': (0, 64, 0), 'spd': 0.9, 'faction': 'Enemy'},
    {'name': 'Spider', 'hp': 15, 'atk': 3, 'def': 2, 'xp': 8, 'col': (128, 128, 64), 'spd': 2.0, 'faction': 'Enemy'},
    {'name': 'Dragon Spawn', 'hp': 100, 'atk': 15, 'def': 10, 'xp': 40, 'col': (255, 69, 0), 'spd': 1.1, 'faction': 'Enemy'},
    {'name': 'Mimic', 'hp': 30, 'atk': 8, 'def': 7, 'xp': 22, 'col': (192, 64, 64), 'spd': 1.4, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.cls = cls
        self.x, self.y = 0, 0
        self.max_hp, self.hp = 100, 100
        self.max_mp, self.mp = 50, 50
        self.max_sta, self.sta = 100, 100
        self.str_, self.dex, self.int_, self.luck = 10, 10, 10, 10
        if cls == 'Warrior':
            self.str_ += 5
        elif cls == 'Mage':
            self.int_ += 5
        elif cls == 'Rogue':
            self.dex += 5
        self.level = 1
        self.xp, self.xp_next = 0, 100
        self.gold = 0
        self.speed = 2.0
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Heal']
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return self.str_ + (self.dex // 2) + (self.equipped['weapon'].atk if self.equipped['weapon'] else 0)

    def def_power(self):
        return self.dex + self.int_ + (self.equipped['armor'].def_ if self.equipped['armor'] else 0)

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
        self.max_hp += random.randint(8, 12)
        self.hp = self.max_hp
        self.max_mp += random.randint(4, 6) if self.cls == 'Mage' else 0
        self.mp = self.max_mp
        self.max_sta += random.randint(6, 9)
        self.sta = self.max_sta
        self.str_ += random.randint(1, 3)
        self.dex += random.randint(1, 3)
        self.int_ += random.randint(1, 3) if self.cls == 'Mage' else 0
        self.luck += random.randint(1, 2)

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.sta * 0.05 * dt))
        self.mp = min(self.max_mp, self.mp + (self.int_ * 0.03 * dt)) if self.cls == 'Mage' else self.mp

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
        self.x, self.y = tx, ty

    def update(self, player, dt):
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            self.x += (dx / dist) * self.spd * dt
            self.y += (dy / dist) * self.spd * dt

    def draw(self, surf, cx, cy):
        pass  # Placeholder for drawing logic

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x, self.y = tx, ty
        self.dialogue = []
        self.shop_stock = {}
        if job == 'Merchant':
            self.shop_stock = {'Potion': 10, 'Scroll': 5}
        elif job == 'Blacksmith':
            self.shop_stock = {'Sword': 2, 'Shield': 3}
        elif job == 'Alchemist':
            self.shop_stock = {'Elixir': 7, 'Antidote': 4}