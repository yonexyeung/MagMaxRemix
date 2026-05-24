"""Sprite drawing utilities - procedural pixel art."""

import math
import pygame
from settings import *


def draw_ship_body(surface, x, y):
    """Draw the basic MagMax body - sleek mecha fighter core."""
    # Main fuselage - angular fighter shape
    body_pts = [(x + 2, y + 8), (x + 10, y + 2), (x + 24, y + 2),
                (x + 30, y + 6), (x + 30, y + 12), (x + 24, y + 16),
                (x + 10, y + 16), (x + 2, y + 10)]
    pygame.draw.polygon(surface, (180, 180, 200), body_pts)
    pygame.draw.polygon(surface, (220, 220, 240), body_pts, 1)
    # Cockpit canopy
    pygame.draw.polygon(surface, (0, 180, 220),
                        [(x + 14, y + 5), (x + 22, y + 5),
                         (x + 20, y + 9), (x + 14, y + 9)])
    # Wing stubs
    pygame.draw.polygon(surface, (140, 140, 160),
                        [(x + 8, y + 2), (x + 16, y), (x + 18, y + 2)])
    pygame.draw.polygon(surface, (140, 140, 160),
                        [(x + 8, y + 16), (x + 16, y + 18), (x + 18, y + 16)])
    # Engine thruster
    pygame.draw.rect(surface, (60, 60, 80), (x, y + 6, 4, 6))
    pygame.draw.rect(surface, ORANGE, (x - 3, y + 7, 4, 4))
    pygame.draw.rect(surface, YELLOW, (x - 2, y + 8, 2, 2))
    # Nose detail
    pygame.draw.rect(surface, CYAN, (x + 28, y + 7, 4, 4))
    pygame.draw.rect(surface, WHITE, (x + 29, y + 8, 2, 2))


def draw_head(surface, x, y):
    """Draw Gundam-style robot head."""
    # Helmet - angular V-shape
    pygame.draw.rect(surface, (200, 200, 210), (x + 4, y + 4, 16, 10))
    # V-fin (iconic Gundam antenna)
    pygame.draw.polygon(surface, YELLOW,
                        [(x + 12, y + 4), (x + 6, y - 4), (x + 8, y - 3), (x + 12, y + 2)])
    pygame.draw.polygon(surface, YELLOW,
                        [(x + 12, y + 4), (x + 18, y - 4), (x + 16, y - 3), (x + 12, y + 2)])
    # Face plate
    pygame.draw.rect(surface, GRAY, (x + 7, y + 7, 10, 6))
    # Eyes - green visor
    pygame.draw.rect(surface, (0, 255, 100), (x + 8, y + 8, 4, 3))
    pygame.draw.rect(surface, (0, 255, 100), (x + 13, y + 8, 4, 3))
    # Chin guard
    pygame.draw.polygon(surface, (180, 180, 190),
                        [(x + 9, y + 13), (x + 15, y + 13), (x + 12, y + 16)])


def draw_legs(surface, x, y):
    """Draw Gundam-style robot legs."""
    # Hip/waist armor
    pygame.draw.rect(surface, (80, 80, 100), (x + 2, y, 20, 5))
    # Left thigh
    pygame.draw.rect(surface, (200, 200, 210), (x + 3, y + 5, 8, 10))
    pygame.draw.rect(surface, BLUE, (x + 4, y + 6, 6, 4))  # armor plate
    # Left shin
    pygame.draw.rect(surface, (200, 200, 210), (x + 4, y + 15, 6, 10))
    # Left foot
    pygame.draw.rect(surface, RED, (x + 2, y + 25, 10, 4))
    # Right thigh
    pygame.draw.rect(surface, (200, 200, 210), (x + 13, y + 5, 8, 10))
    pygame.draw.rect(surface, BLUE, (x + 14, y + 6, 6, 4))  # armor plate
    # Right shin
    pygame.draw.rect(surface, (200, 200, 210), (x + 14, y + 15, 6, 10))
    # Right foot
    pygame.draw.rect(surface, RED, (x + 12, y + 25, 10, 4))
    # Knee joints
    pygame.draw.circle(surface, DARK_GRAY, (x + 7, y + 15), 3)
    pygame.draw.circle(surface, DARK_GRAY, (x + 17, y + 15), 3)


