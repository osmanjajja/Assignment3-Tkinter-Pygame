import pygame

class Timer:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.time_left = time_limit
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.time_left = self.time_limit - elapsed_seconds

    def reset(self, time_limit):
        self.time_limit = time_limit
        self.time_left = time_limit
        self.start_ticks = pygame.time.get_ticks()
