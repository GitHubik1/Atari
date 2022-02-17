import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60
# paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
# ball settings
ball_radius = 10
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), WIDTH - 700, ball_rect, ball_rect)
dx, dy = 1, -1
#
score = 0
# blocks settings
block_list = [pygame.Rect(100 * i, 50 * j, 100, 50) for i in range(12) for j in range(3, 10)]
#block_list = [pygame.Rect(10 + 120 * 2, 10 + 70 * 1, 100, 50), pygame.Rect(10 + 120 * 3, 10 + 70 * 1, 100, 50), pygame.Rect(10 + 120 * 6, 10 + 70 * 1, 100, 50), pygame.Rect(10 + 120 * 7, 10 + 70 * 1, 100, 50), pygame.Rect(10 + 120 * 1, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 2, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 3, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 4, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 6, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 7, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 5, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 8, 10 + 70 * 2, 100, 50), pygame.Rect(10 + 120 * 2, 10 + 70 * 3, 100, 50), pygame.Rect(10 + 120 * 3, 10 + 70 * 3, 100, 50), pygame.Rect(10 + 120 * 4, 10 + 70 * 3, 100, 50), pygame.Rect(10 + 120 * 5, 10 + 70 * 3, 100, 50), pygame.Rect(10 + 120 * 6, 10 + 70 * 3, 100, 50), pygame.Rect(10 + 120 * 7, 10 + 70 * 3, 100, 50), pygame.Rect(10 + 120 * 3, 10 + 70 * 4, 100, 50), pygame.Rect(10 + 120 * 4, 10 + 70 * 4, 100, 50), pygame.Rect(10 + 120 * 5, 10 + 70 * 4, 100, 50), pygame.Rect(10 + 120 * 6, 10 + 70 * 4, 100, 50), pygame.Rect(10 + 120 * 4, 10 + 70 * 5, 100, 50), pygame.Rect(10 + 120 * 5, 10 + 70 * 5, 100, 50), ]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(12) for j in range(7)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# background image
img = pygame.image.load('1.jpg').convert()


def detect_collision(dx, dy, ball, rect):
    global score
    if dx > 0:
        delta_x = ball.right - rect.left
        score += 100
    else:
        delta_x = rect.right - ball.left
        score += 100
    if dy > 0:
        delta_y = ball.bottom - rect.top
        score += 100
    else:
        delta_y = rect.bottom - ball.top
        score += 100

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
        score += 150
    elif delta_x > delta_y:
        dy = -dy
        score += 150
    elif delta_y > delta_x:
        dx = -dx
        score += 150
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    # drawing world
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # collision left right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # collision top
    if ball.centery < ball_radius:
        dy = -dy
    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
    # collision blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        # special effect
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
    # win, game over
    if ball.bottom > HEIGHT:
        print('GAME OVER!')
        exit()
    elif not len(block_list):
        print('WIN!!!')
        exit()
    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed


    # if ball.centerx > paddle.centerx:
    #     paddle.centerx += paddle_speed
    # if ball.centerx < paddle.centerx:
    #     paddle.centerx -= paddle_speed
    # if (paddle.x + paddle_w // 2) > (WIDTH - 170):
    #     paddle.x -= 15
    # if (paddle.x - paddle_w // 2) < -150:
    #     paddle.x += 15
    # update screen
    pygame.display.flip()
    clock.tick(fps)