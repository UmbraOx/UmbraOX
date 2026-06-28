import random

WORLD_MAP = [['plains'] * 200 for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (255, 215, 0),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (85, 107, 47),
    'town': (255, 165, 0),
    'camp': (139, 69, 19),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (150, 75, 0)
}
TOWNS = [(50, 50, 'Stonehaven'), (100, 100, 'Rivergate'), (150, 150, 'Duskmill')]
CITIES = [(25, 25, 'Capital'), (175, 175, 'Metropolis')]
BANDIT_CAMPS = [(30, 30), (60, 60), (90, 90)]
GOBLIN_CAMPS = [(40, 40), (70, 70), (100, 100)]
MINES = [(5, 5), (25, 25), (45, 45)]
WOODCUTS = [(15, 15), (35, 35), (55, 55)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome_choice = random.choices(
                ['plains', 'forest', 'mountain', 'desert', 'water', 'snow', 'swamp'],
                weights=[15, 20, 10, 8, 5, 4, 3], k=1
            )[0]
            WORLD_MAP[x][y] = biome_choice

def draw_world(surf, cam_x, cam_y):
    for x in range(200):
        for y in range(200):
            if (x - cam_x) * 32 < surf.get_width() and (y - cam_y) * 32 < surf.get_height():
                biome_color = BIOME_COL[WORLD_MAP[x][y]]
                pygame.draw.rect(surf, biome_color, ((x - cam_x) * 32, (y - cam_y) * 32, 32, 32))

def get_biome(tx, ty):
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'void'