def draw_wave_gun(surface, x, y):
    """Draw particle cannon (large barrel beam weapon)."""
    # Cannon body - thick and heavy
    pygame.draw.rect(surface, (50, 50, 60), (x, y + 2, 20, 8))
    # Wide barrel
    pygame.draw.rect(surface, (70, 70, 80), (x + 18, y, 14, 12))
    pygame.draw.rect(surface, (90, 90, 100), (x + 30, y + 1, 6, 10))
    # Muzzle ring
    pygame.draw.rect(surface, CYAN, (x + 35, y + 2, 3, 8))
    # Energy coils
    pygame.draw.rect(surface, (0, 150, 200), (x + 4, y + 3, 3, 6))
    pygame.draw.rect(surface, (0, 150, 200), (x + 10, y + 3, 3, 6))
    # Mounting bracket
    pygame.draw.rect(surface, DARK_GRAY, (x - 2, y + 4, 4, 4))


def draw_full_robot(surface, x, y, has_head, has_legs, has_gun):
    """Draw MagMax as a Gundam-style mecha in current assembly state."""
    # Calculate positions relative to torso center
    torso_x = x + 4
    torso_y = y

    if has_legs:
        # Legs below torso
        draw_legs(surface, torso_x, torso_y + 16)

    # Draw torso (always present)
    draw_ship_body(surface, x, torso_y)

    if has_head:
        # Head above torso
        draw_head(surface, torso_x, torso_y - 16)

    if has_gun:
        # Beam rifle held to the right, at shoulder level
        draw_wave_gun(surface, x + 28, torso_y)


def draw_enemy_basic(surface, x, y):
    """Basic flying enemy."""
    points = [(x + 12, y), (x + 24, y + 8), (x + 12, y + 16), (x, y + 8)]
    pygame.draw.polygon(surface, RED, points)
    pygame.draw.polygon(surface, ORANGE, points, 1)
    pygame.draw.circle(surface, YELLOW, (x + 12, y + 8), 3)


def draw_enemy_tank(surface, x, y):
    """Ground tank enemy."""
    pygame.draw.rect(surface, DARK_GRAY, (x, y + 8, 28, 12))
    pygame.draw.rect(surface, GRAY, (x + 4, y + 4, 16, 10))
    pygame.draw.rect(surface, GRAY, (x + 18, y + 6, 14, 4))
    pygame.draw.circle(surface, RED, (x + 30, y + 8), 2)


def draw_enemy_turret(surface, x, y):
    """Stationary turret enemy."""
    pygame.draw.rect(surface, DARK_GRAY, (x + 4, y + 10, 16, 10))
    pygame.draw.circle(surface, GRAY, (x + 12, y + 10), 8)
    pygame.draw.circle(surface, RED, (x + 12, y + 10), 4)
    pygame.draw.rect(surface, GRAY, (x + 16, y + 8, 12, 4))


def draw_enemy_flyer(surface, x, y):
    """Fast flying enemy with wings."""
    pygame.draw.polygon(surface, ORANGE,
                        [(x + 16, y + 4), (x + 24, y + 10),
                         (x + 16, y + 16), (x, y + 10)])
    pygame.draw.polygon(surface, YELLOW,
                        [(x + 4, y), (x + 16, y + 4), (x + 16, y + 10),
                         (x + 4, y + 10)])
    pygame.draw.polygon(surface, YELLOW,
                        [(x + 4, y + 20), (x + 16, y + 16), (x + 16, y + 10),
                         (x + 4, y + 10)])


def draw_bullet(surface, x, y):
    """Player bullet."""
    pygame.draw.rect(surface, YELLOW, (x, y, 8, 3))
    pygame.draw.rect(surface, WHITE, (x + 6, y, 4, 3))


def draw_particle_cannon(surface, x, y, frame):
    """Particle cannon shot - large glowing energy ball."""
    # Outer glow (pulsing)
    pulse = (frame % 6)
    radius = 7 + pulse // 2
    pygame.draw.circle(surface, (0, 80, 150), (x + 8, y), radius)
    # Core
    pygame.draw.circle(surface, CYAN, (x + 8, y), 5)
    pygame.draw.circle(surface, WHITE, (x + 8, y), 2)
    # Trailing energy
    for i in range(3):
        trail_x = x - 4 - i * 5
        trail_r = 3 - i
        alpha_color = (0, max(0, 150 - i * 50), max(0, 200 - i * 60))
        pygame.draw.circle(surface, alpha_color, (trail_x + 8, y), trail_r)


def draw_enemy_bullet(surface, x, y):
    """Enemy bullet."""
    pygame.draw.circle(surface, RED, (x + 3, y + 3), 3)
    pygame.draw.circle(surface, ORANGE, (x + 3, y + 3), 2)


