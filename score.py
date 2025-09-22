from peewee import *
import pygame, sys
from peewee import *
from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os
from pygame.locals import *
import random


db = MySQLDatabase(
    'pirate',
    host='localhost',
    port=3306,
    user='root',
    password='root'
)

class BaseModel(Model):
    class Meta:
        database = db

class Scores(BaseModel):
    #scoreID = AutoField() 
    ScoreName = CharField
    ScoreVal = IntegerField()

# try:
#     db.connect()
# except:
#     print("nah")

db.connect()


scores=[None for _ in range(3)]
scoreVals = [None for _ in range(3)]

cursor = db.execute_sql("select scores.scorename, scores.scoreval from scores order by scores.scoreval desc limit 3")

i = 0
for row in cursor.fetchall():
    scores[i] = row[0] + " " + str(row[1])
    scoreVals[i] = row[1]
    print(scores[i])
    i += 1

db.close


addingScore = False
doneAdding = False
initial1 = ''
initial2 = ''
initial3 = ''
def addScore(name, score):
    global scores
    global db
    global addingScore
    db.connect() 
    cursor = db.execute_sql("insert into scores(scorename, scoreval) VALUES ('" + name + "', " + str(score) + ")")
    cursor = db.execute_sql("select scores.scorename, scores.scoreval from scores order by scores.scoreval desc limit 3")
    i = 0
    for row in cursor.fetchall():
        #print(row[0], row[1])
        scores[i] = row[0] + " " + str(row[1])
        print(scores[i])
        i += 1
    db.close()

# Colors we want to use
pink = (255,157,195)
black = (0, 0, 0)
red = (255,0,0)
white = (255,255,255)

# set up the display
pygame.init()
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption("Read from database")
screen.fill(pink)

# create some fonts
headerfont = Font('freesansbold.ttf', 24)
headerfont.set_bold(True)
header2font = Font('freesansbold.ttf', 18)
header2font.set_bold(True) 
infofont = Font('freesansbold.ttf', 16)
buttonfont = pygame.font.SysFont('Corbel',32)
buttonfont.set_bold(True)

# create some text
headerText = headerfont.render("Your score is in the top 3! Add to high scores?", True, black, pink)
headerRect = headerText.get_rect()
headerRect.center = (350,50)
pygame.draw.rect(screen,pink,headerRect)
screen.blit(headerText, headerRect)

subheaderText = header2font.render("Current Top 3", True, black,pink)
subheaderRect = subheaderText.get_rect() 
subheaderRect.center = (350,150)
screen.blit(subheaderText, subheaderRect)

highscore1Text = infofont.render(scores[0], True, red, pink)
highscore1Rect = highscore1Text.get_rect() 
highscore1Rect.center = (350, 170) 
pygame.draw.rect(screen,pink,highscore1Rect)
highscore2Text = infofont.render(scores[1], True, red, pink)
highscore2Rect = highscore2Text.get_rect() 
highscore2Rect.center = (350, 190) 
pygame.draw.rect(screen,pink,highscore2Rect)
highscore3Text = infofont.render(scores[2], True, red, pink)
highscore3Rect = highscore3Text.get_rect() 
highscore3Rect.center = (350, 210) 
pygame.draw.rect(screen,pink,highscore3Rect)

initial1Text = infofont.render("_", True, black, white)
initial1Rect = initial1Text.get_rect()
initial1Rect.center = (330, 280) 
pygame.draw.rect(screen,pink,initial1Rect)
initial2Text = infofont.render("_", True, black, white)
initial2Rect = initial2Text.get_rect()
initial2Rect.center = (345, 280) 
pygame.draw.rect(screen,pink,initial1Rect)
initial3Text = infofont.render("_", True, black, white)
initial3Rect = initial3Text.get_rect()
initial3Rect.center = (360, 280) 
pygame.draw.rect(screen,pink,initial1Rect)
instructionText = header2font.render("Enter your 3 initials", True,black,pink)
instructionRect = instructionText.get_rect()
instructionRect.center = (350,250)
pygame.draw.rect(screen,pink,instructionRect)
init1 = init2 = init3 = '_'

