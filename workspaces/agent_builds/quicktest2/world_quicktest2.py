import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (248, 248, 165),
    'water': (0, 176, 240),
    'snow': (255, 250, 250),
    'swamp': (32, 178, 170),
    'town': (255, 215, 0),
    'camp': (255, 69, 0),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'CityA'), (150, 150, 'CityB')]
BANDIT_CAMPS = [(20, 30), (40, 60), (70, 90)]
GOBLIN_CAMPS = [(10, 10), (80, 120), (150, 180)]
MINES = [(30, 40), (60, 70), (90, 100)]
WOODCUTS = [(10, 20), (50, 60), (90, 100)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choice(list(BIOME_COL.keys()))
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    tile_size = 10
    for x in range(-cam_x // tile_size, (surf.get_width() + cam_x) // tile_size + 1):
        for y in range(-cam_y // tile_size, (surf.get_height() + cam_y) // tile_size + 1):
            biome = WORLD_MAP[x][y]
            color = BIOME_COL[biome]
            pygame.draw.rect(surf, color, ((x * tile_size - cam_x, y * tile_size - cam_y), (tile_size, tile_size)))

def get_biome(tx, ty) -> str:
    return WORLD_MAP[tx][ty]