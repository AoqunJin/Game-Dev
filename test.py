import pygame

from controller import Moveable, Vector2

# 初始化Pygame
pygame.init()

# 设置窗口尺寸
window_width = 1200
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# 设置窗口标题
pygame.display.set_caption("移动方块")

# 设置方块初始位置和速度
block_x = window_width // 2
block_y = window_height // 2
block_width = 50
block_height = 50
block_speed_x = 0
block_speed_y = 0

moveable = Moveable(init_speed=Vector2(block_speed_x, block_speed_y))
moveable.set_acceleration_y(0.5)
# 游戏循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 处理键盘事件
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveable.set_acceleration_x(-0.2)
                moveable.add_speed_x(-0.2)

            elif event.key == pygame.K_RIGHT:
                moveable.set_acceleration_x(0.2)
                moveable.add_speed_x(0.2)
  
            elif event.key == pygame.K_UP:
                moveable.set_acceleration_y(-0.2)
                moveable.add_speed_y(-1)

            elif event.key == pygame.K_DOWN:
                moveable.set_acceleration_y(0.2)
                moveable.add_speed_y(0.2)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                moveable.set_acceleration_x(0)

            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                moveable.set_acceleration_y(0.5)


    # 移动方块
    x, y = moveable.update(0.1)
    block_x += x
    block_y += y

    # 边界检测
    if block_x < 0:
        block_x = 0
    elif block_x > window_width - block_width:
        block_x = window_width - block_width
    if block_y < 0:
        block_y = 0
    elif block_y > window_height - block_height:
        block_y = window_height - block_height

    # 清空窗口
    window.fill((255, 255, 255))

    # 绘制方块
    pygame.draw.rect(window, (0, 0, 0), (block_x, block_y, block_width, block_height))

    # 更新窗口
    pygame.display.update()

# 退出Pygame
pygame.quit()