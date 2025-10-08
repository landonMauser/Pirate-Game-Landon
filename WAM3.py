import os
import sys
import random
import pygame
import tkinter as tk
from pygame.locals import QUIT, MOUSEBUTTONDOWN, USEREVENT
from score import scorePage  # Assuming this is a function you use

# --- Constants ---
MENU = "menu"
GAME = "game"
SHOP = "shop"
SETTINGS = "settings"
LEVELSELECT = "level select"
BOSSLEVEL = "boss level"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD_COLOR = (255, 215, 0)

# --- Helper Functions ---

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller EXE."""
    if getattr(sys, '_MEIPASS', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def load_image(path, size=None, convert_alpha=True):
    img = pygame.image.load(resource_path(path))
    if convert_alpha:
        img = img.convert_alpha()
    else:
        img = img.convert()
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_sound(path):
    return pygame.mixer.Sound(resource_path(path))

# --- Tkinter Popup Management ---

class PopupManager:
    def __init__(self, root):
        self.root = root
        self.popup = None

    def show(self, text, x, y, font=("Arial", 10)):
        if self.popup is not None:
            return
        self.popup = tk.Toplevel()
        self.popup.wm_overrideredirect(True)
        self.popup.attributes('-topmost', True)
        self.popup.configure(bg="#222222")
        label = tk.Label(self.popup, text=text, fg="white", bg="#222222", font=font)
        label.pack(ipadx=10, ipady=5)
        self.popup.geometry(f"+{x}+{y}")

    def hide(self):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None

    def update_position(self, x, y):
        if self.popup is not None:
            self.popup.geometry(f"+{x}+{y}")
            self.popup.update_idletasks()

# --- Game State ---

class GameState:
    def __init__(self):
        self.gold = 0
        self.audio_on = True
        self.missed = 0
        self.killed = 0
        self.seconds_remaining = 120
        self.current_page = MENU
        self.current_level = None

# --- Main Game Setup ---

pygame.init()
gameWidth, gameHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("There be treasure!!!")
clock = pygame.time.Clock()

# Tkinter root for popups
root = tk.Tk()
root.withdraw()
popup_mgr = PopupManager(root)

# --- Load Resources ---

backgrounds = {
    "game": load_image("resources/background10.png", (gameWidth, gameHeight), False),
    "menu": load_image("resources/boatCamp2.png", (gameWidth, gameHeight), False),
    "shop": load_image("resources/boatCamp1.png", (gameWidth, gameHeight), False),
    "boss": load_image("resources/background9.png", (gameWidth, gameHeight), False),
}

sounds = {
    "boom1": load_sound("resources/sound/boom1.mp3"),
    "boom2": load_sound("resources/sound/boom2.mp3"),
    "boom3": load_sound("resources/sound/boom3.mp3"),
}

sprites = {
    "ship1": load_image("resources/ships/piratePixelShip1.png", (120, 120)),
    "ship2": load_image("resources/ships/piratePixelShip2.png", (120, 120)),
    "ship3": load_image("resources/ships/piratePixelShip3.png", (120, 120)),
    "fly1": load_image("resources/ships/dutch.png", (200, 200)),
    "fly2": load_image("resources/ships/ghostShip1.png", (200, 200)),
    "fly3": load_image("resources/ships/ghostShip2.png", (120, 180)),
    "kraken1": load_image("resources/ships/kraken1.png", (200, 200)),
    "kraken2": load_image("resources/ships/kraken2.png", (200, 200)),
    "gold": load_image("resources/buttons/goldCoin.png", (75, 75)),
    "scoreboard": load_image("resources/scorePlate.png", (200, 200)),
    "start": load_image("resources/buttons/arcade.png", (300, 150)),
    "quit": load_image("resources/quitButton2.png", (300, 150)),
    "shop": load_image("resources/buttons/shop.png", (300, 150)),
    "story": load_image("resources/storyMode.png", (330, 165)),
    "settings": load_image("resources/settingsButton.png", (200, 150)),
    "audio_on": load_image("resources/audioOnButton.png", (200, 150)),
    "audio_off": load_image("resources/audioOffButton.png", (200, 150)),
    "back": load_image("resources/backButton1.png", (200, 150)),
}

# --- Fonts ---
headerfont = pygame.font.Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Arial', 40, bold=True)

# --- Rects ---
scoreBoardRect = sprites["scoreboard"].get_rect(topleft=(gameWidth-400, 40))
playButtonRect = sprites["start"].get_rect(topleft=(gameWidth / 2 - 120, 500))
quitButtonRect = sprites["quit"].get_rect(topleft=(gameWidth / 2 - 110, 900))
shopButtonRect = sprites["shop"].get_rect(topleft=(gameWidth / 2 - 120, 700))
storyButtonRect = sprites["story"].get_rect(topleft=(gameWidth / 2 - 130, 300))
settingsButtonRect = sprites["settings"].get_rect(topleft=(80, 40))
audioOnButtonRect = sprites["audio_on"].get_rect(topleft=(300, 40))
audioOffButtonRect = sprites["audio_off"].get_rect(topleft=(300, 40))
backButtonRect = sprites["back"].get_rect(topleft=(gameWidth / 2 - 100, 750))

scorex = gameWidth - 300
scorey = gameHeight / 6.4

# --- Sprite Groups ---
boats = pygame.sprite.Group()

# --- Events ---
SPAWN_EVENT = USEREVENT + 1
SPAWN_EVENT2 = USEREVENT + 2
SPAWN_EVENT3 = USEREVENT + 3
TIMER_EVENT = USEREVENT + 10

pygame.time.set_timer(SPAWN_EVENT, 2300)
pygame.time.set_timer(SPAWN_EVENT2, 3000)
pygame.time.set_timer(SPAWN_EVENT3, 4000)
pygame.time.set_timer(TIMER_EVENT, 1000)

# --- PirateShip Sprite ---

class PirateShip(pygame.sprite.Sprite):
    def __init__(self, y, direction="right", kind="normal"):
        super().__init__()
        if kind == "normal":
            self.image = random.choice([sprites["ship1"], sprites["ship3"]])
            self.speed = random.randint(100, 200)
        elif kind == "special":
            self.image = sprites["ship2"]
            self.speed = random.randint(100, 200)
        elif kind == "fly":
            chance = random.random()
            if chance < 0.01:
                self.image = sprites["fly1"]
            elif chance < 0.31:
                self.image = sprites["fly3"]
            else:
                self.image = sprites["fly2"]
            self.speed = 400
        elif kind == "kraken1":
            self.image = sprites["kraken1"]
            self.speed = random.randint(50, 100)
        elif kind == "kraken2":
            self.image = sprites["kraken2"]
            self.speed = random.randint(70, 170)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.pos_x = float(0 if direction == "right" else gameWidth)
        self.rect.y = y

    def update(self, dt):
        if self.direction == "right":
            self.pos_x += self.speed * dt
        else:
            self.pos_x -= self.speed * dt
        self.rect.x = int(self.pos_x)
        if self.rect.right < 0 or self.rect.left > gameWidth:
            state.missed += 1
            self.kill()

# --- Drawing Functions ---

def draw_menu():
    screen.blit(backgrounds["menu"], (0, 0))
    gold_text = buttonfont.render(f"{state.gold}", True, GOLD_COLOR)
    gold_rect = gold_text.get_rect(topright=(gameWidth/2 + 400, 710))
    screen.blit(gold_text, gold_rect)
    screen.blit(sprites["gold"], (gameWidth/2 + 260, 700))
    # ... (rest of the button drawing and popup logic, as in your original code)
    # Use popup_mgr for popups

def draw_game(dt):
    screen.blit(backgrounds["game"], (0, 0))
    headerText = headerfont.render("Whack 'A pirateShip!", True, BLACK)
    headerRect = headerText.get_rect(center=(gameWidth / 2, 100))
    screen.blit(headerText, headerRect)
    screen.blit(sprites["back"], backButtonRect)
    screen.blit(sprites["scoreboard"], scoreBoardRect)
    boats.update(dt)
    boats.draw(screen)
    score_text = buttonfont.render(f"{state.killed}", True, BLACK)
    score_rect = score_text.get_rect(center=(scorex, scorey))
    screen.blit(score_text, score_rect)
    minutes = str(state.seconds_remaining // 60).zfill(2)
    seconds = str(state.seconds_remaining % 60).zfill(2)
    timer_text = buttonfont.render(f"Time: {minutes}:{seconds}", True, BLACK)
    timer_rect = timer_text.get_rect(center=(scorex, scorey + 80))
    screen.blit(timer_text, timer_rect)

# ... (similarly refactor draw_shop, draw_boss_level, draw_settings, etc.)

# --- Main Loop ---

state = GameState()

while True:
    dt = min(clock.tick(60) / 1000, 0.05)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # ... (handle events, update state, spawn ships, etc.)

    # Draw current page
    if state.current_page == MENU:
        draw_menu()
    elif state.current_page == GAME:
        draw_game(dt)
    # ... (other pages)

    pygame.display.update()