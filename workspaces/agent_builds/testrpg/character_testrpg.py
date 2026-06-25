import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.cls = cls
        self.x, self.y = 0, 0
        self.max_hp, self.hp = 100, 100
        self.max_mp, self.mp = 50, 50
        self.max_sta, self.sta = 100, 100
        self.str_, self.dex, self.int_, self.luck = 10, 10, 10, 10
        self.level, self.xp, self.xp_next = 1, 0, 100
        self.gold = 0
        self.speed = 5
        self.inventory = {}
        self.equipped = {}
        self.spells = []
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
        self.xp_next = int(self.xp_next * 1.5)
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5
        self.mp = self.max_mp
        self.max_sta += 5
        self.sta = self.max_sta
        self.str_ += 2
        self.dex += 2
        self.int_ += 1
        self.luck += 1

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.max_hp * 0.01 * dt))
        self.mp = min(self.max_mp, self.mp + (self.max_mp * 0.01 * dt))
        self.sta = min(self.max_sta, self.sta + (self.max_sta * 0.01 * dt))

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
        self.tx, self.ty = tx, ty
        self.path = [(tx, ty)]
        self.patrol_index = 0

    def update(self, player, dt):
        if self.hp <= 0:
            return
        target_x, target_y = self.path[self.patrol_index]
        dx, dy = target_x - self.tx, target_y - self.ty
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 1:
            move_speed = self.spd * dt
            angle = math.atan2(dy, dx)
            self.tx += move_speed * math.cos(angle)
            self.ty += move_speed * math.sin(angle)
        else:
            self.patrol_index = (self.patrol_index + 1) % len(self.path)

    def draw(self, surf, cx, cy):
        pygame.draw.circle(surf, self.col, (int(cx + self.tx), int(cy + self.ty)), 10)

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x, self.y = tx, ty
        self.dialogue = []
        self.shop_stock = {}

# END OF CODE