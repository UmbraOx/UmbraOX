# Import necessary modules
import pygame

class Entity:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col

    def draw(self, surf, cam_x, cam_y):
        pygame.draw.rect(surf, self.col, (self.x - cam_x, self.y - cam_y, 32, 32))

class Player(Entity):
    def __init__(self, x, y, col):
        super().__init__(x, y, col)
        self.hp = 100
        self.mp = 50
        self.sta = 75
        self.gold = 100
        self.level = 1
        self.xp = 0
        self.inventory = []
        self.equipped = {}
        self.spells = []

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= self.level * 25:
            self.xp -= self.level * 25
            self.level_up()

    def level_up(self):
        self.hp += 10
        self.mp += 5
        self.sta += 7

    def atk_power(self):
        return sum(item.get('atk', 0) for item in self.equipped.values())

    def def_power(self):
        return sum(item.get('def', 0) for item in self.equipped.values())

    def add_item(self, item):
        self.inventory.append(item)

    def regen(self, dt):
        self.hp = min(100, self.hp + (self.sta / 100 * dt))
        self.mp = min(50, self.mp + (self.level / 2 * dt))

class NPC(Entity):
    def __init__(self, x, y, col, name, job, dialogue, shop_stock=None):
        super().__init__(x, y, col)
        self.name = name
        self.job = job
        self.dialogue = dialogue
        self.shop_stock = shop_stock if shop_stock is not None else []

class Enemy(Entity):
    def __init__(self, x, y, col, name, hp, atk, defense, xp_val, spd, aggro):
        super().__init__(x, y, col)
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.xp_val = xp_val
        self.spd = spd
        self.aggro = aggro

    def update(self, player, dt):
        if abs(player.x - self.x) < 100 and abs(player.y - self.y) < 100:
            self.move_towards(player, dt)

    def move_towards(self, target, dt):
        dx = (target.x - self.x) / self.spd
        dy = (target.y - self.y) / self.spd
        self.x += dx * dt
        self.y += dy * dt


if __name__ == '__main__':
    main()