def draw_part_pickup(surface, x, y, part_type):
    """Draw a collectible part on the ground."""
    # Glowing platform
    pygame.draw.rect(surface, GREEN, (x, y + 16, 24, 4))
    if part_type == PART_HEAD:
        draw_head(surface, x, y)
    elif part_type == PART_LEGS:
        draw_legs(surface, x, y)
    elif part_type == PART_WAVE_GUN:
        draw_wave_gun(surface, x, y)


def draw_warp_hole(surface, x, y, frame):
    """Draw a warp hole to go underground."""
    radius = 16 + (frame % 20) // 5
    pygame.draw.ellipse(surface, DARK_BROWN, (x - radius, y - radius // 2,
                                              radius * 2, radius))
    pygame.draw.ellipse(surface, BLACK, (x - radius + 4, y - radius // 2 + 2,
                                        radius * 2 - 8, radius - 4))

# === DEEP SEA ENEMIES ===

def draw_enemy_jellyfish(surface, x, y, frame):
    """Translucent jellyfish that drifts and pulses."""
    pulse = int(math.sin(frame * 0.08) * 3)
    # Bell/dome
    pygame.draw.ellipse(surface, (80, 0, 120), (x + 2, y, 20, 12 + pulse))
    pygame.draw.ellipse(surface, (120, 50, 180), (x + 4, y + 2, 16, 8 + pulse))
    # Tentacles
    for i in range(4):
        tx = x + 5 + i * 5
        wave = int(math.sin(frame * 0.06 + i) * 3)
        pygame.draw.line(surface, (100, 30, 150),
                         (tx, y + 12 + pulse), (tx + wave, y + 22 + pulse), 1)
    # Glow
    pygame.draw.circle(surface, (150, 80, 200), (x + 12, y + 6), 3)


def draw_enemy_anglerfish(surface, x, y, frame):
    """Small anglerfish with glowing lure."""
    # Body
    pygame.draw.ellipse(surface, (30, 50, 60), (x + 4, y + 4, 18, 14))
    # Mouth
    jaw = int(math.sin(frame * 0.1) * 2)
    pygame.draw.polygon(surface, (20, 30, 40),
                        [(x, y + 8), (x + 6, y + 6 - jaw), (x + 6, y + 14 + jaw)])
    # Teeth
    pygame.draw.line(surface, WHITE, (x + 1, y + 9), (x + 4, y + 8), 1)
    pygame.draw.line(surface, WHITE, (x + 1, y + 11), (x + 4, y + 12), 1)
    # Lure
    lure_glow = 3 + int(math.sin(frame * 0.12) * 2)
    pygame.draw.line(surface, (40, 60, 80), (x + 14, y + 4), (x + 16, y), 1)
    pygame.draw.circle(surface, (0, 220, 255), (x + 16, y), lure_glow)
    # Eye
    pygame.draw.circle(surface, YELLOW, (x + 16, y + 8), 2)
    pygame.draw.circle(surface, BLACK, (x + 16, y + 8), 1)
    # Fin
    pygame.draw.polygon(surface, (40, 60, 70),
                        [(x + 20, y + 6), (x + 24, y + 4), (x + 24, y + 12), (x + 20, y + 14)])


def draw_enemy_torpedo(surface, x, y):
    """Fast torpedo projectile."""
    # Body
    pygame.draw.ellipse(surface, (60, 60, 70), (x, y + 5, 24, 10))
    # Nose cone
    pygame.draw.polygon(surface, (80, 80, 90),
                        [(x + 22, y + 7), (x + 28, y + 10), (x + 22, y + 13)])
    # Propeller trail
    pygame.draw.circle(surface, (100, 200, 255), (x + 2, y + 10), 3)
    pygame.draw.circle(surface, WHITE, (x + 2, y + 10), 1)
    # Fins
    pygame.draw.polygon(surface, (50, 50, 60),
                        [(x + 4, y + 5), (x + 2, y + 2), (x + 8, y + 5)])
    pygame.draw.polygon(surface, (50, 50, 60),
                        [(x + 4, y + 15), (x + 2, y + 18), (x + 8, y + 15)])


# === HIVE ENEMIES ===

