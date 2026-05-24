"""Game entities: Player, Enemies, Bullets, Pickups."""

import pygame
import math
import random
from settings import *
from sprites import *


class Player:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.width = 32
        self.height = 16
        self.has_head = False
        self.has_legs = False
        self.has_gun = False
        self.fire_cooldown = 0
        self.lives = 3
        self.invincible = 0  # frames of invincibility after hit
        self.underground = False
        self.lost_part = None  # track last lost part for guaranteed respawn

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > 10:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - 60:
            self.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.y > 40:
            self.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - 60:
            self.y += PLAYER_SPEED
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1

    def shoot(self):
        if self.fire_cooldown <= 0:
            self.fire_cooldown = PLAYER_FIRE_RATE
            bullets = []

            if self.has_head and self.has_legs and self.has_gun:
                # Full assembly: 5 bullets in forward fan + particle cannon
                import math as _m
                for i in range(5):
                    angle = (i - 2) * 0.15  # spread from -0.3 to +0.3 radians
                    vx = PLAYER_BULLET_SPEED * _m.cos(angle)
                    vy = PLAYER_BULLET_SPEED * _m.sin(angle)
                    bullets.append(Bullet(self.x + 30, self.y + 6, vx, vy))
                bullets.append(ParticleCannon(self.x + 56, self.y + 4))
            else:
                # Base: single forward shot
                bullets.append(Bullet(self.x + 30, self.y + 6, PLAYER_BULLET_SPEED, 0))
                # Head: adds extra shot angled slightly upward-forward
                if self.has_head:
                    bullets.append(Bullet(self.x + 26, self.y - 2, PLAYER_BULLET_SPEED, -1.5))
                # Legs: adds extra shot angled slightly downward-forward
                if self.has_legs:
                    bullets.append(Bullet(self.x + 26, self.y + 14, PLAYER_BULLET_SPEED, 1.5))
                # Wave cannon: slow but powerful particle blast
                if self.has_gun:
                    bullets.append(ParticleCannon(self.x + 56, self.y + 4))
            return bullets
        return []

    def hit(self):
        """Handle being hit. Returns True if player dies."""
        if self.invincible > 0:
            return False
        # If has parts, lose them instead of dying
        if self.has_gun:
            self.has_gun = False
            self.lost_part = PART_WAVE_GUN
            self.invincible = 60
            return False
        elif self.has_head:
            self.has_head = False
            self.lost_part = PART_HEAD
            self.invincible = 60
            return False
        elif self.has_legs:
            self.has_legs = False
            self.lost_part = PART_LEGS
            self.invincible = 60
            return False
        else:
            self.lives -= 1
            self.invincible = 120
            self.x = 100
            self.y = SCREEN_HEIGHT // 2
            return self.lives <= 0

    def draw(self, surface, frame):
        if self.invincible > 0 and (frame // 4) % 2 == 0:
            return  # Blink when invincible
        draw_full_robot(surface, int(self.x), int(self.y),
                        self.has_head, self.has_legs, self.has_gun)


class Bullet:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 10, 4)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x > SCREEN_WIDTH or self.x < 0 or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.alive = False

    def draw(self, surface, frame):
        draw_bullet(surface, int(self.x), int(self.y))


