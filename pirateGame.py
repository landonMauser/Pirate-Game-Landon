import sys, os
from pygame import *
from peewee import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os, random
from pygame.locals import *
from score import *
import tkinter as tk

root = tk.Tk()
root.withdraw() 
popup = None

import os, sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller EXE."""
    if getattr(sys, '_MEIPASS', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

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

bossBackground = pygame.image.load(resource_path("resources/background9.png")).convert()
bossBackground = pygame.transform.scale(bossBackground, (gameWidth, gameHeight))

# audio
boom1 = pygame.mixer.Sound(resource_path("resources/sound/boom1.mp3"))
boom2 = pygame.mixer.Sound(resource_path("resources/sound/boom2.mp3"))
boom3 = pygame.mixer.Sound(resource_path("resources/sound/boom3.mp3"))


# Sprite
shipSprite = pygame.image.load(resource_path("resources/ships/piratePixelShip1.png")).convert_alpha()
shipSprite = pygame.transform.scale(shipSprite, (120, 120))

shipSprite3 = pygame.image.load(resource_path("resources/ships/piratePixelShip3.png")).convert_alpha()
shipSprite3 = pygame.transform.scale(shipSprite3, (120, 120))

powerUp1 = pygame.image.load(resource_path("resources/buttons/crewPower.png")).convert_alpha()
powerUp1 = pygame.transform.scale(powerUp1, (120, 120))

powerUp2 = pygame.image.load(resource_path("resources/buttons/goldPower.png")).convert_alpha()
powerUp2 = pygame.transform.scale(powerUp2, (120, 120))

powerUp3 = pygame.image.load(resource_path("resources/buttons/scoreUp.png")).convert_alpha()
powerUp3 = pygame.transform.scale(powerUp3, (120, 120))

powerUp4 = pygame.image.load(resource_path("resources/buttons/misc3.png")).convert_alpha()
powerUp4 = pygame.transform.scale(powerUp4, (120, 120))

shipSprite2 = pygame.image.load(resource_path("resources/ships/piratePixelShip2.png")).convert_alpha()
shipSprite2 = pygame.transform.scale(shipSprite2, (120, 120))

flyShip = pygame.image.load(resource_path("resources/ships/dutch.png")).convert_alpha()
flyShip = pygame.transform.scale(flyShip, (200, 200))

flyShip2 = pygame.image.load(resource_path("resources/ships/ghostShip1.png")).convert_alpha()
flyShip2 = pygame.transform.scale(flyShip2, (200, 200))

flyShip3 = pygame.image.load(resource_path("resources/ships/ghostShip2.png")).convert_alpha()
flyShip3 = pygame.transform.scale(flyShip3, (120, 180))

kraken1 = pygame.image.load(resource_path("resources/ships/kraken1.png")).convert_alpha()
kraken1 = pygame.transform.scale(kraken1, (200, 200))

kraken2 = pygame.image.load(resource_path("resources/ships/kraken2.png")).convert_alpha()
kraken2 = pygame.transform.scale(kraken2, (200, 200))

goldIcon = pygame.image.load(resource_path("resources/buttons/goldCoin.png")).convert_alpha()
goldIcon = pygame.transform.scale(goldIcon, (75, 75))  

scoreBoard = pygame.image.load(resource_path("resources/scorePlate.png")).convert_alpha()
scoreBoard = pygame.transform.scale(scoreBoard, (200, 200))
scoreBoardRect = scoreBoard.get_rect(topleft=(gameWidth-400, 40))

startButton = pygame.image.load(resource_path("resources/buttons/arcade.png")).convert_alpha()
startButton = pygame.transform.scale(startButton, (300, 150)) 
playButtonRect = startButton.get_rect(topleft=(gameWidth / 2 - 120, 500))

quitButton = pygame.image.load(resource_path("resources/buttons/quitButton2.png")).convert_alpha()
quitButton = pygame.transform.scale(quitButton, (300, 150))
quitButtonRect = quitButton.get_rect(topleft=(gameWidth / 2 - 110, 900))

shopButton = pygame.image.load(resource_path("resources/buttons/shop.png")).convert_alpha()
shopButton = pygame.transform.scale(shopButton, (300, 150))
shopButtonRect = shopButton.get_rect(topleft=(gameWidth / 2 - 120, 700))

storyButton = pygame.image.load(resource_path("resources/buttons/storyMode.png")).convert_alpha()
storyButton = pygame.transform.scale(storyButton, (330, 165))
storyButtonRect = storyButton.get_rect(topleft=(gameWidth / 2 - 130, 300))

audioOnButton = pygame.image.load(resource_path("resources/buttons/audioOnButton.png")).convert_alpha()
audioOnButton = pygame.transform.scale(audioOnButton, (200, 150))
audioOnButtonRect = audioOnButton.get_rect(topleft=(300, 40))

audioOffButton = pygame.image.load(resource_path("resources/buttons/audioOffButton.png")).convert_alpha()
audioOffButton = pygame.transform.scale(audioOffButton, (200, 150))
audioOffButtonRect = audioOffButton.get_rect(topleft=(300, 40))

white = (255, 255, 255)
black = (0, 0, 0)

headerfont = Font('freesansbold.ttf', 48)
smallFont = Font('freesansbold.ttf', 20)
buttonfont = pygame.font.SysFont('Arial', 40, bold=True)

headerText = headerfont.render("Whack 'A pirateShip!", True, black, None)
headerRect = headerText.get_rect(center=(gameWidth / 2, 100))

# Back button image
backButtonImg = pygame.image.load(resource_path("resources/buttons/backButton1.png")).convert_alpha()
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
LEVELSELECT = "level select"
BOSSLEVEL = "boss level" 

current_page = MENU

class PirateShip(pygame.sprite.Sprite):
    def __init__(self, y, direction="right", kind="normal"):
        super().__init__()

        if kind == "normal":
            self.image = random.choice([shipSprite, shipSprite3])
            self.speed = random.randint(100, 200) * current_difficulty.get("speed_mult", 1.0)
        elif kind == "special":
            self.image = shipSprite2
            self.speed = random.randint(100, 200) * current_difficulty.get("speed_mult", 1.0)
        elif kind == "fly":
            chance = random.random()
            if chance < 0.01:
                self.image = flyShip
                self.speed = 200
            elif chance < 0.31:  
                self.image = flyShip3
                self.speed = 300
            else:
                self.image = flyShip2
                self.speed = random.randint(100, 200) * current_difficulty.get("speed_mult", 1.0)
        elif kind == "kraken1":
            self.image = kraken1
            self.speed = random.randint(50, 100) 
        elif kind == "kraken2":
            self.image = kraken2
            self.speed = random.randint(70, 170)  

        # Setup rect and position
        self.rect = self.image.get_rect()
        self.direction = direction
        self.pos_x = float(0 if direction == "right" else gameWidth) 
        self.rect.y = y

    def update(self, dt):
        global missed
        if self.direction == "right":
            self.pos_x += self.speed * dt
        else:
            self.pos_x -= self.speed * dt
            

        self.rect.x = round(self.pos_x)     
           
        if self.rect.right < 0 or self.rect.left > gameWidth:
            missed += 1
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
    
    gold_text = headerfont.render(f"{gold}", True, (255, 215, 0))  # gold color text
    gold_rect = gold_text.get_rect(topleft=(gameWidth/2 + 360, 710))
    screen.blit(gold_text, gold_rect)

    screen.blit(goldIcon, (gameWidth/2 + 260, 700))

    mouse_pos = pygame.mouse.get_pos()
    mx, my = mouse_pos
    popup_text = None
    clicked = pygame.mouse.get_pressed()[0]  # Left mouse button

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

    if storyButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(storyButton, (350, 175))
        hover_rect = hover.get_rect(center=storyButtonRect.center)
        screen.blit(hover, hover_rect)
        popup_text = "A series of levels"
        if clicked:
            hide_popup()
    else:
        screen.blit(storyButton, storyButtonRect)

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

    if shopButtonRect.collidepoint(mouse_pos):
        hover = pygame.transform.scale(shopButton, (350, 175))
        hover_rect = hover.get_rect(center=shopButtonRect.center)
        screen.blit(hover, hover_rect)
        popup_text = "Buy powerful abilities"
    else:
        screen.blit(shopButton, shopButtonRect)

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

current_level = None

def draw_level_select():
    """
    Draws the Level Select page with 8 levels in a 4x2 grid.
    Returns the rects for click detection.
    """
    screen.blit(backgroundMenu, (0, 0))
    
    title = headerfont.render("Level Select", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 150))
    screen.blit(title, titleRect)

    mouse_pos = pygame.mouse.get_pos()

    if backButtonRect.collidepoint(pygame.mouse.get_pos()):
        hover = pygame.transform.scale(backButtonImg, (250, 200))
        hover_rect = hover.get_rect(center=backButtonRect.center)
        screen.blit(hover, hover_rect)
    else:
        screen.blit(backButtonImg, backButtonRect)

    button_width = 150
    button_height = 100
    spacing_x = 60
    spacing_y = 60
    columns = 4
    rows = 2

    total_width = columns * button_width + (columns - 1) * spacing_x
    start_x = (gameWidth - total_width) / 2
    start_y = 400  # top row Y position
    levelRects = []
    for row in range(rows):
        for col in range(columns):
            level_num = row * columns + col + 1
            if level_num > 8:
                break
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            rect = pygame.Rect(x, y, button_width, button_height)
            levelRects.append(rect)

            color = (180, 180, 180)
            if rect.collidepoint(mouse_pos):
                color = (255, 255, 255)

            pygame.draw.rect(screen, color, rect, border_radius=12)

            # Level text
            text = buttonfont.render(f"Level {level_num}", True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    level8_note = buttonfont.render("Level 8 gives no gold", True, white)
    level8_rect = levelRects[-1]  # Level 8 is the last one
    note_x = level8_rect.right + 20  
    note_y = level8_rect.centery
    note_rect = level8_note.get_rect(midleft=(note_x, note_y))
    screen.blit(level8_note, note_rect)
    
    return {
        "back": backButtonRect,
        "levels": levelRects
    }

def handle_level_select_click(event):
    global current_page, current_level, killed, secondsRemaining

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        rects = draw_level_select()  # Get level and back rects
        if rects["back"].collidepoint(mouse_pos):
            current_page = MENU
            return

        for i, level_rect in enumerate(rects["levels"], start=1):
            if level_rect.collidepoint(mouse_pos):
                current_level = i
                killed = 0
                secondsRemaining = 120
                if i in LEVEL_SETTINGS:
                    settings = LEVEL_SETTINGS[i]
                    pygame.time.set_timer(SPAWN_EVENT, settings["spawn_rate"][0])
                    pygame.time.set_timer(SPAWN_EVENT2, settings["spawn_rate"][1])
                    pygame.time.set_timer(SPAWN_EVENT3, settings["spawn_rate"][2])
                    global current_difficulty
                    current_difficulty = settings
                else:
                    current_difficulty = {"speed_mult": 1.0, "fly_chance": 0.05}

                if i == 8:
                    current_page = BOSSLEVEL
                else:
                    current_page = GAME
                return
def draw_game():
    screen.blit(backgroundGame, (0, 0))
    screen.blit(headerText, headerRect)
    screen.blit(backButtonImg, backButtonRect)
    screen.blit(scoreBoard, scoreBoardRect)

    boats.draw(screen)

    score_text = buttonfont.render(f"{killed}", True, black)
    score_rect = score_text.get_rect(center=(scorex, scorey))
    screen.blit(score_text, score_rect)
    draw_powerUp4_counter()

    minutes = str(secondsRemaining // 60)
    seconds = str(secondsRemaining % 60)
    if len(minutes) < 2: minutes = "0" + minutes
    if len(seconds) < 2: seconds = "0" + seconds

    timer_text = buttonfont.render(f"Time: {minutes}:{seconds}", True, black)
    timer_rect = timer_text.get_rect(center=(scorex, scorey + 80))
    screen.blit(timer_text, timer_rect)

def draw_shop():
    global powerUpOwned, powerUpCost
    screen.blit(backgroundMenu, (0, 0))

    gold_text = headerfont.render(f"{gold}", True, (255, 215, 0))
    gold_rect = gold_text.get_rect(topleft=(gameWidth/2 + 290, 260))
    screen.blit(gold_text, gold_rect)
    screen.blit(goldIcon, (gameWidth/2 + 190, 250))

    shopText = buttonfont.render("Buy Powerups", True, white)
    screen.blit(shopText, (gameWidth / 2 - 100, 250))

    if backButtonRect.collidepoint(pygame.mouse.get_pos()):
        hover = pygame.transform.scale(backButtonImg, (250, 200))
        hover_rect = hover.get_rect(center=backButtonRect.center)
        screen.blit(hover, hover_rect)
    else:
        screen.blit(backButtonImg, backButtonRect)

    button_y = 350
    button_width = 200
    button_height = 200
    spacing = 100
    total_width = 3 * button_width + 2 * spacing  # only 3 power-ups now
    start_x = (gameWidth - total_width) / 2

    powerUpData = [
        ("powerUp2", powerUp2, "Increases gold earned!"),
        ("powerUp3", powerUp3, "Multiplies score by 2 for each purchase!"),
        ("powerUp4", powerUp4, "Press space bar to eliminate each enemy on the screen!")
    ]

    powerUpRects = {}
    mouse_pos = pygame.mouse.get_pos()
    popup_text = None

    for i, (name, image, desc) in enumerate(powerUpData):
        x = start_x + i * (button_width + spacing)
        rect = pygame.Rect(x, button_y, button_width, button_height)
        powerUpRects[name] = rect

        if rect.collidepoint(mouse_pos):
            hoverImg = pygame.transform.scale(image, (int(button_width * 1.1), int(button_height * 1.1)))
            hover_rect = hoverImg.get_rect(center=rect.center)
            screen.blit(hoverImg, hover_rect)
            popup_text = desc
        else:
            normalImg = pygame.transform.scale(image, (button_width, button_height))
            screen.blit(normalImg, rect)

        # Owned + cost text
        owned_text = smallFont.render(f"Owned: {powerUpOwned[name]}", True, white)
        cost_text = smallFont.render(f"Cost: {powerUpCost[name]}", True, white)

        owned_rect = owned_text.get_rect(center=(rect.centerx, rect.bottom + 20))
        cost_rect = cost_text.get_rect(center=(rect.centerx, rect.bottom + 45))

        screen.blit(owned_text, owned_rect)
        screen.blit(cost_text, cost_rect)

    # === Tooltip Handling ===
    mx, my = mouse_pos
    if popup_text:
        if popup is None:
            show_popup(popup_text, mx + 20, my + 20)
        else:
            popup.geometry(f"+{mx + 20}+{my + 20}")
            popup.update_idletasks()
    else:
        hide_popup()

    root.update_idletasks()
    root.update()

    return {
        "back": backButtonRect,
        "powerUps": powerUpRects
    }

def draw_boss_level():
    screen.blit(bossBackground, (0, 0)) 
    screen.blit(headerText, headerRect)  

    screen.blit(backButtonImg, backButtonRect)
    screen.blit(scoreBoard, scoreBoardRect)

    boats.draw(screen)

    score_text = buttonfont.render(f"{killed}", True, black)  
    score_rect = score_text.get_rect(center=(scorex, scorey))
    screen.blit(score_text, score_rect) 
    draw_powerUp4_counter()
    minutes = str(secondsRemaining // 60)
    seconds = str(secondsRemaining % 60)
    if len(minutes) < 2: minutes = "0" + minutes
    if len(seconds) < 2: seconds = "0" + seconds

    timer_text = buttonfont.render(f"Time: {minutes}:{seconds}", True, black)
    timer_rect = timer_text.get_rect(center=(scorex, scorey + 80))
    screen.blit(timer_text, timer_rect)

powerUp4_x = 150  
powerUp4_y = 50  
powerUp4_size = 50  
def draw_powerUp4_counter():
    icon = pygame.transform.scale(powerUp4, (powerUp4_size, powerUp4_size))
    screen.blit(icon, (powerUp4_x, powerUp4_y))

    count_text = buttonfont.render(f"x{powerUpOwned['powerUp4']}", True, black)
    count_rect = count_text.get_rect(midleft=(powerUp4_x + powerUp4_size + 10, powerUp4_y + powerUp4_size / 2))
    screen.blit(count_text, count_rect)

def show_score_popup(killed, missed):
    popup = tk.Toplevel()
    popup.wm_overrideredirect(True)
    popup.attributes('-topmost', True)
    popup.configure(bg="#222222")

    if missed == 0:
        text = f"PERFECT SCORE!!!\nShips Killed: {killed}\nShips Missed: {missed}"
    else:
        text = f"Nice Work Captain\nShips Killed: {killed}\nShips Missed: {missed}"
    label = tk.Label(popup, text=text, fg="white", bg="#222222", font=("Arial", 20))
    label.pack(ipadx=20, ipady=20)

    x = (gameWidth // 2) - 450
    y = (gameHeight // 2) - 75
    popup.geometry(f"300x150+{x}+{y}")

    popup.after(4500, popup.destroy)

LEVEL_SETTINGS = {
    1: {"spawn_rate": (3000, 4500, 6500), "speed_mult": 0.75, "fly_chance": 0.005},
    2: {"spawn_rate": (2800, 4300, 6000), "speed_mult": 0.85, "fly_chance": 0.015},
    3: {"spawn_rate": (2600, 4100, 5600), "speed_mult": 0.95, "fly_chance": 0.03},
    4: {"spawn_rate": (2400, 3900, 5200), "speed_mult": 1.05, "fly_chance": 0.05},
    5: {"spawn_rate": (2200, 3700, 4800), "speed_mult": 1.15, "fly_chance": 0.07},
    6: {"spawn_rate": (2000, 3500, 4600), "speed_mult": 1.25, "fly_chance": 0.09},
    7: {"spawn_rate": (1800, 3300, 4400), "speed_mult": 1.35, "fly_chance": 0.11}
}

def go_to_page(page_name):
    """Switch to a new page and hide any popup."""
    global current_page
    hide_popup()  
    current_page = page_name

global gold
gold = 0 # gold/money
global audioOn 
audioOn = True
global missed
missed = 0 
global gold_multiplier
gold_multiplier = 1
global score_multiplier
score_multiplier = 1 
powerUpOwned = {"powerUp1": 0, "powerUp2": 0, "powerUp3": 0, "powerUp4": 0}
powerUpCost = {"powerUp1": 0, "powerUp2": 150, "powerUp3": 400, "powerUp4": 300}

while True:
    dt = min(clock.tick(60) / 1000, 0.05)
    dt = max(0.016, min(dt, 0.033))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if current_page == BOSSLEVEL or current_page == GAME:
                if event.key == pygame.K_SPACE and powerUpOwned['powerUp4'] > 0:
                    for boat in boats.sprites():
                        boat.kill()
                        killed += 1 * score_multiplier
                        if current_page != BOSSLEVEL:
                            gold += 1 * gold_multiplier
                    powerUpOwned['powerUp4'] -= 1

        if current_page == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitButtonRect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                elif playButtonRect.collidepoint(pygame.mouse.get_pos()):
                    killed = 0
                    missed = 0
                    secondsRemaining = 120
                    current_difficulty = LEVEL_SETTINGS[3]  # Default mid-level difficulty
                    pygame.time.set_timer(SPAWN_EVENT, current_difficulty["spawn_rate"][0])
                    pygame.time.set_timer(SPAWN_EVENT2, current_difficulty["spawn_rate"][1])
                    pygame.time.set_timer(SPAWN_EVENT3, current_difficulty["spawn_rate"][2])
                    go_to_page(GAME)
                elif shopButtonRect.collidepoint(pygame.mouse.get_pos()):
                    go_to_page(SHOP)
                elif audioOnButtonRect.collidepoint(pygame.mouse.get_pos()):
                    audioOn = not audioOn
                elif storyButtonRect.collidepoint(pygame.mouse.get_pos()):
                    go_to_page(LEVELSELECT)

        elif current_page == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if backButtonRect.collidepoint(mouse_pos):
                    show_score_popup(killed, missed)
                    boats.empty()
                    current_page = MENU
                    try:
                        scorePage(killed=killed)
                    except:
                        pass

                for boat in boats:
                    if boat.rect.collidepoint(mouse_pos):
                        boat.kill()
                        killed += 1 * score_multiplier
                        gold += 1 * gold_multiplier
                        if audioOn:
                            random.choice([boom2, boom3]).play()

            if event.type == SPAWN_EVENT:
                y = random.randint(gameHeight // 3 + 40, gameHeight - 100)
                chance = random.random()
                if chance <= 0.1:
                    boats.add(PirateShip(y, direction="right", kind="kraken2"))
                else:
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
                    show_score_popup(killed, missed)
                    boats.empty()
                    current_page = MENU
                    try:
                        scorePage(killed=killed)
                    except:
                        pass

        elif current_page == BOSSLEVEL:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if backButtonRect.collidepoint(mouse_pos):
                    show_score_popup(killed, missed)
                    boats.empty()
                    current_page = MENU
                    try:
                        scorePage(killed=killed)
                    except:
                        pass

                for boat in boats:
                    if boat.rect.collidepoint(mouse_pos):
                        boat.kill()
                        killed += 1 * score_multiplier
                        if audioOn:
                            random.choice([boom2, boom3]).play()
            if event.type == SPAWN_EVENT:
                y = random.randint(gameHeight // 3 + 40, gameHeight - 100)
                boats.add(PirateShip(y, direction="right", kind="normal"))

            if event.type == SPAWN_EVENT2:
                y = random.randint(gameHeight // 3 + 40, gameHeight - 100)
                boats.add(PirateShip(y, direction="left", kind="special"))
            
            if SPAWN_EVENT:
                 y = random.randint(gameHeight // 3 + 40, gameHeight - 100)
                 boats.add(PirateShip(y, direction="right", kind="kraken1"))

            if event.type == SPAWN_EVENT3:
                y = 300
                boats.add(PirateShip(y, direction="left", kind="fly"))

            if SPAWN_EVENT3:
                 y = random.randint(gameHeight // 3 + 40, gameHeight - 100)
                 boats.add(PirateShip(y, direction="right", kind="kraken2"))

            if event.type == TIMER_EVENT:
                secondsRemaining -= 1
                if secondsRemaining < 0:
                    show_score_popup(killed, missed)
                    boats.empty()
                    current_page = MENU
                    try:
                        scorePage(killed=killed)
                    except:
                        pass

        elif current_page == LEVELSELECT:
            handle_level_select_click(event)

        elif current_page == SHOP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                shopRects = draw_shop()

                if shopRects["back"].collidepoint(mouse_pos):
                    current_page = MENU

                for name, rect in shopRects["powerUps"].items():
                    if rect.collidepoint(mouse_pos):
                        cost = powerUpCost[name]
                        if gold >= cost:
                            gold -= cost
                            powerUpOwned[name] += 1
                            if name == "powerUp2":
                                gold_multiplier += 1
                            elif name == "powerUp1":
                                print("Crew Power Up! (example effect)")
                            elif name == "powerUp3":
                                score_multiplier *= 2
                        else:
                            print("Not enough gold!")

    if current_page in (GAME, BOSSLEVEL):
        boats.update(dt)

    if current_page == MENU:
        draw_menu()
    elif current_page == GAME:
        draw_game()           
    elif current_page == BOSSLEVEL:
        draw_boss_level()
    elif current_page == SHOP:
        draw_shop()
    elif current_page == LEVELSELECT:
        draw_level_select()

    pygame.display.flip()
