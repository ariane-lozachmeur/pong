import pygame
import sys
from pygame.locals import *
from scripts.game import Game, Ball
from scripts.interface import Interface
from scripts.locals import *


if __name__ == '__main__':

    game_board = Game(HEIGHT, WIDTH)
    pygame.mixer.init()
    pygame.mixer.music.load('sound/got.mp3')
    pygame.mixer.music.play()
    NPLAYER = game_board.menu('player')['n']
    game_board.level = game_board.menu('level')['level']
    speed = SPEED[game_board.level]
    game_board.set_players(NPLAYER)
    game_board.show('rules')
    game_board.update()
    game_board.menu('start')

            
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        while game_board.player1.score < MAX_SCORE and game_board.player2.score < MAX_SCORE:
            game_board.play(speed)
            game_board.incr_score(game_board.ball.scored, 1)
            game_board.show('score') 
            if game_board.player1.score < MAX_SCORE and game_board.player2.score < MAX_SCORE:
                game_board.menu('score')
            else:
                game_board.show('winner')
                game_board.menu('replay')
        game_board.reset()
