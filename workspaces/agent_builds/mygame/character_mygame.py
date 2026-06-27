import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 2, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orc', 'hp': 30, 'atk': 7, 'def': 3, 'xp': 20, 'col': (128, 0, 0), 'spd': 1.2, 'faction': 'Enemy'},
    {'name': 'Troll', 'hp': 50, 'atk': 10, 'def': 4, 'xp': 30, 'col': (64, 128, 64), 'spd': 0.9, 'faction': 'Enemy'},
    {'name': 'Skeleton', 'hp': 15, 'atk': 3, 'def': 1, 'xp': 5, 'col': (192, 192, 192), 'spd': 2.0, 'faction': 'Enemy'},
    {'name': 'Zombie', 'hp': 25, 'atk': 4, 'def': 2, 'xp': 8, 'col': (64, 64, 128), 'spd': 1.3, 'faction': 'Enemy'},
    {'name': 'Bandit', 'hp': 20, 'atk': 5, 'def': 2, 'xp': 12, 'col': (192, 64, 64), 'spd': 1.8, 'faction': 'Enemy'},
    {'name': 'Witch', 'hp': 30, 'atk': 7, 'def': 3, 'xp': 25, 'col': (128, 64, 192), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Dragon', 'hp': 100, 'atk': 15, 'def': 5, 'xp': 100, 'col': (255, 64, 0), 'spd': 0.7, 'faction': 'Enemy'},
    {'name': 'Golem', 'hp': 80, 'atk': 10, 'def': 6, 'xp': 75, 'col': (128, 128, 64), 'spd': 0.6, 'faction': 'Enemy'},
    {'name': 'Wraith', 'hp': 40, 'atk': 8, 'def': 3, 'xp': 35, 'col': (64, 192, 192), 'spd': 1.5, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.x = 0
        self.y = 0
        self.cls = cls
        self.max_hp = 100 if cls == 'Warrior' else 80 if cls == 'Mage' else 90
        self.hp = self.max_hp
        self.max_mp = 100 if cls == 'Mage' else 50 if cls == 'Warrior' else 70
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
        self.gold = 0
        self.speed = 2.0 if cls == 'Rogue' else 1.5 if cls == 'Mage' else 1.8
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Heal']
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return self.str_ + (self.dex // 2) + (self.equipped['weapon'].atk if self.equipped['weapon'] else 0)

    def def_power(self):
        return self.dex + (self.equipped['armor'].def_ if self.equipped['armor'] else 0)

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
        self.sta = min(self.max_sta, self.sta + (self.speed * dt))
        if self.hp < self.max_hp:
            self.hp += (self.str_ / 2) * dt
        if self.mp < self.max_mp and self.cls == 'Mage':
            self.mp += (self.int_ / 2) * dt

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
        pygame.draw.circle(surf, self.col, (int(cx + self.x), int(cy + self.y)), 10)

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x = tx
        self.y = ty
        self.dialogue = []
        self.shop_stock = {}

JOBS = ['Blacksmith', 'Healer', 'Trader']