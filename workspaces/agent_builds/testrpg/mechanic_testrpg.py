# Game Mechanic Helpers Module

import json
import math

class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, px, py, speed=0.1):
        self.x += (px - self.x) * speed
        self.y += (py - self.y) * speed

class FloatText:
    def __init__(self, text, x, y, col=(255, 255, 255), lifespan=60, fade_rate=1):
        self.text = text
        self.x = x
        self.y = y
        self.col = col
        self.lifespan = lifespan
        self.fade_rate = fade_rate

    def update(self):
        if self.lifespan > 0:
            self.y -= 0.5
            self.lifespan -= self.fade_rate
            self.col = (self.col[0], self.col[1], self.col[2], max(0, int(self.col[3] - self.fade_rate * 4)))

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
        'House': {'col': (165, 42, 42), 'w': 2, 'h': 2, 'cost': {'wood': 10, 'stone': 5}},
        'Shop': {'col': (255, 182, 193), 'w': 3, 'h': 2, 'cost': {'wood': 15, 'stone': 7}},
        'Barracks': {'col': (100, 149, 237), 'w': 4, 'h': 3, 'cost': {'wood': 20, 'stone': 10}},
        'Farm': {'col': (34, 139, 34), 'w': 3, 'h': 2, 'cost': {'wood': 8, 'stone': 3}},
        'Tower': {'col': (165, 42, 42), 'w': 2, 'h': 3, 'cost': {'wood': 12, 'stone': 8}},
        'Warehouse': {'col': (210, 105, 30), 'w': 3, 'h': 3, 'cost': {'wood': 18, 'stone': 9}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.col = Building.TYPES[btype]['col']
        self.w = Building.TYPES[btype]['w']
        self.h = Building.TYPES[btype]['h']

    def draw(self, surf, cx, cy, tile_size):
        x = (self.tx * tile_size) - cx
        y = (self.ty * tile_size) - cy
        pygame.draw.rect(surf, self.col, (x, y, self.w * tile_size, self.h * tile_size))
        pygame.draw.polygon(surf, (105, 105, 105), [(x + self.w * tile_size / 2, y),
                                                   (x, y - tile_size / 2),
                                                   (x + self.w * tile_size, y - tile_size / 2)])
        pygame.draw.rect(surf, (0, 0, 0), (x + tile_size // 4, y + self.h * tile_size - tile_size // 4, tile_size // 2, tile_size // 4))
        pygame.draw.rect(surf, (255, 255, 255), (x + tile_size // 2, y + tile_size // 2, tile_size // 8, tile_size // 8))

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