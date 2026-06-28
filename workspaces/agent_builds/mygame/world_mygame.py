# World System for MyGame

import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (139, 69, 19),
    'forest': (34, 139, 34),
    'mountain': (139, 137, 137),
    'desert': (250, 235, 181),
    'water': (65, 105, 225),
    'snow': (255, 250, 240),
    'swamp': (32, 178, 170),
    'town': (255, 165, 0),
    'camp': (192, 192, 192),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (160, 82, 45)
}
TOWNS = []
CITIES = [(50, 50, 'CityA'), (150, 150, 'CityB')]
BANDIT_CAMPS = [(20, 30), (70, 90), (180, 160)]
GOBLIN_CAMPS = [(40, 60), (100, 120), (190, 180)]
MINES = [(30, 40), (80, 100), (170, 150)]
WOODCUTS = [(10, 20), (60, 80), (160, 140)]

def gen_world():
    random.seed(42)
    for i in range(200):
        for j in range(200):
            biome_choice = random.choice(list(BIOME_COL.keys()))
            WORLD_MAP[i][j] = biome_choice

def draw_world(surf, cam_x, cam_y):
    visible_tiles = 10
    for dx in range(-visible_tiles, visible_tiles + 1):
        for dy in range(-visible_tiles, visible_tiles + 1):
            tx, ty = cam_x + dx, cam_y + dy
            if 0 <= tx < 200 and 0 <= ty < 200:
                biome = WORLD_MAP[tx][ty]
                color = BIOME_COL.get(biome, (0, 0, 0))
                pygame.draw.rect(surf, color, (dx * 16, dy * 16, 16, 16))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'unknown'