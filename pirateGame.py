from pygame import *
from peewee import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os, random
from pygame.locals import *
from score import scorePage
import tkinter as tk

root = tk.Tk()
root.withdraw() 
popup = None

def resource_path(my_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, my_path)
# Init
pygame.init()
gameWidth, gameHeight = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("There be treasure!!!")
clock = pygame.time.Clock()

# Backgrounds
backgroundGame = pygame.image.load(resource_path("resources/background10.png")).convert()
backgroundGame = pygame.transform.scale(backgroundGame, (gameWidth, gameHeight))

backgroundMenu = pygame.image.load(resource_path("resources/boatCamp2.png")).convert()
backgroundMenu = pygame.transform.scale(backgroundMenu, (gameWidth, gameHeight))

backgroundShop = pygame.image.load(resource_path("resources/boatCamp1.png")).convert()
backgroundShop = pygame.transform.scale(backgroundShop, (gameWidth, gameHeight))


# audio
boom1 = pygame.mixer.Sound(resource_path("resources/sound/boom1.mp3"))
boom2 = pygame.mixer.Sound(resource_path("resources/sound/boom2.mp3"))
boom3 = pygame.mixer.Sound(resource_path("resources/sound/boom3.mp3"))


# Sprite
shipSprite = pygame.image.load(resource_path("resources/ships/piratePixelShip1.png")).convert_alpha()
shipSprite = pygame.transform.scale(shipSprite, (120, 120))

shipSprite3 = pygame.image.load(resource_path("resources/ships/piratePixelShip3.png")).convert_alpha()
shipSprite3 = pygame.transform.scale(shipSprite3, (120, 120))

shipSprite2 = pygame.image.load(resource_path("resources/ships/piratePixelShip2.png")).convert_alpha()
shipSprite2 = pygame.transform.scale(shipSprite2, (120, 120))

flyShip = pygame.image.load(resource_path("resources/ships/dutch.png")).convert_alpha()
flyShip = pygame.transform.scale(flyShip, (200, 200))

flyShip2 = pygame.image.load(resource_path("resources/ships/ghostShip1.png")).convert_alpha()
flyShip2 = pygame.transform.scale(flyShip2, (200, 200))

scoreBoard = pygame.image.load(resource_path("resources/scorePlate.png")).convert_alpha()
scoreBoard = pygame.transform.scale(scoreBoard, (200, 200))
scoreBoardRect = scoreBoard.get_rect(topleft=(gameWidth-400, 40))

startButton = pygame.image.load(resource_path("resources/startButton1.png")).convert_alpha()
startButton = pygame.transform.scale(startButton, (300, 150)) 
playButtonRect = startButton.get_rect(topleft=(gameWidth / 2 - 120, 500))

quitButton = pygame.image.load(resource_path("resources/quitButton2.png")).convert_alpha()
quitButton = pygame.transform.scale(quitButton, (300, 150))
quitButtonRect = quitButton.get_rect(topleft=(gameWidth / 2 - 110, 900))

shopButton = pygame.image.load(resource_path("resources/shopButton3.png")).convert_alpha()
shopButton = pygame.transform.scale(shopButton, (300, 150))
shopButtonRect = shopButton.get_rect(topleft=(gameWidth / 2 - 110, 700))

storyButton = pygame.image.load(resource_path("resources/storyMode.png")).convert_alpha()
storyButton = pygame.transform.scale(storyButton, (330, 165))
storyButtonRect = storyButton.get_rect(topleft=(gameWidth / 2 - 130, 300))

settingsButton = pygame.image.load(resource_path("resources/settingsButton.png")).convert_alpha()
settingsButton = pygame.transform.scale(settingsButton, (200, 150))
settingsButtonRect = settingsButton.get_rect(topleft=(80, 40))

audioOnButton = pygame.image.load(resource_path("resources/audioOnButton.png")).convert_alpha()
audioOnButton = pygame.transform.scale(audioOnButton, (200, 150))
audioOnButtonRect = audioOnButton.get_rect(topleft=(300, 40))

audioOffButton = pygame.image.load(resource_path("resources/audioOffButton.png")).convert_alpha()
audioOffButton = pygame.transform.scale(audioOffButton, (200, 150))
audioOffButtonRect = audioOffButton.get_rect(topleft=(300, 40))
# Colors
pink = (255, 157, 195)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Arial', 40, bold=True)

headerText = headerfont.render("Whack 'A pirateShip!", True, black, None)
headerRect = headerText.get_rect(center=(gameWidth / 2, 100))

# Back button image
backButtonImg = pygame.image.load(resource_path("resources/backButton1.png")).convert_alpha()
backButtonImg = pygame.transform.scale(backButtonImg, (200, 150)) 
backButtonRect = backButtonImg.get_rect(topleft=(gameWidth / 2 - 100, 750))


scoreText = buttonfont.render("Score:     ", True, black)
scoreRect = scoreText.get_rect()
scorex = gameWidth - 300
scorey = gameHeight / 6.4
scoreRect.center = (scorex,scorey)
pygame.draw.rect(screen,True,scoreRect)

