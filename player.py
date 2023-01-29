import pygame
import os
from pygame.locals import *

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

FPS = 60
VEL = 5    # velocity
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets/Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets/Gun+Silencer.mp3'))


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = VEL
        self.bullets = []
        self.health = 10
        self.connected = False



    def str(self):
        return "connected: " + str(self.connected)

    def getHealth(self):
        return self.health

    def gotHit(self):
        self.health -= 1

    def getConnected(self):
        return self.connected

    def isConnected(self):
        self.connected = True

    def createRedBullet(self):
        bullet = pygame.Rect(self.x, self.y + self.height // 2 - 2, 10, 5)
        self.bullets.append(bullet)
        BULLET_FIRE_SOUND.play()

    def createYellowBullet(self):
        bullet = pygame.Rect(self.x + self.width, self.y + self.height // 2 - 2, 10, 5)
        self.bullets.append(bullet)
        BULLET_FIRE_SOUND.play()

    def getBullets(self):
        return self.bullets

    def getRect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def getColor(self):
        return self.color

    def movement(self):
        keys = pygame.key.get_pressed()

        if self.color == 'red':
            if keys[pygame.K_LEFT] and self.x - VEL > BORDER.x + BORDER.width:  # LEFT
                self.x -= VEL
            if keys[pygame.K_RIGHT] and self.x + VEL + self.width < WIDTH:  # RIGHT
                self.x += VEL
            if keys[pygame.K_UP] and self.y - VEL > 0:  # UP
                self.y -= VEL
            if keys[pygame.K_DOWN] and self.y + VEL + self.height < HEIGHT - 15:  # DOWN
                self.y += VEL

        elif self.color == 'yellow':
            if keys[pygame.K_a] and self.x - VEL > 0:  # LEFT
                self.x -= VEL
            if keys[pygame.K_d] and self.x + VEL + self.width < BORDER.x:  # RIGHT
                self.x += VEL
            if keys[pygame.K_w] and self.y - VEL > 0:  # UP
                self.y -= VEL
            if keys[pygame.K_s] and self.y + VEL + self.height < HEIGHT - 15:  # DOWN
                self.y += VEL

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)