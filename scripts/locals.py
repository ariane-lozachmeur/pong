import pygame

pygame.font.init()

# Dimensions of the game_board
HEIGHT = 600
WIDTH = 1200

# Global speed variable. 
# To change speed of the game change SPEED.
SPEED = {'easy':7, 'medium':9, 'difficult':11}
FRAME_RATE = {'easy':60, 'medium':60, 'difficult':60}

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Dimension of the mobile objects
PADDLE_THICK = 10
PADDLE_HEIGHT = 100
BALL_RADIUS = 5

# Fonts
FONT = pygame.font.Font('font/ZillaSlab-Light.ttf',32)
TEXT_WIDTH = 50

# Rules
MAX_SCORE = 5

MENUS = {
    'start': {
        'title': None,
        'opt': ({'id':'Start game !', 'action':'START'},
                {'id':'Quit game','action':'QUIT'})
        },
    'score' : {
        'title':None,
        'opt':({'id':'New ball', 'action':'START'},
                {'id':'Quit game','action':'QUIT'})
        },
    'replay' : {
        'title':None,
        'opt':({'id':'Replay game','action': 'START'},
                {'id':'Quit game','action':'QUIT'})
        },
    'player' : {
        'title':None,
        'opt': ({'id':'1 player','action':'1player'},
                {'id': '2 player','action':'2player'})
        },
    'level' : {
        'title':'Choose difficulty',
        'opt': ({'id':'easy','action':'easy'},
                {'id':'medium','action':'medium'},
                {'id':'difficult','action':'difficult'})
        },
    'keys': {
        'title':'Choose the keys to use for:',
        'opt': ({'id':'Up key', 'action':'upkey'},
                {'id':'Down key', 'action': 'downkey'},
                {'id': 'Start game !', 'action': 'START'})
        },
    }

# CAPTIONS = {
#     'score': {
#         'captions':[
#                     'Player ' + self.ball.scored + ' scored !',
#                     'Score: ' + str(self.player1.score) + ' - '+ str(self.player2.score)
#                     ]
#             },
#     'winner': {
#         'captions': [
#                 'Player '+ str(argmax([self.player1.score, self.player2.score])+1) + ' won !',
#                 'Score: ' + str(self.player1.score) + ' - '+ str(self.player2.score)
#                 ]
#             },
#     'rules': {
#         'captions':[
#                 'Controls :',
#                 'Player 1, to go up press: '+ str(pygame.key.name(self.player1.paddle.up)),
#                 'Player 1 to go down press: '+ str(pygame.key.name(self.player1.paddle.down)),
#                 'Player 2 to go up press: '+ str(pygame.key.name(self.player2.paddle.up)),
#                 'Player 2 to go down press: '+ str(pygame.key.name(self.player2.paddle.down))
#                 ]
#             }
#         }

