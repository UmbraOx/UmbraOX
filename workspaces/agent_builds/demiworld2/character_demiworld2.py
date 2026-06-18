import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (0, 128, 0), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Bandit', 'hp': 30, 'atk': 7, 'def': 4, 'xp': 15, 'col': (192, 64, 0), 'spd': 1.2, 'faction': 'Enemy'},
    {'name': 'Orc', 'hp': 40, 'atk': 8, 'def': 5, 'xp': 20, 'col': (128, 0, 0), 'spd': 1.3, 'faction': 'Enemy'},
    {'name': 'Skeleton', 'hp': 25, 'atk': 4, 'def': 2, 'xp': 12, 'col': (255, 255, 255), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Wolf', 'hp': 35, 'atk': 6, 'def': 3, 'xp': 14, 'col': (192, 192, 192), 'spd': 1.8, 'faction': 'Enemy'},
    {'name': 'Dark Mage', 'hp': 50, 'atk': 10, 'def': 6, 'xp': 30, 'col': (64, 0, 128), 'spd': 1.1, 'faction': 'Enemy'},
    {'name': 'Troll', 'hp': 75, 'atk': 12, 'def': 8, 'xp': 40, 'col': (0, 64, 0), 'spd': 0.9, 'faction': 'Enemy'},
    {'name': 'Spider', 'hp': 15, 'atk': 3, 'def': 2, 'xp': 8, 'col': (192, 192, 64), 'spd': 2.0, 'faction': 'Enemy'},
    {'name': 'Dragon Spawn', 'hp': 100, 'atk': 15, 'def': 10, 'xp': 50, 'col': (255, 69, 0), 'spd': 1.4, 'faction': 'Enemy'},
    {'name': 'Mimic', 'hp': 30, 'atk': 5, 'def': 4, 'xp': 18, 'col': (128, 128, 64), 'spd': 1.2, 'faction': 'Enemy'}
]

class Player:
    def __init__(self, cls):
        self.cls = cls
        self.x, self.y = 0, 0
        self.max_hp, self.hp = 100, 100
        self.max_mp, self.mp = 50, 50 if cls == 'Mage' else 20
        self.max_sta, self.sta = 100, 100
        self.str_, self.dex, self.int_, self.luck = 10, 10, 10, 10
        self.level, self.xp, self.xp_next = 1, 0, 100
        self.gold = 50
        self.speed = 2.0 if cls == 'Rogue' else 1.5
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Heal']
        self.quests = []
        self.crouching = False

    def atk_power(self):
        base_atk = 10
        weapon_bonus = self.equipped['weapon'].get('atk', 0) if self.equipped['weapon'] else 0
        return base_atk + (self.str_ * 2) + weapon_bonus

    def def_power(self):
        base_def = 5
        armor_bonus = self.equipped['armor'].get('def', 0) if self.equipped['armor'] else 0
        return base_def + (self.dex // 2) + armor_bonus

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
        self.max_mp += random.randint(3, 6) if self.cls == 'Mage' else 2
        self.mp = self.max_mp
        self.max_sta += random.randint(4, 8)
        self.sta = self.max_sta
        self.str_ += random.randint(1, 2)
        self.dex += random.randint(1, 2)
        self.int_ += random.randint(1, 2) if self.cls == 'Mage' else 0
        self.luck += random.randint(1, 2)
        self.xp_next = int(self.xp_next * 1.5)

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.sta / 10) * dt)
        if self.cls == 'Mage':
            self.mp = min(self.max_mp, self.mp + (self.int_ / 20) * dt)

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
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            move_x = (dx / distance) * self.spd * dt
            move_y = (dy / distance) * self.spd * dt
            self.x += move_x
            self.y += move_y

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
            self.dialogue = ["Welcome to my shop!", "What can I get for you?"]
            self.shop_stock = {'Potion': 10, 'Sword': 50}
        elif job == 'Guard':
            self.dialogue = ["Stay safe out there.", "The king's law applies here."]
        elif job == 'Blacksmith':
            self.dialogue = ["Need a weapon or armor?", "Let me see what I can do."]
            self.shop_stock = {'Iron Sword': 100, 'Steel Armor': 200}
        elif job == 'Farmer':
            self.dialogue = ["Fresh produce for sale!", "Come back tomorrow for more."]
            self.shop_stock = {'Apple': 5, 'Carrot': 3}
        elif job == 'Miner':
            self.dialogue = ["Mining is hard work.", "Do you need any minerals?"]
            self.shop_stock = {'Iron Ore': 20, 'Gold Ore': 100}
        elif job == 'Alchemist':
            self.dialogue = ["I can brew potions for you.", "What do you need?"]
            self.shop_stock = {'Health Potion': 15, 'Mana Potion': 20}