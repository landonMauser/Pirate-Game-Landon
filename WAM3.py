from peewee import *
import pygame, sys, os, random
from pygame.font import Font
from pygame.locals import *
from tkinter import messagebox

def scorePage(player_score=None, player_name=None, screen=None):
    """
    Show the high-score screen.
    - player_score: int or None. If given, it’s used to decide if we prompt for adding a new high score.
    - player_name: str or None. If given together with player_score, it will insert the score immediately.
    - screen: optional Pygame surface. If None, a full-screen window is created.
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

    # Fetch current top 3
    scores = ["", "", ""]
    scoreVals = [0, 0, 0]
    cursor = db.execute_sql(
        "SELECT scorename, scoreval FROM scores ORDER BY scoreval DESC LIMIT 3"
    )
    for i, row in enumerate(cursor.fetchall()):
        scores[i] = f"{row[0]} {row[1]}"
        scoreVals[i] = int(row[1])
    db.close()

    # ---------- Pygame Setup ----------
    pygame.init()  # <-- add this line
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
    highestscore = scoreVals[0] if scoreVals[0] else 0
    thirdhighest = scoreVals[2] if scoreVals[2] else 0

    addingScore = False
    doneAdding = False
    initials = ["_", "_", "_"]
    initial_index = 0
    clock = pygame.time.Clock()

    # Decide if we should prompt to add score automatically
    if player_score is not None and player_score > thirdhighest:
        addingScore = True

    # If both score and name given: insert and skip interactive adding
    if player_score is not None and player_name:
        try:
            db.connect()
            db.execute_sql(
                "INSERT INTO scores(scorename, scoreval) VALUES (%s, %s)",
                (player_name, player_score),
            )
        finally:
            db.close()
        doneAdding = True  # we still show the screen but skip input

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

            elif event.type == pygame.MOUSEBUTTONDOWN and not doneAdding:
                if yesRect.collidepoint(event.pos):
                    addingScore = True
                elif noRect.collidepoint(event.pos):
                    running = False

            elif addingScore and not doneAdding and event.type == pygame.KEYUP:
                if event.unicode.isalpha() and initial_index < 3:
                    initials[initial_index] = event.unicode.upper()
                    initial_index += 1
                if initial_index == 3 and player_score is not None:
                    addScore("".join(initials), player_score)
                    doneAdding = True

        # ---------- Drawing ----------
        screen.fill(pink)

        headerText = headerfont.render(
            "High Scores", True, black, pink
        )
        screen.blit(headerText, headerText.get_rect(center=(350, 40)))

        subheader = smallfont.render("Current Top 3", True, black, pink)
        screen.blit(subheader, subheader.get_rect(center=(350, 100)))

        for i, s in enumerate(scores):
            txt = infofont.render(s, True, red, pink)
            screen.blit(txt, txt.get_rect(center=(350, 130 + i * 20)))

        # Show prompt only if we have a score to add and we haven’t finished
        if player_score is not None and not doneAdding:
            prompt = "Your score is in the top 3! Add it?"
            promptText = smallfont.render(prompt, True, black, pink)
        
scorePage()