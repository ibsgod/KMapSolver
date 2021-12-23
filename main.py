import sys

import pygame
import os

import Info
from And import And
from Button import Button
from Input import Input
from Not import Not
from Or import Or
from Output import Output
from Wire import Wire

pygame.mixer.init()
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 1200
height = 650
buttDict = {}
screen = pygame.display.set_mode((width, height))
buttDict["and"] = Button(width - 125, 25, 100, 100, screen, color=(0, 204, 255), label=pygame.font.SysFont("", 55).render("AND", True, (255, 255, 255)))
buttDict["or"] = Button(width - 125, 150, 100, 100, screen, color=(255, 0, 0), label=pygame.font.SysFont("", 55).render("OR", True, (255, 255, 255)))
buttDict["not"] = Button(width - 125, 275, 100, 100, screen, color=(0, 204, 33), label=pygame.font.SysFont("", 55).render("NOT", True, (255, 255, 255)))
buttDict["inp"] = Button(width - 125, 400, 100, 100, screen, color=(245, 245, 0), label=pygame.font.SysFont("", 45).render("INPUT", True, (255, 255, 255)))
buttDict["reset"] = Button(width - 125, 525, 100, 100, screen, color=(140, 140, 140), label=pygame.font.SysFont("", 40).render("RESET", True, (255, 255, 255)))
buttDict["simplify"] = Button(width/2 - 125, height - 120, 250, 100, screen, color=(215, 30, 200), label=pygame.font.SysFont("", 63).render("Simplify!", True, (255, 255, 255)))
botLbl = ""
gatex = 80
gatey = 160
c = pygame.time.Clock()
Info.out = [(Output(width / 2, height / 2, screen))]
def kmap(output):
    mappy = [[None] * 4 for i in range(4)]
    bins = [[False, False], [False, True], [True, True], [True, False]]
    for i in range(4):
        for j in range(4):
            if output.evaluate(bins[i] + bins[j]) == True:
                mappy[i][j] = 1
            else:
                mappy[i][j] = 0
    bigmappy = [[None] * 12 for i in range(12)]
    for i in range(12):
        for j in range(12):
            bigmappy[i][j] = mappy[i%4][j%4]
    groups = []
    # for i in bigmappy:
    #     print(i)
    for i in range(4, 8):
        for j in range(4, 8):
            if bigmappy[i][j] == 1:
                groupie = findgroups(bigmappy, groups, (i, j, 1, 1))
                # print(groupie, "h")
                if groupie != -1:
                    yes = False
                    for g in groups:
                        if not (groupie[0] != g[0] or groupie[1] != g[1] or groupie[2] != g[2] or groupie[3] != g[3]):
                            yes = True
                    if not yes:
                        groups.append(groupie)
# each element in 2d for loop to return biggest possible thinghy
#     print(groups)
    interpret(groups)

def interpret(groups):
    orlist = []
    for g in groups:
        bins = [[False, False], [False, True], [True, True], [True, False]]
        bools = [bins[g[0]][0], bins[g[0]][1], bins[g[1]][0], bins[g[1]][1]]
        inc = [True, True, True, True]
        for i in range(g[0], g[0] + g[2]):
            for j in range(g[1], g[1] + g[3]):
                if bins[i%4][0] != bools[0]:
                    inc[0] = False
                if bins[i%4][1] != bools[1]:
                    inc[1] = False
                if bins[j%4][0] != bools[2]:
                    inc[2] = False
                if bins[j%4][1] != bools[3]:
                    inc[3] = False
        andlist = []
        for k in range(4):
            if inc[k]:
                andlist.append(bools[k])
            else:
                andlist.append(None)
        orlist.append(andlist)
    layout(orlist)

def layout(orlist):
    global gatex
    global gatey
    Info.gates = []
    Info.wires = []
    Info.out[0].inp = None
    Info.inp[0].x = 80
    Info.inp[0].y = 160
    for i in range(1,4):
        Info.inp[i].x = 80
        Info.inp[i].y = Info.inp[i-1].y + 100
    gatex = 230
    gatey = 160
    curror = None
    for i in orlist:
        currand = None
        for j in range(len(i)):
            newinp = Info.inp[j]
            if i[j] == None:
                continue
            if i[j] == False:
                newinp = Not(gatex, gatey, screen)
                newinp.inp = Info.inp[j]
                Info.gates.append(newinp)
                Info.wires.append(Wire(Info.inp[j], newinp, "b", screen))
                if gatey > height - 200:
                    gatex += 150
                    gatey = 160
                else:
                    gatey += 100
            if currand == None:
                currand = newinp
            else:
                newand = And(gatex, gatey, screen)
                newand.topin = currand
                newand.botin = newinp
                Info.wires.append(Wire(currand, newand, "bt", screen))
                Info.wires.append(Wire(newinp, newand, "bb", screen))
                Info.gates.append(newand)
                currand = newand
                if gatey > height - 200:
                    gatex += 150
                    gatey = 160
                else:
                    gatey += 100
        if curror == None:
            curror = currand
        else:
            newor = Or(gatex, gatey, screen)
            newor.topin = curror
            newor.botin = currand
            Info.wires.append(Wire(curror, newor, "bt", screen))
            Info.wires.append(Wire(currand, newor, "bb", screen))
            Info.gates.append(newor)
            curror = newor
            if gatey > height - 200:
                gatex += 150
                gatey = 160
            else:
                gatey += 100
    if curror is not None:
        Info.out[0].inp = curror
        Info.wires.append(Wire(curror, Info.out[0], "b", screen))


