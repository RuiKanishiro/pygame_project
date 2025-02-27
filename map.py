from library import *
from groups import *
from theGAMEE import trees, grass_plots, tile_images


def load_level(filename):
    filename = "data/maps-n-grass/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, filename):
    cur_plots = []
    if filename[0] == 'G':
        cur_plots = grass_plots
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Tile(cur_plots[0], x, y)
            elif level[y][x] == '1':
                Tile(cur_plots[1], x, y)
            elif level[y][x] == '2':
                Tile(cur_plots[2], x, y)
            elif level[y][x] == '3':
                Tile(cur_plots[3], x, y)
            elif level[y][x] == '4':
                Tile(cur_plots[4], x, y)
            elif level[y][x] == '5':
                Tile(cur_plots[5], x, y)
            elif level[y][x] == '6':
                Tile(cur_plots[6], x, y)
            elif level[y][x] == '7':
                Tile(cur_plots[7], x, y)
            elif level[y][x] == '8':
                Tile(cur_plots[8], x, y)
            elif level[y][x] == '9':
                Tile(cur_plots[9], x, y)
            elif level[y][x] == 'A':
                Tile(cur_plots[10], x, y)
            elif level[y][x] == 'B':
                Tile(cur_plots[11], x, y)
            elif level[y][x] == 'C':
                Tile(cur_plots[12], x, y)
            elif level[y][x] == 'D':
                Tile(cur_plots[13], x, y)
            elif level[y][x] == 'E':
                Tile(cur_plots[14], x, y)
            elif level[y][x] == 'F':
                Tile(cur_plots[15], x, y)
            elif level[y][x] == 'G':
                Tile(cur_plots[16], x, y)
            elif level[y][x] == 'H':
                Tile(cur_plots[17], x, y)
            elif level[y][x] == 'I':
                Tile(cur_plots[18], x, y)
            elif level[y][x] == 'N':
                Tile(tile_images['light-wood'], x, y)
            elif level[y][x] == 'W':
                Tile(tile_images['wood'], x, y)
            elif level[y][x] == 'O':
                Tile(tile_images['dark-wood'], x, y)
    return x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
