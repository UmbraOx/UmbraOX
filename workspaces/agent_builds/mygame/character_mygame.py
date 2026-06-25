import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.x = 0
        self.y = 0
        self.cls = cls
        self.max_hp = 100 if cls == 'Warrior' else 80 if cls == 'Mage' else 90
        self.hp = self.max_hp
        self.max_mp = 50 if cls == 'Mage' else 30 if cls == 'Archer' else 20
        self.mp = self.max_mp
        self.max_sta = 100
        self.sta = self.max_sta
        self.str_ = 10 if cls == 'Warrior' else 5 if cls == 'Mage' else 7
        self.dex = 7 if cls == 'Archer' else 5 if cls == 'Mage' else 6
        self.int_ = 12 if cls == 'Mage' else 4 if cls == 'Warrior' else 6
        self.luck = random.randint(1, 10)
        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 50
        self.speed = 2.0 if cls == 'Archer' else 1.8 if cls == 'Mage' else 1.6
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = ['Fireball'] if cls == 'Mage' else []
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return (self.str_ + self.dex) / 2 * (1 + self.luck / 100)

    def def_power(self):
        return self.dex if self.equipped['armor'] is None else self.dex + self.equipped['armor'].def_

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
        self.dex += 2 if self.cls == 'Archer' else 1
        self.int_ += 2 if self.cls == 'Mage' else 1

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.str_ / 10) * dt)
        self.mp = min(self.max_mp, self.mp + (self.int_ / 10) * dt)
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
            move_x = (dx / dist) * self.spd * dt
            move_y = (dy / dist) * self.spd * dt
            self.x += move_x
            self.y += move_y

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
        elif job == 'Healer':
            self.dialogue.append("Greetings! I can heal you.")
        elif job == 'Trader':
            self.dialogue.append("Hello traveler! What do you need?")
            self.shop_stock['Potion'] = {'price': 50, 'qty': 10}
            self.shop_stock['Scroll'] = {'price': 75, 'qty': 4}

if __name__ == '__main__':
    main()
