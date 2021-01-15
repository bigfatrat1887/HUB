import pygame
from random import randrange
import sys
import time

fps = 60
W = H = 12
SIZE = 30
GAME_RES = W * SIZE
MAIN_RES = [GAME_RES + 300, GAME_RES + 60]
# create grid
grid = [pygame.Rect(x * SIZE, y * SIZE, SIZE, SIZE) for x in range(W) for y in range(H)]


# methods for randomising
def getxy():
    return randrange(SIZE, GAME_RES - SIZE, SIZE), randrange(SIZE, GAME_RES - SIZE, SIZE)


def getapple():
    return randrange(SIZE, GAME_RES - SIZE, SIZE), randrange(SIZE, GAME_RES - SIZE, SIZE)


def get_color():
    return randrange(30, 256), randrange(30, 256), randrange(30, 256)


# short closure /that needs to be reset
def renew():
    global score, speed_count, snake_speed, x, y, length, snake, dx, dy, dirs, apple
    set_record(record, score)
    apple = getapple()
    score, speed_count, snake_speed = 0, 0, 10
    x, y = getxy()
    length = 1
    snake = [(x, y)]
    dx, dy = 0, 0
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


# methods for setting record score
def get_record():
    try:
        with open('SNAKE_data/record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('SNAKE_data/record', 'w') as f:
            f.write('0')


def set_record(recd, sco):
    rec = max(int(recd), sco)
    with open('SNAKE_data/record', 'w') as f:
        f.write(str(rec))


x, y = getxy()
apple = getapple()

length = 1
snake = [(x, y)]
dx, dy = 0, 0

dirs = {'W': True, 'S': True, 'A': True, 'D': True}
score, speed_count, snake_speed, record = 0, 0, 10, get_record()

pygame.init()
# initialize multiple surfaces
main_surface = pygame.display.set_mode(MAIN_RES)
game_surface = pygame.Surface((GAME_RES, GAME_RES))
# initialize utils
clock = pygame.time.Clock()
pygame.display.set_caption("SNAKE THE GAME")
pygame.display.set_icon(pygame.image.load("SNAKE_data/img/icon.bmp").convert())
# initialize fonts
font_title = pygame.font.Font('SNAKE_data/font/Audiowide-Regular.ttf', 40)
font_text = pygame.font.Font('SNAKE_data/font/Orbitron-Black.ttf', 25)
font_number = pygame.font.Font('SNAKE_data/font/PressStart2P-Regular.ttf', 20)
# create texts
render_score = font_text.render('SCORE:', True, (151, 188, 98))
render_record = font_text.render('RECORD:', True, (151, 188, 98))
render_title = font_title.render("SNAKE", True, (139, 194, 140))
# load images
bg = pygame.image.load('SNAKE_data/img/bg.jpg').convert()
bg2 = pygame.image.load('SNAKE_data/img/bg2.jpg').convert()


# main loop
while True:

    main_surface.blit(bg, (0, 0))
    main_surface.blit(game_surface, (30, 30))
    game_surface.blit(bg2, (0, 0))
    # drawing grid
    [pygame.draw.rect(game_surface, (40, 40, 40), i_rect, width=1) for i_rect in grid]
    # drawing snake, apple
    [pygame.draw.rect(game_surface, 'green', (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
    pygame.draw.ellipse(game_surface, 'red', (*apple, SIZE, SIZE))
    # throw me some numbers
    main_surface.blit(render_score, (420, 90))
    main_surface.blit(render_record, (420, 150))
    main_surface.blit(render_title, (420, 20))
    main_surface.blit(font_number.render(str(score), True, 'red'), (550, 97))
    main_surface.blit(font_number.render(str(record), True, 'gold'), (563, 157))
    # snake movement
    speed_count += 1
    if not speed_count % snake_speed:
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]
    # eating food
    if snake[-1] == apple:
        apple = getapple()
        length += 1
        score += 100
        snake_speed -= 1
        snake_speed = max(snake_speed, 4)
    # game over and restart
    if x < 0 or x > GAME_RES - SIZE or y < 0 or y > GAME_RES - SIZE or len(snake) != len(set(snake)):
        for i_rect in grid:
            pygame.draw.rect(game_surface, get_color(), i_rect)
            main_surface.blit(game_surface, (30, 30))
            pygame.display.flip()
            clock.tick(200)
        pygame.display.flip()
        renew()
        time.sleep(0.2)
        continue
    # controls
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        if dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True}
    elif key[pygame.K_DOWN]:
        if dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True}
    elif key[pygame.K_LEFT]:
        if dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False}
    elif key[pygame.K_RIGHT]:
        if dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True}
    pygame.display.flip()
    clock.tick(fps)
    close_game()
