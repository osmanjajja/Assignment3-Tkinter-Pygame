import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        if self.type == 'health':
            self.image = pygame.image.load('assets/health_collectible.png').convert_alpha()
        elif self.type == 'life':
            self.image = pygame.image.load('assets/life_collectible.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def apply_effect(self, player):
        if self.type == 'health':
            player.health += 20
            if player.health > player.max_health:
                player.health = player.max_health
        elif self.type == 'life':
            player.lives += 1
        player.score += 50
        self.kill()