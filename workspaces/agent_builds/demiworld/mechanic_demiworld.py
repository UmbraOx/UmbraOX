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

    def draw(self, surf, cx, cy):
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 5)

class Building:
    TYPES = {
        'House': {'col': (139, 69, 19), 'w': 2, 'h': 2, 'cost': {'wood': 40, 'stone': 20}},
        'Shop': {'col': (255, 215, 0), 'w': 3, 'h': 2, 'cost': {'wood': 60, 'stone': 30}},
        'Barracks': {'col': (192, 192, 192), 'w': 4, 'h': 3, 'cost': {'wood': 80, 'stone': 50}},
        'Farm': {'col': (34, 139, 34), 'w': 3, 'h': 3, 'cost': {'wood': 70, 'stone': 25}},
        'Tower': {'col': (165, 42, 42), 'w': 2, 'h': 4, 'cost': {'wood': 90, 'stone': 60}},
        'Warehouse': {'col': (218, 165, 32), 'w': 3, 'h': 3, 'cost': {'wood': 75, 'stone': 40}}
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
        pygame.draw.polygon(surf, (165, 42, 42), [(x + self.w * 16, y), (x, y - 16), (x + self.w * 32, y - 16)])
        pygame.draw.rect(surf, (0, 0, 0), (x + 8, y + self.h * 32 - 16, 16, 16))
        pygame.draw.rect(surf, (255, 255, 255), (x + 12, y + self.h * 32 - 12, 8, 8))

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