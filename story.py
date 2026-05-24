"""Story sequences - Opening and Ending cutscenes."""

import pygame
from settings import *

# Opening story - line by line reveal
OPENING_LINES = [
    "",
    "Year 2187 A.D.",
    "",
    "Deep beneath the ocean floor,",
    "humanity unearthed a colossal metallic skeleton",
    "dormant for over a billion years.",
    "",
    "Scientists named it the 'Primordial Machine God'.",
    "",
    "When its sealed energy was accidentally released,",
    "alien lifeforms parasitizing Earth awakened.",
    "",
    "Ancient leviathans stirred in the abyss.",
    "An insect queen began breeding a mechanized army.",
    "Alien nests spread from deep fissures to the surface.",
    "And from the void of space, the true entity",
    "sensed the signal and began its approach.",
    "",
    "From the Machine God's remains,",
    "humanity reverse-engineered their only weapon --",
    "",
    "A transformable combining combat mecha:",
    "",
    "\"MagMax\"",
    "",
    "Gather the scattered divine parts.",
    "Assemble the complete form.",
    "Annihilate the alien threat across four war zones.",
    "",
    "This is humanity's final counterattack.",
    "",
    "Launch now, pilot.",
]

ENDING_LINES = [
    "",
    "The final alien entity has been destroyed.",
    "The signal from deep space fell silent forever.",
    "",
    "MagMax's frame was critically damaged in battle.",
    "The pilot guided the broken mecha",
    "to a slow descent onto the scarred earth below.",
    "",
    "People emerged from the ruins,",
    "gazing up at the sky, peaceful at last.",
    "",
    "The Machine God's energy was spent.",
    "MagMax's parts detached one by one,",
    "dissolving into particles of light.",
    "",
    "But the pilot knew --",
    "as long as humanity still has the will to fight,",
    "the Machine God will awaken again when needed.",
    "",
    "...",
    "",
    "Three months later.",
    "A deep-sea monitoring station detected",
    "a faint metallic signature.",
    "",
    "The coordinates matched exactly",
    "where the Primordial Machine God was first found.",
    "",
    "",
    "-- THE END --",
    "",
    "...or is it?",
]


class StoryPlayer:
    """Plays story text line by line with typewriter effect."""

    def __init__(self, lines):
        self.lines = lines
        self.current_line = 0
        self.char_index = 0
        self.frame = 0
        self.done = False
        self.revealed_lines = []
        self.scroll_offset = 0
        # Timing
        self.chars_per_frame = 0.8  # speed of typewriter
        self.line_pause = 40  # frames to pause between lines
        self.pause_timer = 0

    def update(self):
        if self.done:
            return

        self.frame += 1

        if self.pause_timer > 0:
            self.pause_timer -= 1
            return

        if self.current_line >= len(self.lines):
            self.done = True
            return

        line = self.lines[self.current_line]

        if len(line) == 0:
            # Empty line - just add it and move on
            self.revealed_lines.append("")
            self.current_line += 1
            self.pause_timer = 15
            self._auto_scroll()
            return

        self.char_index += self.chars_per_frame
        if self.char_index >= len(line):
            # Line complete
            self.revealed_lines.append(line)
            self.current_line += 1
            self.char_index = 0
            self.pause_timer = self.line_pause
            self._auto_scroll()
        # else: still typing current line

    def _auto_scroll(self):
        """Scroll up if too many lines visible."""
        visible_lines = (SCREEN_HEIGHT - 100) // 28
        if len(self.revealed_lines) > visible_lines:
            self.scroll_offset = len(self.revealed_lines) - visible_lines

    def draw(self, surface, font, small_font):
        surface.fill(BLACK)

        # Draw revealed lines
        start_y = 60
        line_height = 28
        visible_start = self.scroll_offset

        for i, line in enumerate(self.revealed_lines[visible_start:]):
            y = start_y + i * line_height
            if y > SCREEN_HEIGHT - 60:
                break
            # Highlight key words
            if line in ('"MagMax"', "-- THE END --", "...or is it?"):
                color = CYAN
                t = font.render(line, True, color)
            elif line.startswith("Year 2187") or line.startswith("Three months"):
                color = YELLOW
                t = small_font.render(line, True, color)
            else:
                color = WHITE
                t = small_font.render(line, True, color)
            surface.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, y))

        # Draw currently typing line
        if not self.done and self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            partial = line[:int(self.char_index)]
            if partial:
                idx = len(self.revealed_lines) - self.scroll_offset
                y = start_y + idx * line_height
                if y <= SCREEN_HEIGHT - 60:
                    t = small_font.render(partial, True, (180, 180, 180))
                    surface.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, y))

        # Skip hint
        hint = small_font.render("Press any key to skip", True, GRAY)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 30))
