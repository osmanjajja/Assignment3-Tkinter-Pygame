import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=1, image_path='assets/sword.png'):
        super().__init__()
        # Load the sword image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10 * direction
        self.direction = direction

    def update(self):
        self.rect.x += self.speed
        # Remove projectile if it goes off-screen
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
