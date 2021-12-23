import pygame


class Button:
    def __init__(self, x, y, width, height, screen, color=(255, 0, 0), label=None):
        self.coll = pygame.Rect(x, y, width, height)
        self.color = color
        self.screen = screen
        self.label = label

    def tick(self, mousePos, click):
        if self.coll.collidepoint(mousePos[0], mousePos[1]):
            pygame.draw.rect(self.screen, (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50)), self.coll)
            self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2, self.coll.y + (self.coll.height - self.label.get_height()) / 2))
            if click:
                return True
        else:
            pygame.draw.rect(self.screen, self.color, self.coll)
            self.screen.blit(self.label, (self.coll.x + (self.coll.width - self.label.get_width()) / 2, self.coll.y + (self.coll.height - self.label.get_height()) / 2))
        return False

    def changeLabel(self, label):
        self.label = label