class ParticleCannon:
    """Slow but powerful particle cannon shot. Deals 3x damage."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PLAYER_BULLET_SPEED * 0.5  # slower
        self.alive = True
        self.frame = 0
        self.damage = 3  # hits harder

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y - 4, 18, 12)

    def update(self):
        self.x += self.speed
        self.frame += 1
        if self.x > SCREEN_WIDTH:
            self.alive = False

    def draw(self, surface, frame):
        draw_particle_cannon(surface, int(self.x), int(self.y), self.frame)


class EnemyBullet:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 6, 6)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if (self.x > SCREEN_WIDTH or self.x < -10 or
                self.y < -10 or self.y > SCREEN_HEIGHT + 10):
            self.alive = False

    def draw(self, surface, frame):
        draw_enemy_bullet(surface, int(self.x), int(self.y))


class Enemy:
    def __init__(self, x, y, enemy_type, hp=1):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.hp = hp
        self.alive = True
        self.frame = 0
        self.fire_timer = random.randint(60, 180)
        self.width = 24
        self.height = 20
        self.score_value = {
            # Generic
            "basic": 100, "tank": 200, "turret": 150, "flyer": 300,
            # Deep Sea
            "jellyfish": 150, "anglerfish": 250, "torpedo": 200,
            # Hive
            "wasp": 200, "larva": 100, "beetle": 300,
            # Alien
            "facehugger": 250, "spitter": 200, "crawler": 150,
            # Space
            "drone": 150, "comet": 200, "sentinel": 300,
        }
        self.angle = random.uniform(0, math.pi * 2)
        self.speed = self._get_speed()
        self.start_y = y

    def _get_speed(self):
        speeds = {
            "basic": 2, "tank": 1, "turret": 0, "flyer": 3,
            "jellyfish": 0.8, "anglerfish": 2.5, "torpedo": 5,
            "wasp": 3.5, "larva": 0.5, "beetle": 1,
            "facehugger": 4, "spitter": 1.5, "crawler": 1.5,
            "drone": 2.5, "comet": 4.5, "sentinel": 1.5,
        }
        return speeds.get(self.enemy_type, 1.5)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, player_x, player_y):
        self.frame += 1
        self.x -= SCROLL_SPEED

        if self.enemy_type == "basic":
            self.x -= self.speed
            self.angle += 0.05
            self.y += math.sin(self.angle) * 1.5
        elif self.enemy_type == "tank":
            self.x -= self.speed
        elif self.enemy_type == "turret":
            pass
        elif self.enemy_type == "flyer":
            dx = player_x - self.x
            dy = player_y - self.y
            dist = max(1, math.sqrt(dx * dx + dy * dy))
            self.x += (dx / dist) * self.speed * 0.5 - SCROLL_SPEED
            self.y += (dy / dist) * self.speed
        # --- Deep Sea ---
        elif self.enemy_type == "jellyfish":
            self.y += math.sin(self.frame * 0.04) * 1.2
            self.x -= self.speed * 0.5
        elif self.enemy_type == "anglerfish":
            # Charges toward player in bursts
            if self.frame % 90 < 30:
                dx = player_x - self.x
                dy = player_y - self.y
                dist = max(1, math.sqrt(dx * dx + dy * dy))
                self.x += (dx / dist) * self.speed - SCROLL_SPEED
                self.y += (dy / dist) * self.speed * 0.6
            else:
                self.x -= self.speed * 0.3
                self.y += math.sin(self.frame * 0.03) * 0.8
        elif self.enemy_type == "torpedo":
            self.x -= self.speed
        # --- Hive ---
        elif self.enemy_type == "wasp":
            self.x -= self.speed
            self.angle += 0.12
            self.y += math.sin(self.angle) * 3
        elif self.enemy_type == "larva":
            self.x -= self.speed
            self.y += math.sin(self.frame * 0.02) * 0.3
        elif self.enemy_type == "beetle":
            self.x -= self.speed
        # --- Alien ---
        elif self.enemy_type == "facehugger":
            dx = player_x - self.x
            dy = player_y - self.y
            dist = max(1, math.sqrt(dx * dx + dy * dy))
            self.x += (dx / dist) * self.speed * 0.7 - SCROLL_SPEED
            self.y += (dy / dist) * self.speed * 0.8
        elif self.enemy_type == "spitter":
            self.x -= self.speed
            self.y += math.sin(self.frame * 0.03) * 1
        elif self.enemy_type == "crawler":
            self.x -= self.speed
            # Stick near top or bottom
            target_y = 50 if self.start_y < SCREEN_HEIGHT // 2 else SCREEN_HEIGHT - 70
            self.y += (target_y - self.y) * 0.02
        # --- Space ---
        elif self.enemy_type == "drone":
            self.x -= self.speed
            self.y += math.sin(self.frame * 0.06) * 1.5
        elif self.enemy_type == "comet":
            self.x -= self.speed
            self.y += 1.5 if self.start_y < SCREEN_HEIGHT // 2 else -1.5
        elif self.enemy_type == "sentinel":
            # Orbits a point
            cx = self.x
            self.angle += 0.04
            self.y = self.start_y + math.sin(self.angle) * 40
            self.x -= self.speed * 0.5

        if self.x < -50 or self.y < -50 or self.y > SCREEN_HEIGHT + 50:
            self.alive = False
        self.fire_timer -= 1

    def should_fire(self):
        non_firing = ("basic", "torpedo", "comet", "larva", "facehugger")
        if self.fire_timer <= 0 and self.enemy_type not in non_firing:
            self.fire_timer = random.randint(80, 180)
            return True
        return False

    def fire_at(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = max(1, math.sqrt(dx * dx + dy * dy))
        speed = 3
        return EnemyBullet(self.x, self.y + self.height // 2,
                           dx / dist * speed, dy / dist * speed)

    def draw(self, surface, frame):
        x, y = int(self.x), int(self.y)
        t = self.enemy_type
        if t == "basic":
            draw_enemy_basic(surface, x, y)
        elif t == "tank":
            draw_enemy_tank(surface, x, y)
        elif t == "turret":
            draw_enemy_turret(surface, x, y)
        elif t == "flyer":
            draw_enemy_flyer(surface, x, y)
        elif t == "jellyfish":
            draw_enemy_jellyfish(surface, x, y, self.frame)
        elif t == "anglerfish":
            draw_enemy_anglerfish(surface, x, y, self.frame)
        elif t == "torpedo":
            draw_enemy_torpedo(surface, x, y)
        elif t == "wasp":
            draw_enemy_wasp(surface, x, y, self.frame)
        elif t == "larva":
            draw_enemy_larva(surface, x, y, self.frame)
        elif t == "beetle":
            draw_enemy_beetle(surface, x, y)
        elif t == "facehugger":
            draw_enemy_facehugger(surface, x, y, self.frame)
        elif t == "spitter":
            draw_enemy_spitter(surface, x, y, self.frame)
        elif t == "crawler":
            draw_enemy_crawler(surface, x, y, self.frame)
        elif t == "drone":
            draw_enemy_drone(surface, x, y)
        elif t == "comet":
            draw_enemy_comet(surface, x, y, self.frame)
        elif t == "sentinel":
            draw_enemy_sentinel(surface, x, y, self.frame)


class Boss:
    """Base boss class with stage-specific subclasses."""
    def __init__(self, stage, difficulty=0):
        self.x = SCREEN_WIDTH + 20
        self.y = SCREEN_HEIGHT // 2 - 40
        self.width = 90
        self.height = 80
        self.stage = stage
        self.alive = True
        self.frame = 0
        self.fire_timer = 0
        self.entered = False
        # Stage-specific HP with difficulty multiplier
        hp_table = {STAGE_DEEP_SEA: 40, STAGE_HIVE: 50,
                    STAGE_ALIEN_NEST: 60, STAGE_SPACE: 75}
        _, hp_mult = DIFF_MULTIPLIERS[difficulty]
        self.hp = int(hp_table.get(stage, 50) * hp_mult)
        self.max_hp = self.hp

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, player_x, player_y):
        self.frame += 1
        if not self.entered:
            self.x -= 1.5
            if self.x <= SCREEN_WIDTH - 130:
                self.entered = True
        else:
            # Movement pattern varies by stage
            if self.stage == STAGE_DEEP_SEA:
                self.y += math.sin(self.frame * 0.015) * 2
                self.x += math.cos(self.frame * 0.01) * 0.5
            elif self.stage == STAGE_HIVE:
                self.y += math.sin(self.frame * 0.03) * 2.5
            elif self.stage == STAGE_ALIEN_NEST:
                # Aggressive - moves toward player
                dy = player_y - (self.y + 40)
                self.y += max(-1.5, min(1.5, dy * 0.02))
            else:  # SPACE
                self.y += math.sin(self.frame * 0.02) * 2
                self.x += math.sin(self.frame * 0.015) * 1
        self.fire_timer -= 1

    def should_fire(self):
        if self.entered and self.fire_timer <= 0:
            rate = {STAGE_DEEP_SEA: 45, STAGE_HIVE: 35,
                    STAGE_ALIEN_NEST: 25, STAGE_SPACE: 30}
            self.fire_timer = rate.get(self.stage, 35)
            return True
        return False

    def fire_at(self, player_x, player_y):
        bullets = []
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2

        if self.stage == STAGE_DEEP_SEA:
            # Ink burst - 3 slow spread shots
            for offset in [-0.2, 0, 0.2]:
                angle = math.atan2(player_y - cy, player_x - cx) + offset
                bullets.append(EnemyBullet(cx, cy,
                               math.cos(angle) * 2.5, math.sin(angle) * 2.5))
        elif self.stage == STAGE_HIVE:
            # Stinger barrage - 5 fast narrow spread
            for offset in [-0.15, -0.07, 0, 0.07, 0.15]:
                angle = math.atan2(player_y - cy, player_x - cx) + offset
                bullets.append(EnemyBullet(cx, cy,
                               math.cos(angle) * 4, math.sin(angle) * 4))
        elif self.stage == STAGE_ALIEN_NEST:
            # Acid spray - wide fan
            for offset in [-0.4, -0.2, 0, 0.2, 0.4]:
                angle = math.atan2(player_y - cy, player_x - cx) + offset
                speed = 3 + random.uniform(-0.5, 0.5)
                bullets.append(EnemyBullet(cx, cy,
                               math.cos(angle) * speed, math.sin(angle) * speed))
        else:  # SPACE
            # Laser burst - 4 precise shots
            for offset in [-0.1, -0.03, 0.03, 0.1]:
                angle = math.atan2(player_y - cy, player_x - cx) + offset
                bullets.append(EnemyBullet(cx, cy,
                               math.cos(angle) * 5, math.sin(angle) * 5))
        return bullets

    def draw(self, surface, frame):
        x, y = int(self.x), int(self.y)
        if self.stage == STAGE_DEEP_SEA:
            self._draw_deep_sea_boss(surface, x, y)
        elif self.stage == STAGE_HIVE:
            self._draw_hive_boss(surface, x, y)
        elif self.stage == STAGE_ALIEN_NEST:
            self._draw_alien_boss(surface, x, y)
        else:
            self._draw_space_boss(surface, x, y)
        # HP bar
        bar_width = 70
        hp_ratio = self.hp / self.max_hp
        bar_x = x + (self.width - bar_width) // 2
        pygame.draw.rect(surface, RED, (bar_x, y - 12, bar_width, 6))
        pygame.draw.rect(surface, GREEN, (bar_x, y - 12, int(bar_width * hp_ratio), 6))
        pygame.draw.rect(surface, WHITE, (bar_x, y - 12, bar_width, 6), 1)

    def _draw_deep_sea_boss(self, surface, x, y):
        """Mechanized deep-sea leviathan - metal plating with bioluminescent accents."""
        # Armored body hull
        pygame.draw.ellipse(surface, (50, 55, 70), (x + 10, y + 20, 70, 50))
        pygame.draw.ellipse(surface, (80, 90, 100), (x + 15, y + 25, 60, 40))
        # Metal plate lines
        for i in range(4):
            px = x + 20 + i * 15
            pygame.draw.line(surface, (120, 130, 140), (px, y + 25), (px, y + 60), 1)
        # Rivets
        for i in range(5):
            rx = x + 18 + i * 12
            pygame.draw.circle(surface, (160, 170, 180), (rx, y + 28), 2)
            pygame.draw.circle(surface, (160, 170, 180), (rx, y + 58), 2)
        # Mechanical jaw
        jaw_open = 5 + int(math.sin(self.frame * 0.05) * 4)
        pygame.draw.polygon(surface, (70, 75, 85),
                            [(x + 5, y + 40), (x, y + 45 + jaw_open),
                             (x + 30, y + 55 + jaw_open), (x + 35, y + 45)])
        pygame.draw.polygon(surface, (100, 110, 120),
                            [(x + 5, y + 40), (x, y + 45 + jaw_open),
                             (x + 30, y + 55 + jaw_open), (x + 35, y + 45)], 2)
        # Chrome teeth
        for i in range(5):
            tx = x + 5 + i * 6
            pygame.draw.polygon(surface, (200, 210, 220),
                                [(tx, y + 45 + jaw_open), (tx + 3, y + 52 + jaw_open),
                                 (tx + 6, y + 45 + jaw_open)])
        # Angler lure - neon cyan
        lure_y = y + 5 + int(math.sin(self.frame * 0.08) * 4)
        pygame.draw.line(surface, (100, 110, 120), (x + 40, y + 20), (x + 35, lure_y), 2)
        glow = 8 + int(math.sin(self.frame * 0.1) * 3)
        pygame.draw.circle(surface, (0, 255, 255), (x + 35, lure_y), glow)
        pygame.draw.circle(surface, WHITE, (x + 35, lure_y), glow // 2)
        # Glowing red eye
        pygame.draw.circle(surface, (40, 40, 50), (x + 55, y + 32), 8)
        pygame.draw.circle(surface, (255, 50, 0), (x + 55, y + 32), 6)
        pygame.draw.circle(surface, (255, 200, 0), (x + 55, y + 32), 3)
        # Armored fins
        fin_wave = int(math.sin(self.frame * 0.06) * 5)
        pygame.draw.polygon(surface, (90, 100, 110),
                            [(x + 70, y + 30), (x + 90, y + 25 + fin_wave),
                             (x + 85, y + 45 + fin_wave), (x + 70, y + 45)])
        pygame.draw.polygon(surface, (140, 150, 160),
                            [(x + 70, y + 30), (x + 90, y + 25 + fin_wave),
                             (x + 85, y + 45 + fin_wave), (x + 70, y + 45)], 1)

    def _draw_hive_boss(self, surface, x, y):
        """Cybernetic insect queen - chitin armor with metallic exoskeleton."""
        # Armored abdomen
        pygame.draw.ellipse(surface, (80, 70, 20), (x + 40, y + 40, 50, 35))
        pygame.draw.ellipse(surface, (120, 100, 30), (x + 42, y + 42, 46, 31), 2)
        # Chrome stripes
        for i in range(4):
            stripe_x = x + 48 + i * 10
            pygame.draw.rect(surface, (180, 160, 0), (stripe_x, y + 48, 4, 20))
        # Metal thorax
        pygame.draw.ellipse(surface, (100, 90, 40), (x + 25, y + 35, 30, 25))
        pygame.draw.ellipse(surface, (150, 140, 60), (x + 25, y + 35, 30, 25), 2)
        # Head with chrome plating
        pygame.draw.ellipse(surface, (110, 100, 50), (x + 10, y + 30, 25, 20))
        # Compound eyes - bright red/orange contrast
        pygame.draw.circle(surface, (50, 45, 30), (x + 18, y + 36), 7)
        pygame.draw.circle(surface, (255, 0, 0), (x + 18, y + 36), 5)
        pygame.draw.circle(surface, (255, 150, 0), (x + 18, y + 36), 2)
        pygame.draw.circle(surface, (50, 45, 30), (x + 28, y + 36), 7)
        pygame.draw.circle(surface, (255, 0, 0), (x + 28, y + 36), 5)
        pygame.draw.circle(surface, (255, 150, 0), (x + 28, y + 36), 2)
        # Steel mandibles
        mand = int(math.sin(self.frame * 0.07) * 3)
        pygame.draw.polygon(surface, (180, 180, 190),
                            [(x + 10, y + 42), (x + 2, y + 48 + mand), (x + 12, y + 48)])
        pygame.draw.polygon(surface, (180, 180, 190),
                            [(x + 10, y + 48), (x + 2, y + 54 - mand), (x + 12, y + 50)])
        # Metallic wings
        wing_y = int(math.sin(self.frame * 0.15) * 3)
        pygame.draw.ellipse(surface, (180, 180, 140),
                            (x + 30, y + 10 + wing_y, 40, 20))
        pygame.draw.ellipse(surface, (220, 220, 180),
                            (x + 30, y + 10 + wing_y, 40, 20), 1)
        pygame.draw.ellipse(surface, (180, 180, 140),
                            (x + 30, y + 55 - wing_y, 40, 20))
        pygame.draw.ellipse(surface, (220, 220, 180),
                            (x + 30, y + 55 - wing_y, 40, 20), 1)
        # Chrome stinger
        pygame.draw.polygon(surface, (200, 200, 210),
                            [(x + 85, y + 54), (x + 98, y + 57), (x + 85, y + 60)])
        pygame.draw.polygon(surface, (255, 255, 0),
                            [(x + 93, y + 56), (x + 98, y + 57), (x + 93, y + 58)])
        # Armored legs
        for i in range(3):
            ly = y + 50 + i * 6
            pygame.draw.line(surface, (140, 130, 60), (x + 30, ly), (x + 20, ly + 10), 3)
            pygame.draw.line(surface, (140, 130, 60), (x + 55, ly), (x + 65, ly + 10), 3)

    def _draw_alien_boss(self, surface, x, y):
        """Biomechanical xenomorph - dark metal skeleton with acid green highlights."""
        # Elongated chrome skull
        pygame.draw.ellipse(surface, (40, 40, 50), (x, y + 15, 50, 20))
        pygame.draw.ellipse(surface, (70, 70, 80), (x + 2, y + 17, 46, 16), 1)
        pygame.draw.ellipse(surface, (50, 50, 60), (x + 5, y + 10, 20, 30))
        # Inner jaw - chrome with green drool
        jaw = int(math.sin(self.frame * 0.06) * 3)
        pygame.draw.rect(surface, (150, 150, 160), (x + 2, y + 30 + jaw, 12, 5))
        pygame.draw.rect(surface, (200, 200, 210), (x + 3, y + 30 + jaw, 10, 2))
        # Armored body - dark steel with visible structure
        pygame.draw.ellipse(surface, (45, 45, 55), (x + 20, y + 30, 50, 40))
        pygame.draw.ellipse(surface, (80, 80, 90), (x + 20, y + 30, 50, 40), 2)
        # Chrome ribs
        for i in range(4):
            ry = y + 35 + i * 8
            pygame.draw.arc(surface, (160, 160, 170),
                            (x + 25, ry, 40, 10), 0, math.pi, 2)
        # Reactor core - bright green
        pygame.draw.circle(surface, (0, 255, 80), (x + 45, y + 48), 5)
        pygame.draw.circle(surface, (150, 255, 150), (x + 45, y + 48), 3)
        # Metal tail
        tail_pts = []
        for i in range(8):
            tx = x + 65 + i * 5
            ty = y + 50 + int(math.sin((self.frame * 0.04) + i * 0.5) * (3 + i))
            tail_pts.append((tx, ty))
        if len(tail_pts) > 1:
            pygame.draw.lines(surface, (100, 100, 110), False, tail_pts, 4)
            pygame.draw.lines(surface, (150, 150, 160), False, tail_pts, 2)
        # Tail blade - bright chrome
        if tail_pts:
            last = tail_pts[-1]
            pygame.draw.polygon(surface, (200, 200, 210),
                                [(last[0], last[1] - 6), (last[0] + 10, last[1]),
                                 (last[0], last[1] + 6)])
            pygame.draw.polygon(surface, (240, 240, 250),
                                [(last[0], last[1] - 6), (last[0] + 10, last[1]),
                                 (last[0], last[1] + 6)], 1)
        # Chrome claws
        claw_y = int(math.sin(self.frame * 0.05) * 4)
        pygame.draw.line(surface, (160, 160, 170), (x + 25, y + 40),
                         (x + 10, y + 55 + claw_y), 3)
        pygame.draw.line(surface, (160, 160, 170), (x + 25, y + 45),
                         (x + 8, y + 62 + claw_y), 3)
        # Claw tips - bright
        pygame.draw.circle(surface, (200, 255, 0), (x + 10, y + 55 + claw_y), 3)
        pygame.draw.circle(surface, (200, 255, 0), (x + 8, y + 62 + claw_y), 3)
        # Acid drip - neon green
        if self.frame % 20 < 10:
            drip = (self.frame % 20) * 2
            pygame.draw.circle(surface, (0, 255, 50), (x + 5, y + 36 + drip), 3)
            pygame.draw.circle(surface, (150, 255, 100), (x + 5, y + 36 + drip), 1)

    def _draw_space_boss(self, surface, x, y):
        """Cosmic mech-horror - metallic shell with eldritch energy."""
        # Outer armored shell
        pulse = int(math.sin(self.frame * 0.03) * 3)
        pygame.draw.circle(surface, (60, 60, 70), (x + 45, y + 40), 34 + pulse)
        pygame.draw.circle(surface, (90, 90, 100), (x + 45, y + 40), 34 + pulse, 3)
        # Inner hull
        pygame.draw.circle(surface, (40, 40, 55), (x + 45, y + 40), 26 + pulse)
        pygame.draw.circle(surface, (110, 110, 130), (x + 45, y + 40), 26 + pulse, 2)
        # Central eye - intense contrast
        pygame.draw.circle(surface, (30, 30, 40), (x + 45, y + 40), 12)
        pygame.draw.circle(surface, (255, 220, 0), (x + 45, y + 40), 10)
        pygame.draw.circle(surface, (255, 0, 0), (x + 45, y + 40), 6)
        pygame.draw.circle(surface, (0, 0, 0), (x + 45, y + 40), 3)
        # Metal tentacles with glowing tips
        for i in range(6):
            angle = (i / 6) * math.pi * 2 + self.frame * 0.02
            pts = []
            for seg in range(6):
                seg_angle = angle + math.sin(self.frame * 0.03 + seg * 0.5) * 0.3
                sx = x + 45 + int(math.cos(seg_angle) * (28 + seg * 9))
                sy = y + 40 + int(math.sin(seg_angle) * (22 + seg * 7))
                pts.append((sx, sy))
            if len(pts) > 1:
                pygame.draw.lines(surface, (120, 120, 140), False, pts, 3)
                pygame.draw.lines(surface, (170, 170, 190), False, pts, 1)
            # Glowing tip
            if pts:
                pygame.draw.circle(surface, (200, 0, 255), pts[-1], 4)
                pygame.draw.circle(surface, (255, 150, 255), pts[-1], 2)
        # Energy crackling - bright purple/white
        if self.frame % 8 < 4:
            for _ in range(4):
                ex = x + 45 + random.randint(-30, 30)
                ey = y + 40 + random.randint(-30, 30)
                pygame.draw.circle(surface, (220, 100, 255), (ex, ey), 3)
                pygame.draw.circle(surface, WHITE, (ex, ey), 1)
        # Armor plate details
        for i in range(4):
            angle = (i / 4) * math.pi * 2 + 0.4
            px = x + 45 + int(math.cos(angle) * 30)
            py = y + 40 + int(math.sin(angle) * 24)
            pygame.draw.rect(surface, (140, 140, 160), (px - 4, py - 2, 8, 4))
            pygame.draw.rect(surface, (180, 180, 200), (px - 4, py - 2, 8, 4), 1)


class PartPickup:
    def __init__(self, x, y, part_type):
        self.x = x
        self.y = y
        self.part_type = part_type
        self.alive = True
        self.width = 24
        self.height = 20

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= SCROLL_SPEED
        if self.x < -30:
            self.alive = False

    def draw(self, surface, frame):
        # Pulsing glow
        glow_size = 2 + (frame % 30) // 10
        pygame.draw.circle(surface, (0, 80, 0), (int(self.x) + 12, int(self.y) + 10),
                           14 + glow_size)
        draw_part_pickup(surface, int(self.x), int(self.y), self.part_type)


class LifeUpPickup:
    """Rare life up item."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.part_type = "life_up"
        self.alive = True
        self.width = 24
        self.height = 20

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= SCROLL_SPEED
        if self.x < -30:
            self.alive = False

    def draw(self, surface, frame):
        x, y = int(self.x), int(self.y)
        # Red pulsing glow
        glow_size = 2 + (frame % 20) // 5
        pygame.draw.circle(surface, (100, 0, 0), (x + 12, y + 10), 14 + glow_size)
        # Heart / cross shape
        pygame.draw.rect(surface, (255, 50, 50), (x + 8, y + 4, 8, 14))
        pygame.draw.rect(surface, (255, 50, 50), (x + 4, y + 8, 16, 6))
        # White highlight
        pygame.draw.rect(surface, (255, 200, 200), (x + 10, y + 6, 4, 4))


