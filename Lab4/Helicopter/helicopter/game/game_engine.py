"""
GameEngine: owns the helicopter and all obstacles.

The helicopter moves and obstacles scroll by. Tasks 2 adds obstacle
collision detection and a game-over state. Task 3 adds distance
scoring. Task 4 adds a one-collision shield.
"""

import random

import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0
        self.shield_active = False
        # A shielded collision is ignored only while the helicopter remains
        # in contact with that same obstacle. This prevents one overlap from
        # being counted as multiple collisions across consecutive frames.
        self._shielded_obstacles = set()

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self.__init__()
        elif key == pygame.K_SPACE and not self.game_over and not self.shield_active:
            self.shield_active = True

    def update(self):
        if self.game_over:
            return

        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()

        # Distance represents horizontal game-world progress. It advances
        # with the obstacle scroll while the game is actively running, not
        # according to the player's vertical input.
        self.distance += SCROLL_SPEED

        helicopter_rect = self.helicopter.get_rect()
        current_collisions = set()
        for obstacle in self.obstacles:
            collides = (
                helicopter_rect.colliderect(obstacle.get_top_rect()) or
                helicopter_rect.colliderect(obstacle.get_bottom_rect())
            )
            if not collides:
                continue

            current_collisions.add(obstacle)
            if obstacle in self._shielded_obstacles:
                # This is the same continuous contact that the shield already
                # absorbed, so it must not be treated as another collision.
                continue

            if self.shield_active:
                self.shield_active = False
                self._shielded_obstacles.add(obstacle)
                continue

            self.game_over = True
            break

        # Once the helicopter is no longer touching an obstacle whose hit was
        # absorbed, a future contact with that obstacle is a new collision.
        self._shielded_obstacles.intersection_update(current_collisions)

        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(
            surface, self.helicopter, self.obstacles,
            shield_active=self.shield_active,
        )
        renderer.draw_distance(surface, font, self.distance)
        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER")
