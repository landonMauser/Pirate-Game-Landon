from peewee import *
import pygame, sys, os, random
from pygame import *
from pygame.font import Font
from pygame.locals import *
from tkinter import messagebox, Tk, Label, Entry, Button


def get_player_name():
    name_result = {"value": None}

    def submit():
        val = entry.get().strip()
        if val:
            name_result["value"] = val
            root.quit()
        else:
            error_label.config(text="Name cannot be empty!")

    def force_focus(event=None):
        entry.focus_force()  # put typing focus back in the Entry
        root.grab_set()       # keep modal behavior

    root = Tk()
    root.title("Enter Your Name")
    root.geometry("300x150")

    # Make unmovable, unresizable, no close button
    root.overrideredirect(True)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Center the popup
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 300) // 2
    y = (screen_height - 150) // 2
    root.geometry(f"+{x}+{y}")

    Label(root, text="Enter your name:", font=("Arial", 12)).pack(pady=10)
    entry = Entry(root, font=("Arial", 12))
    entry.pack()
    entry.focus()

    Button(root, text="Submit", command=submit).pack(pady=10)
    error_label = Label(root, text="", font=("Arial", 10), fg="red")
    error_label.pack()

    # Make modal and refocus entry if focus is lost
    root.grab_set()
    root.bind("<FocusOut>", force_focus)

    root.mainloop()
    root.destroy()

    return name_result["value"]




def scorePage(killed=None, screen=None):
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
    pygame.init()
    pygame.font.init()

    if screen is None:
        gameWidth, gameHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
        screen = pygame.display.set_mode((gameWidth, gameHeight))
    else:
        gameWidth, gameHeight = screen.get_size()

    scoreScroll2 = pygame.image.load("scoreScroll2.png").convert()
    scoreScroll2 = pygame.transform.scale(scoreScroll2, (gameWidth, gameHeight))

    black, white = (0, 0, 0), (255, 255, 255)
    headerfont = Font('freesansbold.ttf', 24)
    headerfont.set_bold(True)
    smallfont = Font('freesansbold.ttf', 18)
    infofont = Font('freesansbold.ttf', 16)
    buttonfont = pygame.font.SysFont('Corbel', 32, bold=True)

    buttonx, buttony, buttonw, buttonh = gameWidth / 2 + 200, 400, 200, 50
    yesRect = pygame.Rect(buttonx, buttony, buttonw, buttonh)
    noRect = pygame.Rect(buttonx + 300, buttony, buttonw, buttonh)

    addingScore = False
    doneAdding = False
    highestscore = scoreVals[0] if scoreVals[0] else 0
    thirdhighest = scoreVals[2] if scoreVals[2] else 0

    clock = pygame.time.Clock()

    def addScore(name, score):
        try:
            db.connect(reuse_if_open=True)
            db.execute_sql(
                "INSERT INTO scores(scorename, scoreval) VALUES (%s, %s)",
                (name, score),
            )
        finally:
            db.close()

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yesRect.collidepoint(event.pos) and not doneAdding:
                    addingScore = True
                    playerName = get_player_name()
                    if playerName:
                        newScore = killed if killed is not None else random.randint(
                            thirdhighest + 1, highestscore + 4
                        )
                        addScore(playerName, newScore)
                        doneAdding = True
                elif noRect.collidepoint(event.pos):
                    running = False

        # ---------- Draw screen ----------
        screen.blit(scoreScroll2, (0, 0))

        headerText = headerfont.render(
            "Would you like to add your score?", True, black
        )
        screen.blit(headerText, headerText.get_rect(center=(gameWidth / 2, 400)))

        subheader = smallfont.render("Current Top 3", True, black)
        screen.blit(subheader, subheader.get_rect(center=(gameWidth / 2, 450)))

        for i, s in enumerate(scores):
            txt = infofont.render(s, True, black)
            screen.blit(txt, txt.get_rect(center=(gameWidth / 2, 500 + i * 30)))

        def draw_button(rect, text, hover):
            border = 30
            inner = rect.inflate(-10, -10)
            pygame.draw.rect(screen, black, rect, border_radius=border)
            pygame.draw.rect(screen, white, inner, border_radius=border - 5)
            t = buttonfont.render(text, True, hover)
            screen.blit(t, t.get_rect(center=inner.center))

        m = pygame.mouse.get_pos()
        if not doneAdding:
            draw_button(yesRect, "Yes", black if yesRect.collidepoint(m) else black)
            draw_button(noRect, "No thanks", black if noRect.collidepoint(m) else black)
        else:
            draw_button(noRect, "Back", black if noRect.collidepoint(m) else black)

        pygame.display.flip()
