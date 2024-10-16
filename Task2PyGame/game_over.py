import pygame

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        # Use default font by setting font to None
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        self.background = pygame.Surface(screen.get_size())
        self.background.fill((0, 0, 0))

    def display(self):
        self.screen.blit(self.background, (0, 0))
        game_over_text = self.font_large.render('Game Over', True, (255, 0, 0))
        restart_game_text = self.font_small.render('Press R to Restart Game', True, (255, 255, 255))
        restart_level_text = self.font_small.render('Press L to Restart Level', True, (255, 255, 255))
        self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(restart_game_text, (self.screen.get_width() // 2 - restart_game_text.get_width() // 2, 300))
        self.screen.blit(restart_level_text, (self.screen.get_width() // 2 - restart_level_text.get_width() // 2, 350))
