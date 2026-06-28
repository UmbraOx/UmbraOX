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
        self.timer = 60

    def update(self):
        if self.timer > 0:
            self.timer -= 1
            self.y -= 0.5
            self.alpha -= 4
        else:
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
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 3)

class Building:
    TYPES = {
        'House': {'col': (128, 64, 0), 'w': 2, 'h': 2, 'cost': {'wood': 5, 'stone': 3}},
        'Shop': {'col': (255, 165, 0), 'w': 2, 'h': 2, 'cost': {'wood': 7, 'stone': 4}},
        'Barracks': {'col': (192, 192, 192), 'w': 3, 'h': 2, 'cost': {'wood': 8, 'stone': 5}},
        'Farm': {'col': (0, 128, 0), 'w': 2, 'h': 2, 'cost': {'wood': 4, 'stone': 2}},
        'Tower': {'col': (64, 64, 64), 'w': 3, 'h': 3, 'cost': {'wood': 10, 'stone': 7}},
        'Warehouse': {'col': (192, 192, 192), 'w': 3, 'h': 3, 'cost': {'wood': 6, 'stone': 4}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty

    def draw(self, surf, cx, cy):
        import pygame
        col = Building.TYPES[self.btype]['col']
        w = Building.TYPES[self.btype]['w'] * 32
        h = Building.TYPES[self.btype]['h'] * 32
        x = self.tx * 32 - cx
        y = self.ty * 32 - cy
        pygame.draw.rect(surf, col, (x, y, w, h))
        pygame.draw.polygon(surf, (192, 192, 192), [(x + w // 2, y), (x, y - h // 4), (x + w, y - h // 4)])
        if self.btype == 'House':
            pygame.draw.rect(surf, (0, 0, 0), (x + w // 4, y + h * 3 // 4, w // 2, h // 4))
            pygame.draw.rect(surf, (255, 255, 255), (x + w // 2 - 8, y + h // 2, 16, 16))

def save_game(player, buildings, filepath):
    import json
    data = {
        'player': player.__dict__,
        'buildings': [{'btype': b.btype, 'tx': b.tx, 'ty': b.ty} for b in buildings]
    }
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(e)
        return False

def load_game(player, buildings, filepath):
    import json
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