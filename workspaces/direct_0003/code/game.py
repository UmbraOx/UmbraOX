import pygame
import json
import urllib.request

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quest and Story Generation Agent")
clock = pygame.time.Clock()

def generate_story(setting, premise):
    url = "http://localhost:11434"
    data = {
        "setting": setting,
        "premise": premise
    }
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def main():
    running = True
    setting = "A medieval fantasy world"
    premise = "The kingdom is under threat from an ancient evil."
    
    story_data = generate_story(setting, premise)
    
    print(json.dumps(story_data, indent=4))
    
    # Example game loop (not related to story generation)
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    player_speed = 5
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed
        
        # Boundary checking
        player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - 50))
        player_pos[1] = max(0, min(player_pos[1], SCREEN_HEIGHT - 50))
        
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], 50, 50))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()