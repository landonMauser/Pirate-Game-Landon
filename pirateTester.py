from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os, random
from pygame.locals import *

# Resource path helper (for EXE builds later)
def resource_path(myPath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = r"C:\Genral school work\userInterface\pirateGame"
    return os.path.join(basePath, myPath)

# Init
pygame.init()
gameWidth, gameHeight = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("There be treasure!!!")
clock = pygame.time.Clock()

# Backgrounds
backgroundGame = pygame.image.load(resource_path("background10.png")).convert()
backgroundGame = pygame.transform.scale(backgroundGame, (gameWidth, gameHeight))

backgroundMenu = pygame.image.load(resource_path("boatCamp2.png")).convert()
backgroundMenu = pygame.transform.scale(backgroundMenu, (gameWidth, gameHeight))

# Sprite
shipSprite = pygame.image.load(resource_path("piratePixelShip1.png")).convert_alpha()
shipSprite = pygame.transform.scale(shipSprite, (90, 90))

# Colors
pink = (255, 157, 195)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Fonts
headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Arial', 32, bold=True)

# Text & Buttons
headerText = headerfont.render("Whack 'A pirateShip!", True, black, pink)
headerRect = headerText.get_rect(center=(gameWidth / 2, 100))

# --- MENU BUTTONS ---
playButtonNormal = buttonfont.render(" Play ", True, black, pink)
playButtonHover = buttonfont.render(" Play ", True, red, pink)
playButtonRect = playButtonNormal.get_rect(topleft=(gameWidth / 2 - 60, 400))

# --- GAME QUIT BUTTON ---
quitButtonNormal = buttonfont.render(" Quit ", True, black, pink)
quitButtonHover = buttonfont.render(" Quit ", True, red, pink)
quitButtonRect = quitButtonNormal.get_rect(topleft=(gameWidth / 2 - 60, 750))

# Pages
MENU = "menu"
GAME = "game"
current_page = MENU

# --- PirateShip class ---
class PirateShip(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Create grid slots for ship to appear ---
boat_slots = [(columns * 150, 200 + rows * 150) for rows in range(4) for columns in range(8)]

# Create ONE ship and a group for drawing
active_ship = PirateShip(0, 0, shipSprite)
ship_group = pygame.sprite.Group(active_ship)

# Timer for ship repositioning
ship_timer = 0
ship_interval = 1.5  # seconds

# --- Draw Functions ---

def draw_menu():
    screen.blit(backgroundMenu, (0, 0))
    title = headerfont.render("Main Menu", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 200))
    screen.blit(title, titleRect)

    playBtnText = playButtonHover if playButtonRect.collidepoint(pygame.mouse.get_pos()) else playButtonNormal
    pygame.draw.rect(screen, white, playButtonRect)
    screen.blit(playBtnText, playButtonRect)

def draw_game(dt):
    global ship_timer

    ship_timer += dt
    if ship_timer >= ship_interval:
        ship_timer = 0
        new_x, new_y = random.choice(boat_slots)
        active_ship.rect.topleft = (new_x, new_y)

    screen.blit(backgroundGame, (0, 0))
    ship_group.draw(screen)
    screen.blit(headerText, headerRect)

    quitBtnText = quitButtonHover if quitButtonRect.collidepoint(pygame.mouse.get_pos()) else quitButtonNormal
    pygame.draw.rect(screen, white, quitButtonRect)
    screen.blit(quitBtnText, quitButtonRect)

# --- Main Loop ---
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if current_page == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButtonRect.collidepoint(pygame.mouse.get_pos()):
                    current_page = GAME

        elif current_page == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitButtonRect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit(); sys.exit()

    # Page Rendering
    if current_page == MENU:
        draw_menu()
    elif current_page == GAME:
        draw_game(dt)

    pygame.display.update()
