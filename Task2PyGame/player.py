import pygame
from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load player image
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.speed = 5
        self.jumping = False
        self.on_ground = False
        self.projectiles = pygame.sprite.Group()
        self.health = 100
        self.max_health = 100
        self.lives = 3
        self.score = 0
        self.move_left = False
        self.move_right = False
        self.current_platform = None  # Track the platform the player is currently on

        # Direction the player is facing: 1 for right, -1 for left
        self.direction = 1

        # Load sounds
        self.jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
        self.shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.wav')
        self.hurt_sound = pygame.mixer.Sound('assets/sounds/player_hurt.wav')

    def update(self, platforms, starting_platform):
        dx = 0

        # Movement
        if self.move_left:
            dx = -self.speed
            self.direction = -1
        if self.move_right:
            dx = self.speed
            self.direction = 1

        # Adjust horizontal speed while in the air to allow moving further when jumping
        if not self.on_ground:
            dx *= 1.5  # Increase horizontal speed in air

        # Apply gravity
        self.vel_y += 0.5
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        # Collision with platforms
        self.on_ground = False
        self.current_platform = None  # Reset current platform
        for platform in platforms:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.current_platform = platform  # Set the current platform
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                dy = 0

        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Update projectiles
        self.projectiles.update()

    def jump(self, starting_platform):
        if self.on_ground:
            if self.current_platform == starting_platform:
                # Higher jump on the starting platform
                self.vel_y = -25  # Increased jump height
            else:
                # Normal jump on other platforms
                self.vel_y = -15  # Normal jump height
            self.jump_sound.play()

    def shoot(self):
        # Adjust projectile to use sword image
        projectile_start_x = self.rect.centerx
        projectile_start_y = self.rect.centery
        projectile = Projectile(projectile_start_x, projectile_start_y, direction=self.direction, image_path='assets/sword.png')
        self.projectiles.add(projectile)
        self.shoot_sound.play()

    def take_damage(self, amount):
        self.health -= amount
        self.hurt_sound.play()

    def lose_life(self):
        self.lives -= 1
        self.health = self.max_health

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        self.projectiles.draw(screen)

    def reset(self, x, y):
        self.rect.topleft = (x, y)
        self.health = self.max_health
        self.lives = 3
        self.score = 0
        self.projectiles.empty()
