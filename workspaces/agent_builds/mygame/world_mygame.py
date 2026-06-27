# World System Module for MyGame

import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 234),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (240, 230, 140),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (85, 107, 47),
    'town': (255, 165, 0),
    'camp': (139, 69, 19),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (150, 75, 0)
}
TOWNS = [(50, 50, 'Village of Hope'), (100, 100, 'City of Light'), (150, 150, 'Fortress of Shadows')]
CITIES = [(25, 25, 'Capital City'), (175, 175, 'Metropolis')]
BANDIT_CAMPS = [(30, 30), (60, 60), (90, 90)]
GOBLIN_CAMPS = [(40, 40), (70, 70), (100, 100)]
MINES = [(5, 5), (25, 25), (45, 45)]
WOODCUTS = [(15, 15), (35, 35), (55, 55)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choice(list(BIOME_COL.keys()))
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    tile_size = 10
    for dx in range(-cam_x // tile_size, (surf.get_width() + cam_x) // tile_size + 1):
        for dy in range(-cam_y // tile_size, (surf.get_height() + cam_y) // tile_size + 1):
            x = dx * tile_size - cam_x % tile_size
            y = dy * tile_size - cam_y % tile_size
            biome = WORLD_MAP[dx][dy]
            color = BIOME_COL.get(biome, (0, 0, 0))
            pygame.draw.rect(surf, color, (x, y, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'unknown'