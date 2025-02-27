import pygame.sprite

from library import *
from groups import *


tile_width, tile_height = 16, 16


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = image
        self.x, self.y = pos_x, pos_y
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def on_click(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, cur_decor)
        self.image = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Item(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, window, parent):
        super().__init__(items)
        self.image = image
        self.window = window
        self.x, self.y = pos_x, pos_y
        self.width, self.height = 70, 70
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.parent = parent

    def on_click(self, x, y):
        if self.is_clickable():
            if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
                return self.parent

    def is_clickable(self):
        if self.window.is_show():
            return True
        return False


class SystemWindow(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.x, self.y = pos_x, pos_y
        system.add(self)
        self.showable = False

    def event_show(self):
        if not self.showable:
            self.showable = True
            all_sprites.add(self)
            j = 0
            for i in accessories:
                Item(i.get_main(), self.x + 20 + 70 * (j % 5), self.y + 20 + 70 * (j // 4), self, i)
                j += 1
            all_sprites.add(items)
        else:
            self.showable = False
            all_sprites.remove(items)
            all_sprites.remove(system)

    def is_show(self):
        return self.showable

    def catch_click(self, x, y):
        for i in items:
            j = i.on_click(x, y)
            if j is not None:
                return j


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, group):
        super().__init__()
        group.add(self)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, imagin_x, imagin_y):
        super().__init__(cur_decor)
        width, height = tile_type.get_width(), tile_type.get_height()
        Border(imagin_x + 15, imagin_y + height, imagin_x + width - 15, imagin_y + height, borders_tmp)
        Border(imagin_x + 15, imagin_y, imagin_x + 15, imagin_y + height, borders_tmp)
        Border(imagin_x + 15, pos_y, imagin_x + width - 15, pos_y, borders_tmp)
        Border(imagin_x + width - 15, imagin_y, imagin_x + width - 15, imagin_y + height, borders_tmp)
        all_sprites.add(self)
        self.image = tile_type

        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, sheet_right, sheet_left, sheet_stand_r, sheet_stand_l,
                 sheet_right_down, sheet_left_down, sheet_stand_r_down, sheet_stand_l_down, mask, columns, rows, x, y):
        super().__init__(all_sprites, main_rat)
        self.frames_right = []
        self.frames_left = []
        self.frames_stand_r = []
        self.frames_stand_l = []
        self.frames_right_down = []
        self.frames_left_down = []
        self.frames_stand_r_down = []
        self.frames_stand_l_down = []
        self.cur_frames = []
        self.cut_sheet(sheet_right, columns, rows, self.frames_right)
        self.cut_sheet(sheet_left, columns, rows, self.frames_left)
        self.cut_sheet(sheet_stand_r, columns, rows, self.frames_stand_r)
        self.cut_sheet(sheet_stand_l, columns, rows, self.frames_stand_l)
        self.cut_sheet(sheet_right_down, columns, rows, self.frames_right_down)
        self.cut_sheet(sheet_left_down, columns, rows, self.frames_left_down)
        self.cut_sheet(sheet_stand_r_down, columns, rows, self.frames_stand_r_down)
        self.cut_sheet(sheet_stand_l_down, columns, rows, self.frames_stand_l_down)
        self.cur_frame = 0
        self.cur_frames = self.frames_stand_r
        self.image = self.cur_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.side = 'right'
        self.ears = 'up'
        self.possible = True
        self.mask = pygame.mask.from_surface(mask)
        self.status_x = 0
        self.status_y = 0

    def get_side(self):
        return self.side

    def cut_sheet(self, sheet, columns, rows, frame):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move_with_check(self, delta_x: int, delta_y: int):
        self.rect = self.rect.move(delta_x, delta_y)
        if (pygame.sprite.spritecollideany(self, horizontal_borders) and not
                pygame.sprite.spritecollideany(self, borders_tmp)):
            if delta_y > 0:
                self.status_y = 1
            else:
                self.status_y = -1
            self.rect = self.rect.move(0, -delta_y)
        elif (pygame.sprite.spritecollideany(self, horizontal_borders) and
                pygame.sprite.spritecollideany(self, borders_tmp)):
            self.rect = self.rect.move(0, -delta_y)
        if (pygame.sprite.spritecollideany(self, vertical_borders) and not
                pygame.sprite.spritecollideany(self, borders_tmp)):
            if delta_x > 0:
                self.status_x = 1
            else:
                self.status_x = -1
            self.rect = self.rect.move(-delta_x, 0)
        elif (pygame.sprite.spritecollideany(self, vertical_borders) and
              pygame.sprite.spritecollideany(self, borders_tmp)):
            self.rect = self.rect.move(-delta_x, 0)
        if pygame.sprite.spritecollideany(self, blocks):
            self.rect = self.rect.move(0, -delta_y)
        if pygame.sprite.spritecollideany(self, blocks):
            self.rect = self.rect.move(-delta_x, 0)

    def check_status(self):
        return f'{self.status_x} {self.status_y}'

    def ears_switch(self):
        if self.possible:
            if self.ears == 'up':
                if self.cur_frames == self.frames_stand_r:
                    self.cur_frames = self.frames_stand_r_down
                if self.cur_frames == self.frames_stand_l:
                    self.cur_frames = self.frames_stand_l_down
                if self.cur_frames == self.frames_right:
                    self.cur_frames = self.frames_right_down
                if self.cur_frames == self.frames_left:
                    self.cur_frames = self.frames_left_down
                self.ears = 'down'
            else:
                if self.cur_frames == self.frames_stand_r_down:
                    self.cur_frames = self.frames_stand_r
                if self.cur_frames == self.frames_stand_l_down:
                    self.cur_frames = self.frames_stand_l
                if self.cur_frames == self.frames_right_down:
                    self.cur_frames = self.frames_right
                if self.cur_frames == self.frames_left_down:
                    self.cur_frames = self.frames_left
                self.ears = 'up'

    def check_to_wear(self):
        if self.cur_frames == self.frames_stand_r:
            self.cur_frames = self.frames_stand_r_down
        if self.cur_frames == self.frames_stand_l:
            self.cur_frames = self.frames_stand_l_down
        if self.cur_frames == self.frames_right:
            self.cur_frames = self.frames_right_down
        if self.cur_frames == self.frames_left:
            self.cur_frames = self.frames_left_down
        self.ears = 'down'

    def stand(self):
        if self.side == 'right':
            if self.ears == 'up':
                self.cur_frames = self.frames_stand_r
            else:
                self.cur_frames = self.frames_stand_r_down
        else:
            if self.ears == 'up':
                self.cur_frames = self.frames_stand_l
            else:
                self.cur_frames = self.frames_stand_l_down

    def start_go(self):
        if self.side == 'right':
            if self.ears == 'up':
                self.cur_frames = self.frames_right
            else:
                self.cur_frames = self.frames_right_down
        else:
            if self.ears == 'up':
                self.cur_frames = self.frames_left
            else:
                self.cur_frames = self.frames_left_down

    def switch(self):
        if self.side == 'right':
            self.side = 'left'
            if self.ears == 'up':
                self.cur_frames = self.frames_left
            else:
                self.cur_frames = self.frames_left_down
        else:
            self.side = 'right'
            if self.ears == 'up':
                self.cur_frames = self.frames_right
            else:
                self.cur_frames = self.frames_right_down

    def get_cur(self):
        return self.cur_frame

    def get_sheet(self):
        return self.side

    def wearable(self):
        return self.possible

    def forcing(self):
        self.possible = True
        for i in main_rat:
            i.remove()
            all_sprites.remove(i)
        main_rat.add(self)
        all_sprites.add(self)

    def wear(self, accessor):
        if self.possible:
            self.check_to_wear()
            self.possible = False
            main_rat.add(accessor)
            self.add_to_group(accessor)
        else:
            self.possible = True
            self.ears_switch()
            main_rat.remove_internal(accessor)
            self.remove_from_group(accessor)

    def add_to_group(self, accessor):
        all_sprites.add(accessor)

    def remove_from_group(self, accessor):
        all_sprites.remove_internal(accessor)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.cur_frames)
        self.image = self.cur_frames[self.cur_frame]


