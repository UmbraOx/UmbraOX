import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (255, 228, 181),
    'water': (0, 176, 240),
    'snow': (255, 250, 250),
    'swamp': (32, 178, 170),
    'town': (255, 215, 0),
    'camp': (220, 20, 60),
    'mine': (128, 128, 128),
    'wood_area': (34, 93, 34),
    'road': (128, 128, 128)
}
TOWNS = [(50, 50, 'Village of Eldoria'), (100, 100, 'City of Arcanis'), (150, 150, 'Fortress of Ironclad')]
CITIES = [(30, 30, 'Metropolis A'), (170, 170, 'Metropolis B')]
BANDIT_CAMPS = [(20, 80), (80, 20), (160, 160)]
GOBLIN_CAMPS = [(40, 160), (160, 40), (80, 80)]
MINES = [(50, 150), (150, 50), (100, 100)]
WOODCUTS = [(20, 20), (180, 180), (90, 90)]

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
    tile_size = 4
    for x in range(50):
        for y in range(50):
            tx, ty = cam_x + x, cam_y + y
            if 0 <= tx < 200 and 0 <= ty < 200:
                biome = WORLD_MAP[tx][ty]
                color = BIOME_COL.get(biome, (0, 0, 0))
                pygame.draw.rect(surf, color, (x * tile_size, y * tile_size, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'unknown'