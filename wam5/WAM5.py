# collision detection
# operational timer and game over
# keep score and transparent images to show points
import random
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *

# need for making .exe later
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Colors we want to use
pink = (255,157,195)
white = (255,255,255)
black = (0, 0, 0)
lightblue = (30,144,255)
darkblue = (0,0,139)
red = (255,0,0)

# Sounds we want to use
pygame.mixer.init()
hitsound = pygame.mixer.Sound('hit.wav')
buzzer = pygame.mixer.Sound('buzzer.wav')
gameover = pygame.mixer.Sound('gameover.mp3')

# set up the display
pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption("Whack a Mole!")
screen.fill(pink)

moleabsent = image.load(resource_path("molehole.png")).convert()
molealive = image.load(resource_path("molealive.png")).convert()
moledead = image.load(resource_path("moledead.png")).convert()
plus2 = image.load(resource_path("p22.png")).convert_alpha()
minus1 = image.load(resource_path("m22.png")).convert_alpha()

# Mole class
class Mole(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        # Each mole sprite is 80X62
        self.image = moleabsent
        self.x = x
        self.y = y
        self.points = 0
        self.rect = self.image.get_rect().move(x,y)
        self.status = 'absent'

# for timing
framerate = 1000  # you can modify to adjust speed of animation, 1 second = 1000 milliseconds
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, framerate)
points = 0

# create our moles
moles = [[None for _ in range(5)] for _ in range(5)]
x = 100
y = 100
for i in range(5):
    for j in range(5):
        moles[i][j] = Mole(x,y)
        x += 100
    x = 100
    y += 100

# create some fonts
headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Corbel',32)
buttonfont.set_bold(True)

# create some text
headerText = headerfont.render("Whack 'A Mole!", True, black, pink)
headerRect = headerText.get_rect()
headerRect.center = (350,50)
pygame.draw.rect(screen,pink,headerRect)
screen.blit(headerText, headerRect)

timerText = buttonfont.render("00:00:00",True,black,pink)
timerRect = timerText.get_rect()
timerRect.center = (150,600)
pygame.draw.rect(screen,pink,timerRect)

scoreText = buttonfont.render("Score:     ", True, black,pink)
scoreRect = scoreText.get_rect()
scorex = 350
scorey = 650
scoreRect.center = (scorex,scorey)
pygame.draw.rect(screen,pink,scoreRect)

# create text and info for our quit button
quitButtonText = buttonfont.render(" Quit ", True, black, pink)
quitButtonRect = quitButtonText.get_rect()
quitButtonx = 200
quitButtony = 600
quitButtonwidth = quitButtonRect.width
quitButtonheight = quitButtonRect.height
quitButtonRect.topleft = (quitButtonx,quitButtony)
pygame.draw.rect(screen,white,quitButtonRect)
screen.blit(quitButtonText, quitButtonRect)

# create text and info for our start button
startButtonText = buttonfont.render(" Start ", True, black, pink)
startButtonRect = startButtonText.get_rect()
startButtonx = 400
startButtony = 600
startButtonwidth = startButtonRect.width
startButtonheight = startButtonRect.height
startButtonRect.topleft = (startButtonx,startButtony)
pygame.draw.rect(screen,white,startButtonRect)
screen.blit(startButtonText, startButtonRect)

