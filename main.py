import pygame, sys
from pygame.locals import *
from settings import *
from base_classes.widget import *
from base_classes.controller import *

def test():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    base_panel = Widget(screen, (0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    base_controller = Controller(base_panel)

    menu_panel = Panel(base_panel, (SCREEN_WIDTH / 2 - 60, SCREEN_HEIGHT / 2 - 60), (120, 120), (0, 0, 0))
    button_start = Button(menu_panel, (20, 20), (80, 20), 'game start', 18)
    button_setting = Button(menu_panel, (20, 50), (80, 20), 'settings', 18)


    def draw_rect(rect: pygame.Rect, color: str):
        pygame.draw.rect(screen, color, rect)

    while True:
        screen.fill((255, 255, 255))

        base_controller.listen()
        base_panel.draw_subs()
        

        pygame.display.update()

if __name__ == '__main__':
    test()