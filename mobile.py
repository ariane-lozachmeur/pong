from math import sqrt
import pygame
from pygame.locals import *
import __main__ as main
import random as rand

HEIGHT = 600
WIDTH = 1200
SPEED = 2

PADDLE_THICK = 10
PADDLE_HEIGHT = 100
BALL_RADIUS = 5

WHITE = (255,255,255)


class Mobile:
    def __init__(self, type, dim, speed):
        self.type = type
        self.dimension = dim
        self.speed = speed

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_speed(self, vx, vy):
        if vx ** 2 + vy ** 2 == self.speed ** 2:
            self.vx = vx
            self.vy = vy
        else:
            if not (vx==0 and vy==0):
                self.vx = self.speed * vx / sqrt(vx ** 2 + vy ** 2)
                self.vy = self.speed * vy / sqrt(vx ** 2 + vy ** 2)
            else:
                self.vx = 0
                self.vy = 0

    def control_player(self, event):
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
        else:
            up = False
            down = False
        if up and not down:
            self.vy = -1
        elif down and not up:
            self.vy = 1
        else:
            self.vy = 0

    def control_ia(self, ball):
        t_impact = max((WIDTH-40 - ball.x)/ball.vx,0)
        y_impact = ball.y + ball.vy * t_impact
        if ball.x == WIDTH/2:
            self.rand = rand.gauss(0,PADDLE_HEIGHT/3)
            print(self.rand)
        if ball.vx < 0 or ball.x < WIDTH/2:
            go_to = WIDTH/4 - PADDLE_HEIGHT/2
        else:
            go_to = y_impact- PADDLE_HEIGHT/2 + self.rand
            # go_to = y_impact - PADDLE_HEIGHT/2

        try:
            self.vy = int(go_to - self.y)/t_impact
        except ZeroDivisionError:
            self.vy = int(go_to - self.y)/100



    def control_ball(self, game):
        # If the ball is at the level of player 2
        if  WIDTH - 50 > self.x > WIDTH - 55:
            if game.player2.paddle.y < self.y < game.player2.paddle.y + PADDLE_HEIGHT:
                self.vx = -self.vx
        # If the ball is at the level of player 1
        elif self.x < 50 + BALL_RADIUS:
            if game.player1.paddle.y < self.y < game.player1.paddle.y + PADDLE_HEIGHT:
                self.vx = -self.vx
        # If the ball hits the uper or lower side
        if self.y < BALL_RADIUS or self.y > HEIGHT - BALL_RADIUS:
            self.vy = -self.vy

    def move(self, speed):
        self.x += int(self.vx * speed)
        self.y += int(self.vy * speed)
