import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Topia")
clock = pygame.time.Clock()

# Player stats
player_stats = {
    'hp': 100,
    'atk': 10,
    'def': 8,
    'spd': 6,
    'level': 1,
    'exp': 0,
    'next_level_exp': 100
}

# Enemy stats template
enemy_stats_template = {
    'hp': 50,
    'atk': 5,
    'def': 3,
    'spd': 4
}

# Items, weapons, equipment
items = ['potion', 'food']
weapons = ['sword', 'axe']
equipment = ['helmet', 'armor']

# Inventory and gear
inventory = {'potion': 2, 'food': 1}
gear = {}

# Enemies
enemies = [{'id': i, **enemy_stats_template} for i in range(10)]

# NPCs
npcs = [
    {
        'name': 'Graveyard Keeper',
        'dialogue': "I have a quest for you. Bring me 5 rocks.",
        'quest_item': 'rock',
        'quest_amount': 5,
        'reward_exp': 20,
        'reward_items': {'potion': 1}
    }
]

# Quests
quests = []

# Materials
materials = {}

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def handle_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_stats['x'] -= player_stats['spd']
    if keys[pygame.K_d]:
        player_stats['x'] += player_stats['spd']
    if keys[pygame.K_w]:
        player_stats['y'] -= player_stats['spd']
    if keys[pygame.K_s]:
        player_stats['y'] += player_stats['spd']

def draw_health_bar():
    pygame.draw.rect(screen, RED, (10, 10, player_stats['hp'], 20))
    pygame.draw.rect(screen, GREEN, (10, 10, player_stats['hp'], 20), 2)

def handle_attack(target):
    damage = max(0, player_stats['atk'] - target['def'])
    target['hp'] -= damage
    if target['hp'] <= 0:
        gain_exp(target)
        enemies.remove(target)

def gain_exp(enemy):
    exp_gained = enemy['level'] * 10
    player_stats['exp'] += exp_gained
    while player_stats['exp'] >= player_stats['next_level_exp']:
        level_up()

def level_up():
    player_stats['level'] += 1
    player_stats['hp'] += random.randint(5, 15)
    player_stats['atk'] += random.randint(2, 4)
    player_stats['def'] += random.randint(1, 3)
    player_stats['spd'] += random.randint(1, 2)
    player_stats['exp'] -= player_stats['next_level_exp']
    player_stats['next_level_exp'] = int(player_stats['next_level_exp'] * 1.5)

def draw_inventory():
    screen.fill(BLACK)
    draw_text("Inventory", WHITE, 10, 10)
    y_offset = 40
    for item, quantity in inventory.items():
        draw_text(f"{item}: {quantity}", WHITE, 10, y_offset)
        y_offset += 30

def draw_gear():
    screen.fill(BLACK)
    draw_text("Gear", WHITE, 10, 10)
    y_offset = 40
    for slot, item in gear.items():
        draw_text(f"{slot}: {item}", WHITE, 10, y_offset)
        y_offset += 30

def handle_npc_interaction(npc):
    screen.fill(BLACK)
    draw_text(npc['dialogue'], WHITE, 10, 10)
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    player_stats.update({'x': SCREEN_WIDTH // 2, 'y': SCREEN_HEIGHT // 2})
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for enemy in enemies:
                    if (enemy['x'] - mouse_x) ** 2 + (enemy['y'] - mouse_y) ** 2 < 50**2:
                        handle_attack(enemy)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                draw_inventory()
                pygame.display.flip()
                pygame.time.wait(2000)

        screen.fill(BLACK)
        
        # Handle input
        handle_input()

        # Draw player
        pygame.draw.circle(screen, WHITE, (player_stats['x'], player_stats['y']), 15)

        # Draw enemies
        for enemy in enemies:
            if 'x' not in enemy or 'y' not in enemy:
                enemy.update({'x': random.randint(0, SCREEN_WIDTH), 'y': random.randint(0, SCREEN_HEIGHT)})
            pygame.draw.circle(screen, RED, (enemy['x'], enemy['y']), 10)

        # Draw NPCs
        for npc in npcs:
            if 'x' not in npc or 'y' not in npc:
                npc.update({'x': random.randint(0, SCREEN_WIDTH), 'y': random.randint(0, SCREEN_HEIGHT)})
            pygame.draw.circle(screen, GREEN, (npc['x'], npc['y']), 12)
            if abs(npc['x'] - player_stats['x']) < 50 and abs(npc['y'] - player_stats['y']) < 50:
                handle_npc_interaction(npc)

        # Draw health bar
        draw_health_bar()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()