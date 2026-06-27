import random
import math

ENEMY_DEFS = [
    {'name': 'Goblins', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (0, 255, 0), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Orcs', 'hp': 40, 'atk': 8, 'def': 6, 'xp': 20, 'col': (255, 0, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Trolls', 'hp': 60, 'atk': 10, 'def': 8, 'xp': 30, 'col': (0, 255, 255), 'spd': 0.75, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.x = 0
        self.y = 0
        self.cls = cls
        self.max_hp = 100 if cls == 'Warrior' else (80 if cls == 'Mage' else 90)
        self.hp = self.max_hp
        self.max_mp = 50 if cls == 'Mage' else (30 if cls == 'Rogue' else 40)
        self.mp = self.max_mp
        self.max_sta = 100
        self.sta = self.max_sta
        self.str_ = random.randint(8, 12) if cls == 'Warrior' else random.randint(5, 9)
        self.dex = random.randint(8, 12) if cls == 'Rogue' else random.randint(5, 9)
        self.int_ = random.randint(8, 12) if cls == 'Mage' else random.randint(5, 9)
        self.luck = random.randint(3, 7)
        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 100
        self.speed = 2.0 if cls == 'Rogue' else (1.5 if cls == 'Mage' else 1.0)
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = ['Fireball'] if cls == 'Mage' else []
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return (self.str_ + self.dex) / 2 * (1 + len(self.equipped['weapon']) / 10 if self.equipped['weapon'] else 1)

    def def_power(self):
        return self.dex * (1 + len(self.equipped['armor']) / 10 if self.equipped['armor'] else 1)

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
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5 if self.cls == 'Mage' else 3
        self.mp = self.max_mp
        self.str_ += random.randint(1, 2)
        self.dex += random.randint(1, 2)
        self.int_ += random.randint(1, 2) if self.cls == 'Mage' else 0
        self.luck += random.randint(0, 1)
        self.xp_next = int(self.xp_next * 1.5)

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.str_ / 2) * dt)
        self.mp = min(self.max_mp, self.mp + (self.int_ / 4) * dt if self.cls == 'Mage' else self.mp)
        self.sta = min(self.max_sta, self.sta + self.dex * dt)

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

# Example initialization of classes (not part of the module)
# player = Player('Warrior')
# enemy = Enemy(ENEMY_DEFS[0], 10, 10)
# npc = NPC('Bob', 'Blacksmith', 5, 5)