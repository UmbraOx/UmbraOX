import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (143, 255, 107),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (255, 255, 87),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (32, 165, 218),
    'town': (255, 140, 0),
    'camp': (192, 192, 192),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (165, 42, 42)
}
TOWNS = []
CITIES = [(50, 50, 'Capital'), (150, 150, 'Metropolis')]
BANDIT_CAMPS = [(20, 30), (80, 90), (160, 170)]
GOBLIN_CAMPS = [(40, 60), (100, 110), (180, 190)]
MINES = [(30, 40), (90, 100), (170, 180)]
WOODCUTS = [(25, 35), (85, 95), (165, 175)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choice(list(BIOME_COL.keys()))
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    tile_size = 10
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            x = cam_x + dx
            y = cam_y + dy
            if 0 <= x < 200 and 0 <= y < 200:
                biome = WORLD_MAP[x][y]
                color = BIOME_COL[biome]
                pygame.draw.rect(surf, color, (dx * tile_size, dy * tile_size, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'plains'