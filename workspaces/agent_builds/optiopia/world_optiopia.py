import random

WORLD_MAP = [['plains'] * 200 for _ in range(200)]
BIOME_COL = {
    'plains': (143, 255, 107),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (255, 255, 87),
    'water': (65, 105, 225),
    'snow': (255, 250, 250),
    'swamp': (32, 178, 170),
    'town': (255, 140, 0),
    'camp': (210, 105, 30),
    'mine': (128, 128, 128),
    'wood_area': (34, 93, 62),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'Capital'), (150, 150, 'Metropolis')]
BANDIT_CAMPS = [(30, 30), (70, 70), (110, 110)]
GOBLIN_CAMPS = [(40, 40), (80, 80), (120, 120)]
MINES = [(50, 60), (90, 90), (130, 130)]
WOODCUTS = [(60, 70), (100, 100), (140, 140)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choices(
                ['plains', 'forest', 'mountain', 'desert', 'water', 'snow', 'swamp'],
                weights=[3, 5, 4, 3, 2, 1, 2], k=1
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