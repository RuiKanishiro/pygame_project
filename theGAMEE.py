from library import *
from image_downloading import load_image
# from map import *
from cutting_sheets import cut_sheet
from classes import *

pygame.init()
width, height = 1120, 720
screen = pygame.display.set_mode((width, height))
cur = 'G-spawn.txt'
cur_i, cur_j = 0, 1
maps = ['G-forest.txt', 'G-spawn.txt', 'G-for.txt', 'G-for.txt']
clock = pygame.time.Clock()


Border(-1, -1, width + 1, -1, borders)
Border(-1, height - 95, width + 1, height - 95, borders)
Border(-1, -1, -1, height + 1, borders)
Border(width + 1, -1, width + 1, height + 1, borders)
pole = []
for i in range(2):
    ls = []
    for j in range(2):
        ls.append(maps[i * 2 + j])
    pole.append(ls)


def catch_bumping():
    global cur, level_x, level_y, cur_i, cur_j
    ls = list(map(int, rat.check_status().split()))
    cur_prev = cur
    if ls[0] > 0:
        if cur_j + 1 < 2:
            cur = pole[cur_i][cur_j + 1]
            cur_j = cur_j + 1
    if ls[0] < 0:
        if cur_j - 1 >= 0:
            cur = pole[cur_i][cur_j - 1]
            cur_j = cur_j - 1
    if ls[1] > 0:
        if cur_i + 1 < 2:
            cur = pole[cur_i + 1][cur_j]
            cur_i = cur_i + 1
    if ls[1] < 0:
        if cur_i - 1 >= 0:
            cur = pole[cur_i - 1][cur_j]
            cur_i = cur_i - 1
    if cur_prev != cur:
        level_x, level_y = generate_level(load_level(cur), cur)
        return True


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [" Игра про крысу:", "",
                  " Лютый бета-тест",
                  " ",
                  "не бейте палками :("]

    fon = pygame.transform.scale(load_image('fon.png', 'buttons'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    button = Button(load_image('start.png', 'buttons'), 450, 500)
    all_sprites.add(button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.on_click(*event.pos):
                    return
        pygame.display.flip()
        all_sprites.draw(screen)
        clock.tick(20)


start_screen()
for i in all_sprites:
    i.kill()


def cur_check(filename):
    if filename == 'G-spawn.txt':
        for i in range(0, width, 55):
            Decoration(tile_images['tree'], i, -55, i, -95)
        for i in range(0, width, 75):
            Decoration(tile_images['tree'], i, -45, i, -85)
        for i in range(-30, width, 75):
            Decoration(tile_images['tree'], i, -5, i, -45)
        Decoration(tile_images['tree'], 560, 30, 560, -5)
        Decoration(tile_images['light-tree'], 530, 50, 530, 15)
        Decoration(tile_images['tree'], 580, 80, 580, 55)
        Decoration(tile_images['tree'], 1060, 30, 1060, -5)
        Decoration(tile_images['tree'], 1010, 30, 1010, -5)
        Decoration(tile_images['light-tree'], 1080, 50, 1080, 15)
        Decoration(tile_images['tree'], 1030, 80, 1030, 55)
        for i in range(-60, 500, 75):
            Decoration(tile_images['light-tree'], i, 10, i, -30)
        Decoration(tile_images['tavern'], 600, -170, 600, -240)
        Decoration(tile_images['light'], 620, 200, 620, 155)
    if filename == 'G-forest.txt':
        for i in range(0, width, 55):
            Decoration(tile_images['tree'], i, -55, i, -95)
        for i in range(0, width, 75):
            Decoration(tile_images['tree'], i, -45, i, -85)
        for i in range(-30, width, 75):
            Decoration(tile_images['tree'], i, -5, i, -45)
        Decoration(tile_images['tree'], 560, 30, 560, -5)
        Decoration(tile_images['light-tree'], 530, 50, 530, 15)
        Decoration(tile_images['tree'], 580, 80, 580, 55)
        Decoration(tile_images['tree'], 1060, 30, 1060, -5)
        Decoration(tile_images['tree'], 1010, 30, 1010, -5)
        Decoration(tile_images['light-tree'], 1080, 50, 1080, 15)
        Decoration(tile_images['tree'], 1030, 80, 1030, 55)
        for i in range(-60, 500, 75):
            Decoration(tile_images['light-tree'], i, 10, i, -30)


def load_level(filename):
    filename = "data/maps-n-grass/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, filename):
    for i in cur_decor:
        i.kill()
    for i in borders_tmp:
        i.kill()
    Border(-1, -1, width + 1, -1, borders)
    Border(-1, height - 95, width + 1, height - 95, borders)
    Border(-1, -1, -1, height + 1, borders)
    Border(width + 1, -1, width + 1, height + 1, borders)
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
        cur_check(filename)
    return x, y


trees = []
cut_sheet(load_image('trees.png', 'wood'), 2, 1, trees)
tile_images = {
    'light-wood': load_image('light-wood.png', 'wood'),
    'wood': load_image('wood.png', 'wood'),
    'dark-wood': load_image('dark-wood.png', 'wood'),
    'light-tree': trees[1],
    'tree': trees[0],
    'tavern': load_image('tavern.png', 'decorations'),
    'light': load_image('light.png', 'decorations')
}
grass_plots = [load_image('grass.png', 'maps-n-grass')]
cut_sheet(load_image('corner-grass.png', 'maps-n-grass'), 3, 3, grass_plots)
cut_sheet(load_image('grass-footpath.png', 'maps-n-grass'), 3, 3, grass_plots)
tile_width = tile_height = 16
level_x, level_y = generate_level(load_level(cur), cur)

crown = Accessories(load_image("crown.png", 'accessories', 'crown-n-flower'),
                    load_image("crown-right.png", 'accessories', 'crown-n-flower'),
                    load_image("crown-left.png", 'accessories', 'crown-n-flower'),
                    9, 2, 0, 0)
bubble = Accessories(load_image("bubble-bottle.png", 'accessories', 'bubble'),
                     load_image("bubble-right.png", 'accessories', 'bubble'),
                     load_image("bubble-left.png", 'accessories', 'bubble'),
                     9, 2, 0, 0)
# blocker = Accessories(load_image("nothing.png", 'accessories'),
#                       load_image("blocker.png", 'accessories'),
#                       load_image("blocker.png", 'accessories'),
#                       9, 2, 0, 0)

rat = MainCharacter(load_image("go-right.png", 'main-rat'),
                    load_image("go-left.png", 'main-rat'),
                    load_image("stand-right.png", 'main-rat'),
                    load_image("stand-left.png", 'main-rat'),
                    load_image("go-right-down.png", 'main-rat'),
                    load_image("go-left-down.png", 'main-rat'),
                    load_image("stand-right-down.png", 'main-rat'),
                    load_image("stand-left-down.png", 'main-rat'),
                    load_image("main-rat-mask.png", 'main-rat'),
                    9, 2, width // 2, height // 2)
Button(load_image('E.png', 'buttons'), 20, 650)
Button(load_image('controling.png', 'buttons'), 220, 650)
system = SystemWindow(load_image('inventory.png', 'wood'), 300, 150)
is_running = True
accessorie = None
is_reacting = True
while is_running:
    if catch_bumping():
        tmp = accessorie
        for i in main_rat:
            main_rat.remove_internal(i)
            all_sprites.remove_internal(i)
        rat = MainCharacter(load_image("go-right.png", 'main-rat'),
                            load_image("go-left.png", 'main-rat'),
                            load_image("stand-right.png", 'main-rat'),
                            load_image("stand-left.png", 'main-rat'),
                            load_image("go-right-down.png", 'main-rat'),
                            load_image("go-left-down.png", 'main-rat'),
                            load_image("stand-right-down.png", 'main-rat'),
                            load_image("stand-left-down.png", 'main-rat'),
                            load_image("main-rat-mask.png", 'main-rat'),
                            9, 2, width // 2, height // 2)
        if rat.wearable():
            if not rat.possible:
                rat.wear(accessorie)
        Button(load_image('E.png', 'buttons'), 20, 650)
        Button(load_image('controling.png', 'buttons'), 220, 650)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rat.ears_switch()
            if event.key == pygame.K_e:
                system.event_show()
                if is_reacting:
                    is_reacting = False
                else:
                    is_reacting = True
            if event.key == pygame.K_j:
                for i in cur_decor:
                    i.kill()
        if event.type == pygame.MOUSEBUTTONUP:
            if system.is_show():
                accessorie = system.catch_click(*event.pos)
                if accessorie is not None:
                    accessorie.make_it_appropriate(rat)
                    if rat.wearable():
                        rat.wear(accessorie)
                        system = SystemWindow(load_image('inventory.png', 'wood'), 300, 150)
                        system.event_show()
                    else:
                        rat.forcing()
                        rat.wear(accessorie)
                        system = SystemWindow(load_image('inventory.png', 'wood'), 300, 150)
                        system.event_show()

    if is_reacting:
        if pygame.key.get_pressed()[K_RIGHT] and rat.get_side() == 'right':
            rat.start_go()
            rat.move_with_check(4, 0)
            if not rat.possible:
                accessorie.make_it_appropriate(rat)
        if pygame.key.get_pressed()[K_RIGHT] and rat.get_side() != 'right':
            rat.switch()
            rat.move_with_check(4, 0)
            if not rat.possible:
                accessorie.make_it_appropriate(rat)
        if pygame.key.get_pressed()[K_LEFT] and rat.get_side() == 'left':
            rat.start_go()
            rat.move_with_check(-4, 0)
            if not rat.possible:
                accessorie.make_it_appropriate(rat)
        if pygame.key.get_pressed()[K_LEFT] and rat.get_side() != 'left':
            rat.switch()
            rat.move_with_check(-4, 0)
            if not rat.possible:
                accessorie.make_it_appropriate(rat)
        if pygame.key.get_pressed()[K_UP]:
            rat.start_go()
            rat.move_with_check(0, -4)
            if not rat.possible:
                accessorie.make_it_appropriate(rat)
        if pygame.key.get_pressed()[K_DOWN]:
            rat.start_go()
            rat.move_with_check(0, 4)
            if not rat.possible:
                accessorie.make_it_appropriate(rat)
        if (not pygame.key.get_pressed()[K_RIGHT] and
            not pygame.key.get_pressed()[K_LEFT] and
            not pygame.key.get_pressed()[K_UP] and
                not pygame.key.get_pressed()[K_DOWN]):
            rat.stand()
    all_sprites.update()
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
