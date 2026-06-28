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
    'town': (255, 228, 181),
    'camp': (210, 180, 140),
    'mine': (169, 169, 169),
    'wood_area': (34, 139, 34),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'CityA'), (150, 150, 'CityB')]
BANDIT_CAMPS = [(30, 30), (70, 70), (110, 110)]
GOBLIN_CAMPS = [(40, 40), (80, 80), (120, 120)]
MINES = [(50, 50), (90, 90), (130, 130)]
WOODCUTS = [(60, 60), (100, 100), (140, 140)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choice(list(BIOME_COL.keys()))
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    tile_size = 1
    for x in range(-cam_x // tile_size, (surf.get_width() + cam_x) // tile_size):
        for y in range(-cam_y // tile_size, (surf.get_height() + cam_y) // tile_size):
            if 0 <= x < 200 and 0 <= y < 200:
                biome = WORLD_MAP[x][y]
                color = BIOME_COL[biome]
                pygame.draw.rect(surf, color, (x * tile_size - cam_x % tile_size, y * tile_size - cam_y % tile_size, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'plains'