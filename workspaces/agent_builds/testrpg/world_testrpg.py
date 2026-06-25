import random

WORLD_MAP = [['plains'] * 200 for _ in range(200)]
BIOME_COL = {
    'plains': (153, 217, 102),
    'forest': (34, 139, 34),
    'mountain': (165, 42, 42),
    'desert': (218, 165, 32),
    'water': (72, 202, 228),
    'snow': (255, 250, 250),
    'swamp': (94, 129, 162),
    'town': (255, 215, 0),
    'camp': (210, 180, 140),
    'mine': (128, 128, 128),
    'wood_area': (34, 93, 67),
    'road': (150, 150, 150)
}
TOWNS = [(random.randint(0, 199), random.randint(0, 199), 'Village') for _ in range(1)]
CITIES = [(random.randint(0, 199), random.randint(0, 199), f'City{i+1}') for i in range(2)]
BANDIT_CAMPS = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]
GOBLIN_CAMPS = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]
MINES = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]
WOODCUTS = [(random.randint(0, 199), random.randint(0, 199)) for _ in range(3)]

def gen_world():
    random.seed(42)
    biomes = list(BIOME_COL.keys())
    for x in range(200):
        for y in range(200):
            WORLD_MAP[x][y] = random.choice(biomes)

def draw_world(surf, cam_x, cam_y):
    tile_size = 10
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            x = cam_x + dx
            y = cam_y + dy
            if 0 <= x < 200 and 0 <= y < 200:
                biome = WORLD_MAP[x][y]
                color = BIOME_COL[biome]
                pygame.draw.rect(surf, color, (dx * tile_size, dy * tile_size, tile_size, tile_size))

def get_biome(tx, ty) -> str:
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return 'plains'