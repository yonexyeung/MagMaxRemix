"""MagMax Remix - Main entry point."""

import pygame
import random
import sys
from settings import *
from entities import *
from game import Background, StageManager
from leaderboard import load_leaderboard, is_high_score, add_score


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 48)

    run_game(screen, clock, font, small_font, big_font)


def draw_title(screen, font, small_font, frame, difficulty):
    screen.fill(BLACK)
    title_text = font.render("MAGMAX REMIX", True, CYAN)
    sub_text = small_font.render("組 合 金 剛", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 120))
    screen.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, 160))

    # Difficulty selector
    diff_label = small_font.render("DIFFICULTY:", True, GRAY)
    screen.blit(diff_label, (SCREEN_WIDTH // 2 - 100, 220))
    for i, name in enumerate(DIFF_NAMES):
        color = YELLOW if i == difficulty else GRAY
        marker = "> " if i == difficulty else "  "
        t = small_font.render(f"{marker}{name}", True, color)
        screen.blit(t, (SCREEN_WIDTH // 2 - 40, 250 + i * 28))

    # Blinking start text
    if (frame // 30) % 2 == 0:
        start_text = small_font.render("Press ENTER to Start", True, YELLOW)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 360))

    hint = small_font.render("UP/DOWN to change difficulty", True, GRAY)
    screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 395))

    # Controls
    controls = [
        "Arrow Keys - Move    Space/Z - Shoot    P - Pause",
        "Collect parts to build the robot!",
    ]
    for i, line in enumerate(controls):
        t = small_font.render(line, True, GRAY)
        screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 440 + i * 25))


def draw_hud(screen, small_font, player, score, stage_mgr, difficulty):
    score_text = small_font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    lives_text = small_font.render(f"LIVES: {player.lives}", True, WHITE)
    screen.blit(lives_text, (10, 35))
    diff_text = small_font.render(f"[{DIFF_NAMES[difficulty]}]", True, YELLOW)
    screen.blit(diff_text, (10, 55))
    # Stage
    stage_name = STAGE_NAMES[stage_mgr.current_stage]
    underground_tag = " [UNDERGROUND]" if player.underground else ""
    stage_text = small_font.render(f"STAGE: {stage_name}{underground_tag}", True, CYAN)
    screen.blit(stage_text, (SCREEN_WIDTH - stage_text.get_width() - 10, 10))
    # Parts
    parts_str = ""
    if player.has_head:
        parts_str += "[HEAD] "
    if player.has_legs:
        parts_str += "[LEGS] "
    if player.has_gun:
        parts_str += "[GUN] "
    if parts_str:
        parts_text = small_font.render(parts_str, True, GREEN)
        screen.blit(parts_text, (SCREEN_WIDTH - parts_text.get_width() - 10, 35))


