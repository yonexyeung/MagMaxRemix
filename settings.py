"""Game constants and settings."""

# Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "MagMax Remix - 組合金剛"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 100, 0)
SAND = (194, 178, 128)
DARK_BLUE = (0, 0, 80)
DARK_BROWN = (60, 30, 0)

# Player
PLAYER_SPEED = 4
PLAYER_BULLET_SPEED = 8
PLAYER_FIRE_RATE = 10  # frames between shots

# Scrolling
SCROLL_SPEED = 2

# Stages
STAGE_DEEP_SEA = 0
STAGE_HIVE = 1
STAGE_ALIEN_NEST = 2
STAGE_SPACE = 3
STAGE_NAMES = ["Deep Sea", "Insect Hive", "Alien Nest", "Outer Space"]
STAGE_LENGTH = 3000  # pixels per stage

# Parts
PART_HEAD = "head"
PART_LEGS = "legs"
PART_WAVE_GUN = "wave_gun"

# Difficulty
DIFF_EASY = 0
DIFF_NORMAL = 1
DIFF_HARD = 2
DIFF_NAMES = ["EASY", "NORMAL", "HARD"]
# Multipliers: [spawn_rate_divisor, boss_hp_multiplier]
DIFF_MULTIPLIERS = {
    DIFF_EASY: (1.0, 1.0),
    DIFF_NORMAL: (2.0, 2.0),
    DIFF_HARD: (4.0, 4.0),
}

# Leaderboard
LEADERBOARD_FILE = "leaderboard.json"
LEADERBOARD_MAX = 10