class WarpHole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.width = 32
        self.height = 16

    @property
    def rect(self):
        return pygame.Rect(self.x - 16, self.y - 8, self.width, self.height)

    def update(self):
        self.x -= SCROLL_SPEED
        if self.x < -40:
            self.alive = False

    def draw(self, surface, frame):
        draw_warp_hole(surface, int(self.x), int(self.y), frame)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.alive = True
        self.max_frames = 20

    def update(self):
        self.frame += 1
        if self.frame >= self.max_frames:
            self.alive = False

    def draw(self, surface, frame):
        progress = self.frame / self.max_frames
        radius = int(8 + progress * 20)
        color = (255, max(0, 200 - int(progress * 200)), 0)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), radius)
        if radius > 4:
            pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), radius // 2)


class BigExplosion:
    """Large boss death explosion with multiple rings."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.alive = True
        self.max_frames = 60

    def update(self):
        self.frame += 1
        if self.frame >= self.max_frames:
            self.alive = False

    def draw(self, surface, frame):
        progress = self.frame / self.max_frames
        # Expanding white flash
        if progress < 0.2:
            flash_r = int(progress * 5 * 80)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), flash_r)
        # Multiple expanding rings
        for i in range(3):
            ring_progress = max(0, progress - i * 0.15)
            if ring_progress > 0 and ring_progress < 1:
                radius = int(ring_progress * 100)
                thickness = max(1, int(4 * (1 - ring_progress)))
                colors = [(255, 100, 0), (255, 200, 0), (255, 50, 50)]
                pygame.draw.circle(surface, colors[i],
                                   (int(self.x), int(self.y)), radius, thickness)
        # Core fireball
        if progress < 0.6:
            core_r = int(30 * (1 - progress / 0.6))
            pygame.draw.circle(surface, (255, 150, 0), (int(self.x), int(self.y)), core_r)
            pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), core_r // 2)
