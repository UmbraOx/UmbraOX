import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
HEALTH_THRESHOLD = 0

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Health Game")

# Font for displaying text
font = pygame.font.Font(None, 74)

def game_over_screen():
    """Display the game over screen."""
    game_over_text = font.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

def main():
    """Main game loop."""
    clock = pygame.time.Clock()
    health = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Simulate health decrease
        health -= 1
        if health <= HEALTH_THRESHOLD:
            game_over_screen()

        screen.fill(WHITE)
        
        # Display health
        health_text = font.render(f"Health: {health}", True, BLACK)
        screen.blit(health_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()
