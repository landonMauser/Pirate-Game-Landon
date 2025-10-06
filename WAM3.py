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
        entry.focus_force()
        root.grab_set()

    root = Tk()
    root.title("Enter Your Name")
    root.geometry("300x150")
    root.overrideredirect(True)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", lambda: None)

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
        return "error"

    scores = [""] * 5
    scoreVals = [0] * 5

    cursor = db.execute_sql(
        "SELECT scorename, scoreval FROM scores ORDER BY scoreval DESC LIMIT 5"
    )

    for i, row in enumerate(cursor.fetchall()):
        scores[i] = f"{row[0]} - {row[1]}"
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

    # ---------- Colors and Fonts ----------
    parchment_brown = (67, 45, 18)
    dark_brown = (35, 22, 10)
    gold = (205, 160, 58)
    white = (255, 255, 255)
    shadow = (0, 0, 0)
    black = (0, 0, 0)

    headerfont = Font('freesansbold.ttf', 48)
    smallfont = Font('freesansbold.ttf', 32)
    infofont = Font('freesansbold.ttf', 26)
    buttonfont = pygame.font.SysFont('Corbel', 36, bold=True)

    # ---------- Layout ----------
    yesRect = pygame.Rect(gameWidth/2 - 250, gameHeight - 200, 200, 60)
    noRect = pygame.Rect(gameWidth/2 + 50, gameHeight - 200, 200, 60)

    addingScore = False
    doneAdding = False
    highestscore = scoreVals[0] if scoreVals[0] else 0
    fifthhighest = scoreVals[4] if scoreVals[4] else 0

    newScore = killed if killed is not None else random.randint(fifthhighest + 1, highestscore + 4)

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

    def draw_shadowed_text(text, font, color, shadow_color, pos, center=True):
        txt_surface = font.render(text, True, color)
        shadow_surface = font.render(text, True, shadow_color)
        rect = txt_surface.get_rect(center=pos) if center else txt_surface.get_rect(topleft=pos)
        shadow_rect = rect.copy()
        shadow_rect.move_ip(3, 3)
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(txt_surface, rect)

    def draw_button(rect, text, hover):
        border_radius = 25
        base_color = gold if hover else parchment_brown
        pygame.draw.rect(screen, dark_brown, rect.inflate(6, 6), border_radius=border_radius)
        pygame.draw.rect(screen, base_color, rect, border_radius=border_radius)
        draw_shadowed_text(text, buttonfont, white, shadow, rect.center)

    # ---------- Main Loop ----------
    running = True
    result = None
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                result = "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yesRect.collidepoint(event.pos) and not doneAdding:
                    playerName = get_player_name()
                    if playerName:
                        addScore(playerName, newScore)
                        doneAdding = True
                elif noRect.collidepoint(event.pos):
                    running = False
                    result = "back"

        # ---------- Draw Screen ----------
        screen.blit(scoreScroll2, (0, 0))
        offset = 190

        draw_shadowed_text("Top Pirate Scores", headerfont, gold, shadow, (gameWidth/2-50, 150 + offset))
        subtitle_surface = smallfont.render("Will ye add yer name to history?", True, parchment_brown)
        subtitle_rect = subtitle_surface.get_rect(center=(gameWidth/2-50, 240 + offset))
        screen.blit(subtitle_surface, subtitle_rect)

        for i, s in enumerate(scores):
            y = 350 + i * 60 + offset
            txt_surface = infofont.render(f"{i+1}. {s}", True, dark_brown)
            rect = txt_surface.get_rect(center=(gameWidth/2-50, y))
            screen.blit(txt_surface, rect)

        # ---------- Buttons ----------
        m = pygame.mouse.get_pos()
        if not doneAdding:
            draw_button(yesRect, "Aye!", yesRect.collidepoint(m))
            draw_button(noRect, "Nay...", noRect.collidepoint(m))
        else:
            draw_button(noRect, "Back to Sea", noRect.collidepoint(m))

        pygame.display.flip()

    # ---------- Return instead of exit ----------
    return result