# Pages
MENU = "menu"
GAME = "game"
SHOP = "shop"
SETTINGS = "SETTINGS"


current_page = MENU

class PirateShip(pygame.sprite.Sprite):
    def __init__(self, y, direction="right", kind="normal"):
        super().__init__()

        if kind == "normal":
            self.image = random.choice([shipSprite, shipSprite3])
            self.speed = random.randint(100, 200) 
        elif kind == "special":
            self.image = shipSprite2
            self.speed = random.randint(100, 200) 
        elif kind == "fly":
            self.image = flyShip if random.random() < 0.01 else flyShip2
            self.speed = (400) 

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
            self.kill()

boats = pygame.sprite.Group()

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2300)  

SPAWN_EVENT2 = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_EVENT2, 3000)  

SPAWN_EVENT3 = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWN_EVENT3, 4000)  

TIMER_EVENT = pygame.USEREVENT + 10
pygame.time.set_timer(TIMER_EVENT, 1000)  


def show_popup(text, x, y):
    global popup
    if popup is not None:
        return  
    popup = tk.Toplevel()
    popup.wm_overrideredirect(True)  
    popup.attributes('-topmost', True)
    popup.configure(bg="#222222")
    label = tk.Label(popup, text=text, fg="white", bg="#222222", font=("Arial", 10))
    label.pack(ipadx=10, ipady=5)
    popup.geometry(f"+{x}+{y}") 

def hide_popup():
    global popup
    if popup is not None:
        popup.destroy()
        popup = None
def draw_menu():
    global popup, current_page, audioOn
    screen.blit(backgroundMenu, (0, 0))
    title = headerfont.render("Main Menu", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 200))
    screen.blit(title, titleRect)
    

    mouse_pos = pygame.mouse.get_pos()
    mx, my = mouse_pos
    popup_text = None
    clicked = pygame.mouse.get_pressed()[0]  # Left mouse button

    # --- PLAY BUTTON ---
    if playButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(startButton, (350, 175))
        hover_rect = hover.get_rect(center=playButtonRect.center)
        screen.blit(hover, hover_rect)
        popup_text = "Play the game"
        if clicked:
            hide_popup()
            current_page = "game"
            return  # Exit menu after click
    else:
        screen.blit(startButton, playButtonRect)

    # --- QUIT BUTTON ---
    if quitButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(quitButton, (350, 175))
        hover_rect = hover.get_rect(center=quitButtonRect.center)
        screen.blit(hover, hover_rect)
        popup_text = "Quit the game"
        if clicked:
            hide_popup()
            pygame.quit()
            sys.exit()
    else:
        screen.blit(quitButton, quitButtonRect)

    # --- STORY BUTTON ---
    if storyButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(storyButton, (350, 175))
        hover_rect = hover.get_rect(center=storyButtonRect.center)
        screen.blit(hover, hover_rect)
        popup_text = "A "
    else:
        screen.blit(storyButton, storyButtonRect)

    # --- SETTINGS BUTTON ---
    if settingsButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(settingsButton, (220, 175))
        hover_rect = hover.get_rect(center=settingsButtonRect.center)
        screen.blit(hover, hover_rect)
        popup_text = "Game settings"
        if clicked:
            hide_popup()
            current_page = "settings"
            go_to_page(SETTINGS)
            return
    else:
        screen.blit(settingsButton, settingsButtonRect)

    # --- AUDIO BUTTON ---
    if audioOn:
        currentAudioButton = audioOnButton
    else:
        currentAudioButton = audioOffButton

    if audioOnButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(currentAudioButton, (220, 175))
        hover_rect = hover.get_rect(center=audioOnButtonRect.center)
        screen.blit(hover, hover_rect)
        popup_text = "Toggle game sounds"
    else:
        screen.blit(currentAudioButton, audioOnButtonRect)


    # --- SHOP BUTTON ---
    if shopButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(shopButton, (350, 175))
        hover_rect = hover.get_rect(center=shopButtonRect.center)
        screen.blit(hover, hover_rect)
    else:
        screen.blit(shopButton, shopButtonRect)


    # --- HANDLE POPUP DISPLAY ---
    if popup_text and not clicked:  
        if popup is None:
            show_popup(popup_text, mx + 20, my + 20)
        else:
            popup.geometry(f"+{mx + 20}+{my + 20}")
            popup.update_idletasks()
    else:
        hide_popup()

    root.update_idletasks()
    root.update()

