import pygame
import os
from network import Network

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets/Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets/Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5  # velocity
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

START_SCREEN = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'startscreen.png')), (WIDTH, HEIGHT))

WAITING = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'waiting.png')), (WIDTH, HEIGHT))

HEART = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'heart.png')), (10, 10))

#def draw_heart():


def draw_wait():
    WIN.blit(WAITING, (0, 0))
    pygame.display.update()


def draw_start():
    WIN.blit(START_SCREEN, (0, 0))
    pygame.display.update()


def start(p):
    run = True

    while run:
        draw_start()

        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            loc = [mx, my]

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(loc)
                if event.button == 1:
                    if loc[0] >= 125 and loc[0] <= 205 and loc[1] >= 280 and loc[1] <= 330:
                        return

                        # if loc[0] >= 125 and loc[0] <= 205 and loc[1] <= 280 and loc[1] >= 330: # rules

                    if loc[0] >= 125 and loc[0] <= 205 and loc[1] >= 384 and loc[1] <= 434:
                        run = False
                        pygame.quit()


def draw_window(red, yellow, red_health, yellow_health):
    #while not red.getConnected() or not yellow.getConnected():
    #    draw_wait()

    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red.getBullets():
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow.getBullets():
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

    # yellow_bullets, red_bullets, yellow = p or p2, red = p or p2
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.getRect().colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.getRect().colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():

    n = Network()

    p = n.getP()

    start(p)

    first = True

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        p2 = n.send(p)

        if not p2.getConnected():
            draw_wait()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(p.getBullets()) < MAX_BULLETS and p.getColor() == 'yellow':
                    p.createYellowBullet()

                if event.key == pygame.K_RCTRL and len(p.getBullets()) < MAX_BULLETS and p.getColor() == 'red':
                    p.createRedBullet()

            if p.getColor() == 'red':
                if event.type == RED_HIT:
                    p.gotHit()
                    BULLET_HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    p2.gotHit()
                    BULLET_HIT_SOUND.play()

            if p.getColor() == 'yellow':
                if event.type == RED_HIT:
                    p2.gotHit()
                    BULLET_HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    p.gotHit()
                    BULLET_HIT_SOUND.play()

        winner_text = ""

        if p.getColor() == 'yellow':
            if p2.getHealth() <= 0:
                winner_text = "Yellow Wins!"

            if p.getHealth() <= 0:
                winner_text = "Red Wins!"

            if winner_text != "":
                draw_winner(winner_text)  # SOMEONE WON
                break

            p.movement()

            handle_bullets(p.getBullets(), p2.getBullets(), p, p2)  # yellow_bullets, red_bullets, yellow, red
            draw_window(p2, p, p2.getHealth(), p.getHealth())

        if p.getColor() == 'red':
            if p.getHealth() <= 0:
                winner_text = "Yellow Wins!"

            if p2.getHealth() <= 0:
                winner_text = "Red Wins!"

            if winner_text != "":
                draw_winner(winner_text)  # SOMEONE WON
                break

            p.movement()

            handle_bullets(p2.getBullets(), p.getBullets(), p2, p)  # yellow_bullets, red_bullets, yellow, red
            draw_window(p, p2, p.getHealth(), p2.getHealth())


if __name__ == '__main__':
    main()
