class Camera:
    def __init__(self, player, width, height):
        self.player = player
        self.offset = [0, 0]
        self.width = width
        self.height = height

    def update(self):
        # Camera follows the player
        self.offset[0] = self.player.rect.centerx - self.width // 2
        self.offset[1] = self.player.rect.centery - self.height // 2

    def apply(self, entity):
        return entity.rect.move(-self.offset[0], -self.offset[1])
