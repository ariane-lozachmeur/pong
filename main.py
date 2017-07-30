import pygame
import sys
from pygame.locals import *
import board
import mobile
import menu

HEIGHT = 600
WIDTH = 1200
SPEED = 2

BLACK = (0,0,0)
WHITE = (255,255,255)

def init():
    pygame.init()
    pygame.display.set_caption('Pong')
    game = board.Game(HEIGHT, WIDTH)
    game.update()
    return game

def draw_field():
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF, WHITE, (50, y1, 10, PADDLE_HEIGHT))
    pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH - 50, y2, 10, PADDLE_HEIGHT))
    pygame.draw.circle(DISPLAYSURF, WHITE, ball, BALL_RADIUS)
    for i in range(HEIGHT / 20):
        pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH / 2, i * 20, 5, 10))

def score(ball):
    if ball[0]<45 or ball[0]>WIDTH-45:
        DISPLAYSURF.blit(SCORE_SURFACE,SCORE_TEXT)
        scored = True

def game(game):
    clock = pygame.time.Clock()
    print('Game !')
    game.ball = board.Ball()

    while game.ball.scored is None:
        clock.tick(100)
        game.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            game.player1.control(event)

        game.player2.control(game.ball)
        game.ball.control(game)
        
        game.player1.move(SPEED)
        game.player2.move(SPEED)
        game.ball.move(SPEED)

if __name__ == '__main__':

    game_board = init()
    start = False
    start_menu = menu.Menu('start')
    while not start:
        opt = ({'id':'Start game !', 'action':'START'},
                {'id':'Quit game','action':'QUIT'})
        start_menu.set_options(*opt)
        start_menu.display(game_board.board)
        for event in pygame.event.get():
            action = start_menu.handle_event(event)
            if action == 'QUIT' or event.type == QUIT:
                pygame.quit()
                sys.exit()
            if action == 'START':
                start = True
            
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        print('Start game')
        game(game_board)

        start = False
        game_board.incr_score(game_board.ball.scored, 1)
        while not start:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    start = True

            text = FONT.render('Player' + game_board.ball.scored + ' scored !',
                True,WHITE, BLACK)
            text2 = FONT.render('Score :' + str(game_board.player1.score) +
             ' - ' + str(game_board.player2.score),
             True, WHITE, BLACK)
            game_board.board.blit(text,(WIDTH/2,HEIGHT/2))
            game_board.board.blit(text2,(WIDTH/2,HEIGHT/2+100))