def draw_enemy_wasp(surface, x, y, frame):
    """Aggressive wasp with rapid wing beat."""
    # Abdomen
    pygame.draw.ellipse(surface, (200, 180, 0), (x + 10, y + 8, 14, 10))
    # Stripes
    pygame.draw.rect(surface, (30, 20, 0), (x + 13, y + 10, 3, 6))
    pygame.draw.rect(surface, (30, 20, 0), (x + 18, y + 10, 3, 6))
    # Thorax
    pygame.draw.ellipse(surface, (180, 150, 0), (x + 5, y + 7, 10, 8))
    # Head
    pygame.draw.circle(surface, (160, 130, 0), (x + 3, y + 10), 4)
    # Eyes
    pygame.draw.circle(surface, RED, (x + 2, y + 9), 2)
    # Wings (flutter)
    wing_up = (frame % 4) < 2
    wy = y + 4 if wing_up else y + 6
    pygame.draw.ellipse(surface, (200, 200, 150), (x + 8, wy, 12, 5))
    pygame.draw.ellipse(surface, (200, 200, 150), (x + 8, y + 14 - (wy - y - 4), 12, 5))
    # Stinger
    pygame.draw.polygon(surface, (100, 80, 0),
                        [(x + 23, y + 12), (x + 27, y + 13), (x + 23, y + 14)])


def draw_enemy_larva(surface, x, y, frame):
    """Slow grub/larva, segmented body."""
    # Segments
    wave = int(math.sin(frame * 0.05) * 2)
    for i in range(4):
        seg_x = x + i * 6
        seg_y = y + 6 + int(math.sin(frame * 0.04 + i * 0.8) * 2)
        color = (180 - i * 20, 200 - i * 20, 100 - i * 10)
        pygame.draw.ellipse(surface, color, (seg_x, seg_y, 8, 10))
    # Head
    pygame.draw.circle(surface, (200, 220, 120), (x + 2, y + 10 + wave), 5)
    # Mandibles
    pygame.draw.line(surface, (100, 80, 0), (x, y + 10 + wave), (x - 3, y + 8 + wave), 2)
    pygame.draw.line(surface, (100, 80, 0), (x, y + 12 + wave), (x - 3, y + 14 + wave), 2)


def draw_enemy_beetle(surface, x, y):
    """Armored beetle - tough and slow."""
    # Shell
    pygame.draw.ellipse(surface, (40, 60, 20), (x + 2, y + 2, 22, 16))
    pygame.draw.ellipse(surface, (60, 90, 30), (x + 4, y + 4, 18, 12))
    # Shell line
    pygame.draw.line(surface, (30, 40, 10), (x + 13, y + 3), (x + 13, y + 17), 1)
    # Head
    pygame.draw.ellipse(surface, (50, 70, 25), (x - 2, y + 6, 8, 8))
    # Horns
    pygame.draw.line(surface, (80, 60, 20), (x, y + 7), (x - 4, y + 3), 2)
    pygame.draw.line(surface, (80, 60, 20), (x, y + 13), (x - 4, y + 17), 2)
    # Legs
    for i in range(3):
        lx = x + 6 + i * 6
        pygame.draw.line(surface, (30, 40, 10), (lx, y + 16), (lx - 2, y + 20), 2)
        pygame.draw.line(surface, (30, 40, 10), (lx, y + 2), (lx - 2, y - 2), 2)


# === ALIEN NEST ENEMIES ===

def draw_enemy_facehugger(surface, x, y, frame):
    """Fast alien facehugger - spider-like."""
    # Body
    pygame.draw.ellipse(surface, (60, 50, 40), (x + 6, y + 6, 14, 10))
    # Legs (4 pairs, animated)
    for i in range(4):
        angle = frame * 0.15 + i * 0.8
        lx = x + 8 + i * 3
        leg_ext = int(math.sin(angle) * 3)
        pygame.draw.line(surface, (80, 60, 40),
                         (lx, y + 6), (lx - 3, y + 2 - abs(leg_ext)), 1)
        pygame.draw.line(surface, (80, 60, 40),
                         (lx, y + 16), (lx - 3, y + 18 + abs(leg_ext)), 1)
    # Tail
    tail_wave = int(math.sin(frame * 0.08) * 4)
    pygame.draw.line(surface, (70, 55, 35),
                     (x + 20, y + 10), (x + 26, y + 8 + tail_wave), 2)
    # Front grabbers
    pygame.draw.line(surface, (90, 70, 50), (x + 6, y + 8), (x + 2, y + 5), 2)
    pygame.draw.line(surface, (90, 70, 50), (x + 6, y + 14), (x + 2, y + 17), 2)