def draw_game(dt):
    
    screen.blit(backgroundGame, (0, 0))
    screen.blit(headerText, headerRect)

    screen.blit(backButtonImg, backButtonRect)

    screen.blit(scoreBoard,scoreBoardRect)

    boats.update(dt)
    boats.draw(screen)

    score_text = buttonfont.render(f"{killed}", True, black)  
    score_rect = score_text.get_rect(center=(scorex, scorey))
    screen.blit(score_text, score_rect) 

    minutes = str(secondsRemaining // 60)
    seconds = str(secondsRemaining % 60)
    if len(minutes) < 2: minutes = "0" + minutes
    if len(seconds) < 2: seconds = "0" + seconds

    timer_text = buttonfont.render(f"Time: {minutes}:{seconds}", True, black)
    timer_rect = timer_text.get_rect(center=(scorex, scorey + 80))
    screen.blit(timer_text, timer_rect)


def draw_shop():
    screen.blit(backgroundMenu, (0, 0))
    title = headerfont.render("Shop", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 150))
    screen.blit(title, titleRect)

    shopText = buttonfont.render("Buy! BUY! BUY! AND! SPEND MONEY!!!!!!!", True, white)
    screen.blit(shopText, (gameWidth / 2 - 200, 300))

    # Draw back button
    if backButtonRect.collidepoint(pygame.mouse.get_pos()):
        hover = pygame.transform.scale(backButtonImg, (250, 200))
        hover_rect = hover.get_rect(center=backButtonRect.center)
        screen.blit(hover, hover_rect)
    else:
        screen.blit(backButtonImg, backButtonRect)

    # ---- Power-up Buttons ----
    # Define button positions (evenly spaced across the screen)
    button_y = 600
    button_width = 150
    button_height = 100
    spacing = 80  # space between buttons

    total_width = 4 * button_width + 3 * spacing
    start_x = (gameWidth - total_width) / 2

    powerUpRects = []
    for i in range(4):
        x = start_x + i * (button_width + spacing)
        rect = pygame.Rect(x, button_y, button_width, button_height)
        powerUpRects.append(rect)

    # Draw the power-up buttons
    for i, rect in enumerate(powerUpRects, start=1):
        color = (180, 180, 180)
        if rect.collidepoint(pygame.mouse.get_pos()):
            color = (255, 255, 255)
        pygame.draw.rect(screen, color, rect, border_radius=12)

        text = buttonfont.render(f"PowerUp{i}", True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # You can return these rects for click detection elsewhere if needed
    return {
        "back": backButtonRect,
        "powerUps": powerUpRects
    }


def draw_settings():
    screen.blit(backgroundMenu, (0, 0))

    # --- Title ---
    title = headerfont.render("Settings", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 180))
    screen.blit(title, titleRect)

    # --- Example settings text (visual placeholders) ---
    musicLabel = buttonfont.render("The settings are perfect, GO AWAY?:", True, white)
    #sfxLabel = buttonfont.render("SFX Volume:", True, white)

    screen.blit(musicLabel, (gameWidth / 2 - 150, 300))

    # --- Back button ---
    backButton = buttonfont.render("Back", True, white)
    backRect = backButton.get_rect(center=(gameWidth / 2, 650))
    screen.blit(backButton, backRect)

    return backRect


def go_to_page(page_name):
    """Switch to a new page and hide any popup."""
    global current_page
    hide_popup()  
    current_page = page_name


gold = 0 # gold/money
global audioOn  
audioOn = True

while True:
    dt = min(clock.tick(60) / 1000, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_page == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitButtonRect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit(); sys.exit()
                elif playButtonRect.collidepoint(pygame.mouse.get_pos()):
                    killed = 0
                    missed = 0
                    secondsRemaining = 15
                    go_to_page(GAME)
                elif shopButtonRect.collidepoint(pygame.mouse.get_pos()):
                  current_page = SHOP
                elif audioOnButtonRect.collidepoint(pygame.mouse.get_pos()):
                    audioOn = not audioOn

        elif current_page == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                

                if backButtonRect.collidepoint(mouse_pos):
                    #pygame.mixer.stop()
                    boats.empty()
                    scorePage(killed=killed)
                    current_page = MENU

                for boat in boats:
                    if boat.rect.collidepoint(mouse_pos):
                        boat.kill() 
                        killed += 1
                        if audioOn:
                            random.choice([boom2, boom3]).play()                        
            
            if event.type == SPAWN_EVENT:
                y = random.randint(gameHeight // 3 + 40, gameHeight - 100)
                boats.add(PirateShip(y, direction="right", kind="normal"))

            if event.type == SPAWN_EVENT2:
                y = random.randint(gameHeight // 3 + 40, gameHeight - 100)
                boats.add(PirateShip(y, direction="left", kind="special"))

            if event.type == SPAWN_EVENT3:
                y = 300
                boats.add(PirateShip(y, direction="left", kind="fly"))

            if event.type == TIMER_EVENT:
                secondsRemaining -= 1
                if secondsRemaining < 0:
                    boats.empty()
                    scorePage(killed=killed)
                    current_page = MENU


        elif current_page == SHOP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButtonRect.collidepoint(pygame.mouse.get_pos()):
                    current_page = MENU

        elif current_page == SETTINGS:
            backRect = draw_settings()

            if event.type == MOUSEBUTTONDOWN:
                if backRect.collidepoint(pygame.mouse.get_pos()):
                    go_to_page(MENU)


    if current_page == MENU:
        draw_menu()
    elif current_page == GAME:
        draw_game(dt)
    elif current_page == SHOP:
        draw_shop()

    pygame.display.update()
