import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (255, 228, 181),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (32, 178, 170),
    'town': (255, 165, 0),
    'camp': (194, 178, 128),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (160, 82, 45)
}
TOWNS = [(50, 50, 'Stonehaven'), (100, 100, 'Rivergate'), (150, 150, 'Duskmill')]
CITIES = [(30, 30, 'Capital'), (170, 170, 'Metropolis')]
BANDIT_CAMPS = [(20, 20), (80, 80), (140, 140)]
GOBLIN_CAMPS = [(60, 60), (120, 120), (180, 180)]
MINES = [(40, 40), (100, 40), (160, 40)]
WOODCUTS = [(50, 90), (110, 90), (170, 90)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choices(
                ['plains', 'forest', 'mountain', 'desert', 'water', 'snow', 'swamp'],
                weights=[15, 20, 10, 10, 5, 5, 5], k=1
            )[0]
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    for x in range(30):  # Assuming a viewport of 30x30 tiles
        for y in range(30):
            tile_x = cam_x + x
            tile_y = cam_y + y
            if 0 <= tile_x < 200 and 0 <= tile_y < 200:
                biome = WORLD_MAP[tile_x][tile_y]
                color = BIOME_COL[biome]
                pygame.draw.rect(surf, color, (x * 32, y * 32, 32, 32))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'void'