import random

WORLD_MAP = [['plains' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'plains': (154, 205, 50),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (248, 248, 255),
    'water': (0, 191, 255),
    'snow': (255, 250, 250),
    'swamp': (32, 178, 170),
    'town': (255, 165, 0),
    'camp': (255, 69, 0),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (128, 128, 128)
}
TOWNS = []
CITIES = [(50, 50, 'Capital'), (150, 150, 'Metropolis')]
BANDIT_CAMPS = [(20, 30), (70, 90), (140, 160)]
GOBLIN_CAMPS = [(30, 20), (90, 70), (160, 140)]
MINES = [(40, 40), (80, 80), (120, 120)]
WOODCUTS = [(60, 60), (100, 100), (140, 140)]

def gen_world():
    random.seed(42)
    for i in range(200):
        for j in range(200):
            biome_choice = random.choices(
                ['plains', 'forest', 'mountain', 'desert', 'water', 'snow', 'swamp'],
                weights=[15, 30, 10, 10, 5, 5, 5], k=1
            )[0]
            WORLD_MAP[i][j] = biome_choice

def draw_world(surf, cam_x, cam_y):
    for i in range(20):
        for j in range(20):
            tx, ty = cam_x + i, cam_y + j
            if 0 <= tx < 200 and 0 <= ty < 200:
                biome = WORLD_MAP[tx][ty]
                col = BIOME_COL.get(biome, (0, 0, 0))
                pygame.draw.rect(surf, col, (i * 32, j * 32, 32, 32))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'unknown'