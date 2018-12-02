import pygame
import scripts.mobile as mb
from pygame.locals import *
import random as rand
from scripts.interface import Caption, Menu
from scripts.locals import *
from numpy import argmax
import sys
import time

import numpy as np

class Game:

    def __init__(self, height, width):
        pygame.init()
        pygame.display.set_caption('Pong')
        self.board = pygame.display.set_mode((width, height))
        self.ball = Ball()

    def reset(self):
        self.ball = Ball()
        self.set_players(self.n)

    def set_players(self, n, keys):
        self.n = n
        self.player1 = Player(name = 'Player1', type='player1', k_up=keys[0], k_down=keys[1])
        if n == 1:
            self.player2 = Player(name= 'Player2', type='ia2')
        elif n == 2:
            self.player2 = Player(name= 'Player2', type='player2', k_up=keys[2], k_down=keys[3])

    def update(self):
        self.board.fill(BLACK)
        for i in range(int(HEIGHT / 20)):
            pygame.draw.rect(self.board, WHITE, (WIDTH / 2, i * 20, 5, 10))

        score1 = Caption(self.player1.score)
        score2 = Caption(self.player2.score)
        score1.display(((WIDTH/2 - 50),(HEIGHT-50)),self.board, update=False)
        score2.display(((WIDTH/2 + 50),(HEIGHT-50)),self.board, update=False)

        self.player1.update(self.board)
        self.player2.update(self.board)
        self.ball.update(self.board)

        pygame.display.flip()

    def incr_score(self, player, goal):
        if player == '1':
            self.player1.incr_score(goal)
        elif player == '2':
            self.player2.incr_score(goal)

    def play(self, speed):
        clock = pygame.time.Clock()
        self.player1.reset_pos(x = 50, y = HEIGHT/2)
        self.player2.reset_pos(x= WIDTH-50, y = HEIGHT/2)
        self.ball = Ball()
        while self.ball.mobile.vy == 0 or self.ball.mobile.vx/self.ball.mobile.vy < 1:
            self.ball = Ball()

        while self.ball.scored is None:
            clock.tick()#FRAME_RATE[self.level])
            self.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                self.player1.control(event)
                if self.n == 2:
                    self.player2.control(event)
            if self.n == 1:
                self.player2.control(self.ball)
            self.ball.control(self)
            
            self.player1.move(speed)
            self.player2.move(speed)
            self.ball.move(speed*0.4)


    def menu(self, type):
        start = False
        ans = {}
        menu = Menu(type)
        while not start:
            opt = MENUS[type]['opt']
            title = MENUS[type]['title']
            
            if title is not None:
                menu.set_title(title)
            menu.set_options(*opt)
            menu.display(self.board)
            for event in pygame.event.get():
                action = menu.handle_event(event)
                if action == 'QUIT' or event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif action == 'START':
                    start = True
                elif action == '1player':
                    start = True
                    ans['n'] = 1
                elif action == '2player':
                    start = True
                    ans['n'] = 2
                elif action in ['easy','medium','difficult']:
                    start = True
                    ans['level'] = action

                elif action == 'upkey':
                    MENUS[type]['opt'][0]['id'] = 'Up key:' + str(event.unicode)
                    if 'p1_keys' not in ans.keys():
                        ans['p1_keys'] = [event.key, np.nan]
                    else:
                        ans['p1_keys'][0] = event.key

                elif action == 'downkey':
                    MENUS[type]['opt'][1]['id'] = 'Down key:' + str(event.unicode)
                    if 'p1_keys' not in ans.keys():
                        ans['p1_keys'] = [np.nan, event.key]
                    else:
                        ans['p1_keys'][1] = event.key

        self.board.fill(BLACK)
        return ans

    def show(self, type):
        if type == 'score':
            captions = [
                'Player ' + self.ball.scored + ' scored !',
                'Score: ' + str(self.player1.score) + ' - '+ str(self.player2.score)
            ]
        elif type == 'winner':
            captions = [
                'Player '+ str(argmax([self.player1.score, self.player2.score])+1) + ' won !',
                'Score: ' + str(self.player1.score) + ' - '+ str(self.player2.score)
            ]
        elif type == 'rules':
            captions = [
                'Controls :',
                'Player 1, to go up press: '+ str(pygame.key.name(self.player1.paddle.up)),
                'Player 1 to go down press: '+ str(pygame.key.name(self.player1.paddle.down)),
                # 'Player 2 to go up press: '+ str(pygame.key.name(self.player2.paddle.up)),
                # 'Player 2 to go down press: '+ str(pygame.key.name(self.player2.paddle.down))
            ]
        captions = ['Press enter to continue...'] + captions
        n_caption = len(captions)
        h = (HEIGHT - (n_caption*TEXT_WIDTH))/2
        for i in range(n_caption):
            caption = Caption(captions[i])
            caption.display(((WIDTH/2),(h+i*TEXT_WIDTH)), self.board)
            start = False
        while not start:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        start = True

        self.update()

class Player:

    def __init__(self, name, type, k_up=None, k_down=None):
        self.paddle = mb.Mobile('rect', dim = (PADDLE_THICK, PADDLE_HEIGHT), speed = SPEED['medium'])
        self.name = name
        self.score = 0
        self.type = type

        if '1' in type:
            self.paddle.set_position(50, HEIGHT/2)
            self.paddle.set_controls(k_up,k_down)
        elif '2' in type:
            self.paddle.set_position(WIDTH-50,HEIGHT/2)
            self.paddle.set_controls(k_up,k_down)
            # self.paddle.set_controls(K_p, K_m)
        else:
            raise ValueError('type of player'+name+' incorrect. It doesn\'t contain 1 or 2')

        self.paddle.set_speed(0, 0)

    def incr_score(self, goal=1):
        self.score += goal

    def update(self, board):
        pygame.draw.rect(board, WHITE, (self.paddle.x, self.paddle.y, 10, PADDLE_HEIGHT))

    def move(self, speed):
        self.paddle.move(speed)

    def control(self, indication):
        if 'player' in self.type:
            self.paddle.control_player(indication)
        elif 'ia' in self.type:
            self.paddle.control_ia(indication.mobile)

    def reset_pos(self, x, y):
        self.paddle.set_position(x,y)
        self.paddle.set_speed(0, 0)

class Ball:

    def __init__(self):
        self.mobile = mb.Mobile('circle', dim = (BALL_RADIUS), speed = SPEED['medium'])
        self.mobile.set_position(WIDTH/2, HEIGHT/2)
        self.mobile.set_speed(rand.uniform(-2,2),rand.uniform(-2,2))

        self.scored = None

    def update(self, board):
        pygame.draw.circle(board, WHITE, (self.mobile.x,self.mobile.y), BALL_RADIUS)

    def move(self, speed):
        self.mobile.move(speed)

    def control(self, game):
        self.mobile.control_ball(game)

        if self.mobile.x < 5:
            self.scored = '2'
        elif self.mobile.x > WIDTH-5:
            self.scored = '1'

