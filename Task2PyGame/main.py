import pygame
import sys
from player import Player
from level import Level
from camera import Camera
from game_over import GameOverScreen
from ui import ControlDisplay
from timer import Timer

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side-Scrolling Adventure")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Create player instance
player = Player(50, SCREEN_HEIGHT - 150)

# Create camera
camera = Camera(player, SCREEN_WIDTH, SCREEN_HEIGHT)

# Load sounds
pygame.mixer.music.load('assets/sounds/background_music.mp3')
pygame.mixer.music.play(-1)  # Loop indefinitely
game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')

# Create control display (Pass SCREEN_WIDTH)
control_display = ControlDisplay(SCREEN_WIDTH)

# Create level timer
level_time_limit = 120  # Increased time limit
timer = Timer(level_time_limit)

# Initialize the current level number
current_level_number = 1

# Initialize level before the game loop
level = Level(player, current_level_number)

def main():
    global current_level_number, level
    running = True
    game_over = False
    game_over_screen = GameOverScreen(screen)
    level_reset = False

    while running:
        clock.tick(90)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle player input
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Pass the starting platform to jump method
                        player.jump(level.platforms.sprites()[0])  
                    if event.key == pygame.K_l:
                        # Reset level
                        level_reset = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.move_left = False
                    if event.key == pygame.K_RIGHT:
                        player.move_right = False
                # Continuous movement handling
                keys = pygame.key.get_pressed()
                player.move_left = keys[pygame.K_LEFT]
                player.move_right = keys[pygame.K_RIGHT]
            else:
                # Handle game over screen input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        player.reset(50, SCREEN_HEIGHT - 150)
                        current_level_number = 1
                        level = Level(player, current_level_number)
                        timer.reset(level_time_limit)
                        game_over = False
                        pygame.mixer.music.play(-1)  # Restart music
                    elif event.key == pygame.K_l:
                        # Restart the current level
                        player.reset(50, SCREEN_HEIGHT - 150)
                        level = Level(player, current_level_number)
                        timer.reset(level_time_limit)
                        game_over = False
                        pygame.mixer.music.play(-1)  # Restart music

        if not game_over:
            # Update game objects
            player.update(level.platforms, level.platforms.sprites()[0])  # Pass starting platform
            level.update()
            camera.update()
            timer.update()

            # Check for level completion
            if level.is_completed:
                current_level_number += 1  # Move to the next level
                level = Level(player, current_level_number)
                timer.reset(level_time_limit)
                player.rect.bottom = level.platforms.sprites()[0].rect.top
                player.rect.x = 50

            # Check for game over conditions
            if player.lives <= 0 or timer.time_left <= 0:
                game_over = True
                pygame.mixer.music.stop()
                game_over_sound.play()

            # Reset level if requested
            if level_reset:
                player.reset(50, SCREEN_HEIGHT - 150)
                level = Level(player, current_level_number)
                timer.reset(level_time_limit)
                level_reset = False

            # Draw everything
            screen.fill((135, 206, 235))  # Sky blue background
            level.draw(screen, camera)
            player.draw(screen, camera)

            # Display HUD
            display_hud(screen, player, timer)
            # Display controls
            control_display.draw(screen)
            # Display guidance
            level.display_guidance(screen, camera)
        else:
            # Display game over screen
            game_over_screen.display()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def display_hud(screen, player, timer):
    # Display health bar
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, 204, 24))  # White border
    pygame.draw.rect(screen, (255, 0, 0), (22, 22, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (22, 22, 200 * (player.health / player.max_health), 20))
    # Display lives
    font = pygame.font.SysFont('Arial', 24)
    lives_text = font.render(f'Lives: {player.lives}', True, (255, 255, 255))
    screen.blit(lives_text, (20, 50))
    # Display score
    score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
    screen.blit(score_text, (20, 80))
    # Display timer
    timer_text = font.render(f'Time Left: {int(timer.time_left)}s', True, (255, 255, 255))
    screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 20))

if __name__ == '__main__':
    main()
