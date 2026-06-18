import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DemiWorldTw")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.health = 100
        self.mana = 50
        self.stamina = 75
        self.inventory = []
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.velocity = [0, 0]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity[1] = -TILE_SIZE
        elif keys[pygame.K_s]:
            self.velocity[1] = TILE_SIZE
        else:
            self.velocity[1] = 0

        if keys[pygame.K_a]:
            self.velocity[0] = -TILE_SIZE
        elif keys[pygame.K_d]:
            self.velocity[0] = TILE_SIZE
        else:
            self.velocity[0] = 0

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.rect.topleft = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Add player to all sprites group
        self.all_sprites.add(self.player)

        # Create enemies
        for _ in range(10):
            x, y = random.randint(0, SCREEN_WIDTH - TILE_SIZE), random.randint(0, SCREEN_HEIGHT - TILE_SIZE)
            enemy = Enemy(x, y)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def run(self):
        running = True
        paused = False

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                    elif event.key == pygame.K_i:
                        self.show_inventory()
                    elif event.key == pygame.K_F5:
                        self.save_game()
                    elif event.key == pygame.K_F9:
                        self.load_game()

            if not paused:
                self.update()
                self.draw()

        pygame.quit()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        screen.fill(WHITE)
        self.all_sprites.draw(screen)
        pygame.display.flip()

    def show_inventory(self):
        print("Inventory:", self.player.inventory)

    def save_game(self):
        # Placeholder for saving game state
        print("Game saved.")

    def load_game(self):
        # Placeholder for loading game state
        print("Game loaded.")

# Main function
if __name__ == "__main__":
    game = Game()
    game.run()