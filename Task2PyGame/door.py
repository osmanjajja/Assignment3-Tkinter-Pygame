import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load door image or create a simple representation
        self.image = pygame.Surface((50, 80))
        self.image.fill((0, 0, 255))  # Blue color for the door
        self.rect = self.image.get_rect(midbottom=(x, y))

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))
