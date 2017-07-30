import pygame
from pygame.locals import *


pygame.font.init()
FONT = pygame.font.Font('font/ZillaSlab-Light.ttf',32)

HEIGHT = 600
WIDTH = 1200

BLACK = (0,0,0)
WHITE = (255,255,255)

def start_menu(board, event):
    display_text(board, 'Start game !', ((WIDTH/2),(HEIGHT/2)-50),highlight=True)
    display_text(board, 'Quit', ((WIDTH/2),(HEIGHT/2)+50), highlight=False)

class Option:
    def __init__(self, **kargs):
        self.id = kargs['id']
        self.text = kargs['id']
        self.action = kargs['action']

    def display(self, position, state, board):
        if state:
            surf = FONT.render(str(self.text), True, BLACK, WHITE)
        else:
            surf = FONT.render(str(self.text), True, WHITE, BLACK)
        rect = surf.get_rect()
        rect.center = position
        board.blit(surf, rect)
        pygame.display.update()

class Menu:

    global TEXT_WIDTH 
    TEXT_WIDTH = 100

    def __init__(self, name):
        self.id = name
        self.options = []
        self.cursor = 0

    def set_options(self, *args):
        self.options = [Option(**args[0])]
        for text in args[1:]:
            self.options.append(Option(**text))

    def display(self, board):
        n_opt = len(self.options)
        # h is the space between the upper side of the board and the first option of the menu.
        h = (HEIGHT - (n_opt*TEXT_WIDTH))/2
        for i in range(n_opt):
            state = (i == self.cursor % n_opt)
            self.options[i].display(((WIDTH/2),(h+i*TEXT_WIDTH)), state, board)
        pygame.display.update()

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.cursor  += -1
            elif event.key == K_DOWN:
                self.cursor += 1
            elif event.key == K_RETURN:
                return self.options[self.cursor % len(self.options)].action

