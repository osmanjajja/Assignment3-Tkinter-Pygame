import pygame
import os

class ControlDisplay:
    def __init__(self, screen_width):
        self.font = pygame.font.SysFont('Arial', 20)
        self.controls = []
        icons = ['left_arrow.png', 'right_arrow.png', 'up_arrow.png']
        labels = ['Move Left', 'Move Right', 'Jump']
        x, y = screen_width - 200, 20  # Use the passed screen_width

        for icon_file, label in zip(icons, labels):
            icon_path = os.path.join('assets', 'icons', icon_file)
            try:
                image = pygame.image.load(icon_path).convert_alpha()
                # Resize and make transparent
                image = pygame.transform.scale(image, (24, 24))
                image.set_alpha(150)  # Make image more transparent
            except FileNotFoundError:
                # Create a placeholder surface if the image is missing
                image = pygame.Surface((24, 24), pygame.SRCALPHA)
                image.fill((200, 200, 200, 150))  # Light gray with transparency
                pygame.draw.rect(image, (0, 0, 0), image.get_rect(), 2)  # Black border
                placeholder_text = self.font.render('?', True, (0, 0, 0))
                image.blit(placeholder_text, (6, 2))
            self.controls.append({'image': image, 'label': label, 'position': (x, y)})
            y += 40  # Move down for the next control

    def draw(self, screen):
        for control in self.controls:
            screen.blit(control['image'], control['position'])
            label = self.font.render(control['label'], True, (255, 255, 255))
            screen.blit(label, (control['position'][0] + 30, control['position'][1] + 5))
