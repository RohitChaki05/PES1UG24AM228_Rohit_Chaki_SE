
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

from game.game_engine import GameEngine
from game.bullet import Bullet


def test_consecutive_bullet_collisions():
    engine = GameEngine(600, 700)
    engine.enemy_fire_chance = 0.0

    enemies = engine.enemy_grid.alive_enemies()
    enemy1 = enemies[0]
    enemy2 = enemies[1]

    enemy1_rect = enemy1.rect()
    enemy2_rect = enemy2.rect()

    bullet1 = Bullet(
        enemy1_rect.centerx - 2,
        enemy1_rect.bottom + 1,
        direction=-1
    )
    bullet2 = Bullet(
        enemy2_rect.centerx - 2,
        enemy2_rect.bottom + 1,
        direction=-1
    )

    engine.player_bullets = [bullet1, bullet2]
    engine.enemy_grid.move = lambda: None

    initial_score = engine.score
    engine.update()

    assert not enemy1.alive, "First enemy was not destroyed"
    assert not enemy2.alive, "Second enemy was not destroyed"
    assert engine.score == initial_score + 2, (
        f"Expected score {initial_score + 2}, got {engine.score}"
    )
    assert bullet1 not in engine.player_bullets
    assert bullet2 not in engine.player_bullets

    print("Task 1 consecutive collision test passed.")


if __name__ == "__main__":
    try:
        test_consecutive_bullet_collisions()
    finally:
        pygame.quit()