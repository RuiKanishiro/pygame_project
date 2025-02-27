import os
import sys
import pygame


def load_image(name, folder: str = '', folder_extra: str = '', colorkey=None) -> pygame.Surface:
    fullname = os.path.join('data', folder, folder_extra, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
