import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Optiopia")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player stats
player_stats = {
    'Warrior': {'hp': 120, 'attack': 15, 'defense': 12},
    'Mage': {'mana': 70, 'attack': 8, 'speed': 8},
    'Ranger': {'speed': 10, 'attack': 12}
}

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, character_type):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.stats = player_stats[character_type]
        self.hp = self.stats['hp']
        self.attack = self.stats['attack']

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Keep player within screen boundaries
        self.rect.clamp_ip(screen.get_rect())

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

    def update(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = max(abs(dx), abs(dy))
        if dist > 0:
            self.rect.x += dx / dist
            self.rect.y += dy / dist

# Main game loop
def main():
    running = True
    paused = False
    character_type = input("Choose your character type (Warrior, Mage, Ranger): ")
    player = Player(character_type)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    enemies = pygame.sprite.Group()

    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        if not paused:
            all_sprites.update(player)
            hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in hits:
                player.hp -= 10
                if player.hp <= 0:
                    running = False

        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw health bar
        pygame.draw.rect(screen, RED, (10, 10, player.hp * 2, 20))
        pygame.draw.rect(screen, WHITE, (10, 10, 240, 20), 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()