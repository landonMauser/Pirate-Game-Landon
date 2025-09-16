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
        basePath = r"C:\Genral school work\userInterface\pirateGame\resources"
    return os.path.join(basePath, myPath)

# Init
pygame.init()
#gameWidth, gameHeight = [pygame.display.Info().current_w, pygame.display.Info().current_h]
gameWidth, gameHeight = 1536,1024
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("There be treasure!!!")
clock = pygame.time.Clock()

# Backgrounds
backgroundGame = pygame.image.load(resource_path("background10.png")).convert()
backgroundGame = pygame.transform.scale(backgroundGame, (gameWidth, gameHeight))

backgroundMenu = pygame.image.load(resource_path("boatCamp2.png")).convert()
backgroundMenu = pygame.transform.scale(backgroundMenu, (gameWidth, gameHeight))

backgroundShop = pygame.image.load(resource_path("boatCamp1.png")).convert()
backgroundShop = pygame.transform.scale(backgroundShop, (gameWidth, gameHeight))

# Sprite
shipSprite = pygame.image.load(resource_path("piratePixelShip1.png")).convert_alpha()
shipSprite = pygame.transform.scale(shipSprite, (90, 90))

shipSprite3 = pygame.image.load(resource_path("piratePixelShip3.png")).convert_alpha()
shipSprite3 = pygame.transform.scale(shipSprite3, (90, 90))

# Colors
pink = (255, 157, 195)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Arial', 32, bold=True)

headerText = headerfont.render("Whack 'A pirateShip!", True, black, pink)
headerRect = headerText.get_rect(center=(gameWidth / 2, 100))

startButton = pygame.image.load(resource_path("startButton1.png")).convert_alpha()
startButton = pygame.transform.scale(startButton, (400, 200)) 
playButtonRect = startButton.get_rect(topleft=(gameWidth / 2 - 200, 300))

quitButtonNormal = buttonfont.render(" Quit ", True, black, pink)
quitButtonHover = buttonfont.render(" Quit ", True, red, pink)
quitButtonRect = quitButtonNormal.get_rect(topleft=(gameWidth / 2 - 60, 750))


shopButtonNormal = buttonfont.render(" Shop ", True, black, pink)
shopButtonHover = buttonfont.render(" Shop ", True, red, pink)
shopButtonRect = shopButtonNormal.get_rect(topleft=(gameWidth / 2 - 60, 480))

backButtonNormal = buttonfont.render(" Back ", True, black, pink)
backButtonHover = buttonfont.render(" Back ", True, red, pink)
backButtonRect = backButtonNormal.get_rect(topleft=(gameWidth / 2 - 60, 750))


# Pages
MENU = "menu"
GAME = "game"
SHOP = "shop"

current_page = MENU

class PirateShip(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = random.choice([shipSprite, shipSprite3])
        self.rect = self.image.get_rect(topleft=(0, y))
        self.speed = random.randint(100, 200)
        self.x = float(self.rect.x)  

    def update(self, dt):
        self.x += self.speed * dt
        self.rect.x = int(self.x)
        if self.rect.left > gameWidth:
            self.kill()



boats = pygame.sprite.Group()

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1800)  

def draw_menu():
    screen.blit(backgroundMenu, (0, 0))
    title = headerfont.render("Main Menu", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 200))
    screen.blit(title, titleRect)


    mouse_pos = pygame.mouse.get_pos()
    if playButtonRect.collidepoint(mouse_pos):
        # Grow 10% larger on hover
        hover_img = pygame.transform.scale(startButton, (int(420),int(210)))

        # Re-center so it grows outward evenly
        hover_rect = hover_img.get_rect(center=playButtonRect.center)
        screen.blit(hover_img, hover_rect)
    else:
        # Normal size
        screen.blit(startButton, playButtonRect)


    shopBtnText = shopButtonHover if shopButtonRect.collidepoint(pygame.mouse.get_pos()) else shopButtonNormal
    pygame.draw.rect(screen, white, shopButtonRect)
    screen.blit(shopBtnText, shopButtonRect)
    
    quitBtnText = quitButtonHover if quitButtonRect.collidepoint(pygame.mouse.get_pos()) else quitButtonNormal
    pygame.draw.rect(screen, white, quitButtonRect)
    screen.blit(quitBtnText, quitButtonRect)


def draw_game(dt):
    screen.blit(backgroundGame, (0, 0))
    screen.blit(headerText, headerRect)

    boats.update(dt)
    boats.draw(screen)

    quitBtnText = quitButtonHover if quitButtonRect.collidepoint(pygame.mouse.get_pos()) else quitButtonNormal
    pygame.draw.rect(screen, white, quitButtonRect)
    screen.blit(quitBtnText, quitButtonRect)


def draw_shop():
    screen.blit(backgroundMenu, (0, 0))
    title = headerfont.render("Shop", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 150))
    screen.blit(title, titleRect)

    shopText = buttonfont.render("Buy! BUY! BUY! AND! SPEND MONEY!!!!!!!", True, white)
    screen.blit(shopText, (gameWidth / 2 - 200, 300))

    backBtnText = backButtonHover if backButtonRect.collidepoint(pygame.mouse.get_pos()) else backButtonNormal
    pygame.draw.rect(screen, white, backButtonRect)
    screen.blit(backBtnText, backButtonRect)


# --- Main Loop ---
while True:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_page == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButtonRect.collidepoint(pygame.mouse.get_pos()):
                    current_page = GAME
                elif shopButtonRect.collidepoint(pygame.mouse.get_pos()):
                  current_page = SHOP



        elif current_page == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitButtonRect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit(); sys.exit()
            elif event.type == SPAWN_EVENT:
                y = random.randint(50, gameHeight - 100)
                boat = PirateShip(y)
                boats.add(boat)

        elif current_page == SHOP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButtonRect.collidepoint(pygame.mouse.get_pos()):
                    current_page = MENU

    if current_page == MENU:
        draw_menu()
    elif current_page == GAME:
        draw_game(dt)
    elif current_page == SHOP:
        draw_shop()

    pygame.display.update()

