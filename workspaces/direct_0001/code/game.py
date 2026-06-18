import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Demiworld")
clock = pygame.time.Clock()

player_image = pygame.Surface((50, 50))
player_image.fill((255, 0, 0))
player_rect = player_image.get_rect(center=(screen_width // 2, screen_height // 2))

options = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

def main():
    running = True
    direction = (0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_input = pygame.key.name(event.key).lower().strip()
                direction = options.get(key_input, options["up"])

        player_rect.x += direction[1] * 5
        player_rect.y += direction[0] * 5

        if player_rect.left < 0:
            player_rect.left = 0
        elif player_rect.right > screen_width:
            player_rect.right = screen_width

        if player_rect.top < 0:
            player_rect.top = 0
        elif player_rect.bottom > screen_height:
            player_rect.bottom = screen_height

        screen.fill((0, 0, 0))
        screen.blit(player_image, player_rect)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()