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
    'town': (255, 215, 0),
    'camp': (220, 20, 60),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'Capital'), (150, 150, 'Metropolis')]
BANDIT_CAMPS = [(20, 30), (70, 90), (140, 160)]
GOBLIN_CAMPS = [(30, 20), (90, 70), (160, 140)]
MINES = [(40, 50), (80, 100), (130, 150)]
WOODCUTS = [(60, 40), (110, 90), (170, 140)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choices(
                ['plains', 'forest', 'mountain', 'desert', 'water', 'snow', 'swamp'],
                weights=[15, 30, 10, 10, 5, 5, 5], k=1
            )[0]
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    tile_size = 8
    for x in range(25):
        for y in range(25):
            tx, ty = cam_x + x, cam_y + y
            if 0 <= tx < 200 and 0 <= ty < 200:
                biome = WORLD_MAP[tx][ty]
                color = BIOME_COL.get(biome, (0, 0, 0))
                pygame.draw.rect(surf, color, (x * tile_size, y * tile_size, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'unknown'