def draw_gameover(screen, font, small_font, score, countdown):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    go_text = font.render("GAME OVER", True, RED)
    screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, 180))
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 230))
    # Continue countdown
    seconds = max(0, (countdown + FPS - 1) // FPS)
    cont_text = font.render(f"CONTINUE?  {seconds}", True, YELLOW)
    screen.blit(cont_text, (SCREEN_WIDTH // 2 - cont_text.get_width() // 2, 300))
    hint = small_font.render("Press ENTER to continue / Wait to end", True, GRAY)
    screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 350))


def draw_stage_clear(screen, font, small_font, stage_name, timer, score):
    alpha = min(180, (180 - timer) * 3)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(alpha)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    clear_text = font.render("STAGE CLEAR", True, CYAN)
    screen.blit(clear_text, (SCREEN_WIDTH // 2 - clear_text.get_width() // 2, 200))
    stage_text = small_font.render(f"- {stage_name} -", True, WHITE)
    screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 250))
    bonus_text = small_font.render("BOSS BONUS: 5000", True, YELLOW)
    screen.blit(bonus_text, (SCREEN_WIDTH // 2 - bonus_text.get_width() // 2, 300))
    score_text = small_font.render(f"TOTAL SCORE: {score}", True, GREEN)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 340))


def draw_victory(screen, font, small_font, big_font, score, difficulty):
    screen.fill(BLACK)
    vic_text = big_font.render("MISSION COMPLETE", True, CYAN)
    screen.blit(vic_text, (SCREEN_WIDTH // 2 - vic_text.get_width() // 2, 100))
    diff_text = font.render(f"Difficulty: {DIFF_NAMES[difficulty]}", True, YELLOW)
    screen.blit(diff_text, (SCREEN_WIDTH // 2 - diff_text.get_width() // 2, 170))
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 220))
    hint = small_font.render("Press ENTER to continue", True, GRAY)
    screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 280))


def draw_leaderboard(screen, font, small_font, big_font, entries, highlight_idx=-1):
    screen.fill(BLACK)
    title = big_font.render("LEADERBOARD", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))
    # Header
    hdr = small_font.render("RANK   NAME   SCORE        DIFF", True, GRAY)
    screen.blit(hdr, (SCREEN_WIDTH // 2 - 150, 100))
    pygame.draw.line(screen, GRAY, (SCREEN_WIDTH // 2 - 150, 120),
                     (SCREEN_WIDTH // 2 + 150, 120), 1)
    for i, entry in enumerate(entries[:LEADERBOARD_MAX]):
        color = CYAN if i == highlight_idx else WHITE
        rank = f"{i + 1:>2}."
        name = entry["name"].ljust(3)
        score_str = str(entry["score"]).rjust(10)
        diff = entry.get("difficulty", "???")
        line = f"{rank}    {name}    {score_str}    {diff}"
        t = small_font.render(line, True, color)
        screen.blit(t, (SCREEN_WIDTH // 2 - 150, 130 + i * 30))
    hint = small_font.render("Press ENTER to return to title", True, GRAY)
    screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 550))


def draw_name_input(screen, font, small_font, big_font, score, name_chars):
    screen.fill(BLACK)
    title = font.render("NEW HIGH SCORE!", True, YELLOW)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 210))
    prompt = small_font.render("Enter your name (3 chars max):", True, GRAY)
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 280))
    # Name display
    display_name = "".join(name_chars).ljust(3, "_")
    name_text = big_font.render(display_name, True, CYAN)
    screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 320))
    hint = small_font.render("Press ENTER to confirm", True, GRAY)
    screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 400))


