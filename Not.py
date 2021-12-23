import pygame

import Info
from Gate import Gate
from Wire import Wire


class Not(Gate):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, "notgate.png")
        self.inp = None
        self.bcoll = pygame.Rect(self.x, self.y + self.height / 2 - 10, 20, 20)
        self.fcoll = pygame.Rect(self.x + self.width - 20, self.y + self.height / 2 - 10, 20, 20)

    def tick(self, mousePos, click):
        self.screen.blit(self.img, (self.x, self.y))
        if Info.wiring:
            if click and self.bcoll.collidepoint(mousePos) and Info.wirestarter is not self and self.inp is None:
                Info.wires.append(Wire(Info.wirestarter, self, "b", self.screen))
                Info.wiring = False
                self.inp = Info.wirestarter
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
        self.bcoll = pygame.Rect(self.x, self.y + self.height / 2 - 10, 20, 20)
        self.fcoll = pygame.Rect(self.x + self.width - 20, self.y + self.height / 2 - 10, 20, 20)
        pygame.draw.rect(self.screen, (255, 0, 0), self.bcoll, 1)
        pygame.draw.rect(self.screen, (255, 0, 0), self.fcoll, 1)

    def evaluate(self, visit, kmap=False, stri=False):
        if stri:
            return "(~" + self.inp.evaluate(visit, stri=True) + ")"
        if self.inp is None or self in visit:
            return -1
        visit.append(self)
        vis1 = self.inp.evaluate(visit.copy(), kmap)
        if (vis1 == -1):
            return -1
        return not vis1