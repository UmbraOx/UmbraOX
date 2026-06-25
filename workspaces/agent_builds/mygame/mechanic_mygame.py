# Game Mechanic Helpers Module

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
        if (self.tx - self.x) ** 2 + (self.ty - self.y) ** 2 < 16:
            return True
        return False

    def draw(self, surf, cx, cy):
        pygame.draw.circle(surf, self.col, (int(self.x - cx), int(self.y - cy)), 4)

class Building:
    TYPES = {
        'House': {'col': (200, 150, 100), 'w': 3, 'h': 3, 'cost': {'wood': 10}},
        'Shop': {'col': (255, 200, 0), 'w': 4, 'h': 4, 'cost': {'stone': 15}},
        'Barracks': {'col': (180, 180, 180), 'w': 5, 'h': 5, 'cost': {'iron': 20}},
        'Farm': {'col': (34, 177, 76), 'w': 4, 'h': 4, 'cost': {'wood': 12}},
        'Tower': {'col': (100, 150, 200), 'w': 4, 'h': 5, 'cost': {'stone': 25}},
        'Warehouse': {'col': (200, 200, 200), 'w': 6, 'h': 6, 'cost': {'iron': 30}}
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty

    def draw(self, surf, cx, cy):
        col = Building.TYPES[self.btype]['col']
        w = Building.TYPES[self.btype]['w'] * 32
        h = Building.TYPES[self.btype]['h'] * 32
        x = self.tx * 32 - cx
        y = self.ty * 32 - cy
        pygame.draw.rect(surf, col, (x, y, w, h))
        pygame.draw.polygon(surf, (100, 50, 0), [(x + w // 2, y), (x, y - h // 4), (x + w, y - h // 4)])
        pygame.draw.rect(surf, (0, 0, 0), (x + w // 3, y + h * 2 // 3, w // 3, h // 6))
        pygame.draw.rect(surf, (255, 255, 255), (x + w // 4, y + h // 4, w // 8, h // 8))

def save_game(player, buildings, filepath):
    data = {
        'player': player.__dict__,
        'buildings': [{'btype': b.btype, 'tx': b.tx, 'ty': b.ty} for b in buildings]
    }
    with open(filepath, 'w') as f:
        json.dump(data, f)
    return True

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

if __name__ == '__main__':
    main()
