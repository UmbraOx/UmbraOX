import random
import pygame

WORLD_MAP = [['' for _ in range(200)] for _ in range(200)]
BIOME_COL = {
    'FOREST': (34, 139, 34),
    'DESERT': (255, 228, 196),
    'PLAINS': (173, 255, 47),
    'MOUNTAIN': (105, 105, 105),
    'SWAMP': (32, 178, 170)
}
TOWNS = []
CITIES = []
BANDIT_CAMPS = []
GOBLIN_CAMPS = []
MINES = []
WOODCUTS = []

def gen_world():
    for x in range(200):
        for y in range(200):
            biome_chance = random.random()
            if biome_chance < 0.3:
                WORLD_MAP[x][y] = 'FOREST'
            elif biome_chance < 0.4:
                WORLD_MAP[x][y] = 'DESERT'
            elif biome_chance < 0.6:
                WORLD_MAP[x][y] = 'PLAINS'
            elif biome_chance < 0.8:
                WORLD_MAP[x][y] = 'MOUNTAIN'
            else:
                WORLD_MAP[x][y] = 'SWAMP'

def draw_world(surf, cam_x, cam_y):
    for x in range(200):
        for y in range(200):
            tile_color = BIOME_COL.get(WORLD_MAP[x][y], (0, 0, 0))
            pygame.draw.rect(surf, tile_color, ((x - cam_x) * 32, (y - cam_y) * 32, 32, 32))

def get_tile(tx, ty):
    if 0 <= tx < 200 and 0 <= ty < 200:
        return WORLD_MAP[tx][ty]
    return None

if __name__ == '__main__':
    main()
