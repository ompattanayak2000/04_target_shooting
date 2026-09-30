"""
GameEngine: owns the targets and handles player clicks.

Targets move continuously with different speeds and bounce off
the play-area edges. The game also tracks score, combo, and a
30-second round timer.
"""

import random
import time

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.targets = []
        self.velocities = []
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 1
        self.round_active = True
        self.start_time = time.time()

        self._start_new_round()

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)
        return Target(x, y, radius=TARGET_RADIUS)

    def _start_new_round(self):
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]

        self.velocities = [
            [2.0, 1.5],
            [-1.5, 2.5],
            [2.5, -2.0],
        ]

        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 1
        self.start_time = time.time()
        self.round_active = True

    def get_time_left(self):
        elapsed = time.time() - self.start_time
        return max(0, ROUND_DURATION - int(elapsed))

    def handle_click(self, pos):
        if not self.round_active:
            return

        target = check_hit(self.targets, pos)

        if target is not None:
            self.hits += 1
            self.score += 10 * self.combo
            self.combo += 1

            index = self.targets.index(target)
            self.targets.remove(target)
            self.targets.append(self._random_target())

            velocity = self.velocities.pop(index)
            self.velocities.append(velocity)

        else:
            self.misses += 1
            self.combo = 1

    def update(self):
        if self.round_active:
            if self.get_time_left() <= 0:
                self.round_active = False
                return

            for i, target in enumerate(self.targets):
                dx, dy = self.velocities[i]

                target.x += dx
                target.y += dy

                if target.x - target.radius <= 0:
                    target.x = target.radius
                    dx = abs(dx)
                elif target.x + target.radius >= WIDTH:
                    target.x = WIDTH - target.radius
                    dx = -abs(dx)

                if target.y - target.radius <= 0:
                    target.y = target.radius
                    dy = abs(dy)
                elif target.y + target.radius >= HEIGHT:
                    target.y = HEIGHT - target.radius
                    dy = -abs(dy)

                self.velocities[i] = [dx, dy]

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.targets)

        if self.round_active:
            time_left = self.get_time_left()

            renderer.draw_text(
                surface,
                font,
                f"Score: {self.score}  Combo: x{self.combo}",
                (10, 10),
            )

            renderer.draw_text(
                surface,
                font,
                f"Time: {time_left}s",
                (10, 40),
            )

            renderer.draw_text(
                surface,
                font,
                f"Hits: {self.hits}  Misses: {self.misses}",
                (10, 70),
            )

        else:
            renderer.draw_text(
                surface,
                font,
                "TIME UP!",
                (10, 10),
            )

            renderer.draw_text(
                surface,
                font,
                f"Final Score: {self.score}",
                (10, 40),
            )

            renderer.draw_text(
                surface,
                font,
                "Press R to start a new round",
                (10, 70),
            )