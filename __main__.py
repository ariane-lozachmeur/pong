import pygame
import sys
from pygame.locals import *
import numpy as np

HEIGHT = 600
WIDTH = 1200
PADDLE_HEIGHT = 100
SPEED = 5
BALL_RADIUS = 5
BALL_SPEED = 2
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
FONT = pygame.font.Font('font/ZillaSlab-Light.ttf',32)
SCORE_SURFACE = FONT.render('Score!',True,WHITE, BLACK)
SCORE_TEXT = SCORE_SURFACE.get_rect()
SCORE_TEXT.center = (WIDTH/2,HEIGHT/2)

y1 = 300
y2 = 300
player_up = False
player_down = False
ball = [WIDTH/2,HEIGHT/2]
vball =BALL_SPEED*np.array([-2,1])

def draw_field():
    pygame.display.set_caption('Pong')
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF, WHITE, (50, y1, 10, PADDLE_HEIGHT))
    pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH - 50, y2, 10, PADDLE_HEIGHT))
    pygame.draw.circle(DISPLAYSURF, WHITE, ball, BALL_RADIUS)
    for i in range(HEIGHT / 20):
        pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH / 2, i * 20, 5, 10))


def move(y,up,down):
    if up:
        y += -SPEED
    elif down:
        y += SPEED
    return y


def move_ball(ball,vball,y1,y2):
    ball[0] = ball[0]+vball[0]
    ball[1] = ball[1]+vball[1]
    # If the ball is at the level of player 2
    if ball[0]>WIDTH-50:
        if y2<ball[1]<y2+PADDLE_HEIGHT:
            vball[0] = -vball[0]
    # If the ball is at the level of player 1
    elif ball[0]<50+BALL_RADIUS:
        if y1<ball[1]<y1+PADDLE_HEIGHT:
            vball[0] = -vball[0]
    # If the ball hits the uper or lower side
    if ball[1]<BALL_RADIUS or ball[1]>HEIGHT-BALL_RADIUS:
        vball[1]=-vball[1]

    return ball,vball


def IA(y, ball, vball):
    if y>ball[1]:
        up = True
        down = False
    elif y<ball[1]:
        up = False
        down = True
    else:
        up = False
        down = False
    return up, down


def control_player(event):
    if event.type == KEYDOWN:
        if event.key == K_UP:
            up = True
            down = False
        elif event.key == K_DOWN:
            up = False
            down = True
    else:
        up = False
        down = False
    return up, down


def score(ball):
    if ball[0]<45 or ball[0]>WIDTH-45:
        DISPLAYSURF.blit(SCORE_SURFACE,SCORE_TEXT)
        scored = True


def game():
    scored = False
    while not scored:
        clock.tick(100)
        draw_field()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            player_up, player_down = control_player(event)
        ia_up, ia_down = IA(y2, ball, vball)
        y1 = move(y1, player_up, player_down)
        y2 = move(y2, ia_up, ia_down)
        ball, vball = move_ball(ball, vball, y1, y2)
        scored = score(ball)
        pygame.display.update()

clock = pygame.time.Clock()
start = False
draw_field()
pygame.display.update()
while not start:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            start = True
            if event.key == K_KP_ENTER:
                start = True

while True:
    clock.tick(100)
    draw_field()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        player_up,player_down = control_player(event)
    ia_up,ia_down = IA(y2,ball, vball)
    y1 = move(y1,player_up,player_down)
    y2 = move(y2,ia_up, ia_down)
    ball,vball = move_ball(ball,vball,y1,y2)
    score(ball)
    pygame.display.update()
