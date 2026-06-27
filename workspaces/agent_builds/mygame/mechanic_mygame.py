# Game Mechanic Helpers Module

import json
import math
import pygame

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
        self.font = pygame.font.Font(None, 36)

    def update(self):
        self.y -= 1
        self.alpha -= 4
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surf, cx, cy):
        text_surface = self.font.render(self.text, True, (self.col[0], self.col[1], self.col[2], self.alpha))
        surf.blit(text_surface, (int(self.x - cx), int(self.y - cy)))

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
        'House': {'col': (255, 160, 122), 'w': 2, 'h': 2, 'cost': {'wood': 4, 'stone': 2}},
        'Shop': {'col': (255, 218, 185), 'w': 3, 'h': 2, 'cost': {'wood': 6, 'stone': 3}},
        'Barracks': {'col': (190, 190, 190), 'w': 4, 'h': 3, 'cost': {'wood': 8, 'stone': 5}},
        'Farm': {'col': (34, 139, 34), 'w': 2, 'h': 2, 'cost': {'wood': 3, 'stone': 1}},
        'Tower': {'col': (160, 82, 45), 'w': 3, 'h': 3, 'cost': {'wood': 7, 'stone': 6}},
        'Warehouse': {'col': (255, 228, 196), 'w': 3, 'h': 3, 'cost': {'wood': 5, 'stone': 4}}
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
        pygame.draw.polygon(surf, (160, 82, 45), [(x + 16, y), (x, y - 16), (x + self.w * 32, y - 16)])
        pygame.draw.rect(surf, (0, 0, 0), (x + 10, y + self.h * 32 - 10, 8, 10))
        pygame.draw.rect(surf, (255, 255, 255), (x + 14, y + self.h * 32 - 6, 4, 6))

def save_game(player, buildings, filepath):
    try:
        data = {
            'player': player.__dict__,
            'buildings': [{'btype': b.btype, 'tx': b.tx, 'ty': b.ty} for b in buildings]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except Exception:
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
    except Exception:
        return False