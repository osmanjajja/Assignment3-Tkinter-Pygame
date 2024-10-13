import pygame


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.image = pygame.image.load('assets/boss_enemy.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 2
        self.health = health
        self.max_health = health
        self.direction = -1  # Move towards the player
        self.movement_range = 800  # Boss can move within this range

        # Load sound
        self.hit_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.wav')

    def update(self):
        # Simple Algoritham to move back and forth
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= self.movement_range:
            self.direction *= -1

    def take_damage(self, amount):
        self.health -= amount
        self.hit_sound.play()
        if self.health <= 0:
            self.kill()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
        # Draw health bar
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (camera.apply(
            self).x, camera.apply(self).y - 15, self.rect.width, 10))
        pygame.draw.rect(screen, (0, 255, 0), (camera.apply(self).x, camera.apply(
            self).y - 15, self.rect.width * health_ratio, 10))
