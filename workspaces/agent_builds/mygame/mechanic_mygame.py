# Game Mechanic Helpers Module

import json
import math
import pygame

class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, px, py, width, height, map_width, map_height):
        self.x = -px + width / 2
        self.y = -py + height / 2
        self.x = min(0, max(-(map_width - width), self.x))
        self.y = min(0, max(-(map_height - height), self.y))

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
        self.alpha -= 5

    def draw(self, surf, cx, cy):
        if self.alpha <= 0:
            return
        text_surf = self.font.render(self.text, True, (self.col[0], self.col[1], self.col[2], self.alpha))
        surf.blit(text_surf, (int(self.x + cx), int(self.y + cy)))

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
        pygame.draw.circle(surf, self.col, (int(self.x + cx), int(self.y + cy)), 5)

class Building:
    TYPES = {
        'House': {'col': (204, 153, 255), 'w': 2, 'h': 2, 'cost': {'wood': 10, 'stone': 5}},
        'Shop': {'col': (255, 204, 153), 'w': 3, 'h': 2, 'cost': {'wood': 15, 'stone': 7}},
        'Barracks': {'col': (153, 255, 204), 'w': 3, 'h': 3, 'cost': {'wood': 20, 'stone': 10}},
        'Farm': {'col': (255, 153, 153), 'w': 2, 'h': 2, 'cost': {'wood': 8, 'stone': 4}},
        'Tower': {'col': (153, 153, 255), 'w': 2, 'h': 3, 'cost': {'wood': 12, 'stone': 6}},
        'Warehouse': {'col': (204, 255, 153), 'w': 3, 'h': 3, 'cost': {'wood': 25, 'stone': 15}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.col = Building.TYPES[btype]['col']
        self.w = Building.TYPES[btype]['w']
        self.h = Building.TYPES[btype]['h']

    def draw(self, surf, cx, cy):
        x = (self.tx * 32) + cx
        y = (self.ty * 32) + cy
        pygame.draw.rect(surf, self.col, (x, y, self.w * 32, self.h * 32))
        pygame.draw.polygon(surf, (100, 50, 0), [(x + self.w * 16, y - 16), (x, y), (x + self.w * 32, y)])
        pygame.draw.rect(surf, (0, 0, 0), (x + self.w * 8, y + self.h * 32 - 8, 16, 8))
        pygame.draw.rect(surf, (255, 255, 255), (x + self.w * 4, y + self.h * 16, 8, 8))

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