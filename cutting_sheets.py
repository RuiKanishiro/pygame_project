from library import *


def cut_sheet(sheet, columns, rows, frame):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frame.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))