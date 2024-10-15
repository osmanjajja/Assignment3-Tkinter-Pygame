import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, platform, health=50, speed=1):
        super().__init__()
        self.image = pygame.image.load('assets/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.health = health
        self.max_health = health
        self.direction = 1  # 1 for right, -1 for left
        self.platform = platform  # The platform the enemy is on

        # Load sound
        self.hit_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.wav')

    def update(self):
        # Move enemy back and forth on the platform
        self.rect.x += self.speed * self.direction

        # Check boundaries of the platform
        if self.rect.left < self.platform.rect.left or self.rect.right > self.platform.rect.right:
            self.direction *= -1  # Change direction

        # Keep enemy on top of the platform
        self.rect.bottom = self.platform.rect.top

    def take_damage(self, amount):
        self.health -= amount
        self.hit_sound.play()
        if self.health <= 0:
            self.kill()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        # Draw health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (camera.apply(self).x, camera.apply(self).y - 10, self.rect.width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (camera.apply(self).x, camera.apply(self).y - 10, self.rect.width * health_ratio, 5))
