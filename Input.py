import pygame

import Info


class Input:
    def __init__(self, x, y, screen, label):
        self.screen = screen
        self.height = 40
        self.width = 40
        self.x = x
        self.y = y
        self.coll = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fcoll = pygame.Rect(self.x + self.width - 5, self.y + self.height / 2 - 10, 20, 20)
        self.on = False
        self.label = label
        self.rendlabel = pygame.font.SysFont("", 55).render(self.label, True, (255, 255, 255))

    def tick(self, mousePos, click):
        if Info.wiring:
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
            self.on = not self.on
        self.coll = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fcoll = pygame.Rect(self.x + self.width - 5, self.y + self.height / 2 - 10, 20, 20)
        pygame.draw.rect(self.screen, (0, 255, 0) if self.on else (255, 0, 0), self.coll)
        self.screen.blit(self.rendlabel,
         (self.coll.x + (self.coll.width - self.rendlabel.get_width()) / 2, self.coll.y + (self.coll.height - self.rendlabel.get_height()) / 2))
        pygame.draw.rect(self.screen, (255, 0, 0), self.fcoll, 1)

    def evaluate(self, visit, kmap=False, stri=False):
        if stri:
            return self.label
        if kmap is not False:
            # print(kmap, self.label, kmap[(ord(self.label[0])) - ord('A')])
            return kmap[(ord(self.label[0])) - ord('A')]
        return self.on