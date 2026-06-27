import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (248, 162, 70),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (32, 178, 170),
    'town': (255, 165, 0),
    'camp': (194, 178, 128),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (160, 82, 45)
}
TOWNS = [(50, 50, 'Village of Harmony'), (100, 100, 'City of Light'), (150, 150, 'Fortress of Strength')]
CITIES = [(30, 30, 'Capital City'), (170, 170, 'Metropolis')]
BANDIT_CAMPS = [(20, 20), (80, 80), (140, 140)]
GOBLIN_CAMPS = [(60, 60), (120, 120), (180, 180)]
MINES = [(40, 40), (100, 40), (160, 40)]
WOODCUTS = [(35, 35), (95, 95), (155, 155)]

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
    for x in range(40, 60):  # Assuming a viewport of 20x20 tiles centered on (cam_x, cam_y)
        for y in range(40, 60):
            tile_x = cam_x + x - 50
            tile_y = cam_y + y - 50
            if 0 <= tile_x < 200 and 0 <= tile_y < 200:
                biome = WORLD_MAP[tile_x][tile_y]
                color = BIOME_COL[biome]
                surf.fill(color, (x * 16, y * 16, 16, 16))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'unknown'