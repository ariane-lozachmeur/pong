import pygame
import mobile as mb
from pygame.locals import *
import __main__ as main

BLACK = (0,0,0)
WHITE = (255,255,255)

HEIGHT = 600
WIDTH = 1200
SPEED = 2

PADDLE_THICK = 10
PADDLE_HEIGHT = 100
BALL_RADIUS = 5

class Game:

    def __init__(self, height, width):
        self.board = pygame.display.set_mode((width, height))
        self.player1 = Player(name = 'Player1', type='player1')
        self.player2 = Player(name= 'Player2', type='ia2')
        self.ball = Ball()

    def update(self):
        self.board.fill(BLACK)
        self.player1.update(self.board)
        self.player2.update(self.board)
        self.ball.update(self.board)

        for i in range(HEIGHT / 20):
            pygame.draw.rect(self.board, WHITE, (WIDTH / 2, i * 20, 5, 10))

        pygame.display.update()

    def incr_score(self, player, goal):
        if player == '1':
            self.player1.incr_score(goal)
        elif player == '2':
            self.player2.incr_score(goal)

class Player:

    def __init__(self, name, type):
        self.paddle = mb.Mobile('rect', dim = (PADDLE_THICK, PADDLE_HEIGHT), speed = SPEED)
        self.name = name
        self.score = 0
        self.type = type

        if '1' in type:
            self.paddle.set_position(50, HEIGHT/2)
        elif '2' in type:
            self.paddle.set_position(WIDTH-50,HEIGHT/2)
        else:
            raise ValueError('type of player'+name+' incorrect. It doesn\'t contain 1 or 2')

        self.paddle.set_speed(0,0)

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



class Ball:

    def __init__(self):
        self.mobile = mb.Mobile('circle', dim = (BALL_RADIUS), speed = SPEED)
        self.mobile.set_position(WIDTH/2, HEIGHT/2)
        self.mobile.set_speed(-2,1)

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

