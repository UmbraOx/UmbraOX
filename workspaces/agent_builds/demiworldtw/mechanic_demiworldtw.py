import pygame
import json

class Camera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, player):
        self.x += (player.rect.centerx - self.x - 400) * 0.1
        self.y += (player.rect.centery - self.y - 300) * 0.1

class FloatText:
    def __init__(self, text, x, y, col=(255, 255, 255), life=60):
        self.text = text
        self.x = x
        self.y = y
        self.col = col
        self.life = life

    def update(self):
        self.y -= 1
        self.life -= 1

    def draw(self, surf, cam_x, cam_y):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.col)
        surf.blit(text_surface, (self.x - cam_x, self.y - cam_y))

class Projectile:
    def __init__(self, x, y, vx, vy, dmg, col=(255, 0, 0)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dmg = dmg
        self.col = col
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if abs(self.vx) < 0.1 and abs(self.vy) < 0.1:
            self.alive = False

    def draw(self, surf, cam_x, cam_y):
        pygame.draw.circle(surf, self.col, (int(self.x - cam_x), int(self.y - cam_y)), 5)

class Building:
    TYPES = {
        'House': 'house.png',
        'Shop': 'shop.png',
        'Barracks': 'barracks.png',
        'Farm': 'farm.png',
        'Tower': 'tower.png',
        'Warehouse': 'warehouse.png'
    }

    def __init__(self, btype, tx, ty):
        self.btype = btype
        self.tx = tx
        self.ty = ty
        self.image = pygame.image.load(Building.TYPES[btype]).convert_alpha()

    def draw(self, surf, cam_x, cam_y):
        surf.blit(self.image, (self.tx * 64 - cam_x, self.ty * 64 - cam_y))

def save_game(player, buildings, filepath):
    try:
        data = {
            'player': {'x': player.rect.x, 'y': player.rect.y},
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
        player.rect.x = data['player']['x']
        player.rect.y = data['player']['y']
        buildings.clear()
        for b in data['buildings']:
            buildings.append(Building(b['btype'], b['tx'], b['ty']))
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    main()
