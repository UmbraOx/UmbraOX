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
    'town': (255, 255, 0),
    'camp': (255, 69, 0),
    'mine': (128, 128, 128),
    'wood_area': (34, 139, 34),
    'road': (128, 128, 128)
}
TOWNS = [(50, 50, 'Demiworld Town')]
CITIES = [(20, 20, 'City A'), (180, 180, 'City B')]
BANDIT_CAMPS = [(30, 30), (70, 70), (110, 110)]
GOBLIN_CAMPS = [(40, 40), (80, 80), (120, 120)]
MINES = [(50, 60), (90, 90), (130, 130)]
WOODCUTS = [(60, 50), (100, 100), (140, 140)]

def gen_world():
    random.seed(42)
    for x in range(200):
        for y in range(200):
            biome = random.choice(list(BIOME_COL.keys()))
            WORLD_MAP[x][y] = biome

def draw_world(surf, cam_x, cam_y):
    tile_size = 16
    for dx in range(-cam_x // tile_size, (surf.get_width() + cam_x) // tile_size + 1):
        for dy in range(-cam_y // tile_size, (surf.get_height() + cam_y) // tile_size + 1):
            x = dx * tile_size - cam_x % tile_size
            y = dy * tile_size - cam_y % tile_size
            biome = get_biome(dx + cam_x // tile_size, dy + cam_y // tile_size)
            surf.fill(BIOME_COL[biome], (x, y, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'plains'

if __name__ == '__main__':
    main()
