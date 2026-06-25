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
TOWNS = [(50, 50, 'Stonehaven'), (100, 100, 'Rivergate'), (150, 150, 'Duskmill')]
CITIES = [(30, 70, 'Capital City'), (180, 120, 'Metropolis')]
BANDIT_CAMPS = [(40, 60), (90, 110), (140, 160)]
GOBLIN_CAMPS = [(60, 40), (110, 90), (160, 140)]
MINES = [(25, 35), (75, 85), (125, 135)]
WOODCUTS = [(15, 25), (65, 75), (115, 125)]

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
    for x in range(20):
        for y in range(20):
            tile_x = (cam_x + x) % 200
            tile_y = (cam_y + y) % 200
            biome = WORLD_MAP[tile_x][tile_y]
            color = BIOME_COL[biome]
            surf.fill(color, ((x * 32, y * 32), (32, 32)))

def get_biome(tx, ty):
    return WORLD_MAP[tx % 200][ty % 200]

if __name__ == '__main__':
    main()