def findgroups(mappy, groups, pos):
    if pos[2] == 1 and pos[3] == 1 and not checknew(pos, groups):
        return -1
    else:
        if pos[2] < 4 and checkones(mappy, (pos[0], pos[1], pos[2] * 2, pos[3]))\
        and checknew((pos[0], pos[1], pos[2] * 2, pos[3]), groups):
            return findgroups(mappy, groups, (pos[0], pos[1], pos[2] * 2, pos[3]))
        elif pos[2] < 4 and checkones(mappy, (pos[0] - pos[2], pos[1], pos[2] * 2, pos[3]))\
        and checknew((pos[0] - pos[2], pos[1], pos[2] * 2, pos[3]), groups):
            return findgroups(mappy, groups, (pos[0] - pos[2], pos[1], pos[2] * 2, pos[3]))
        elif pos[3] < 4 and checkones(mappy, (pos[0], pos[1], pos[2], pos[3] * 2))\
        and checknew((pos[0], pos[1], pos[2], pos[3] * 2), groups):
            return findgroups(mappy, groups, (pos[0], pos[1], pos[2], pos[3] * 2))
        elif pos[3] < 4 and checkones(mappy, (pos[0], pos[1] - pos[3], pos[2], pos[3] * 2))\
        and checknew((pos[0], pos[1] - pos[3], pos[2], pos[3] * 2), groups):
            return findgroups(mappy, groups, (pos[0], pos[1] - pos[3], pos[2], pos[3] * 2))
        else:
            return (pos[0]%4, pos[1]%4, pos[2], pos[3])



def checkones(mappy, pos):
    for i in range(pos[0], pos[0] + pos[2]):
        for j in range(pos[1], pos[1] + pos[3]):
            if mappy[i][j] == 0:
                return False
    return True

def checknew(pos, groups):
    # print(pos, "p")
    # print(groups)
    yes = False
    for i in range(pos[0], pos[0] + pos[2]):
        for j in range(pos[1], pos[1] + pos[3]):
            if len(groups) == 0:
                yes = True
                break
            # print(groups, "g")
            yesyes = False
            for g in groups:
                if not((g[0] + g[2] - 1 < 4 and g[0] > i%4) or (g[0] + g[2] - 1 >= 4 and (g[0] + g[2] - 1)%4 < i%4) or g[0] + g[2] - 1 < i%4
                       or (g[1] + g[3] - 1 < 4 and g[1] > j%4) or (g[1] + g[3] - 1 > 4 and (g[1] + g[3] - 1)%4 < j%4) or g[1] + g[3] - 1 < j%4):
                    yesyes = True
                    break
            if not yesyes:
                # print(i, j)
                yes = True
                break
    if not yes:
        return False
    return True


while True:
    mousePos = pygame.mouse.get_pos()
    screen.fill((240, 240, 255))
    click = False
    rightclick = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            rightclick = True
        if event.type == pygame.MOUSEBUTTONUP:
            Info.dragging = False
    if not(len(Info.inp) == 4 and len(Info.out) >= 1 and Info.out[0].evaluate() != -1):
        buttDict["simplify"].color = (100, 100, 100)
        buttDict["simplify"].label = pygame.font.SysFont("", 33).render("Not valid 4-input circuit", True, (255, 255, 255))
    else:
        buttDict["simplify"] = Button(width / 2 - 125, height - 120, 250, 100, screen, color=(215, 30, 200),
                                      label=pygame.font.SysFont("", 63).render("Simplify!", True, (255, 255, 255)))

    for i in buttDict:
        val = buttDict[i].tick(mousePos, click)
        if val and i == "and":
            Info.gates.append(And(gatex, gatey, screen))
            if gatey > height - 200:
                gatex += 150
                gatey = 160
            else:
                gatey += 100
        if val and i == "or":
            Info.gates.append(Or(gatex, gatey, screen))
            if gatey > height - 200:
                gatex += 150
                gatey = 160
            else:
                gatey += 100
        if val and i == "not":
            Info.gates.append(Not(gatex, gatey, screen))
            if gatey > height - 200:
                gatex += 150
                gatey = 160
            else:
                gatey += 100
        if val and i == "inp":
            if len(Info.inp) == 0:
                Info.inp.append(Input(gatex, gatey, screen, "A"))
            else:
                Info.inp.append(Input(gatex, gatey, screen, str(chr(ord(Info.inp[len(Info.inp)-1].label[0])+1))))
            if gatey > height - 200:
                gatex += 150
                gatey = 160
            else:
                gatey += 100
        if val and i == "simplify":
            if len(Info.inp) == 4 and len(Info.out) >= 1 and Info.out[0].evaluate() != -1:
                kmap(Info.out[0])
        if val and i == "reset":
            Info.inp = []
            Info.gates = []
            Info.wires = []
            Info.out[0].inp = None
            Info.wiring = False
            botLbl = ""
            gatex = 80
            gatey = 160
    for i in Info.gates:
        i.tick(mousePos, click)
    for i in Info.wires:
        i.tick(mousePos, rightclick)
    for i in Info.inp:
        i.tick(mousePos, click)
    for i in Info.out:
        i.tick(mousePos, click)
    botLbl = ""
    if Info.out[0].evaluate() != -1:
        botLbl = Info.out[0].evaluate(stri=True)
    botLbl = pygame.font.SysFont("", 63).render(botLbl, True, (215, 30, 200))
    screen.blit(botLbl, (width/2 - botLbl.get_width()/2, 20))
    c.tick(30)
    pygame.display.update()

