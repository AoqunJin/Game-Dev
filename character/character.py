import os
import copy
from typing import Dict
import numpy as np
import pygame
from pygame.sprite import Sprite


class Moveable():
    def __init__(self, init_speed: np.ndarray = np.array([0, 0], dtype=np.float16), 
                 init_acceleration: np.ndarray = np.array([0, 1], dtype=np.float16), 
                 max_speed: np.ndarray = np.array([5, 10], dtype=np.float16)) -> None:
        super().__init__()

        self.move_idx = {"x": 0, "y": 1}
        self.move_start_speed = {"x": 5, "y": 10}
        self.move_start_acceleration = {"x": 0.5, "y": 0}
        self.stop_acceleration = copy.deepcopy(init_acceleration)  # TODO

        self.speed = init_speed
        self.acceleration = copy.deepcopy(init_acceleration)
        self.max_speed = max_speed
    
    def move(self, axis: str, sign: int = 1):
        # print(axis, sign)
        self.speed[self.move_idx[axis]] = sign * self.move_start_speed[axis]
        self.acceleration[self.move_idx[axis]] = sign * self.move_start_acceleration[axis]
        self.speed = self.speed.clip(-self.max_speed, self.max_speed)

    # def cancel_move(self, axis: str):
    #     self.acceleration[self.move_idx[axis]] = self.stop_acceleration[axis]

    def step(self, time_t):
        distance = (self.speed + 1 / 2 * self.acceleration * time_t) * time_t
        self.speed += self.acceleration * time_t

        self.speed = self.speed.clip(-self.max_speed, self.max_speed)
        if self.acceleration[0] == 0:
            self.speed[0] /= 1.1

        self.acceleration = copy.deepcopy(self.stop_acceleration)
        # print(self.speed)
        return distance


class BaseCharacter(Sprite, Moveable):
    def __init__(self) -> None:
        super().__init__()
        Moveable.__init__(self)
        # state
        self.all_states = ...
        self.default_state = ...
        self.state = ...
        self.state_idx = ...
        # draw
        self.image = ...
        self.rect = ...
        # position
        ...
        # size
        self.size = (100, 100)
        self.state_setted = True
        
    def load_image(self, dir: str):
        for action in self.all_states:
            action_dir = os.path.join(dir, action)
            images_names = os.listdir(action_dir)
            images = [
                pygame.transform.scale(
                    pygame.image.load(os.path.join(action_dir, images_name)), self.size)   
                for images_name in images_names
            ]
            
            if len(images) == 0:
                raise FileNotFoundError
            
            setattr(self, action, images)

    def set_state(self, state: str):
        self.state_setted = True
        if self.state != state:
            self.state = state
            self.state_idx = 0

    def update(self):
        # state
        self.image = getattr(self, self.state)[self.state_idx]

        self.state_idx += 1
        if self.state_idx == len(getattr(self, self.state)):
            self.state_idx = 0

        # position
        distance = self.step(1)
        # if self.rect.left < 500 or distance[0] < 0:
        self.rect.left += distance[0]
        if self.rect.top < 500 or distance[1] < 0:  
            self.rect.top += distance[1]
        
        # print(self.setted)
        if not self.state_setted:
            self.state = self.default_state
            self.state_idx = 0
        self.state_setted = False

    def set_default_state():
        raise NotImplementedError


class Archer(BaseCharacter):
    def __init__(self, dir: str) -> None:
        super().__init__()
        self.all_states = (
            "idle",  # 闲置动画
            "walk",  # 走动动画
            "shoot",  # 射击动画
            "death"  # 死亡动画
        )
        self.default_state = "idle"
        self.load_image(dir=dir)
        self.set_default_state()

    def set_default_state(self):
        self.state_idx = 0
        self.rect = getattr(self, self.default_state)[self.state_idx].get_rect()
        self.rect.left = 50
        self.rect.top = 50
        self.state = self.default_state


class Golem(BaseCharacter):
    def __init__(self, dir: str) -> None:
        super().__init__()
        self.all_states = (
            "Idle",  # 闲置动画
            "Walking",  # 走动动画
            "Attacking",  # 射击动画
            "Dying"  # 死亡动画
        )
        self.default_state = "Idle"
        self.load_image(dir=dir)
        self.set_default_state()

    def set_default_state(self):
        self.state_idx = 0
        self.rect = getattr(self, self.default_state)[self.state_idx].get_rect()
        self.rect.left = 50
        self.rect.top = 50
        self.state = self.default_state


if __name__ == "__main__":
    group = pygame.sprite.Group()
    
    archer = Archer(r"C:\Users\aojia\Documents\GitHub\Game-Dev\z241\2105141\1\PNG\Archer")
    group.add(archer)

    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption("测试")
    font = pygame.font.Font(None, 18)
    framerate = pygame.time.Clock()

    while True:
        
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            exit()
            
        screen.fill((0,0,100))

        # group.update(ticks)
        group.update()
        group.draw(screen)
        pygame.display.update()