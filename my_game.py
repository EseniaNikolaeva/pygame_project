import sys
import random

import pygame

from pygame import mixer

pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)

# корабль
# координаты
x = WIDTH // 2
y = HEIGHT // 2
# горизонтальная скорость
vx = 0
# цвет
rect_color = (219, 112, 147)
# размер
length = 50

# картинка
img_spaceship = pygame.image.load("spaceship.png")
img_spaceship = pygame.transform.smoothscale(img_spaceship, (65, 45))

# Метеоры
meteors_x = []
meteors_y = []
meteors_vy = []
meteors_vx = []
meteor_rad = 25
meteor_color = (200, 200, 0)
img_meteor = pygame.image.load("meteor.png")
img_meteor = pygame.transform.smoothscale(img_meteor, (50, 50))

# Пули
bullets_x = []
bullets_y = []
bullets_vy = []
bullets_vx = []
bullet_rad = 10
bullet_color = (190, 200, 200)
img_bullet_t = pygame.image.load("bullet_t.png")
img_bullet_t = pygame.transform.smoothscale(img_bullet_t, (20, 20))
img_bullet_r = pygame.image.load("bullet_r.png")
img_bullet_r = pygame.transform.smoothscale(img_bullet_r, (20, 20))
img_bullet_l = pygame.image.load("bullet_l.png")
img_bullet_l = pygame.transform.smoothscale(img_bullet_l, (20, 20))
img_bullet_d = pygame.image.load("bullet_d.png")
img_bullet_d = pygame.transform.smoothscale(img_bullet_d, (20, 20))

# звуки
piu = mixer.Sound('piu.wav')

# жизни
heart = pygame.image.load("heart.png")
img_heart = pygame.transform.smoothscale(heart, (40, 40))

# фон
kosmos = pygame.image.load("kosmos.jpg")
img_kosmos = pygame.transform.smoothscale(kosmos, (1000, 800))

#конец
boom = pygame.image.load("boom.png")
img_boom = pygame.transform.smoothscale(boom, (800, 700))

for i in range(15):
    xm = random.randint(0, WIDTH)
    ym = - 2 * meteor_rad + 1
    vy = random.randint(3, 5)
    vx = random.randint(-2, 2)

    meteors_x.append(xm)
    meteors_y.append(ym)
    meteors_vy.append(vy)
    meteors_vx.append(vx)

lives = 3
score = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if lives == -1:
        score = 0
        lives = 3
    for i in range(15):
        meteors_y[i] -= HEIGHT
    end = False

    while not end:
        score = score + 1
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_d:
                    bullets_y.append(y + length // 2)
                    bullets_x.append(x + length // 2)
                    bullets_vy.append(0)
                    bullets_vx.append(10)
                    piu.play()
                elif e.key == pygame.K_a:
                    bullets_y.append(y + length // 2)
                    bullets_x.append(x + length // 2)
                    bullets_vy.append(0)
                    bullets_vx.append(-10)
                    piu.play()
                elif e.key == pygame.K_s:
                    bullets_y.append(y + length // 2)
                    bullets_x.append(x + length // 2)
                    bullets_vy.append(10)
                    bullets_vx.append(0)
                    piu.play()
                elif e.key == pygame.K_w:
                    bullets_y.append(y + length // 2)
                    bullets_x.append(x + length // 2)
                    bullets_vy.append(-10)
                    bullets_vx.append(0)
                    piu.play()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            x = x - 3
        if pressed_keys[pygame.K_RIGHT]:
            x = x + 3
        if pressed_keys[pygame.K_UP]:
            y = y - 3
        if pressed_keys[pygame.K_DOWN]:
            y = y + 3

        if x > WIDTH:
            x = 0 - length
        if x + length < 0:
            x = WIDTH
        if y > HEIGHT - length:
            y = HEIGHT - length
        if y < 0:
            y = 0

        for i in range(len(meteors_y)):
            meteors_y[i] = meteors_y[i] + meteors_vy[i]
            meteors_x[i] = meteors_x[i] + meteors_vx[i]
            if meteors_y[i] > HEIGHT + 2 * meteor_rad:
                xm = random.randint(0, WIDTH)
                ym = - 2 * meteor_rad + 1
                vy = random.randint(3, 5)
                vx = random.randint(-2, 2)
                meteors_x[i] = xm
                meteors_y[i] = ym
                meteors_vy[i] = vy
                meteors_vx[i] = vx
            dist = ((meteors_y[i] - (y + length // 2)) ** 2 + (meteors_x[i] - (x + length // 2)) ** 2) ** 0.5
            if dist < meteor_rad + length // 2:
                pygame.time.delay(2000)
                end = True

        for i in range(len(bullets_y) - 1, -1, -1):
            bullets_y[i] = bullets_y[i] + bullets_vy[i]
            bullets_x[i] = bullets_x[i] + bullets_vx[i]
            x1 = bullets_x[i]
            y1 = bullets_y[i]
            if x1 < 0 or x1 > WIDTH or y1 > HEIGHT:
                del bullets_y[i]
                del bullets_x[i]
                del bullets_vy[i]
                del bullets_vx[i]
                continue
            for j in range(len(meteors_x)):
                x2 = meteors_x[j]
                y2 = meteors_y[j]
                dist = ((y1 - y2) ** 2 + (x1 - x2) ** 2) ** 0.5
                if dist < meteor_rad + bullet_rad:
                    score += 200
                    xm = random.randint(0, WIDTH)
                    ym = - 2 * meteor_rad + 1
                    vy = random.randint(3, 5)
                    vx = random.randint(-2, 2)
                    meteors_x[j] = xm
                    meteors_y[j] = ym
                    meteors_vy[j] = vy
                    meteors_vx[j] = vx
                    del bullets_y[i]
                    del bullets_x[i]
                    del bullets_vy[i]
                    del bullets_vx[i]
                    break

        screen.fill('#2D143E')
        screen.blit(img_kosmos, (0, 0))
        if lives == 0:
            screen.blit(img_boom, (100, 50))
            lives -= 1
            pygame.display.flip()
            pygame.time.delay(1000)
        for i in range(lives):
            screen.blit(img_heart, (850 + i * 45, 7))
        screen.blit(img_spaceship, (x, y))
        for i in range(len(meteors_y)):
            xm = meteors_x[i] - meteor_rad
            ym = meteors_y[i] - meteor_rad
            screen.blit(img_meteor, (xm, ym))

        for i in range(len(bullets_y)):
            xb = bullets_x[i] - bullet_rad
            yb = bullets_y[i] - bullet_rad
            if bullets_vx[i] == -10:
                img = img_bullet_l
            elif bullets_vx[i] == 10:
                img = img_bullet_r
            elif bullets_vy[i] == 10:
                img = img_bullet_d
            else:
                img = img_bullet_t
            screen.blit(img, (xb + 5, yb))

        my_font = pygame.font.SysFont('Arial', 50)
        t = my_font.render(str(score), True, (233, 213, 196))
        screen.blit(t, (20, 20))

        pygame.display.flip()
        pygame.time.delay(10)

        if end and lives != 0:
            lives -= 1
