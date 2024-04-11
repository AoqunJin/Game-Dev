import pygame, sys
from pygame import *
from base_classes.widget import *

class Controller(object):
    def __init__(self, foucsed_widget: Widget):
        self.possessed_object = None
        self.foucsed_widget = foucsed_widget
        self.last_collided_widget = None
        
    def listen(self):
        # for each frame
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse detect for widgets
            self.widget_mouse_event(pygame.mouse.get_pos())

    def widget_mouse_event(self, mouse_pos):
        collided_widget = self.foucsed_widget.detect_mouse(mouse_pos)
        if not collided_widget:
            # print("no collided widget")
            if self.last_collided_widget:
                self.last_collided_widget.when_lose_hover()
                self.last_collided_widget = None
            return

        self.last_collided_widget = collided_widget
        buttons = pygame.mouse.get_pressed()
        if buttons[0]: # left click
            self.last_collided_widget.when_left_click()
        elif buttons[2]: # right click
            self.last_collided_widget.when_right_click()
        else: # hover only
            self.last_collided_widget.when_hover()
