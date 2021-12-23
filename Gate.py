import pygame

import Info
from Wire import Wire


class Gate:
    def __init__(self, x, y, screen, img):
        self.screen = screen
        self.img = pygame.image.load(img)
        self.height = self.img.get_height()
        self.width = self.img.get_width()
        self.x = x - self.width / 2
        self.y = y - self.height / 2
        self.coll = pygame.Rect(self.x, self.y, self.width, self.height)
        self.btcoll = pygame.Rect(self.x, self.y + 5, 20, 20)
        self.bbcoll = pygame.Rect(self.x, self.y + self.height - 25, 20, 20)
        self.fcoll = pygame.Rect(self.x + self.width - 20, self.y + self.height/2 - 10, 20, 20)
        self.botin = None
        self.topin = None

    def tick(self, mousePos, click):
        self.screen.blit(self.img, (self.x, self.y))
        if Info.wiring:
            if click and self.btcoll.collidepoint(mousePos) and Info.wirestarter is not self and self.topin is None:
                Info.wires.append(Wire(Info.wirestarter, self, "bt", self.screen))
                Info.wiring = False
                self.topin = Info.wirestarter
            elif click and self.bbcoll.collidepoint(mousePos) and Info.wirestarter is not self and self.botin is None:
                Info.wires.append(Wire(Info.wirestarter, self, "bb", self.screen))
                Info.wiring = False
                self.botin = Info.wirestarter
            else:
                pygame.draw.line(self.screen, (255, 255, 0), Info.wirestart, mousePos, 5)
        elif Info.dragging and self == Info.selected:
            self.x = mousePos[0] - Info.xoffset
            self.y = mousePos[1] - Info.yoffset
        elif self.fcoll.collidepoint(mousePos) and click:
            Info.selected = self
            Info.wiring = True
            Info.wirestart = (self.fcoll.x + 10, self.fcoll.y + 10)
            Info.wirestarter = self
        elif self.coll.collidepoint(mousePos) and click:
            Info.selected = self
            Info.dragging = True
            Info.xoffset = mousePos[0] - self.x
            Info.yoffset = mousePos[1] - self.y
        self.coll = pygame.Rect(self.x, self.y, self.width, self.height)
        self.btcoll = pygame.Rect(self.x, self.y + 5, 20, 20)
        self.bbcoll = pygame.Rect(self.x, self.y + self.height - 25, 20, 20)
        self.fcoll = pygame.Rect(self.x + self.width - 20, self.y + self.height / 2 - 10, 20, 20)
        pygame.draw.rect(self.screen, (255, 0, 0), self.btcoll, 1)
        pygame.draw.rect(self.screen, (255, 0, 0), self.bbcoll, 1)
        pygame.draw.rect(self.screen, (255, 0, 0), self.fcoll, 1)






