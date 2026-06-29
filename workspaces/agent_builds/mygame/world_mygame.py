import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (255, 228, 181),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (34, 139, 34),
    'town': (255, 215, 0),
    'camp': (255, 69, 0),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'CityA'), (150, 150, 'CityB')]
BANDIT_CAMPS = [(20, 30), (40, 60), (70, 90)]
GOBLIN_CAMPS = [(10, 10), (80, 80), (120, 120)]
MINES = [(30, 30), (60, 60), (90, 90)]
WOODCUTS = [(10, 50), (50, 10), (90, 50)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choice(list(BIOME_COL.keys()))
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    tile_size = 10
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            x = cam_x + dx
            y = cam_y + dy
            if 0 <= x < 200 and 0 <= y < 200:
                biome = WORLD_MAP[x][y]
                color = BIOME_COL[biome]
                rect = (dx * tile_size, dy * tile_size, tile_size, tile_size)
                surf.fill(color, rect)

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'plains'