def draw_enemy_spitter(surface, x, y, frame):
    """Alien that spits acid - has visible sac."""
    # Body
    pygame.draw.ellipse(surface, (40, 30, 50), (x + 4, y + 4, 18, 14))
    # Acid sac (pulsing)
    sac_size = 5 + int(math.sin(frame * 0.06) * 2)
    pygame.draw.circle(surface, (80, 180, 0), (x + 8, y + 10), sac_size)
    pygame.draw.circle(surface, (120, 220, 0), (x + 8, y + 10), sac_size - 2)
    # Head/mouth
    pygame.draw.ellipse(surface, (50, 40, 60), (x, y + 7, 8, 8))
    pygame.draw.rect(surface, (30, 20, 30), (x - 2, y + 9, 4, 4))
    # Spines
    for i in range(3):
        sx = x + 10 + i * 4
        pygame.draw.line(surface, (60, 50, 70), (sx, y + 4), (sx + 1, y), 1)


def draw_enemy_crawler(surface, x, y, frame):
    """Wall-crawling alien with many legs."""
    # Segmented body
    for i in range(5):
        seg_x = x + i * 5
        seg_y = y + 8 + int(math.sin(frame * 0.06 + i * 0.6) * 1.5)
        color = (30 + i * 5, 20 + i * 3, 40 + i * 5)
        pygame.draw.ellipse(surface, color, (seg_x, seg_y, 7, 6))
    # Legs (many, rippling)
    for i in range(5):
        lx = x + 2 + i * 5
        phase = math.sin(frame * 0.1 + i * 0.7) * 3
        pygame.draw.line(surface, (50, 40, 60),
                         (lx + 3, y + 14), (lx + int(phase), y + 18), 1)
        pygame.draw.line(surface, (50, 40, 60),
                         (lx + 3, y + 8), (lx + int(-phase), y + 4), 1)
    # Head
    pygame.draw.circle(surface, (50, 30, 60), (x + 2, y + 10), 4)
    pygame.draw.circle(surface, (200, 100, 0), (x + 1, y + 9), 2)


# === SPACE ENEMIES ===

def draw_enemy_drone(surface, x, y):
    """Small mechanical drone - flies in formation."""
    # Body
    pygame.draw.polygon(surface, (100, 100, 120),
                        [(x + 12, y + 2), (x + 22, y + 10),
                         (x + 12, y + 18), (x + 2, y + 10)])
    # Core
    pygame.draw.circle(surface, (0, 150, 200), (x + 12, y + 10), 4)
    pygame.draw.circle(surface, WHITE, (x + 12, y + 10), 2)
    # Thrusters
    pygame.draw.rect(surface, (60, 60, 80), (x + 18, y + 8, 6, 4))
    pygame.draw.rect(surface, ORANGE, (x + 23, y + 9, 3, 2))


def draw_enemy_comet(surface, x, y, frame):
    """Fast comet/asteroid chunk hurtling diagonally."""
    # Rocky body
    pts = [(x + 10, y + 2), (x + 18, y + 4), (x + 22, y + 10),
           (x + 18, y + 16), (x + 8, y + 18), (x + 2, y + 12), (x + 4, y + 6)]
    pygame.draw.polygon(surface, (100, 80, 60), pts)
    pygame.draw.polygon(surface, (140, 110, 80), pts, 1)
    # Craters
    pygame.draw.circle(surface, (70, 55, 40), (x + 10, y + 8), 3)
    pygame.draw.circle(surface, (70, 55, 40), (x + 15, y + 13), 2)
    # Flame trail
    for i in range(3):
        trail_x = x + 20 + i * 4
        trail_y = y + 10 + int(math.sin(frame * 0.2 + i) * 2)
        r = 3 - i
        pygame.draw.circle(surface, (255, 150 - i * 40, 0), (trail_x, trail_y), r)


def draw_enemy_sentinel(surface, x, y, frame):
    """Orbiting sentinel - energy shield type."""
    # Outer ring (rotating)
    cx, cy = x + 12, y + 10
    pygame.draw.circle(surface, (60, 0, 80), (cx, cy), 10, 2)
    # Rotating dots on ring
    for i in range(3):
        angle = frame * 0.05 + i * (math.pi * 2 / 3)
        dx = int(math.cos(angle) * 10)
        dy = int(math.sin(angle) * 10)
        pygame.draw.circle(surface, (180, 0, 255), (cx + dx, cy + dy), 2)
    # Core
    pulse = int(math.sin(frame * 0.08) * 2)
    pygame.draw.circle(surface, (100, 0, 150), (cx, cy), 5 + pulse)
    pygame.draw.circle(surface, (200, 100, 255), (cx, cy), 3)
