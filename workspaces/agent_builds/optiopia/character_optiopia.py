import random  
import math  

ENEMY_DEFS = [  
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 2, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Hostile'},  
    {'name': 'Orc', 'hp': 30, 'atk': 7, 'def': 3, 'xp': 20, 'col': (128, 0, 0), 'spd': 1.2, 'faction': 'Hostile'},  
    {'name': 'Skeleton', 'hp': 15, 'atk': 4, 'def': 1, 'xp': 5, 'col': (255, 255, 255), 'spd': 2.0, 'faction': 'Hostile'},  
    {'name': 'Zombie', 'hp': 25, 'atk': 6, 'def': 2, 'xp': 15, 'col': (0, 255, 0), 'spd': 1.8, 'faction': 'Hostile'},  
    {'name': 'Troll', 'hp': 40, 'atk': 9, 'def': 4, 'xp': 30, 'col': (0, 128, 0), 'spd': 1.0, 'faction': 'Hostile'},  
    {'name': 'Bandit', 'hp': 25, 'atk': 6, 'def': 2, 'xp': 15, 'col': (192, 192, 192), 'spd': 1.3, 'faction': 'Hostile'},  
    {'name': 'Golem', 'hp': 50, 'atk': 8, 'def': 6, 'xp': 40, 'col': (128, 128, 128), 'spd': 0.8, 'faction': 'Hostile'},  
    {'name': 'Wraith', 'hp': 35, 'atk': 7, 'def': 3, 'xp': 25, 'col': (64, 64, 192), 'spd': 1.6, 'faction': 'Hostile'},  
    {'name': 'Dragon', 'hp': 100, 'atk': 15, 'def': 8, 'xp': 100, 'col': (255, 64, 64), 'spd': 0.9, 'faction': 'Hostile'},  
    {'name': 'Giant', 'hp': 75, 'atk': 12, 'def': 5, 'xp': 60, 'col': (128, 64, 0), 'spd': 1.1, 'faction': 'Hostile'}  
]  

JOBS = ['Blacksmith', 'Merchant', 'Healer']  

class Player:  
    def __init__(self, cls):  
        self.x = 0  
        self.y = 0  
        self.cls = cls  
        self.max_hp = 100 if cls == 'Warrior' else 80 if cls == 'Mage' else 90  
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
        self.gold = 50  
        self.speed = 2.0 if cls == 'Rogue' else 1.8 if cls == 'Mage' else 1.6  
        self.inventory = {}  
        self.equipped = {'weapon': None, 'armor': None}  
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Heal']  
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
        self.max_hp += random.randint(5, 10)  
        self.hp = self.max_hp  
        self.max_mp += random.randint(3, 6) if self.cls == 'Mage' else random.randint(2, 4)  
        self.mp = self.max_mp  
        self.str_ += random.randint(1, 2)  
        self.dex += random.randint(1, 2)  
        self.int_ += random.randint(1, 2) if self.cls == 'Mage' else random.randint(0, 1)  

    def regen(self, dt):  
        self.sta = min(self.max_sta, self.sta + self.speed * dt / 2)  
        if self.hp < self.max_hp:  
            self.hp += (self.str_ + self.dex) * dt / 10  
        if self.mp < self.max_mp and self.cls == 'Mage':  
            self.mp += self.int_ * dt / 10  

class Enemy:  
    def __init__(self, edef, tx, ty):  
        self.name = edef['name']  
        self.hp = edef['hp']  
        self.atk = edef['atk']  
        self.defense = edef['def']  
        self.xp = edef['xp']  
        self.color = edef['col']  
        self.speed = edef['spd']  
        self.faction = edef['faction']  
        self.x = tx  
        self.y = ty  

    def update(self, player, dt):  
        dx = player.x - self.x  
        dy = player.y - self.y  
        dist = math.sqrt(dx ** 2 + dy ** 2)  
        if dist > 0:  
            self.x += dx / dist * self.speed * dt  
            self.y += dy / dist * self.speed * dt  

    def draw(self, surf, cx, cy):  
        pygame.draw.circle(surf, self.color, (int(cx + self.x), int(cy + self.y)), 10)  

class NPC:  
    def __init__(self, name, job, tx, ty):  
        self.name = name  
        self.job = job  
        self.x = tx  
        self.y = ty  
        self.dialogue = []  
        self.shop_stock = {} if job != 'Merchant' else {'Potion': 10, 'Sword': 5}  


if __name__ == '__main__':
    main()
