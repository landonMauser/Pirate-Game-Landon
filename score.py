from peewee import *
import pygame, sys, os, random
from pygame import *
from pygame.font import Font
from pygame.locals import *
from tkinter import messagebox

def scorePage(killed=None, screen=None):
    """Display top scores and optionally add the player's new score.
       Pass the player's score as `killed`.
    """

    # ---------- Database ----------
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
        ScoreName = CharField()
        ScoreVal = IntegerField()

    try:
        db.connect()
    except Exception:
        messagebox.showwarning("Error", "No database connection")
        return

    scores = ["", "", ""]
    scoreVals = [0, 0, 0]

    cursor = db.execute_sql(
        "SELECT scorename, scoreval FROM scores "
        "ORDER BY scoreval DESC LIMIT 3"
    )
    for i, row in enumerate(cursor.fetchall()):
        scores[i] = f"{row[0]} {row[1]}"
        scoreVals[i] = int(row[1])

    db.close()

    # ---------- Pygame Setup ----------
    pygame.init()                 # <-- parentheses were missing
    pygame.font.init()
    if screen is None:
        gameWidth, gameHeight = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        )
        screen = pygame.display.set_mode((gameWidth, gameHeight))
    else:
        gameWidth, gameHeight = screen.get_size()

    pink = (255, 157, 195)
    black, red, white = (0, 0, 0), (255, 0, 0), (255, 255, 255)

    headerfont = Font('freesansbold.ttf', 24)
    headerfont.set_bold(True)
    smallfont = Font('freesansbold.ttf', 18)
    infofont = Font('freesansbold.ttf', 16)
    buttonfont = pygame.font.SysFont('Corbel', 32, bold=True)

    # ---------- Buttons ----------
    buttonx, buttony, buttonw, buttonh = 100, 75, 200, 50
    yesRect = pygame.Rect(buttonx, buttony, buttonw, buttonh)
    noRect = pygame.Rect(buttonx + 300, buttony, buttonw, buttonh)

    # ---------- State ----------
    addingScore = False
    doneAdding = False
    initials = ["_", "_", "_"]
    initial_index = 0
    highestscore = scoreVals[0] if scoreVals[0] else 0
    thirdhighest = scoreVals[2] if scoreVals[2] else 0

    clock = pygame.time.Clock()

    # ---------- Helpers ----------
    def addScore(name, score):
        try:
            db.connect()
            db.execute_sql(
                "INSERT INTO scores(scorename, scoreval) VALUES (%s, %s)",
                (name, score),
            )
        finally:
            db.close()

    # ---------- Main Loop ----------
    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yesRect.collidepoint(event.pos) and not doneAdding:
                    addingScore = True
                elif noRect.collidepoint(event.pos):
                    running = False

            elif addingScore and event.type == pygame.KEYUP and event.unicode.isalpha():
                if initial_index < 3:
                    initials[initial_index] = event.unicode.upper()
                    initial_index += 1
                if initial_index == 3:
                    # Use the passed-in killed score (fallback to at least 1 above third place)
                    newScore = killed if killed is not None else random.randint(thirdhighest + 1,
                                                                                highestscore + 4)
                    addScore("".join(initials), newScore)
                    doneAdding = True

        # ---------- Drawing ----------
        screen.fill(pink)

        # Header
        headerText = headerfont.render(
            "Your score is in the top 3! Add to high scores?",
            True,
            black,
            pink,
        )
        screen.blit(headerText, headerText.get_rect(center=(350, 50)))

        subheader = smallfont.render("Current Top 3", True, black, pink)
        screen.blit(subheader, subheader.get_rect(center=(350, 150)))

        for i, s in enumerate(scores):
            txt = infofont.render(s, True, red, pink)
            screen.blit(txt, txt.get_rect(center=(350, 170 + i * 20)))

        if addingScore:
            instr = smallfont.render("Enter your 3 initials", True, black, pink)
            screen.blit(instr, instr.get_rect(center=(350, 250)))
            for i, ch in enumerate(initials):
                t = infofont.render(ch, True, black, white)
                screen.blit(t, t.get_rect(center=(330 + i * 15, 280)))
                draw_button(noRect, "Back", red if noRect.collidepoint(m) else black)


        if not doneAdding:
            # draw buttons
            def draw_button(rect, text, hover):
                border = 30
                inner = rect.inflate(-10, -10)
                pygame.draw.rect(screen, red, rect, border_radius=border)
                pygame.draw.rect(screen, white, inner, border_radius=border - 5)
                t = buttonfont.render(text, True, hover, white)
                screen.blit(t, t.get_rect(center=inner.center))

            m = pygame.mouse.get_pos()
            draw_button(yesRect, "Yes", red if yesRect.collidepoint(m) else black)
            draw_button(noRect, "No thanks", red if noRect.collidepoint(m) else black)


        pygame.display.flip()

    return
