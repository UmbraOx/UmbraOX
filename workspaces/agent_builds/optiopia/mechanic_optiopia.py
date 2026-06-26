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
        txt_surf = self.font.render(self.text, True, (self.col[0], self.col[1], self.col[2], self.alpha))
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
        if abs(self.x - self.tx) < 1 and abs(self.y - self.ty) < 1:
            return True
        return False

    def draw(self, surf, cx, cy):
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 3)

class Building:
    TYPES = {
        'House': {'col': (255, 165, 0), 'w': 2, 'h': 2, 'cost': {'wood': 4}},
        'Shop': {'col': (128, 128, 128), 'w': 3, 'h': 2, 'cost': {'stone': 5}},
        'Barracks': {'col': (192, 64, 0), 'w': 4, 'h': 3, 'cost': {'iron': 7}},
        'Farm': {'col': (34, 139, 34), 'w': 3, 'h': 2, 'cost': {'wood': 6}},
        'Tower': {'col': (0, 0, 255), 'w': 3, 'h': 3, 'cost': {'stone': 10}},
        'Warehouse': {'col': (255, 255, 0), 'w': 4, 'h': 3, 'cost': {'wood': 8}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.col = Building.TYPES[btype]['col']
        self.w = Building.TYPES[btype]['w']
        self.h = Building.TYPES[btype]['h']

    def draw(self, surf, cx, cy):
        rect = pygame.Rect((self.tx - cx) * 32, (self.ty - cy) * 32, self.w * 32, self.h * 32)
        pygame.draw.rect(surf, self.col, rect)
        roof_points = [(rect.x + rect.width / 2, rect.y), (rect.x, rect.y + 10), (rect.x + rect.width, rect.y + 10)]
        pygame.draw.polygon(surf, (165, 42, 42), roof_points)
        door_rect = pygame.Rect(rect.x + rect.width / 2 - 8, rect.y + rect.height - 32, 16, 32)
        pygame.draw.rect(surf, (0, 0, 0), door_rect)
        window_rect = pygame.Rect(rect.x + 16, rect.y + 16, 16, 16)
        pygame.draw.rect(surf, (255, 255, 255), window_rect)

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