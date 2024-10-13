import pygame
import random
from enemy import Enemy
from collectible import Collectible
from door import Door  # Import the Door class

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((139, 69, 19))  # Brown color for platforms
        self.rect = self.image.get_rect(topleft=(x, y))

class Level:
    def __init__(self, player, level_number):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.door = None  # Add door attribute
        self.player = player
        self.is_completed = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.level_number = level_number
        self.guidance_messages = []  # List to hold guidance messages

        # Screen dimensions
        self.screen_width = 800
        self.screen_height = 600

        # Generate the level with randomness
        self.generate_level()

    def generate_level(self):
        platform_height = 20
        vertical_gap = 150  # Adjusted for better jump between platforms

        # Randomize enemy count (between 3 to 6 enemies)
        enemy_count = random.randint(3, 6)

        # Adjust platform count based on enemy count
        platform_count = enemy_count + 2  # More platforms for more enemies

        # Fixed starting platform (boundary where player always starts)
        start_platform_y = self.screen_height - 50  # 50 pixels above the bottom boundary
        start_platform_width = 300
        start_platform_x = random.randint(0, self.screen_width - start_platform_width)
        start_platform = Platform(start_platform_x, start_platform_y, start_platform_width, platform_height)
        self.platforms.add(start_platform)

        # Randomly generate the remaining platforms
        previous_platform_top = start_platform_y - vertical_gap
        for i in range(platform_count):
            platform_width = random.randint(200, 400)
            platform_x = random.randint(0, self.screen_width - platform_width)
            platform_y = previous_platform_top - vertical_gap

            # Ensure player can jump between platforms
            self.platforms.add(Platform(platform_x, platform_y, platform_width, platform_height))

            previous_platform_top = platform_y

        # Generate enemies on platforms (except the starting one)
        platforms = self.platforms.sprites()
        for i in range(enemy_count):
            platform = random.choice(platforms[1:])  # Avoid the first platform (start platform)
            self.enemies.add(Enemy(platform.rect.x + 50, platform.rect.top - 50, platform))

        # Door at the end of the level
        self.door = Door(platforms[-1].rect.right - 100, platforms[-1].rect.top - 50)

        # Collectibles for health boost
        self.collectibles.add(Collectible(random.choice(platforms).rect.centerx, platforms[1].rect.top - 100, 'health'))

        # Guidance message
        self.guidance_messages.append(('Reach the door to complete the level!', 100))

        # Position player on the starting platform
        self.player.rect.bottom = start_platform.rect.top
        self.player.rect.x = start_platform.rect.left + 50

    def update(self):
        self.enemies.update()

        # Check for collisions between player and enemies
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in enemy_hits:
            self.player.take_damage(5)  # Reduced damage from regular enemies
            if self.player.health <= 0:
                self.player.lose_life()
                if self.player.lives > 0:
                    self.reset_player_position()
                else:
                    pass  # Game over is handled in main loop

        # Check for player falling off platforms
        if self.player.rect.top > self.screen_height:
            self.player.lose_life()
            if self.player.lives > 0:
                self.reset_player_position()
            else:
                pass  # Game over is handled in main loop

        # Check for collisions between player and door
        if self.door and pygame.sprite.collide_rect(self.player, self.door):
            self.is_completed = True

        # Check for collectible pickups
        collectible_hits = pygame.sprite.spritecollide(self.player, self.collectibles, False)
        for collectible in collectible_hits:
            collectible.apply_effect(self.player)

    def draw(self, screen, camera):
        for platform in self.platforms:
            screen.blit(platform.image, camera.apply(platform))
        for enemy in self.enemies:
            enemy.draw(screen, camera)
        for collectible in self.collectibles:
            screen.blit(collectible.image, camera.apply(collectible))
        if self.door:
            self.door.draw(screen, camera)

    def reset_player_position(self):
        platforms = self.platforms.sprites()
        self.player.rect.bottom = platforms[0].rect.top  # Always reset to the starting platform
        self.player.rect.x = platforms[0].rect.left + 50
        self.player.health = self.player.max_health

    def display_guidance(self, screen, camera):
        """Display guidance messages to the player."""
        for message, x_position in self.guidance_messages:
            # Show the guidance message when the player reaches a certain position
            if self.player.rect.x < x_position:
                text = self.font.render(message, True, (255, 255, 0))
                screen.blit(text, (self.player.rect.x - camera.offset[0], self.player.rect.y - 40))
