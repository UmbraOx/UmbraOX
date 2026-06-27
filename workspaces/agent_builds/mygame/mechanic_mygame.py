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
        self.fade_rate = 3
        self.rise_speed = 0.5

    def update(self):
        self.y -= self.rise_speed
        self.alpha -= self.fade_rate
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surf, cx, cy):
        import pygame
        font = pygame.font.Font(None, 36)
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
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 5)

class Building:
    TYPES = {
        'House': {'col': (200, 160, 120), 'w': 3, 'h': 3, 'cost': {'wood': 10, 'stone': 5}},
        'Shop': {'col': (255, 215, 0), 'w': 4, 'h': 4, 'cost': {'wood': 15, 'stone': 7}},
        'Barracks': {'col': (139, 69, 19), 'w': 5, 'h': 5, 'cost': {'wood': 20, 'stone': 10}},
        'Farm': {'col': (34, 139, 34), 'w': 4, 'h': 4, 'cost': {'wood': 8, 'stone': 3}},
        'Tower': {'col': (255, 69, 0), 'w': 6, 'h': 6, 'cost': {'wood': 25, 'stone': 15}},
        'Warehouse': {'col': (220, 220, 220), 'w': 4, 'h': 3, 'cost': {'wood': 12, 'stone': 6}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.col = Building.TYPES[btype]['col']
        self.w = Building.TYPES[btype]['w']
        self.h = Building.TYPES[btype]['h']

    def draw(self, surf, cx, cy):
        import pygame
        rect = pygame.Rect((self.tx - cx) * 32, (self.ty - cy) * 32, self.w * 32, self.h * 32)
        pygame.draw.rect(surf, self.col, rect)
        # Roof triangle
        roof_points = [(rect.x + rect.width / 2, rect.y), (rect.x, rect.y + 10), (rect.x + rect.width, rect.y + 10)]
        pygame.draw.polygon(surf, (self.col[0] - 50, self.col[1] - 50, self.col[2] - 50), roof_points)
        # Door
        door_rect = pygame.Rect(rect.x + rect.width / 2 - 4, rect.y + rect.height - 32, 8, 32)
        pygame.draw.rect(surf, (165, 42, 42), door_rect)
        # Window
        window_rect = pygame.Rect(rect.x + 10, rect.y + 10, 12, 12)
        pygame.draw.rect(surf, (255, 255, 255), window_rect)

def save_game(player, buildings, filepath):
    import os
    try:
        data = {'player': player.__dict__, 'buildings': [b.__dict__ for b in buildings]}
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(e)
        return False

def load_game(player, buildings, filepath):
    import os
    try:
        if not os.path.exists(filepath):
            return False
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