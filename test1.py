import time

import pygame
import os
import sys
from image_downloading import load_image
from pygame.locals import *
import random

pygame.init()
width, height = 1150, 700
screen = pygame.display.set_mode((width, height))

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


pic = load_image('creature.png')
sprites = pygame.sprite.Group()
creat = pygame.sprite.Sprite(sprites)
creat.image = pic
creat.rect = creat.image.get_rect()

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            creat.rect = creat.rect.move(10, 0)
        if keys[K_LEFT]:
            creat.rect = creat.rect.move(-10, 0)
        if keys[K_DOWN]:
            creat.rect = creat.rect.move(0, 10)
        if keys[K_UP]:
            creat.rect = creat.rect.move(0, -10)
    screen.fill((255, 255, 255))
    sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
