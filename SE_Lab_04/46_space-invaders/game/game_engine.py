import pygame
import random

from game.player import Player
from game.enemy import EnemyGrid
from game.bullet import Bullet

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
YELLOW = (255, 255, 0)

# Difficulty settings: (speed, fire_chance)
DIFFICULTIES = {
    "Easy": (1.0, 0.005),
    "Medium": (1.5, 0.01),
    "Hard": (2.5, 0.02)
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 26)
        self.large_font = pygame.font.SysFont("Arial", 50)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.current_difficulty = "Medium"
        self.state = "MENU"  # States: MENU, PLAYING, GAME_OVER"
        self.game_over = False

        self.reset_game(self.current_difficulty)

    def reset_game(self, difficulty="Medium"):
        self.current_difficulty = difficulty
        speed, fire_chance = DIFFICULTIES[difficulty]

        self.player = Player(self.width // 2 - 20, self.height - 50, 40, 20)
        self.enemy_grid = EnemyGrid(self.width, speed=speed)

        self.player_bullets = []
        self.enemy_bullets = []
        self._shoot_cooldown = 0
        self.enemy_fire_chance = fire_chance

        self.score = 0
        self.game_over = False

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.state in ("MENU", "GAME_OVER"):
            if event.key == pygame.K_1:
                self.reset_game("Easy")
                self.state = "PLAYING"
            elif event.key == pygame.K_2:
                self.reset_game("Medium")
                self.state = "PLAYING"
            elif event.key == pygame.K_3:
                self.reset_game("Hard")
                self.state = "PLAYING"
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.reset_game(self.current_difficulty)
                self.state = "PLAYING"
            elif event.key == pygame.K_q:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif self.state == "PLAYING":
            if event.key == pygame.K_SPACE and self._shoot_cooldown <= 0:
                bullet_x = self.player.center_x() - 2
                self.player_bullets.append(Bullet(bullet_x, self.player.y, direction=-1))
                self._shoot_cooldown = 15

    def handle_input(self):
        if self.state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-self.player.speed, self.width)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(self.player.speed, self.width)

    def update(self):
        if self.state != "PLAYING":
            return

        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

        self.enemy_grid.move()

        for enemy in self.enemy_grid.alive_enemies():
            if random.random() < self.enemy_fire_chance:
                bullet_x = enemy.x + enemy.width // 2
                self.enemy_bullets.append(Bullet(bullet_x, enemy.y + enemy.height, direction=1))

        for bullet in self.player_bullets:
            bullet.move()
        for bullet in self.enemy_bullets:
            bullet.move()

        self.player_bullets = [b for b in self.player_bullets if not b.off_screen(self.height)]
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.off_screen(self.height)]

        bullets_to_remove = set()
        alive_enemies = self.enemy_grid.alive_enemies()

        for bullet in self.player_bullets:
            for enemy in alive_enemies:
                if enemy.alive and bullet.rect().colliderect(enemy.rect()):
                    enemy.alive = False
                    bullets_to_remove.add(bullet)
                    self.score += 1
                    break

        if bullets_to_remove:
            self.player_bullets = [b for b in self.player_bullets if b not in bullets_to_remove]

        for bullet in self.enemy_bullets:
            if bullet.rect().colliderect(self.player.rect()):
                self.game_over = True
                self.state = "GAME_OVER"
                break

        if self.enemy_grid.reached_bottom(self.player.y):
            self.game_over = True
            self.state = "GAME_OVER"

    def render(self, screen):
        if self.state == "MENU":
            title = self.large_font.render("SPACE INVADERS", True, GREEN)
            sub = self.font.render("Select Difficulty to Start:", True, WHITE)

            d1 = self.font.render("1 - Easy", True, WHITE if self.current_difficulty != "Easy" else YELLOW)
            d2 = self.font.render("2 - Medium", True, WHITE if self.current_difficulty != "Medium" else YELLOW)
            d3 = self.font.render("3 - Hard", True, WHITE if self.current_difficulty != "Hard" else YELLOW)

            start_txt = self.small_font.render("Press SPACE or RETURN to Start Current Selection", True, WHITE)
            quit_txt = self.small_font.render("Press Q to Quit", True, WHITE)

            screen.blit(title, title.get_rect(center=(self.width // 2, 180)))
            screen.blit(sub, sub.get_rect(center=(self.width // 2, 260)))

            screen.blit(d1, d1.get_rect(center=(self.width // 2, 320)))
            screen.blit(d2, d2.get_rect(center=(self.width // 2, 360)))
            screen.blit(d3, d3.get_rect(center=(self.width // 2, 400)))

            screen.blit(start_txt, start_txt.get_rect(center=(self.width // 2, 480)))
            screen.blit(quit_txt, quit_txt.get_rect(center=(self.width // 2, 520)))
            return

        # Render active gameplay
        pygame.draw.rect(screen, GREEN, self.player.rect())

        for enemy in self.enemy_grid.alive_enemies():
            pygame.draw.rect(screen, WHITE, enemy.rect())

        for bullet in self.player_bullets:
            pygame.draw.rect(screen, WHITE, bullet.rect())
        for bullet in self.enemy_bullets:
            pygame.draw.rect(screen, RED, bullet.rect())

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        diff_text = self.small_font.render(f"Difficulty: {self.current_difficulty}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(diff_text, (self.width - 150, 15))

        if self.state == "GAME_OVER":
            go_surf = self.large_font.render("GAME OVER", True, RED)
            score_surf = self.font.render(f"Final Score: {self.score}", True, WHITE)

            prompt1 = self.small_font.render("Select Difficulty to Play Again:", True, WHITE)
            opts = self.small_font.render("1: Easy  |  2: Medium  |  3: Hard", True, YELLOW)
            prompt2 = self.small_font.render("Press SPACE to Restart Current  |  Q to Quit", True, WHITE)

            screen.blit(go_surf, go_surf.get_rect(center=(self.width // 2, self.height // 2 - 100)))
            screen.blit(score_surf, score_surf.get_rect(center=(self.width // 2, self.height // 2 - 40)))

            screen.blit(prompt1, prompt1.get_rect(center=(self.width // 2, self.height // 2 + 30)))
            screen.blit(opts, opts.get_rect(center=(self.width // 2, self.height // 2 + 60)))
            screen.blit(prompt2, prompt2.get_rect(center=(self.width // 2, self.height // 2 + 100)))