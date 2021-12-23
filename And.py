import pygame

from Gate import Gate


class And(Gate):
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, "andgate.png")
        self.topin = None
        self.botn = None

    def evaluate(self, visit, kmap=False, stri=False):
        if stri:
            return self.topin.evaluate(visit, stri=True) + self.botin.evaluate(visit, stri=True)
        if self.topin is None or self.botin is None or self in visit:
            return -1
        visit.append(self)
        vis1 = self.topin.evaluate(visit.copy(), kmap)
        vis2 = self.botin.evaluate(visit.copy(), kmap)
        if (vis1 == -1 or vis2 == -1):
            return -1
        return vis1 and vis2