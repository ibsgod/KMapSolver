import pygame

import Info


class Wire:
    def __init__(self, start, end, loc, screen):
        self.start = start
        self.end = end
        self.screen = screen
        self.loc = loc

    def tick(self, mousePos, click):
        pos = None
        if self.loc == "bt":
            pos = (self.end.btcoll.x + 10, self.end.btcoll.y + 10)
        elif self.loc == "bb":
            pos = (self.end.bbcoll.x + 10, self.end.bbcoll.y + 10)
        elif self.loc == "b":
            pos = (self.end.bcoll.x + 10, self.end.bcoll.y + 10)
        if click and mousePos[0] >= min (pos[0], self.start.fcoll.x) and mousePos[0] <= max(pos[0], self.start.fcoll.x):
            if (abs((pos[0] - self.start.fcoll.x) * mousePos[1] + mousePos[0] * (self.start.fcoll.y -
                                                                                 pos[1]) + (
                            self.start.fcoll.x - pos[0]) * self.start.fcoll.y +
                    (pos[1] - self.start.fcoll.y) * self.start.fcoll.x) / ((pos[0] - self.start.fcoll.x) ** 2 +
                                                                           ((self.start.fcoll.y - pos[
                                                                               1]) ** 2)) ** 0.5 <= 25):
                Info.wires.remove(self)
                self.start.out = None
                if self.loc == "bt":
                    self.end.topin = None
                if self.loc == "bb":
                    self.end.botin = None
                if self.loc == "b":
                    self.end.inp = None
            else:
                pygame.draw.line(self.screen, (255, 255, 0), (self.start.fcoll.x + 10, self.start.fcoll.y + 10), pos, 5)

        else:
            pygame.draw.line(self.screen, (255, 255, 0), (self.start.fcoll.x + 10, self.start.fcoll.y + 10), pos, 5)
