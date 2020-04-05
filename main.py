import pygame, math, random, threading


# OPTIONS:
verticeAmount = 3
dotAmount = 2
division = 2
fontSize = 20
allowRepeat = True # If the random choise can be the same dot again
framesPerSec = 1
dotSwitch = False # If True, dots will be pixels instead of circles
circleSize = 6
# -------

w, h = 1200, 1000; run = True; framesCount = 0; 
mouseHold = False; mouseInfo = []
vertices = []; dots = []; previousDot = []
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("The Chaos Game")
font = pygame.font.SysFont("candara", fontSize, 1, 1)
clock = pygame.time.Clock()


def new_vertex():
    ranX, ranY = random.randint(0, w), random.randint(0, h)
    vertices.append([ranX, ranY, (0, 255, 0)])
    pygame.draw.circle(screen, (0, 255, 0), (ranX, ranY), 6)    


def re_fresh():
    screen.fill((0, 0, 0))
    for i in vertices:
        pygame.draw.circle(screen, (0, 255, 0), (i[0], i[1]), 6)   

    text = font.render("[1 2] Size: " + str(round(division, 2)), 1, (255, 255, 255))
    text1 = font.render("[3] Allow repeat: " + str(allowRepeat), 1, (255, 255, 255))
    text2 = font.render("[4 5] Vertice amount: " + str(len(vertices)), 1, (255, 255, 255))
    text3 = font.render("[6 7] Frames per second: " + str(framesPerSec), 1, (255, 255, 255))
    text4 = font.render("[8] Pixel/Circle switch: " + str(dotSwitch), 1, (255, 255, 255))
    text5 = font.render("[9 0] Circle size " + str(circleSize), 1, (255, 255, 255))
    text6 = font.render("[esc] Exit", 1, (255, 255, 255))
    screen.blit(text, (w - fontSize * 12, fontSize * 0))
    screen.blit(text1, (w - fontSize * 12, fontSize * 1))
    screen.blit(text2, (w - fontSize * 12, fontSize * 2))
    screen.blit(text3, (w - fontSize * 12, fontSize * 3))
    screen.blit(text4, (w - fontSize * 12, fontSize * 4))
    screen.blit(text5, (w - fontSize * 12, fontSize * 5))
    screen.blit(text6, (w - fontSize * 12, fontSize * 6))


def change_per_sec(num):
    global framesCount, framesPerSec
    if framesCount + num > 6 or framesCount + num < 0:
        return
    framesCount += num
    if framesCount == 0:
        framesPerSec = 1
    if framesCount == 1:
        framesPerSec = 10
    elif framesCount == 2:
        framesPerSec = 100
    elif framesCount == 3:
        framesPerSec = 500
    elif framesCount == 4:
        framesPerSec = 1000
    elif framesCount == 5:
        framesPerSec = 1001
    elif framesCount == 6:
        framesPerSec = 1000000


def render(i):
    dot = dots[i]
    while run:
        clock.tick(framesPerSec)
        global vertices
        global previousDot
        try:
            ranDot = random.choice(vertices)
        except: pass
        else:
            if allowRepeat == True or ranDot != previousDot[i]:
                previousDot[i] = ranDot
                dot = (dot[0] + (ranDot[0] - dot[0]) / division, dot[1] + (ranDot[1] - dot[1]) / division)   
                # print(dots)
                # print(int(dot[0]), int(dot[1]))
                try:
                    if dotSwitch:
                        screen.set_at((int(dot[0]), int(dot[1])), (255, 255, 255))
                    else:
                        pygame.draw.circle(screen, (255, 255, 255), (int(dot[0]), int(dot[1])), circleSize)
                except: pass


for i in range(0, verticeAmount):
    new_vertex()

for i in range(0, dotAmount):
    dX, dY = random.randint(0, w), random.randint(0, h)
    dots.append([dX, dY])
    pygame.draw.circle(screen, (0, 0, 255), (dX, dY), 6)
    previousDot.append(None)
pygame.display.update()

# ranDot1 = random.choice(vertices)
# newDot = [dot[0] + (ranDot1[0] - dot[0]), dot[1] + (ranDot1[1] - dot[1])]    
# print(ranDot1)
# print(newDot)

for i in range(0, len(dots)):
    rP = threading.Thread(target=render, args=(i,))
    rP.start()

tick1 = pygame.time.get_ticks()
tick2 = pygame.time.get_ticks()
tick3 = pygame.time.get_ticks()
    
while run:
    clock.tick(60)
    key = pygame.key.get_pressed()

    # Exit
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mX, mY = pygame.mouse.get_pos()
            if mouseHold:
                # try: mouseInfo[2][2] = (0, 255, 0)
                # except: pass
                mouseHold = False
            else:
                for i in vertices:
                    if i[0] - 10 < mX < i[0] + 10 and i[1] - 10 < mY < i[1] + 10:
                        mouseInfo = [mX, mY, i]
                        # i[2] = (255, 0, 0)
                        mouseHold = True 
            # re_fresh()   
            
        if event.type == pygame.QUIT:
            break

    if key[pygame.K_ESCAPE]:
        run = False

    # Settings
    if pygame.time.get_ticks() - tick2 > 50:
        if key[pygame.K_1]:
            tick2 = pygame.time.get_ticks()
            division -= 0.02
            re_fresh()

        if key[pygame.K_2]:
            tick2 = pygame.time.get_ticks()
            division += 0.02
            re_fresh()

    if pygame.time.get_ticks() - tick3 > 100:
        if key[pygame.K_3]:
            tick3 = pygame.time.get_ticks()
            if allowRepeat:
                allowRepeat = False
            else:
                allowRepeat = True
            re_fresh()

        if key[pygame.K_4]:
            try:
                vertices.pop(-1)
                tick3 = pygame.time.get_ticks()
                re_fresh()
            except: pass

        if key[pygame.K_5]:
            tick3 = pygame.time.get_ticks()
            new_vertex()
            re_fresh()
        
        if key[pygame.K_6]:
            tick3 = pygame.time.get_ticks()
            change_per_sec(-1)
            
        if key[pygame.K_7]:
            tick3 = pygame.time.get_ticks()
            change_per_sec(1)

        if key[pygame.K_8]:
            tick3 = pygame.time.get_ticks()
            if dotSwitch:
                dotSwitch = False
            else:
                dotSwitch = True
            
        if key[pygame.K_9]:
            tick3 = pygame.time.get_ticks()
            circleSize -= 1

        if key[pygame.K_0]:
            tick3 = pygame.time.get_ticks()
            circleSize += 1

    # Mouse
    if mouseHold and pygame.time.get_ticks() - tick1 > 50:
        tick1 = pygame.time.get_ticks()
        mX, mY = pygame.mouse.get_pos()
        if mouseInfo[0] != mX or mouseInfo[1] != mY:
            mouseInfo[0] = mX; mouseInfo[1] = mY
            mouseInfo[2][0] = mX; mouseInfo[2][1] = mY
            re_fresh()

    pygame.display.update()