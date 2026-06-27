import random

WORLD_MAP = [['plains'] * 200 for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (255, 228, 181),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (32, 178, 72),
    'town': (255, 69, 0),
    'camp': (139, 69, 19),
    'mine': (128, 128, 128),
    'wood_area': (50, 205, 50),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'Capital'), (150, 150, 'Metropolis')]
BANDIT_CAMPS = [(30, 30), (70, 70), (110, 110)]
GOBLIN_CAMPS = [(20, 80), (90, 40), (160, 120)]
MINES = [(45, 145), (135, 65), (75, 185)]
WOODCUTS = [(10, 10), (190, 190), (100, 100)]

def gen_world():
    random.seed(42)
    for y in range(200):
        for x in range(200):
            biome_choice = random.choices(
                ['plains', 'forest', 'mountain', 'desert', 'water', 'snow', 'swamp'],
                weights=[15, 20, 10, 10, 5, 5, 5], k=1
            )[0]
            WORLD_MAP[y][x] = biome_choice

def draw_world(surf, cam_x, cam_y):
    for y in range(10, 30):
        for x in range(10, 30):
            tile_x = cam_x + x - 15
            tile_y = cam_y + y - 15
            if 0 <= tile_x < 200 and 0 <= tile_y < 200:
                biome = WORLD_MAP[tile_y][tile_x]
                color = BIOME_COL[biome]
                pygame.draw.rect(surf, color, (x * 32, y * 32, 32, 32))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[ty][tx]
    return 'plains'