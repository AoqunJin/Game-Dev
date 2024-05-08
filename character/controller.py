import pygame
import numpy as np
from character import BaseCharacter, Archer, Golem


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Listener(metaclass=SingletonMeta):
    def __init__(self):
        self._events = {}

    def register(self, tag, fn, args):
        if self._events.get(tag, "") != "":
            self._events[tag]["fn"].append(fn)
            self._events[tag]["args"].append(args)
        else:
            self._events[tag] = {"down": False, "fn": [fn], "args": [args]}

    def event(self):
        for event in pygame.event.get():
            for key, val in self._events.items():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN and event.key == key: val["down"] = True
                elif event.type == pygame.KEYUP and event.key == key: val["down"] = False

    def excute_register(self):
        for val in self._events.values():
            if val["down"]: 
                for i in range(len(val["fn"])):
                    val["fn"][i](*val["args"][i])


class World():
    def __init__(self, character: BaseCharacter) -> None:
        self.listener = Listener()
        self.listener.register(pygame.K_a, character.move, ("x", -1))
        self.listener.register(pygame.K_a, character.set_state, ("Walking",))
        self.listener.register(pygame.K_d, character.move, ("x", 1))
        self.listener.register(pygame.K_d, character.set_state, ("Walking",))
        self.listener.register(pygame.K_w, character.move, ("y", -1))
        self.listener.register(pygame.K_s, character.move, ("y", 1))
        self.listener.register(pygame.K_f, character.set_state, ("Attacking",))
        self.group = pygame.sprite.Group()
        self.group.add(character)

    def run(self, screen):
        self.listener.event()
        self.listener.excute_register()
        self.group.update()
        self.group.draw(screen)
        

if __name__ == "__main__":
    
    archer = Golem(r"C:\Users\aojia\Documents\GitHub\Game-Dev\z241\2105141\2\PNG\Golem_01\PNG Sequences")
    world = World(character=archer)

    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption("测试")
    font = pygame.font.Font(None, 18)
    framerate = pygame.time.Clock()

    while True:
        
        framerate.tick(30)
        ticks = pygame.time.get_ticks()
        screen.fill((0,0,0))
        world.run(screen)
            
        
        pygame.display.update()