allmoles = Group(moles)
allmoles.draw(screen)
gameStarted = False
gameCompleted = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # find mouse position
        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]

        if event.type == TIMEREVENT:
            # this means our timer went off!
            # randomly set moles to be up or down
            if gameStarted:
                secondsRemaining -= 1
                for i in range(5):
                    for j in range(5):
                        # if mole was absent, randomly makeit alive
                        aliveodds = 20
                        absentodds = 3
                        if moles[i][j].status == 'absent':
                            r = random.randint(1,aliveodds)
                            if r == 1:
                                moles[i][j].status = 'alive'
                                moles[i][j].image = molealive
                        # if alive, randomly make it absent
                        elif moles[i][j].status == 'alive':
                            r = random.randint(1, absentodds)
                            if r == 1:
                                moles[i][j].status = 'absent'
                                moles[i][j].image = moleabsent
                        elif moles[i][j].status == 'dead':
                            moles[i][j].status = 'absent'
                            moles[i][j].image = moleabsent

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # was the quit rectangle clicked?
            if not gameStarted and mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                    mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                pygame.quit()
                sys.exit()
            if not gameStarted and mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                mousey >= startButtony and mousey <= startButtony + startButtonheight:
                gameStarted = True
                secondsRemaining = 120
                points = 0
                pygame.mouse.set_visible(False)
                cursor_image = pygame.image.load("hammer.png")
                cursor_rect = cursor_image.get_rect()
            if gameStarted:
                for i in range(5):
                    for j in range(5):
                        if mousex >= moles[i][j].x and mousex <= moles[i][j].x + 80 and \
                            mousey >= moles[i][j].y and mousey <= moles[i][j].y + 62:
                            if moles[i][j].status == 'alive':
                                moles[i][j].image = moledead
                                moles[i][j].status = 'dead'
                                moles[i][j].points = 2
                                hitsound.play()
                                points += 2
                            else:
                                buzzer.play()
                                points -= 1
                                moles[i][j].points = -1

        # paint the background
        screen.fill(pink)

        # draw the header
        pygame.draw.rect(screen, pink, headerRect)
        screen.blit(headerText, headerRect)

        # draw the moles
        allmoles.draw(screen)

        for i in range(5):
            for j in range(5):
                if moles[i][j].points != 0:
                    if moles[i][j].points == 2:
                        screen.blit(plus2,(moles[i][j].x,moles[i][j].y-30))
                    elif moles[i][j].points == -1:
                        screen.blit(minus1, (moles[i][j].x, moles[i][j].y - 30))
                    moles[i][j].points = 0

        if gameStarted:
            cursor_rect.center = pygame.mouse.get_pos()
            screen.blit(cursor_image, cursor_rect)

            minutes = str(secondsRemaining // 60)
            seconds = str(secondsRemaining % 60)
            if len(minutes) < 2:
                minutes = "0" + minutes
            if len(seconds) < 2:
                seconds = "0" + seconds
            timerText = buttonfont.render(minutes + ":" + seconds, True, black, pink)
            timerRect = timerText.get_rect()
            timerRect.center = (150, 600)
            pygame.draw.rect(screen, pink, timerRect)
            screen.blit(timerText, timerRect)

            scorelen = len(str(points))
            scoreText = buttonfont.render("Score: " + str(points) + " " * (5-scorelen), True, black, pink)
            scoreRect = scoreText.get_rect()
            scoreRect.center = (scorex,scorey)
            pygame.draw.rect(screen, pink, scoreRect)
            screen.blit(scoreText, scoreRect)

            if secondsRemaining < 0:
                gameStarted = False
                for i in range(5):
                    for j in range(5):
                        moles[i][j].image = moleabsent
                        moles[i][j].status = 'absent'
                gameCompleted = True
                gameover.play()
                pygame.mouse.set_cursor(pygame.cursors.Cursor())
        else:
            pygame.mouse.set_visible(True)
            # if hovering on a button, change its color
            if mousex >= quitButtonx and mousex <= quitButtonx + quitButtonwidth and \
                    mousey >= quitButtony and mousey <= quitButtony + quitButtonheight:
                quitButtonText = buttonfont.render(" Quit ", True, red, pink)
            else:
                quitButtonText = buttonfont.render(" Quit ", True, black, pink)

            if gameCompleted:
                scorelen = len(str(points))
                #scoreText = buttonfont.render("Score: " + str(points) + " " * (5 - scorelen), True, black, pink)
                scoreText = buttonfont.render("GAME OVER, Score: " + str(points), True, darkblue, pink)
                scoreRect = scoreText.get_rect()
                scoreRect.center = (scorex,scorey)
                pygame.draw.rect(screen, pink, scoreRect)
                screen.blit(scoreText, scoreRect)

            # draw the quit button text
            screen.blit(quitButtonText, quitButtonRect)

            if mousex >= startButtonx and mousex <= startButtonx + startButtonwidth and \
                    mousey >= startButtony and mousey <= startButtony + startButtonheight:
                startButtonText = buttonfont.render(" Start ", True, red, pink)
            else:
                startButtonText = buttonfont.render(" Start ", True, black, pink)

            # draw the start button text
            screen.blit(quitButtonText, quitButtonRect)
            screen.blit(startButtonText, startButtonRect)

        #update the display
        pygame.display.update()