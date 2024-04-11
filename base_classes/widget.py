import pygame
from pygame.locals import *

# base widget with the base offset
class Widget(pygame.sprite.Sprite):
    def __init__(self, parent, offset_vec: tuple, size: tuple):
        super().__init__()
        self.subs = pygame.sprite.Group()
        self.offset_vec = pygame.Vector2(offset_vec)
        self.parent = parent
        self.is_collidable = False

        self.image = pygame.image.load('buddy_pig.jfif') # default image
        self.rect = pygame.Rect(self.offset_vec, size)
        
        # get offseted coordinate if parent is not screen
        if isinstance(parent, Widget):
            self.add(parent.subs)
            self.rect = self.get_rect(self.offset_vec)

    def get_rect(self, offset_vec: pygame.Vector2):
        if isinstance(self.parent, Widget):
            return self.parent.get_rect(self.parent.offset_vec).move(offset_vec.x, offset_vec.y)
        
        return self.rect

    def update_subs(self):
        self.subs.update()
        for sub in self.subs:
            sub.update_subs()

    def draw_subs(self):
        self.subs.draw(pygame.display.get_surface())
        for sub in self.subs:
            sub.draw_subs()

    def detect_mouse(self, mouse_pos):
        collided_widget = None
        for sub in self.subs:
            # When a collision is detected in a child control
            # it is directly returned to the calling point
            collided_widget = sub.detect_mouse(mouse_pos)
            if collided_widget: return collided_widget

        if self.rect.collidepoint(mouse_pos) and self.is_collidable:
            return self
        
        return collided_widget
            
    def when_hover(self):
        pass

    def when_lose_hover(self):
        pass

    def when_left_click(self):
        pass

    def when_right_click(self):
        pass

# test only
class Panel(Widget):
    def __init__(self, parent, offset_vec: tuple, size: tuple, color: tuple):
        super().__init__(parent, offset_vec, size)
        self.image = pygame.Surface(size)
        self.image.fill(color)

# test only
class Button(Widget):
    def __init__(self, parent, offset_vec: tuple, size: tuple, button_text: str, font_size):
        super().__init__(parent, offset_vec, size)
        self.my_font = pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'], font_size)
        self.button_text = button_text

        self.image = self.my_font.render(button_text, True, (255, 255, 255))
        self.rect.size = size
        
        self.is_collidable = True

    def when_hover(self):
        self.image = self.my_font.render('click me!', True, (255, 255, 255))

    def when_lose_hover(self):
        self.image = self.my_font.render(self.button_text, True, (255, 255, 255))

    def when_left_click(self):
        self.image = self.my_font.render('I was left clicked', True, (255, 255, 255))

    def when_right_click(self):
        self.image = self.my_font.render('I was right clicked', True, (255, 255, 255))

