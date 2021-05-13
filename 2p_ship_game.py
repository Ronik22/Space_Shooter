import pygame
import os
import sys

pygame.init()

""" CONSTANTS """

WIDTH, HEIGHT = 900, 500

WHITE = (255,255,255)
BLACK = (20,20,20)
RED = (255,0,0)
YELLOW = (255,255,0)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
RED_HEALTH = 100
YELLOW_HEALTH = 100
DAMAGE = 5

YELLOW_HIT = pygame.USEREVENT + 1       # user 1 event
RED_HIT = pygame.USEREVENT + 2          # user 2 event

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'WoodCrashesDistant FS022705.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'LaserBlastQuick PE1095107.mp3'))
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Max Brhon - Cyberpunk [NCS Release].mp3'))
pygame.mixer.Sound.set_volume(BACKGROUND_SOUND, 0.4)        
WINNER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'mixkit-wrong-answer-bass-buzzer-948.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
MENU_FONT = pygame.font.SysFont('comicsans', 90)
MENU_SUB_FONT = pygame.font.SysFont('comicsans', 40)
MENU_SUB_MINI_FONT = pygame.font.SysFont('comicsans', 28)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))              # window resolution
pygame.display.set_caption("2-Player Spaceship Game!")      # window title

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'lucas-benjamin-wQLAGv4_OYs-unsplash.jpg')), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)    # rotate and scale image

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)      # rotate and scale image



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """
    Draw objects on the window

    Args:
        red (Rect): To track red ship
        yellow (Rect): To track yellow ship
        red_bullets (list): Store bullets
        yellow_bullets (list): Store bullets
        red_health (int): Health of red ship
        yellow_health (int): Health of yellow ship
    """
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: "+ str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))      # position image
    WIN.blit(RED_SPACESHIP, (red.x, red.y))         # position image

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()     # update the display after change


def yellow_handle_movement(keys_pressed, yellow):
    """
    Handle yellow ship movement

    Args:
        keys_pressed (): All keys pressed
        yellow (Rect): To track yellow ship
    """
    if keys_pressed[pygame.K_a] and (yellow.x - VEL > 0):    # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and (yellow.x + VEL + yellow.width < BORDER.x):    # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and (yellow.y - VEL > 0):    # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and (yellow.y + VEL + yellow.height < HEIGHT - 15):    # down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    """
    Handle red ship movement

    Args:
        keys_pressed (): All keys pressed
        red (Rect): To track red ship
    """
    if keys_pressed[pygame.K_LEFT] and (red.x - VEL > BORDER.x + BORDER.width):    # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x + VEL + red.width < WIDTH):    # right
        red.x += VEL
    if keys_pressed[pygame.K_UP]  and (red.y - VEL > 0):    # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and (red.y + VEL + red.height < HEIGHT - 15):    # down
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    """
    Handle Bullet Logic

    Args:
        yellow_bullets (list): Stores yellow bullets
        red_bullets (list): Stores red bullets
        yellow (Rect): To track yellow ships
        red (Rect): To track red ship
    """
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    """
    Draw Winner

    Args:
        text (str): Winner Text
    """
    WINNER_SOUND.play()
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def game():
    """
    Game Function
    """
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = RED_HEALTH
    yellow_health = YELLOW_HEALTH

    clock = pygame.time.Clock()     # to refresh display acc to FPS value
    run = True
    while run:  
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # To quit when user presses cross window button
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= DAMAGE
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= DAMAGE
                BULLET_HIT_SOUND.play()
            
        keys_pressed = pygame.key.get_pressed()     # keys that are currently pressed down
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS !"

        if yellow_health <= 0:
            winner_text = "RED WINS !"

        if winner_text != "":
            draw_winner(winner_text)
            break


def  how_to_play():
    """
    How to play window
    """
    running = True
    clock = pygame.time.Clock()     # to refresh display acc to FPS value
    while running:
        WIN.fill((0,0,0))
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(20, 20, 200, 50)

        pygame.draw.rect(WIN, WHITE, button_1)
        draw_text = MENU_SUB_FONT.render("Go Back", 1, BLACK)
        WIN.blit(draw_text, (50, 32))

        HOW_TO_PLAY_Y1 = "YELLOW SHIP :" 
        HOW_TO_PLAY_Y2 = "W,A,S,D - Movement,  LCtrl - Fire" 
        HOW_TO_PLAY_R1 = "RED SHIP :"
        HOW_TO_PLAY_R2 = "UP,LEFT,DOWN,RIGHT - Movement,  RCtrl - Fire"
        draw_text_body11 = MENU_SUB_MINI_FONT.render(HOW_TO_PLAY_Y1, 1, WHITE)
        draw_text_body12 = MENU_SUB_MINI_FONT.render(HOW_TO_PLAY_Y2, 1, WHITE)
        draw_text_body21 = MENU_SUB_MINI_FONT.render(HOW_TO_PLAY_R1, 1, WHITE)
        draw_text_body22 = MENU_SUB_MINI_FONT.render(HOW_TO_PLAY_R2, 1, WHITE)
        WIN.blit(draw_text_body11, (30, HEIGHT//2 - draw_text_body11.get_height()//2 - 70))
        WIN.blit(draw_text_body12, (30, HEIGHT//2 - draw_text_body12.get_height()//2 - 30))
        WIN.blit(draw_text_body21, (30, HEIGHT//2 - draw_text_body21.get_height()//2 + 30))
        WIN.blit(draw_text_body22, (30, HEIGHT//2 - draw_text_body22.get_height()//2 + 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_1.collidepoint((mx, my)):
                    running = False
        
        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    """
    Main menu of the game
    """
    click2 = False
    clock = pygame.time.Clock()     # to refresh display acc to FPS value
    while True:
        clock.tick(FPS)
        WIN.blit(MENU_BACKGROUND,(0,0))
        draw_text = MENU_FONT.render("Space Shooter", 1, WHITE)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2 - 80))

        draw_text_footer = MENU_SUB_MINI_FONT.render("Developed by Ronik Bhattacharjee", 1, WHITE)
        WIN.blit(draw_text_footer, (WIDTH//2 - draw_text_footer.get_width()//2, HEIGHT - 60))
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        button_2 = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click2:
                game()
        
        if button_2.collidepoint((mx, my)):
            if click2:
                how_to_play()
        
        pygame.draw.rect(WIN, WHITE, button_1)
        draw_text2 = MENU_SUB_FONT.render("Start", 1, BLACK)
        WIN.blit(draw_text2, (WIDTH//2 - 35, HEIGHT//2 + 12 , 200, 50))

        pygame.draw.rect(WIN, WHITE, button_2)
        draw_text3 = MENU_SUB_FONT.render("How to Play", 1, BLACK)
        WIN.blit(draw_text3, (WIDTH//2 - 80, HEIGHT//2 + 92 , 200, 50))
 
        click2 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click2 = True
 
        pygame.display.update()
            


if __name__ == "__main__":
    BACKGROUND_SOUND.play()
    main_menu()