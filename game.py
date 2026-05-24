"""Main game logic and stage management."""

import pygame
import random
import math
from settings import *
from entities import *


class Background:
    """Parallax scrolling background per stage theme."""

    def __init__(self):
        self.offset = 0
        self.stars = [(random.randint(0, SCREEN_WIDTH),
                       random.randint(0, SCREEN_HEIGHT),
                       random.uniform(0.5, 2.0)) for _ in range(60)]
        # Nebula blobs for space stage (pre-generated)
        self.nebulae = [(random.randint(0, SCREEN_WIDTH * 3),
                         random.randint(20, SCREEN_HEIGHT - 20),
                         random.randint(30, 80),
                         random.choice([(40, 0, 60), (0, 20, 60), (60, 0, 40),
                                        (20, 0, 50), (0, 40, 50)]))
                        for _ in range(15)]

    def update(self):
        self.offset += SCROLL_SPEED

    def draw(self, surface, stage, underground):
        if underground:
            surface.fill((10, 5, 20))
            for i in range(0, SCREEN_WIDTH, 40):
                h = 20 + int(math.sin((i + self.offset) * 0.03) * 10)
                pygame.draw.rect(surface, DARK_BROWN, (i, 0, 40, h))
                pygame.draw.rect(surface, DARK_BROWN,
                                 (i, SCREEN_HEIGHT - h - 10, 40, h + 10))
            return

        if stage == STAGE_DEEP_SEA:
            self._draw_deep_sea(surface)
        elif stage == STAGE_HIVE:
            self._draw_hive(surface)
        elif stage == STAGE_ALIEN_NEST:
            self._draw_alien_nest(surface)
        elif stage == STAGE_SPACE:
            self._draw_space(surface)

    def _draw_deep_sea(self, surface):
        """Dark ocean depths with bioluminescent particles."""
        surface.fill((0, 5, 30))
        # Water gradient layers
        for row in range(6):
            y = row * 100
            alpha = 10 + row * 3
            color = (0, alpha, 40 + row * 8)
            pygame.draw.rect(surface, color, (0, y, SCREEN_WIDTH, 100))
        # Floating particles (bioluminescence)
        for sx, sy, sp in self.stars[:30]:
            nx = (sx - self.offset * sp * 0.5) % SCREEN_WIDTH
            ny = (sy + math.sin((self.offset + sx) * 0.01) * 3) % SCREEN_HEIGHT
            color = random.choice([(0, 200, 200), (0, 150, 255), (100, 255, 200)])
            pygame.draw.circle(surface, color, (int(nx), int(ny)), 1)
        # Seabed
        for i in range(0, SCREEN_WIDTH, 30):
            h = 15 + int(math.sin((i + self.offset * 0.3) * 0.04) * 10)
            pygame.draw.rect(surface, (10, 20, 40), (i, SCREEN_HEIGHT - h, 30, h))

    def _draw_hive(self, surface):
        """Organic insect hive with honeycomb patterns."""
        surface.fill((40, 25, 10))
        # Honeycomb pattern on walls
        for i in range(0, SCREEN_WIDTH, 24):
            for j in range(0, 60, 20):
                hx = (i - int(self.offset * 0.2)) % (SCREEN_WIDTH + 24)
                offset_y = 8 if (i // 24) % 2 else 0
                pygame.draw.polygon(surface, (60, 35, 10), [
                    (hx + 12, j + offset_y), (hx + 22, j + 6 + offset_y),
                    (hx + 22, j + 14 + offset_y), (hx + 12, j + 20 + offset_y),
                    (hx + 2, j + 14 + offset_y), (hx + 2, j + 6 + offset_y)], 1)
        # Floor with organic texture
        for i in range(0, SCREEN_WIDTH, 40):
            h = 20 + int(math.sin((i + self.offset * 0.4) * 0.05) * 12)
            pygame.draw.rect(surface, (50, 30, 15), (i, SCREEN_HEIGHT - h, 40, h))
            pygame.draw.ellipse(surface, (70, 40, 20),
                                (i + 5, SCREEN_HEIGHT - h - 5, 30, 10))
        # Dripping slime
        for sx, sy, sp in self.stars[:15]:
            nx = (sx - self.offset * 0.3) % SCREEN_WIDTH
            drip_len = 10 + int(abs(math.sin(self.offset * 0.02 + sx)) * 20)
            pygame.draw.line(surface, (80, 120, 20), (int(nx), 0), (int(nx), drip_len), 2)

    def _draw_alien_nest(self, surface):
        """Alien organic environment with pulsing walls."""
        surface.fill((15, 0, 20))
        # Pulsing organic walls
        pulse = math.sin(self.offset * 0.03) * 5
        for i in range(0, SCREEN_WIDTH, 50):
            h_top = 30 + int(math.sin((i + self.offset * 0.5) * 0.03) * 15 + pulse)
            h_bot = 40 + int(math.cos((i + self.offset * 0.4) * 0.04) * 12 + pulse)
            pygame.draw.rect(surface, (40, 0, 30), (i, 0, 50, h_top))
            pygame.draw.rect(surface, (40, 0, 30),
                             (i, SCREEN_HEIGHT - h_bot, 50, h_bot))
            # Veins
            pygame.draw.line(surface, (80, 0, 50),
                             (i + 25, 0), (i + 15, h_top), 1)
            pygame.draw.line(surface, (80, 0, 50),
                             (i + 25, SCREEN_HEIGHT),
                             (i + 35, SCREEN_HEIGHT - h_bot), 1)
        # Floating spores
        for sx, sy, sp in self.stars[:20]:
            nx = (sx - self.offset * sp * 0.6) % SCREEN_WIDTH
            ny = sy + math.sin((self.offset * 0.02 + sx * 0.1)) * 10
            pygame.draw.circle(surface, (100, 0, 80), (int(nx), int(ny) % SCREEN_HEIGHT), 2)

    def _draw_space(self, surface):
        """Outer space with nebulae and distant stars."""
        surface.fill((2, 2, 10))
        # Nebula clouds (large colored blobs)
        for nx, ny, size, color in self.nebulae:
            draw_x = (nx - int(self.offset * 0.3)) % (SCREEN_WIDTH + 200) - 100
            # Draw layered circles for nebula effect
            for layer in range(3):
                r = size - layer * 10
                if r > 0:
                    c = tuple(min(255, v + layer * 15) for v in color)
                    pygame.draw.circle(surface, c, (draw_x, ny), r)
        # Stars (different layers for parallax)
        for sx, sy, sp in self.stars:
            nx = (sx - self.offset * sp) % SCREEN_WIDTH
            brightness = int(150 + sp * 50)
            size = 1 if sp < 1.5 else 2
            pygame.draw.circle(surface, (brightness, brightness, brightness),
                               (int(nx), int(sy)), size)
        # Distant galaxy streak
        gx = (500 - int(self.offset * 0.1)) % (SCREEN_WIDTH + 300) - 150
        pygame.draw.ellipse(surface, (20, 10, 40), (gx, 80, 120, 30))
        pygame.draw.ellipse(surface, (30, 15, 50), (gx + 20, 88, 80, 14))


class StageManager:
    """Manages enemy spawning and stage progression."""

    def __init__(self, difficulty=0):
        self.current_stage = STAGE_DEEP_SEA
        self.stage_progress = 0
        self.spawn_timer = 0
        self.part_timer = 0
        self.warp_timer = 0
        self.boss_spawned = False
        self.difficulty = difficulty
        self.spawn_mult, self.hp_mult = DIFF_MULTIPLIERS[difficulty]

    def update(self, enemies, parts, warps, underground, player=None):
        """Returns event string or None. Pass player for smart part spawning."""
        self.stage_progress += SCROLL_SPEED
        self.spawn_timer -= 1
        self.part_timer -= 1
        self.warp_timer -= 1

        # Boss at end of every stage
        if (self.stage_progress >= STAGE_LENGTH and not self.boss_spawned):
            self.boss_spawned = True
            return "spawn_boss"

        # Spawn enemies
        if self.spawn_timer <= 0:
            self._spawn_enemy(enemies, underground)
            stage_diff = 1 + self.current_stage * 0.3
            self.spawn_timer = int(random.randint(40, 90) / (stage_diff * self.spawn_mult))

        # Spawn parts occasionally (smart)
        if self.part_timer <= 0:
            self._spawn_part(parts, player)
            # Also small chance of life_up alongside the part
            if random.random() < 0.08:
                self._spawn_life_up(parts)
            # Higher difficulty = more frequent parts to compensate for more enemies
            base_min, base_max = 350, 700
            part_divisor = {0: 1.0, 1: 1.5, 2: 2.0}[self.difficulty]
            self.part_timer = int(random.randint(base_min, base_max) / part_divisor)

        # Spawn warp holes (surface only)
        if not underground and self.warp_timer <= 0:
            self.warp_timer = random.randint(500, 1000)
            warps.append(WarpHole(SCREEN_WIDTH + 20,
                                  random.randint(200, SCREEN_HEIGHT - 100)))

        return None

    def next_stage(self):
        self.current_stage = (self.current_stage + 1) % 4
        self.stage_progress = 0
        self.boss_spawned = False

    def _spawn_enemy(self, enemies, underground):
        y = random.randint(50, SCREEN_HEIGHT - 100)
        x = SCREEN_WIDTH + random.randint(10, 60)

        stage = self.current_stage
        if underground:
            etype = random.choice(["basic", "basic", "flyer", "flyer"])
        elif stage == STAGE_DEEP_SEA:
            etype = random.choice(["jellyfish", "jellyfish", "anglerfish",
                                   "torpedo", "jellyfish", "anglerfish"])
        elif stage == STAGE_HIVE:
            etype = random.choice(["wasp", "wasp", "larva", "beetle",
                                   "wasp", "beetle"])
        elif stage == STAGE_ALIEN_NEST:
            etype = random.choice(["facehugger", "facehugger", "spitter",
                                   "crawler", "spitter", "facehugger"])
        else:  # SPACE
            etype = random.choice(["drone", "drone", "comet", "sentinel",
                                   "drone", "sentinel"])

        hp_table = {
            "jellyfish": 1, "anglerfish": 2, "torpedo": 1,
            "wasp": 1, "larva": 1, "beetle": 3,
            "facehugger": 1, "spitter": 2, "crawler": 2,
            "drone": 1, "comet": 1, "sentinel": 2,
        }
        hp = hp_table.get(etype, 1)
        enemies.append(Enemy(x, y, etype, hp))

    def _spawn_part(self, parts, player=None):
        """Spawn parts. If player just lost a part, guarantee that part next."""
        if player:
            # If player just lost a part, force spawn that part
            if player.lost_part:
                part_type = player.lost_part
                player.lost_part = None
            else:
                missing = []
                if not player.has_head:
                    missing.append(PART_HEAD)
                if not player.has_legs:
                    missing.append(PART_LEGS)
                if not player.has_gun:
                    missing.append(PART_WAVE_GUN)

                if not missing:
                    # Player has all parts - no part to spawn
                    return
                else:
                    if random.random() < 0.85:
                        part_type = random.choice(missing)
                    else:
                        part_type = random.choice([PART_HEAD, PART_LEGS, PART_WAVE_GUN])
        else:
            part_type = random.choice([PART_HEAD, PART_LEGS, PART_WAVE_GUN])

        x = SCREEN_WIDTH + 20
        y = random.randint(100, SCREEN_HEIGHT - 120)
        parts.append(PartPickup(x, y, part_type))

    def _spawn_life_up(self, parts):
        """Spawn a life up pickup (rare)."""
        x = SCREEN_WIDTH + 20
        y = random.randint(100, SCREEN_HEIGHT - 120)
        parts.append(LifeUpPickup(x, y))
