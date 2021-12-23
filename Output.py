import pygame

import Info
from Wire import Wire


class Output:
    def __init__(self, x, y, screen):
        self.screen = screen
        self.img = pygame.image.load("lightoff.png")
        self.height = self.img.get_height()
        self.width = self.img.get_width()
        self.x = x
        self.y = y
        self.coll = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bcoll = pygame.Rect(self.x + self.width/2 - 10, self.y + self.height - 20, 20, 20)
        self.on = False
        self.inp = None


    def tick(self, mousePos, click):
        if Info.wiring:
            if click and self.bcoll.collidepoint(mousePos) and self.inp is None:
                Info.wires.append(Wire(Info.wirestarter, self, "b", self.screen))
                Info.wiring = False
                self.inp = Info.wirestarter
            else:
                pygame.draw.line(self.screen, (255, 255, 0), Info.wirestart, mousePos, 5)
        elif Info.dragging and self == Info.selected:
            self.x = mousePos[0] - Info.xoffset
            self.y = mousePos[1] - Info.yoffset
        elif self.coll.collidepoint(mousePos) and click:
            Info.selected = self
            Info.dragging = True
            Info.xoffset = mousePos[0] - self.x
            Info.yoffset = mousePos[1] - self.y
        self.coll = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bcoll = pygame.Rect(self.x + self.width/2 - 10, self.y + self.height - 20, 20, 20)
        self.on = self.evaluate()
        if self.on != -1 and self.on != False:
            self.img = pygame.image.load("lighton.png")
        else:
            self.img = pygame.image.load("lightoff.png")
        self.screen.blit(self.img, (self.x, self.y))
        pygame.draw.rect(self.screen, (255, 0, 0), self.bcoll, 1)

    def evaluate(self, kmap=False, stri=False):
        if self.inp is None or self.inp.evaluate([]) == -1:
            return -1
        return self.inp.evaluate([], kmap, stri)

