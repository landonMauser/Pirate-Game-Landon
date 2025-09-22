from pygame import *
from pygame.font import Font
from pygame.sprite import *
import pygame, sys, os, random
from pygame.locals import *
#from score import score

def resource_path(my_path):
    try:
        # When bundled by PyInstaller, files are extracted to a temp folder
        base_path = sys._MEIPASS
    except Exception:
        # When running normally, use the folder of this script
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
boom1 = pygame.mixer.Sound(resource_path("resources/boom1.mp3"))

# Sprite
shipSprite = pygame.image.load(resource_path("resources/piratePixelShip1.png")).convert_alpha()
shipSprite = pygame.transform.scale(shipSprite, (90, 90))

shipSprite3 = pygame.image.load(resource_path("resources/piratePixelShip3.png")).convert_alpha()
shipSprite3 = pygame.transform.scale(shipSprite3, (90, 90))

shipSprite2 = pygame.image.load(resource_path("resources/piratePixelShip2.png")).convert_alpha()
shipSprite2 = pygame.transform.scale(shipSprite2, (90, 90))

scoreBoard = pygame.image.load(resource_path("resources/scorePlate.png")).convert_alpha()
scoreBoard = pygame.transform.scale(scoreBoard, (200, 200))
scoreBoardRect = scoreBoard.get_rect(topleft=(1200, 50))

startButton = pygame.image.load(resource_path("resources/startButton1.png")).convert_alpha()
startButton = pygame.transform.scale(startButton, (250, 125)) 
playButtonRect = startButton.get_rect(topleft=(gameWidth / 2 - 120, 300))

quitButton = pygame.image.load(resource_path("resources/quitButton2.png")).convert_alpha()
quitButton = pygame.transform.scale(quitButton, (200, 100))
quitButtonRect = quitButton.get_rect(topleft=(gameWidth / 2 - 90, 750))

shopButton = pygame.image.load(resource_path("resources/shopButton2.png")).convert_alpha()
shopButton = pygame.transform.scale(shopButton, (200, 200))
shopButtonRect = shopButton.get_rect(topleft=(gameWidth / 2 - 90, 480))

# Colors
pink = (255, 157, 195)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


headerfont = Font('freesansbold.ttf', 48)
buttonfont = pygame.font.SysFont('Arial', 40, bold=True)

headerText = headerfont.render("Whack 'A pirateShip!", True, black, pink)
headerRect = headerText.get_rect(center=(gameWidth / 2, 100))

backButtonNormal = buttonfont.render(" Back ", True, black, pink)
backButtonHover = buttonfont.render(" Back ", True, red, pink)
backButtonRect = backButtonNormal.get_rect(topleft=(gameWidth / 2 - 60, 750))

scoreText = buttonfont.render("Score:     ", True, black)
scoreRect = scoreText.get_rect()
scorex = 1298
scorey = 200
scoreRect.center = (scorex,scorey)
pygame.draw.rect(screen,True,scoreRect)

# Pages
MENU = "menu"
GAME = "game"
SHOP = "shop"

current_page = MENU


class PirateShip(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = random.choice([shipSprite, shipSprite3])
        self.rect = self.image.get_rect(topleft=(10, y))
        self.speed = random.randint(100, 200) 

    def update(self, dt):
        self.rect.x += int(self.speed * dt)
        if self.rect.left > gameWidth - 150:
            self.kill() 
            


class PirateShip2(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = shipSprite2
        self.rect = self.image.get_rect(topright=(gameWidth, y))
        self.speed = random.randint(100, 200) 

    def update(self, dt):
        self.rect.x -= int(self.speed * dt)
        if self.rect.right < 500:
            self.kill()




boats = pygame.sprite.Group()


#spawning

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2300)  

SPAWN_EVENT2 = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_EVENT2, 3000)  

def draw_menu():
    screen.blit(backgroundMenu, (0, 0))
    title = headerfont.render("Main Menu", True, white)
    titleRect = title.get_rect(center=(gameWidth / 2, 200))
    screen.blit(title, titleRect)

    
    mouse_pos = pygame.mouse.get_pos()
    if playButtonRect.collidepoint(mouse_pos):

        hover = pygame.transform.scale(startButton, (int(300),int(150)))

        hover_rect = hover.get_rect(center=playButtonRect.center)
        screen.blit(hover, hover_rect)

    else:
        screen.blit(startButton, playButtonRect)

    if quitButtonRect.collidepoint(pygame.mouse.get_pos()):
        hover = pygame.transform.scale(quitButton, (220, 110))
        hover_rect = hover.get_rect(center=quitButtonRect.center)
        screen.blit(hover, hover_rect)
        
    else:
        screen.blit(quitButton, quitButtonRect)
    

    if shopButtonRect.collidepoint(pygame.mouse.get_pos()):
        hover = pygame.transform.scale(shopButton, (220, 220))
        hover_rect = hover.get_rect(center=shopButtonRect.center)
        screen.blit(hover, hover_rect)
        
    else:
        screen.blit(shopButton, shopButtonRect)

# import score


def draw_game(dt):
    
    screen.blit(backgroundGame, (0, 0))
    screen.blit(headerText, headerRect)

    boats.update(dt)
    boats.draw(screen)

    backBtnText = backButtonHover if backButtonRect.collidepoint(pygame.mouse.get_pos()) else backButtonNormal
    pygame.draw.rect(screen, white, backButtonRect)
    screen.blit(backBtnText, backButtonRect)

    # score plaque
    screen.blit(scoreBoard,scoreBoardRect)

    score_text = buttonfont.render(f"{killed}", True, black)  
    score_rect = score_text.get_rect(center=(scorex, scorey))
    screen.blit(score_text, score_rect) 


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
                    current_page = GAME
                elif shopButtonRect.collidepoint(pygame.mouse.get_pos()):
                  current_page = SHOP



        elif current_page == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if backButtonRect.collidepoint(mouse_pos):
                    #pygame.mixer.stop()
                    boats.empty()
                    import score
                    current_page = MENU

                for boat in boats:
                    if boat.rect.collidepoint(mouse_pos):
                        boat.kill() 
                        killed += 1
                        #pygame.mixer.stop()
                        boom1.play()                        
            
            elif event.type == SPAWN_EVENT:
                margin = 100
                y = random.randint(gameHeight // 3, gameHeight - margin)
                boat = PirateShip(y)
                boats.add(boat)


            elif event.type == SPAWN_EVENT2:                       
                margin = 100
                y = random.randint(gameHeight // 3, gameHeight - margin)
                boat = PirateShip2(y)
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