class Accessories(pygame.sprite.Sprite):
    def __init__(self, main, sheet_right, sheet_left, columns, rows, x, y):
        super().__init__(accessories)
        self.frames_right = []
        self.frames_left = []
        self.cur_frames = []
        self.main = main
        self.cut_sheet(sheet_right, columns, rows, self.frames_right)
        self.cut_sheet(sheet_left, columns, rows, self.frames_left)
        self.cur_frame = 0
        self.cur_frames = self.frames_right
        self.image = self.cur_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.side = 'right'

    def get_main(self):
        return self.main

    def make_it_appropriate(self, match: MainCharacter):
        cur = match.get_cur()
        side = match.get_side()
        self.cur_frame = cur
        if side == 'right':
            self.cur_frames = self.frames_right
        else:
            self.cur_frames = self.frames_left
        self.rect.x, self.rect.y = match.rect.x, match.rect.y

    def get_side(self):
        return self.side

    def cut_sheet(self, sheet, columns, rows, frame):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move_with_check(self, delta_x: int, delta_y: int):
        self.rect = self.rect.move(delta_x, delta_y)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, -delta_y)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(-delta_x, 0)

    def switch(self):
        if self.side == 'right':
            self.side = 'left'
            self.cur_frames = self.frames_left
        else:
            self.side = 'right'
            self.cur_frames = self.frames_right

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.cur_frames)
        self.image = self.cur_frames[self.cur_frame]
