import pytest
import os
import tempfile
from core.runtime.runtime_game_tester import RuntimeGameTester, GameTestResult

COMPLETE_GAME = '''
import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Test Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    player_rect = pygame.Rect(400, 300, 40, 40)
    enemy_rect = pygame.Rect(100, 100, 40, 40)
    health = 3
    score = 0
    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    health = 3
                    game_over = False

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                player_rect.x = max(0, player_rect.x - 4)
            if keys[pygame.K_RIGHT]:
                player_rect.x = min(SCREEN_WIDTH - 40, player_rect.x + 4)
            if keys[pygame.K_UP]:
                player_rect.y = max(0, player_rect.y - 4)
            if keys[pygame.K_DOWN]:
                player_rect.y = min(SCREEN_HEIGHT - 40, player_rect.y + 4)

            if player_rect.colliderect(enemy_rect):
                health -= 1
                if health <= 0:
                    game_over = True

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 255), player_rect)
        pygame.draw.rect(screen, (255, 0, 0), enemy_rect)

        hp_text = font.render(f"HP: {health}", True, (255, 255, 255))
        screen.blit(hp_text, (10, 10))

        if game_over:
            go_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(go_text, (350, 280))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
'''

BROKEN_GAME = '''
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        pygame.display.flip()

if __name__ == "__main__":
    main()
'''

SYNTAX_ERROR_GAME = '''
import pygame
def main(
    pass
'''


@pytest.fixture
def tester():
    return RuntimeGameTester()


def test_complete_game_passes(tester, tmp_path):
    f = tmp_path / "game.py"
    f.write_text(COMPLETE_GAME)
    result = tester.test_file(str(f))
    assert result.score > 60
    assert "Pygame initialization" in result.features_found
    assert "Main game loop" in result.features_found
    assert "Collision detection" in result.features_found
    assert "Health/lives system" in result.features_found


def test_broken_game_has_warnings(tester, tmp_path):
    f = tmp_path / "broken.py"
    f.write_text(BROKEN_GAME)
    result = tester.test_file(str(f))
    assert len(result.warnings) > 0 or len(result.issues) > 0


def test_syntax_error_detected(tester, tmp_path):
    f = tmp_path / "syntax.py"
    f.write_text(SYNTAX_ERROR_GAME)
    result = tester.test_file(str(f))
    assert not result.passed
    assert any("Syntax" in i for i in result.issues)


def test_missing_file_handled(tester):
    result = tester.test_file("/nonexistent/game.py")
    assert not result.passed
    assert len(result.issues) > 0


def test_game_tester_summary(tester, tmp_path):
    f = tmp_path / "game.py"
    f.write_text(COMPLETE_GAME)
    result = tester.test_file(str(f))
    summary = result.summary()
    assert "game.py" in summary
    assert "/100" in summary


def test_result_to_dict(tester, tmp_path):
    f = tmp_path / "game.py"
    f.write_text(COMPLETE_GAME)
    result = tester.test_file(str(f))
    d = result.to_dict()
    assert "score" in d
    assert "issues" in d
    assert "features_found" in d


def test_fps_cap_missing_detected(tester, tmp_path):
    no_fps = BROKEN_GAME  # already missing .tick()
    f = tmp_path / "nofps.py"
    f.write_text(no_fps)
    result = tester.test_file(str(f))
    # Should flag missing FPS cap
    fps_issue = any("FPS" in i or "tick" in i for i in result.issues + result.warnings)
    assert fps_issue


def test_generate_fix_prompt(tester, tmp_path):
    f = tmp_path / "game.py"
    f.write_text(BROKEN_GAME)
    result = tester.test_file(str(f))
    result.add_issue("Missing boundary checking")
    prompt = tester.generate_fix_prompt(result)
    assert prompt is not None
    assert "boundary" in prompt.lower()