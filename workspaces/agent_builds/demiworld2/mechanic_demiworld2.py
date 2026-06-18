import json
import math

class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, px, py):
        self.x += (px - self.x) * 0.1
        self.y += (py - self.y) * 0.1

class FloatText:
    def __init__(self, text, x, y, col):
        self.text = text
        self.x = x
        self.y = y
        self.col = col
        self.alpha = 255
        self.vy = -3

    def update(self):
        self.y += self.vy
        self.alpha -= 4
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surf, cx, cy):
        import pygame
        font = pygame.font.Font(None, 24)
        txt_surf = font.render(self.text, True, (self.col[0], self.col[1], self.col[2], self.alpha))
        surf.blit(txt_surf, (int(self.x - cx), int(self.y - cy)))

class Projectile:
    def __init__(self, x, y, tx, ty, dmg, col, spd=9):
        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty
        self.dmg = dmg
        self.col = col
        self.spd = spd
        angle = math.atan2(ty - y, tx - x)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surf, cx, cy):
        import pygame
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 3)

class Building:
    TYPES = {
        'House': {'col': (150, 75, 0), 'w': 2, 'h': 2, 'cost': {'wood': 4, 'stone': 2}},
        'Shop': {'col': (200, 200, 150), 'w': 3, 'h': 2, 'cost': {'wood': 6, 'stone': 3}},
        'Barracks': {'col': (100, 100, 100), 'w': 4, 'h': 3, 'cost': {'wood': 8, 'stone': 5}},
        'Farm': {'col': (0, 200, 0), 'w': 3, 'h': 2, 'cost': {'wood': 5, 'stone': 1}},
        'Tower': {'col': (100, 0, 0), 'w': 2, 'h': 4, 'cost': {'wood': 7, 'stone': 6}},
        'Warehouse': {'col': (150, 150, 150), 'w': 3, 'h': 3, 'cost': {'wood': 9, 'stone': 4}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.info = Building.TYPES[btype]

    def draw(self, surf, cx, cy):
        import pygame
        x = (self.tx * 32) - cx
        y = (self.ty * 32) - cy
        w = self.info['w'] * 32
        h = self.info['h'] * 32
        col = self.info['col']
        pygame.draw.rect(surf, col, (x, y, w, h))
        pygame.draw.polygon(surf, (100, 50, 0), [(x + w // 2, y - 16), (x, y), (x + w, y)])
        pygame.draw.rect(surf, (0, 0, 0), (x + w // 4, y + h - 32, w // 2, 32))  # door
        pygame.draw.rect(surf, (0, 0, 0), (x + w // 8, y + h // 4, w // 4, h // 4))  # window

def save_game(player, buildings, filepath):
    try:
        data = {'player': player.__dict__, 'buildings': [b.__dict__ for b in buildings]}
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(e)
        return False

def load_game(player, buildings, filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        player.__dict__.update(data['player'])
        buildings.clear()
        for b_data in data['buildings']:
            building = Building(b_data['btype'], b_data['tx'], b_data['ty'])
            buildings.append(building)
        return True
    except Exception as e:
        print(e)
        return False