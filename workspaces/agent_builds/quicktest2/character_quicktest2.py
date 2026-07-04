import random  
import math  

ENEMY_DEFS = [  
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 2, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'},  
    {'name': 'Orc', 'hp': 30, 'atk': 7, 'def': 3, 'xp': 20, 'col': (128, 0, 0), 'spd': 1.0, 'faction': 'Enemy'}  
]  

class Player:  
    def __init__(self, cls):  
        self.x = 100  
        self.y = 100  
        self.cls = cls  
        self.max_hp = 100 if cls == 'Warrior' else 80 if cls == 'Mage' else 90  
        self.hp = self.max_hp  
        self.max_mp = 50 if cls == 'Mage' else 30 if cls == 'Rogue' else 40  
        self.mp = self.max_mp  
        self.max_sta = 100  
        self.sta = self.max_sta  
        self.str_ = 10 if cls == 'Warrior' else 5 if cls == 'Mage' else 8  
        self.dex = 8 if cls == 'Rogue' else 6 if cls == 'Mage' else 7  
        self.int_ = 12 if cls == 'Mage' else 4 if cls == 'Warrior' else 6  
        self.luck = random.randint(5, 10)  
        self.level = 1  
        self.xp = 0  
        self.xp_next = 100  
        self.gold = 50  
        self.speed = 2.0 if cls == 'Rogue' else 1.5 if cls == 'Mage' else 1.0  
        self.inventory = {}  
        self.equipped = {}  
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Heal']  
        self.quests = []  
        self.crouching = False  

    def atk_power(self):  
        return self.str_ + (self.dex // 2)  

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
        self.max_hp += 10  
        self.hp = self.max_hp  
        self.max_mp += 5 if self.cls == 'Mage' else 3  
        self.mp = self.max_mp  
        self.str_ += 2 if self.cls == 'Warrior' else 1  
        self.dex += 2 if self.cls == 'Rogue' else 1  
        self.int_ += 2 if self.cls == 'Mage' else 1  

    def regen(self, dt):  
        self.sta = min(self.max_sta, self.sta + (self.speed * dt))  

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
            self.x += (dx / dist * self.spd * dt)  
            self.y += (dy / dist * self.spd * dt)  

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