# create text and info for our yes button
buttonx = 100
buttony = 75
buttonw = 200
buttonh = 50
yesButtonText = buttonfont.render("YES", True, black, white)
yesButtonRect = yesButtonText.get_rect()
yesButtonRect.x = buttonx
yesButtonRect.y = buttony
yesButtonRect.w = buttonw
yesButtonRect.h = buttonh
# Border rect (outer rectangle)
yesborderRect = pygame.Rect(buttonx, buttony, buttonw, buttonh)
# Inner rect (slightly inset so border is visible)
yesinnerRect = yesborderRect.inflate(-10, -10)  # shrink by 10px in width & height
# Draw red border
pygame.draw.rect(screen, (255, 0, 0), yesborderRect, border_radius=30)
# Draw white fill inside the border
pygame.draw.rect(screen, (255, 255, 255), yesinnerRect, border_radius=25)
# Draw text centered in the inner rect
yestextRect = yesButtonText.get_rect(center=yesinnerRect.center)
screen.blit(yesButtonText, yestextRect)

noButtonText = buttonfont.render("No thanks", True, black, white)
noButtonRect = noButtonText.get_rect()
noButtonRect.x = buttonx+300
noButtonRect.y = buttony
noButtonRect.w = buttonw
noButtonRect.h = buttonh
# Border rect (outer rectangle)
noborderRect = pygame.Rect(buttonx+300, buttony, buttonw, buttonh)
# Inner rect (slightly inset so border is visible)
noinnerRect = noborderRect.inflate(-10, -10)  # shrink by 10px in width & height
# Draw red border
pygame.draw.rect(screen, (255, 0, 0), noborderRect, border_radius=30)
# Draw white fill inside the border
pygame.draw.rect(screen, (255, 255, 255), noinnerRect, border_radius=25)
# Draw text centered in the inner rect
notextRect = noButtonText.get_rect(center=noinnerRect.center)
screen.blit(noButtonText, notextRect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # find mouse position
        mousePos = pygame.mouse.get_pos()
        mousex = mousePos[0]
        mousey = mousePos[1]

        if addingScore and event.type == pygame.KEYUP and event.unicode.isalpha():
            if initial1 == '':
                initial1 = {event.unicode}
                init1 = initial1.pop().upper()
            elif initial2 == '':
                initial2 = {event.unicode}
                init2 = initial2.pop().upper()
            else:
                initial3 = {event.unicode}
                addingScore = False 
                scoreToAdd = random.randint(thirdhighest+1,highestscore+4)
                init3 = initial3.pop().upper()
                addScore(init1 + init2 + init3, scoreToAdd)
                initial1 = initial2 = initial3 = ''
                highestscore = int(scoreVals[0])
                thirdhighest = int(scoreVals[2])
                highscore1Text = infofont.render(scores[0], True, red, pink)
                highscore1Rect = highscore1Text.get_rect() 
                highscore1Rect.center = (350, 170) 
                pygame.draw.rect(screen,pink,highscore1Rect)
                highscore2Text = infofont.render(scores[1], True, red, pink)
                highscore2Rect = highscore2Text.get_rect() 
                highscore2Rect.center = (350, 190) 
                pygame.draw.rect(screen,pink,highscore2Rect)
                highscore3Text = infofont.render(scores[2], True, red, pink)
                highscore3Rect = highscore3Text.get_rect() 
                highscore3Rect.center = (350, 210) 
                pygame.draw.rect(screen,pink,highscore3Rect)
                doneAdding = True
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mousex >= buttonx and mousex <= buttonx + buttonw and \
               mousey >= buttony and mousey <= buttony + buttonh:
                # Create the layout
                addingScore = True
                highestscore = int(scoreVals[0])
                thirdhighest = int(scoreVals[2])
                highscore1Text = infofont.render(scores[0], True, red, pink)
                highscore1Rect = highscore1Text.get_rect() 
                highscore1Rect.center = (350, 170) 
                pygame.draw.rect(screen,pink,highscore1Rect)
                highscore2Text = infofont.render(scores[1], True, red, pink)
                highscore2Rect = highscore2Text.get_rect() 
                highscore2Rect.center = (350, 190) 
                pygame.draw.rect(screen,pink,highscore2Rect)
                highscore3Text = infofont.render(scores[2], True, red, pink)
                highscore3Rect = highscore3Text.get_rect() 
                highscore3Rect.center = (350, 210) 
                pygame.draw.rect(screen,pink,highscore3Rect)

    # paint the background
    screen.fill(pink)

    # draw the header
    if not doneAdding:
        pygame.draw.rect(screen, pink, headerRect)
        screen.blit(headerText, headerRect)

    # draw the scores
    pygame.draw.rect(screen,pink,subheaderRect) 
    screen.blit(subheaderText, subheaderRect )
    pygame.draw.rect(screen, pink, highscore1Rect)
    screen.blit(highscore1Text, highscore1Rect)
    pygame.draw.rect(screen, pink, highscore2Rect)
    screen.blit(highscore2Text, highscore2Rect)
    pygame.draw.rect(screen, pink, highscore3Rect)
    screen.blit(highscore3Text, highscore3Rect)

    # draw the input boxes
    if addingScore:
        #pygame.draw.rect(screen,pink,initial1Rect)
        #screen.blit(initial1Text,initial1Rect)

        initial1Text = infofont.render(init1, True, black, white)
        initial1Rect = initial1Text.get_rect()
        initial1Rect.center = (330, 280) 
        pygame.draw.rect(screen,pink,initial1Rect)
        screen.blit(initial1Text,initial1Rect)

        initial2Text = infofont.render(init2, True, black, white)
        initial2Rect = initial2Text.get_rect()
        initial2Rect.center = (345, 280) 
        pygame.draw.rect(screen,pink,initial2Rect)
        screen.blit(initial2Text,initial2Rect)

        initial3Text = infofont.render(init3, True, black, white)
        initial3Rect = initial3Text.get_rect()
        initial3Rect.center = (360, 280) 
        pygame.draw.rect(screen,pink,initial3Rect)
        screen.blit(initial3Text,initial3Rect)

        pygame.draw.rect(screen,pink,instructionRect)
        screen.blit(instructionText,instructionRect)

    # ✅ draw the button every frame
    if not doneAdding:
        yesborderRect = pygame.Rect(buttonx, buttony, buttonw, buttonh)
        yesinnerRect = yesborderRect.inflate(-10, -10)
        noborderRect = pygame.Rect(buttonx+300, buttony, buttonw, buttonh)
        noinnerRect = noborderRect.inflate(-10, -10)

        # if hovering on a button, change its color
        if mousex >= buttonx and mousex <= buttonx + buttonw and \
                mousey >= buttony and mousey <= buttony + buttonh:
            yesButtonText = buttonfont.render("Yes!", True, red, white)
        else:
            yesButtonText = buttonfont.render("Yes ", True, black, white)
        if mousex >= buttonx+300 and mousex <= buttonx+300 + buttonw and \
                mousey >= buttony and mousey <= buttony + buttonh:
            noButtonText = buttonfont.render("No thanks!", True, red, white)
        else:
            noButtonText = buttonfont.render("No thanks", True, black, white)

        pygame.draw.rect(screen, (255, 0, 0), yesborderRect, border_radius=30)       # red border
        pygame.draw.rect(screen, (255, 255, 255), yesinnerRect, border_radius=25) 
        pygame.draw.rect(screen, (255, 0, 0), noborderRect, border_radius=30)       # red border
        pygame.draw.rect(screen, (255, 255, 255), noinnerRect, border_radius=25)     # white fill

        yestextRect = yesButtonText.get_rect(center=yesinnerRect.center)
        screen.blit(yesButtonText, yestextRect)

        notextRect = noButtonText.get_rect(center=noinnerRect.center)
        screen.blit(noButtonText, notextRect)

    # update the display
    pygame.display.update()