def run_game(screen, clock, font, small_font, big_font):
    # States: title, playing, gameover, victory, name_input, leaderboard
    game_state = "title"
    difficulty = DIFF_EASY
    player = Player()
    bullets = []
    enemy_bullets = []
    enemies = []
    parts = []
    warps = []
    explosions = []
    boss = None
    score = 0
    frame = 0
    stages_cleared = 0
    background = Background()
    stage_mgr = StageManager(difficulty)
    stage_clear_timer = 0
    cleared_stage_name = ""
    paused = False
    name_chars = []
    continue_timer = 0  # 10 second countdown on gameover

    running = True
    while running:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == "playing" and not paused:
                        paused = True
                    else:
                        running = False

                elif game_state == "title":
                    if event.key == pygame.K_UP:
                        difficulty = max(0, difficulty - 1)
                    elif event.key == pygame.K_DOWN:
                        difficulty = min(2, difficulty + 1)
                    elif event.key == pygame.K_RETURN:
                        game_state = "playing"
                        player = Player()
                        bullets = []
                        enemy_bullets = []
                        enemies = []
                        parts = []
                        warps = []
                        explosions = []
                        boss = None
                        score = 0
                        stages_cleared = 0
                        stage_mgr = StageManager(difficulty)
                        stage_clear_timer = 0
                        paused = False
                        continue_timer = 0
                        background = Background()

                elif game_state == "gameover":
                    if event.key == pygame.K_RETURN and continue_timer > 0:
                        # Continue: revive player, keep score and stage
                        game_state = "playing"
                        player = Player()
                        player.lives = 3
                        bullets = []
                        enemy_bullets = []
                        enemies.clear()
                        boss = None
                        continue_timer = 0

                elif game_state == "victory":
                    if event.key == pygame.K_RETURN:
                        if is_high_score(score):
                            game_state = "name_input"
                            name_chars = []
                        else:
                            game_state = "leaderboard"

                elif game_state == "name_input":
                    if event.key == pygame.K_RETURN and len(name_chars) > 0:
                        add_score("".join(name_chars), score, difficulty)
                        game_state = "leaderboard"
                    elif event.key == pygame.K_BACKSPACE:
                        if name_chars:
                            name_chars.pop()
                    elif len(name_chars) < 3:
                        ch = event.unicode.upper()
                        if ch.isalnum():
                            name_chars.append(ch)

                elif game_state == "leaderboard":
                    if event.key == pygame.K_RETURN:
                        game_state = "title"

                elif game_state == "playing":
                    if event.key == pygame.K_p:
                        paused = not paused

        # --- RENDER BY STATE ---
        if game_state == "title":
            draw_title(screen, font, small_font, frame, difficulty)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if game_state == "gameover":
            continue_timer -= 1
            if continue_timer <= 0:
                # Time's up, go to leaderboard
                if is_high_score(score):
                    game_state = "name_input"
                    name_chars = []
                else:
                    game_state = "leaderboard"
                continue
            draw_gameover(screen, font, small_font, score, continue_timer)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if game_state == "victory":
            draw_victory(screen, font, small_font, big_font, score, difficulty)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if game_state == "name_input":
            draw_name_input(screen, font, small_font, big_font, score, name_chars)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if game_state == "leaderboard":
            entries = load_leaderboard()
            draw_leaderboard(screen, font, small_font, big_font, entries)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # --- PLAYING STATE ---
        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            pause_text = font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - 20))
            hint_text = small_font.render("Press P to Resume / ESC to Quit", True, GRAY)
            screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2,
                                    SCREEN_HEIGHT // 2 + 20))
            pygame.display.flip()
            clock.tick(FPS)
            continue

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Shooting
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            new_bullets = player.shoot()
            bullets.extend(new_bullets)

        background.update()

        # Stage management
        if stage_clear_timer > 0:
            stage_clear_timer -= 1
            if stage_clear_timer <= 0:
                stages_cleared += 1
                if stages_cleared >= 4:
                    game_state = "victory"
                    continue
                stage_mgr.next_stage()
                enemies.clear()
                enemy_bullets.clear()
        elif boss is None:
            event = stage_mgr.update(enemies, parts, warps, player.underground, player)
            if event == "spawn_boss":
                boss = Boss(stage_mgr.current_stage, difficulty)
        else:
            stage_mgr.part_timer -= 1
            if stage_mgr.part_timer <= 0:
                stage_mgr._spawn_part(parts, player)
                base_min, base_max = 300, 600
                part_divisor = {0: 1.0, 1: 1.5, 2: 2.0}[difficulty]
                stage_mgr.part_timer = int(random.randint(base_min, base_max) / part_divisor)

        # Update bullets
        for b in bullets:
            b.update()
        bullets = [b for b in bullets if b.alive]
        for b in enemy_bullets:
            b.update()
        enemy_bullets = [b for b in enemy_bullets if b.alive]

        # Update enemies
        for e in enemies:
            e.update(player.x, player.y)
            if e.should_fire():
                enemy_bullets.append(e.fire_at(player.x, player.y))
        enemies = [e for e in enemies if e.alive]

        # Update boss
        if boss:
            boss.update(player.x, player.y)
            if boss.should_fire():
                enemy_bullets.extend(boss.fire_at(player.x, player.y))

        # Update pickups
        for p in parts:
            p.update()
        parts = [p for p in parts if p.alive]
        for w in warps:
            w.update()
        warps = [w for w in warps if w.alive]

        # Update explosions
        for ex in explosions:
            ex.update()
        explosions = [ex for ex in explosions if ex.alive]

        # --- COLLISIONS ---
        for b in bullets:
            for e in enemies:
                if b.rect.colliderect(e.rect):
                    b.alive = False
                    dmg = getattr(b, 'damage', 1)
                    e.hp -= dmg
                    if e.hp <= 0:
                        e.alive = False
                        score += e.score_value.get(e.enemy_type, 100)
                        explosions.append(Explosion(e.x + 12, e.y + 10))
                    break

        if boss:
            for b in bullets:
                if not b.alive:
                    continue
                if b.rect.colliderect(boss.rect):
                    b.alive = False
                    dmg = getattr(b, 'damage', 1)
                    boss.hp -= dmg
                    if boss.hp <= 0:
                        boss.alive = False
                        score += 5000
                        # Big boss explosion
                        bx, by = boss.x, boss.y
                        for i in range(12):
                            ex = bx + random.randint(0, boss.width)
                            ey = by + random.randint(0, boss.height)
                            explosions.append(Explosion(ex, ey))
                        explosions.append(BigExplosion(bx + boss.width // 2,
                                                      by + boss.height // 2))
                        cleared_stage_name = STAGE_NAMES[stage_mgr.current_stage]
                        stage_clear_timer = 180
                        boss = None
                        break

        if player.invincible <= 0:
            for b in enemy_bullets:
                if b.rect.colliderect(player.rect):
                    b.alive = False
                    dead = player.hit()
                    explosions.append(Explosion(player.x + 16, player.y + 8))
                    if dead:
                        game_state = "gameover"
                        continue_timer = 10 * FPS
                    break

        if player.invincible <= 0:
            for e in enemies:
                if e.rect.colliderect(player.rect):
                    e.alive = False
                    explosions.append(Explosion(e.x + 12, e.y + 10))
                    dead = player.hit()
                    explosions.append(Explosion(player.x + 16, player.y + 8))
                    if dead:
                        game_state = "gameover"
                        continue_timer = 10 * FPS
                    break

        if boss and player.invincible <= 0:
            if boss.rect.colliderect(player.rect):
                dead = player.hit()
                explosions.append(Explosion(player.x + 16, player.y + 8))
                if dead:
                    game_state = "gameover"
                    continue_timer = 10 * FPS

        for p in parts:
            if p.rect.colliderect(player.rect):
                p.alive = False
                if p.part_type == PART_HEAD:
                    player.has_head = True
                    score += 500
                elif p.part_type == PART_LEGS:
                    player.has_legs = True
                    score += 500
                elif p.part_type == PART_WAVE_GUN:
                    player.has_gun = True
                    score += 500
                elif p.part_type == "life_up":
                    player.lives += 1
                    score += 1000

        for w in warps:
            if w.rect.colliderect(player.rect):
                w.alive = False
                player.underground = not player.underground

        # --- DRAW ---
        background.draw(screen, stage_mgr.current_stage, player.underground)
        for w in warps:
            w.draw(screen, frame)
        for p in parts:
            p.draw(screen, frame)
        for e in enemies:
            e.draw(screen, frame)
        if boss:
            boss.draw(screen, frame)
        player.draw(screen, frame)
        for b in bullets:
            b.draw(screen, frame)
        for b in enemy_bullets:
            b.draw(screen, frame)
        for ex in explosions:
            ex.draw(screen, frame)
        draw_hud(screen, small_font, player, score, stage_mgr, difficulty)
        if stage_clear_timer > 0:
            draw_stage_clear(screen, font, small_font, cleared_stage_name,
                             stage_clear_timer, score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
