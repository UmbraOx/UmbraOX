# Game Mechanic Helpers Module

import json
import math
from collections import defaultdict

class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, px, py, follow_speed=0.1):
        self.x += (px - self.x) * follow_speed
        self.y += (py - self.y) * follow_speed

class FloatText:
    def __init__(self, text, x, y, col, lifespan=60, fade_rate=2):
        self.text = text
        self.x = x
        self.y = y
        self.col = col
        self.lifespan = lifespan
        self.fade_rate = fade_rate

    def update(self):
        if self.lifespan > 0:
            self.lifespan -= 1
            self.y -= 0.5
            self.col = (self.col[0], self.col[1], self.col[2], max(0, self.col[3] - self.fade_rate))

    def draw(self, surf, cx, cy, font):
        if self.lifespan > 0:
            text_surface = font.render(self.text, True, self.col)
            surf.blit(text_surface, (self.x - cx, self.y - cy))

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
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 3)

class Building:
    TYPES = {
        'House': {'col': (255, 165, 0), 'w': 2, 'h': 2, 'cost': {'wood': 4}},
        'Shop': {'col': (139, 69, 19), 'w': 3, 'h': 2, 'cost': {'stone': 5}},
        'Barracks': {'col': (105, 105, 105), 'w': 4, 'h': 3, 'cost': {'iron': 6}},
        'Farm': {'col': (34, 139, 34), 'w': 2, 'h': 2, 'cost': {'wood': 3}},
        'Tower': {'col': (205, 92, 92), 'w': 3, 'h': 3, 'cost': {'stone': 8}},
        'Warehouse': {'col': (165, 42, 42), 'w': 3, 'h': 2, 'cost': {'iron': 7}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.col = Building.TYPES[btype]['col']
        self.w = Building.TYPES[btype]['w']
        self.h = Building.TYPES[btype]['h']

    def draw(self, surf, cx, cy):
        x = (self.tx * 32) - cx
        y = (self.ty * 32) - cy
        pygame.draw.rect(surf, self.col, (x, y, self.w * 32, self.h * 32))
        # Roof triangle
        pygame.draw.polygon(surf, (165, 42, 42), [(x + self.w * 16, y - 10), (x, y + 10), (x + self.w * 32, y + 10)])
        # Door
        pygame.draw.rect(surf, (0, 0, 0), (x + self.w * 16 - 8, y + self.h * 32 - 20, 16, 20))
        # Window
        pygame.draw.rect(surf, (255, 255, 255), (x + 10, y + 10, 10, 10))

def save_game(player, buildings, filepath):
    try:
        data = {
            'player': player.__dict__,
            'buildings': [{'btype': b.btype, 'tx': b.tx, 'ty': b.ty} for b in buildings]
        }
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
        for b in data['buildings']:
            buildings.append(Building(b['btype'], b['tx'], b['ty']))
        return True
    except Exception as e:
        print(e)
        return False