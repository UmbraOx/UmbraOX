import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 2, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orc', 'hp': 30, 'atk': 7, 'def': 3, 'xp': 20, 'col': (128, 0, 0), 'spd': 1.2, 'faction': 'Enemy'},
    {'name': 'Troll', 'hp': 40, 'atk': 9, 'def': 5, 'xp': 30, 'col': (0, 128, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Skeleton', 'hp': 15, 'atk': 4, 'def': 1, 'xp': 5, 'col': (192, 192, 192), 'spd': 2.0, 'faction': 'Enemy'},
    {'name': 'Zombie', 'hp': 25, 'atk': 6, 'def': 2, 'xp': 15, 'col': (0, 255, 0), 'spd': 1.3, 'faction': 'Enemy'},
    {'name': 'Bandit', 'hp': 22, 'atk': 8, 'def': 4, 'xp': 18, 'col': (255, 0, 0), 'spd': 1.6, 'faction': 'Enemy'},
    {'name': 'Wraith', 'hp': 35, 'atk': 10, 'def': 6, 'xp': 25, 'col': (0, 0, 255), 'spd': 1.4, 'faction': 'Enemy'},
    {'name': 'Golem', 'hp': 50, 'atk': 12, 'def': 8, 'xp': 40, 'col': (128, 128, 128), 'spd': 0.8, 'faction': 'Enemy'},
    {'name': 'Dragon', 'hp': 75, 'atk': 15, 'def': 10, 'xp': 60, 'col': (255, 255, 0), 'spd': 1.1, 'faction': 'Enemy'},
    {'name': 'Phoenix', 'hp': 60, 'atk': 14, 'def': 9, 'xp': 55, 'col': (255, 165, 0), 'spd': 1.8, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.x = 0
        self.y = 0
        self.cls = cls
        self.max_hp = 100 if cls == 'Warrior' else 75 if cls == 'Mage' else 85
        self.hp = self.max_hp
        self.max_mp = 100 if cls == 'Mage' else 50 if cls == 'Warrior' else 60
        self.mp = self.max_mp
        self.max_sta = 100
        self.sta = self.max_sta
        self.str_ = 10 if cls == 'Warrior' else 7 if cls == 'Mage' else 8
        self.dex = 8 if cls == 'Rogue' else 6 if cls == 'Warrior' else 9
        self.int_ = 9 if cls == 'Mage' else 5 if cls == 'Warrior' else 7
        self.luck = random.randint(1, 10)
        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 0
        self.speed = 2.5 if cls == 'Rogue' else 2.0 if cls == 'Warrior' else 1.8
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Ice Shard']
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return self.str_ + (self.dex // 2) + (self.equipped['weapon'].atk if self.equipped['weapon'] else 0)

    def def_power(self):
        return self.dex + (self.int_ // 2) + (self.equipped['armor'].def_ if self.equipped['armor'] else 0)

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
        self.max_mp += random.randint(3, 7) if self.cls == 'Mage' else random.randint(2, 5)
        self.mp = self.max_mp
        self.str_ += random.randint(1, 3)
        self.dex += random.randint(1, 3)
        self.int_ += random.randint(1, 3)
        self.xp_next *= 1.5

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.str_ * 0.1) * dt)
        self.mp = min(self.max_mp, self.mp + (self.int_ * 0.1) * dt if self.cls == 'Mage' else self.mp)
        self.sta = min(self.max_sta, self.sta + (self.dex * 0.1) * dt)

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
        pass  # Placeholder for drawing logic

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x = tx
        self.y = ty
        self.dialogue = []
        self.shop_stock = {}

# END CODE