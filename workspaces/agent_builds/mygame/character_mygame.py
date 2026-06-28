import random  
import math  

ENEMY_DEFS = [  
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 2, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'},  
    {'name': 'Orc', 'hp': 30, 'atk': 7, 'def': 3, 'xp': 20, 'col': (128, 0, 0), 'spd': 1.2, 'faction': 'Enemy'},  
    {'name': 'Troll', 'hp': 50, 'atk': 10, 'def': 4, 'xp': 30, 'col': (64, 0, 0), 'spd': 1.0, 'faction': 'Enemy'},  
    {'name': 'Skeleton', 'hp': 25, 'atk': 4, 'def': 1, 'xp': 8, 'col': (255, 255, 255), 'spd': 1.6, 'faction': 'Enemy'},  
    {'name': 'Zombie', 'hp': 35, 'atk': 5, 'def': 2, 'xp': 12, 'col': (0, 255, 0), 'spd': 1.4, 'faction': 'Enemy'},  
    {'name': 'Bandit', 'hp': 28, 'atk': 6, 'def': 3, 'xp': 15, 'col': (192, 192, 192), 'spd': 1.3, 'faction': 'Enemy'},  
    {'name': 'Golem', 'hp': 70, 'atk': 8, 'def': 6, 'xp': 40, 'col': (128, 128, 128), 'spd': 0.8, 'faction': 'Enemy'},  
    {'name': 'Wraith', 'hp': 30, 'atk': 7, 'def': 5, 'xp': 25, 'col': (64, 64, 192), 'spd': 1.8, 'faction': 'Enemy'},  
    {'name': 'Dragonling', 'hp': 40, 'atk': 9, 'def': 4, 'xp': 35, 'col': (255, 64, 64), 'spd': 1.1, 'faction': 'Enemy'},  
    {'name': 'Gargoyle', 'hp': 55, 'atk': 8, 'def': 7, 'xp': 30, 'col': (64, 192, 64), 'spd': 0.9, 'faction': 'Enemy'}  
]  

JOBS = ['Merchant', 'Healer', 'Blacksmith']  

class Player:  
    def __init__(self, cls):  
        self.x, self.y = 0, 0  
        self.cls = cls  
        self.max_hp, self.hp = 100, 100  
        self.max_mp, self.mp = 50, 50  
        self.max_sta, self.sta = 100, 100  
        self.str_, self.dex, self.int_, self.luck = 10, 10, 10, 10  
        self.level, self.xp, self.xp_next = 1, 0, 100  
        self.gold = 50  
        self.speed = 2.0  
        self.inventory = {}  
        self.equipped = {'weapon': None, 'armor': None}  
        self.spells = [] if cls == 'Mage' else []  
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

    def regen(self, dt):  
        self.hp = min(self.max_hp, self.hp + (self.str_ * 0.1) * dt)  
        self.mp = min(self.max_mp, self.mp + (self.int_ * 0.1) * dt)  
        self.sta = min(self.max_sta, self.sta + (self.dex * 0.1) * dt)  

    def level_up(self):  
        self.xp -= self.xp_next  
        self.xp_next *= 1.5  
        self.level += 1  
        self.str_ += random.randint(1, 3)  
        self.dex += random.randint(1, 3)  
        self.int_ += random.randint(1, 3)  
        self.luck += random.randint(0, 2)  
        self.max_hp += random.randint(5, 10)  
        self.hp = self.max_hp  
        self.max_mp += random.randint(2, 5) if self.cls == 'Mage' else 0  
        self.mp = self.max_mp  

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
        dx = player.x - self.x  
        dy = player.y - self.y  
        dist = math.sqrt(dx**2 + dy**2)  
        if dist > 0:  
            self.x += (dx / dist * self.spd * dt)  
            self.y += (dy / dist * self.spd * dt)  

    def draw(self, surf, cx, cy):  
        pygame.draw.circle(surf, self.col, (int(cx + self.x), int(cy + self.y)), 10)  

class NPC:  
    def __init__(self, name, job, tx, ty):  
        self.name = name  
        self.job = job  
        self.x, self.y = tx, ty  
        self.dialogue = []  
        self.shop_stock = {} if job == 'Merchant' else {}  

# No main(), no pygame.init(). import random, math only.