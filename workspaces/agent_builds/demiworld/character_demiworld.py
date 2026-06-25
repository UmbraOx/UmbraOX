import random
import math

ENEMY_DEFS = [
    {'name': 'Goblin', 'hp': 20, 'atk': 5, 'def': 3, 'xp': 10, 'col': (64, 64, 64), 'spd': 1.5, 'faction': 'Enemy'},
    {'name': 'Bandit', 'hp': 30, 'atk': 7, 'def': 5, 'xp': 15, 'col': (128, 0, 0), 'spd': 1.2, 'faction': 'Enemy'},
    {'name': 'Orc', 'hp': 40, 'atk': 9, 'def': 7, 'xp': 20, 'col': (64, 0, 0), 'spd': 1.0, 'faction': 'Enemy'},
    {'name': 'Skeleton', 'hp': 25, 'atk': 4, 'def': 2, 'xp': 8, 'col': (255, 255, 255), 'spd': 1.3, 'faction': 'Enemy'},
    {'name': 'Wolf', 'hp': 22, 'atk': 6, 'def': 4, 'xp': 12, 'col': (192, 192, 192), 'spd': 1.8, 'faction': 'Enemy'},
    {'name': 'Dark Mage', 'hp': 35, 'atk': 8, 'def': 6, 'xp': 25, 'col': (0, 0, 128), 'spd': 0.9, 'faction': 'Enemy'},
    {'name': 'Troll', 'hp': 50, 'atk': 10, 'def': 8, 'xp': 30, 'col': (64, 64, 0), 'spd': 0.7, 'faction': 'Enemy'},
    {'name': 'Spider', 'hp': 15, 'atk': 2, 'def': 1, 'xp': 5, 'col': (0, 192, 0), 'spd': 2.0, 'faction': 'Enemy'},
    {'name': 'Dragon Spawn', 'hp': 60, 'atk': 12, 'def': 10, 'xp': 40, 'col': (255, 69, 0), 'spd': 0.8, 'faction': 'Enemy'},
    {'name': 'Mimic', 'hp': 30, 'atk': 7, 'def': 5, 'xp': 18, 'col': (128, 128, 64), 'spd': 1.1, 'faction': 'Enemy'}
]

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
        self.str_ = 10 if cls == 'Warrior' else 8 if cls == 'Mage' else 9
        self.dex = 9 if cls == 'Rogue' else 7 if cls == 'Mage' else 8
        self.int_ = 12 if cls == 'Mage' else 6 if cls == 'Warrior' else 7
        self.luck = random.randint(5, 10)
        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 50
        self.speed = 2.0 if cls == 'Rogue' else 1.8 if cls == 'Warrior' else 1.6
        self.inventory = {}
        self.equipped = {'weapon': None, 'armor': None}
        self.spells = [] if cls != 'Mage' else ['Fireball', 'Heal']
        self.quests = []
        self.crouching = False

    def atk_power(self):
        return (self.str_ + self.dex) / 2 + (self.equipped['weapon'].atk if self.equipped['weapon'] else 0)

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
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5 if self.cls == 'Mage' else 3
        self.mp = self.max_mp
        self.str_ += 2 if self.cls == 'Warrior' else 1
        self.dex += 2 if self.cls == 'Rogue' else 1
        self.int_ += 2 if self.cls == 'Mage' else 1

    def regen(self, dt):
        self.hp = min(self.max_hp, self.hp + (self.str_ / 10) * dt)
        self.mp = min(self.max_mp, self.mp + (self.int_ / 15) * dt if self.cls == 'Mage' else self.mp)
        self.sta = min(self.max_sta, self.sta + (self.dex / 20) * dt)

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
        pass  # Placeholder for drawing logic

class NPC:
    def __init__(self, name, job, tx, ty):
        self.name = name
        self.job = job
        self.x = tx
        self.y = ty
        self.dialogue = []
        self.shop_stock = {}

        if job == 'Merchant':
            self.dialogue.append("Welcome to my shop!")
            self.shop_stock = {'Potion': 10, 'Sword': 5}
        elif job == 'Guard':
            self.dialogue.append("Stay safe out there.")
        elif job == 'Blacksmith':
            self.dialogue.append("Need some gear?")
            self.shop_stock = {'Armor': 3, 'Shield': 2}
        elif job == 'Farmer':
            self.dialogue.append("Fresh produce for sale!")
            self.shop_stock = {'Apple': 15, 'Carrot': 20}
        elif job == 'Miner':
            self.dialogue.append("Dug up some treasure!")
            self.shop_stock = {'Ore': 8, 'Gem': 4}
        elif job == 'Alchemist':
            self.dialogue.append("Mixing potions all day.")
            self.shop_stock = {'Healing Potion': 12, 'Mana Potion': 6}

if __name__ == '__main__':
    main()
