from pygame.math import Vector2


class Moveable():
    def __init__(self, init_speed: Vector2 = None, init_acceleration = None, max_speed: Vector2 = Vector2(x=2, y=5)) -> None:
        super().__init__()
        if not init_speed: 
            init_speed = Vector2(x=0, y=0)
        if not init_acceleration:
            init_acceleration = Vector2(x=0, y=0)

        self.speed = init_speed
        self.acceleration = init_acceleration
        self.max_speed = max_speed
    
    def add_speed_x(self, speed_x: float = 0):
        self.speed.x += speed_x

    def add_speed_y(self, speed_y: float = 0):
        self.speed.y += speed_y

    def set_acceleration_x(self, acceleration_x: float = 0):
        self.acceleration.x = acceleration_x

    def set_acceleration_y(self, acceleration_y: float = 0):
        self.acceleration.y = acceleration_y
    
    def update(self, time_t):
        # x = v_0 * t + 1 / 2 * a * t^2
        distance_x = (self.speed.x + 1 / 2 * self.acceleration.x * time_t) * time_t
        distance_y = (self.speed.y + 1 / 2 * self.acceleration.y * time_t) * time_t

        # v = v_0 + a * t
        self.speed.x += self.acceleration.x * time_t
        self.speed.y += self.acceleration.y * time_t

        # Clip speed to `max_speed`
        if self.speed.x > 0 and self.speed.x > self.max_speed.x:
            self.speed.x = self.max_speed.x
        if self.speed.x < 0 and self.speed.x < -self.max_speed.x:
            self.speed.x = -self.max_speed.x

        if self.speed.y > 0 and self.speed.y > self.max_speed.y:
            self.speed.y = self.max_speed.y
        if self.speed.y < 0 and self.speed.y < -self.max_speed.y:
            self.speed.y = -self.max_speed.y

        # Stop
        if self.acceleration.x == 0:
            self.speed.x /= 1.005

        return distance_x, distance_y


if __name__ == "__main__":
    ...