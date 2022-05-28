import math
import pygame
import sys
import settings
import player
import pickle

# --TODO--
# tiled (don't have to use this)
# Update save system with pickle
# draw layer system
# Platforms, moving and not
# Triggers

# --Done!--
# make sprites, tiles are 20x20(actualy 32x32)
# rename to "I Wanna Steal The Intellectual Property!" (IWSTIP)

# settings
screen_width = settings.width
screen_height = settings.height

# pygame setup
pygame.init()

pygame.mixer.music.load(settings.sounds["Moonsong"])
pygame.mixer.music.set_volume(0.5)

pygame.mixer.init()
death_sound = pygame.mixer.Sound(settings.sounds["death"])
death_sound.set_volume(0.1)

pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

pygame.display.set_caption("I Wanna Steal The Intellectual Property!")
clock = pygame.time.Clock()
FPS = pygame.time.Clock()
is_running = True

font = pygame.font.SysFont('arial', 15)

loaded_images = {}
for image in settings.tile_set2:
    loaded_images[image] = pygame.image.load(settings.tile_set2[image]).convert_alpha()

# Set the game mode here!
# 0 is debug,
# 1 is create
# 2 is play
# 3 is build
game_mode = settings.game_mode


# functions
def cap(value, joe, the_cap):
    if value > the_cap:
        pass
        if True:
            return the_cap
    elif value < joe:
        return joe
        # joe mama
    return value


def round_down(rounf_put, val):
    output = int(rounf_put - rounf_put % val)
    return output


def round_to(rounf_put, val):
    rounf_put /= val
    output = (round(rounf_put)) * val
    return output


def load_data(lines):
    data_list = []
    if game_mode == 3:
        data_file = open(settings.game_path + r"/all_saves.txt", "r")

    else:
        data_file = open("all_saves.txt", "r")
    line = int(lines)
    if line < 1:
        line = 1

    for i in range(line):
        data_list = data_file.readline()
    data_file.close()
    tiles = pygame.sprite.Group()
    killers = pygame.sprite.Group()

    concat = ""
    index = 0
    temp = []
    comment = True
    loaded_list = []
    for letter in str(data_list):
        if not comment:
            if letter.isdigit() or letter == "-":
                concat += letter
            elif letter == ",":
                if concat:
                    temp.append(int(concat))
                concat = ""
            elif letter == ";":
                temp.append(int(concat))
                concat = ""
                loaded_list.append(temp)
                index += 1
                id = temp[0]

                if id == 0:
                    tiles.add(Block((temp[-2], temp[-1])))
                elif id >= 1:
                    killers.add(Killer((temp[-3], temp[-2]), start_angle=temp[-1], tile_id=id))

                temp = []

            elif letter == "]":
                index += 1
            else:
                concat = ""
        elif letter == "#":
            comment = False

    return tiles, killers


# garbage, just for converting old format level data
def old_loader():
    data_list = []
    data_file = open(r"C:\Users\687338\PycharmProjects\IWBTripoff\code\all_saves.txt", "r")
    line = 0
    if line < 1:
        line = 1

    for i in range(line):
        data_list = data_file.readline()
    data_file.close()
    tiles = pygame.sprite.Group()
    killers = pygame.sprite.Group()

    concat = ""
    index = 0
    temp = []
    for letter in data_list:
        if letter.isdigit():
            concat += letter
        elif letter == ",":
            if concat:
                temp.append(int(concat))
            concat = ""
        elif letter == ")":
            temp.append(int(concat))
            concat = ""

            if index == 0:
                tiles.add(Block((temp[-2], temp[-1])))
            elif index == 1:
                killers.add(Killer((temp[-3], temp[-2]), start_angle=temp[-1]))
            temp.clear()
        elif letter == "]":
            index += 1
        else:
            concat = ""

    return tiles, killers


def distance(pos1, pos2):
    dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    return dist


def draw_offset(sprites, offset):
    for sprite in sprites:
        sprite.rect.center += offset
    sprites.draw(screen)
    for sprite in sprites:
        sprite.rect.center -= offset

    # if sprite.rect.right+offset.x > 0 or sprite.rect.left+offset.x < screen_width or sprite.rect.top+offset.y < screen_width or sprite.rect.bottom+offset.y > 0:

def load_spritesheet(image, scale=1):
    tile_size = 8
    loaded_image = pygame.image.load(image).convert_alpha()

    images = []
    x = 0
    for column in range(loaded_image.get_width()//tile_size):
        x += 1
        y = 0
        for row in range(loaded_image.get_height()//tile_size):
            y += 1
            images.append(pygame.transform.scale(loaded_image, (loaded_image.get_width() * scale, loaded_image.get_height() * scale)).subsurface((((x-1) * tile_size*scale, (y-1)*tile_size*scale), (tile_size*scale, tile_size*scale))))
    return images

# Classes
class World:
    def __init__(self):
        # self.tiles = [, Block((200, 200), (50, 100)), Block((300, 100), (50, 100))]
        self.startpos = (40, 250)
        self.camera_offset = pygame.math.Vector2(0, 0)
        self.bg_offset = 0

        self.images = loaded_images
        self.tile_sprites = pygame.sprite.Group()
        self.tile_sprites.add(Block((32, 288)))
        self.bg_visuals = pygame.sprite.Group()
        self.visuals = pygame.sprite.Group()
        self.death_screen = pygame.sprite.GroupSingle()
        self.bg_visuals.add(BasicSprite((710, 95), self.images["troll"], size=0.45))
        self.death_screen.add(BasicSprite((100, 200), self.images["death_screen"]))

        self.player = player.Player(self.startpos)
        self.save_facing = self.player.direction
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player)
        self.mouse = MouseSystem()

        self.death_cd = False

        self.scroll_index = 0
        self.preview_sprite = pygame.sprite.GroupSingle()
        self.preview_sprite.add(BasicSprite((0, 0), self.images[0]))
        self.placing = 1
        self.snap = 32
        self.lines = False
        self.snap_toggle = 0
        self.place_angle = 0
        self.room_togle = 1
        self.place_offset = (-self.snap / 2, -self.snap / 2)
        self.create_hold_list = []
        self.undo_list = []
        if game_mode >= 2:
            self.load_data(0)

        # for swag in self.__dir__():
        #     if (type(self.__getattribute__(swag))) == (int or str or bool or float or tuple or dict or list):
        #         print(self.__getattribute__(swag))

    @staticmethod
    def delete(pos, tolerance=0):
        for sprite in level["tiles"]:
            if distance(sprite.rect.topleft, pos) <= tolerance:
                level["tiles"].remove(sprite)

        for sprite in level["killers"]:
            if distance(sprite.rect.topleft, pos) <= tolerance:
                level["killers"].remove(sprite)
        for sprite in level["waters"]:
            if distance(sprite.rect.topleft, pos) <= tolerance:
                level["waters"].remove(sprite)

    def undo(self):
        for position in self.undo_list[0]:
            self.delete(position)
        self.undo_list.pop(0)


    def draw(self):
        # BAD FIX LATER
        for bg_index in range(len(backgrouds)):
            self.looping_image(backgrouds[len(backgrouds) - 1 - bg_index], bg_speeds[bg_index])

        self.bg_offset -= 10

        self.bg_visuals.draw(screen)

        draw_offset(self.visuals, self.camera_offset)

        draw_offset(self.player_sprite, self.camera_offset)

        for group in level:
            draw_offset(level[group], self.camera_offset)


        if game_mode < 2:
            self.preview_sprite.draw(screen)
            if self.lines:
                line_distane = self.snap
                for i in range(int(screen_width / line_distane) + 1):
                    # print(self.camera_offset.x % line_distane + i * line_distane)

                    color = "White"
                    width = 1
                    if (
                            self.camera_offset.x % line_distane + i * line_distane) - self.camera_offset.x % screen_width == 0:
                        width = 3
                    pygame.draw.line(screen, color, (self.camera_offset.x % line_distane + i * line_distane, 0),
                                     (self.camera_offset.x % line_distane + i * line_distane, screen_height),
                                     width=width)
                for i in range(int(screen_height / line_distane) + 1):
                    color = "White"
                    width = 1
                    if (
                            self.camera_offset.y % line_distane + i * line_distane) - self.camera_offset.y % screen_height == 0:
                        width = 3
                    pygame.draw.line(screen, color, (0, self.camera_offset.y % line_distane + i * line_distane),
                                     (screen_width, self.camera_offset.y % line_distane + i * line_distane),
                                     width=width)
        if self.death_cd:
            self.death_screen.draw(screen)

    def run(self):
        key_sys.update()

        # does collision
        if game_mode >= 2:
            self.scroll()

        if self.player.dead and not self.death_cd:
            self.player.kill()
            death_sound.play()
            self.death_cd = True
        else:
            self.player.update()

        if game_mode == 1:
            self.create()
            self.mouse.update()
        if key_sys.individual_frame_down[pygame.K_r]:
            self.reset()
        if key_sys.individual_frame_down[pygame.K_s] and game_mode < 2:
            self.save()

    def scroll(self):
        player_pos = self.player.hitbox.center
        screen_size = (settings.width, settings.height)
        self.camera_offset = pygame.math.Vector2(-round_down(player_pos[0], screen_size[0]),
                                                 -round_down(player_pos[1], screen_size[1]))

    def looping_image(self, image, speed):
        bg_size = image.get_size()
        for i in range(int(screen_width / bg_size[0]) + 2):
            for v in range(int(screen_height / bg_size[1]) + 2):
                screen.blit(image,
                            (((self.camera_offset.x + self.bg_offset) * speed % bg_size[0]) + (i - 1) * bg_size[0],
                             0 + (v - 1) * bg_size[1]))

    def save(self):
        self.player.save_position = self.player.hitbox.topleft
        self.save_facing = self.player.direction

    def reset(self):
        # self.player.position = self.startpos
        self.player = player.Player(self.player.save_position)
        self.player.direction = self.save_facing
        self.player_sprite.add(self.player)
        self.scroll()
        self.death_cd = False

    def create(self):
        keys = key_sys
        pos = self.mouse.current_pos - self.camera_offset
        self.snap_pos = (pos[0] // self.snap * self.snap, pos[1] // self.snap * self.snap)
        # self.scroll_index = self.scroll_index % len(tiles_test)
        # self.preview_sprite.sprite.image = tiles_test[self.scroll_index]

        preview_pos = self.snap_pos + self.camera_offset
        self.preview_sprite.sprite.rect.topleft = preview_pos

        if self.mouse.current_frame_down:
            if not self.snap_pos in self.create_hold_list:
                self.create_hold_list.append(self.snap_pos)
                if self.placing == 1:
                    level["tiles"].add(Block(self.snap_pos))
                elif self.placing == 2:
                    level["killers"].add(Killer(self.snap_pos, start_angle=self.place_angle))
                elif self.placing == 3:
                    level["killers"].add(Killer(self.snap_pos, start_angle=self.place_angle, tile_id=2))
                elif self.placing == 4:
                    level["waters"].add(Water(self.snap_pos))
        elif self.create_hold_list:
            self.undo_list.append(self.create_hold_list)
            self.create_hold_list = []

        if keys.individual_frame_down[pygame.K_PERIOD]:
            self.undo()

        if keys.individual_frame_down[pygame.K_s]:
            self.save()

        # old cam controls
        if game_mode == 1:
            cam_speed = 20
            fast = True
            if keys.current_frame_down[pygame.K_LEFTBRACKET]:
                if not self.cam_cd or fast:
                    self.camera_offset.x += cam_speed  # settings.width
                self.cam_cd = True
            elif keys.current_frame_down[pygame.K_BACKSLASH]:
                if not self.cam_cd or fast:
                    self.camera_offset.x -= cam_speed  # settings.width
                self.cam_cd = True
            elif keys.current_frame_down[pygame.K_RIGHTBRACKET]:
                if not self.cam_cd or fast:
                    self.camera_offset.y -= cam_speed  # settings.height
                self.cam_cd = True
            elif keys.current_frame_down[pygame.K_EQUALS]:
                if not self.cam_cd or fast:
                    self.camera_offset.y += cam_speed  # settings.height
                self.cam_cd = True
            else:
                self.cam_cd = False

        # line toggle
        if keys.individual_frame_down[pygame.K_SEMICOLON]:
            self.lines = not self.lines

        # looping image
        # for i in range(int(screen_width / bg_size[0])+2):
        #     for v in range(int(screen_height / bg_size[1])+2):
        #         screen.blit(bg, (self.camera_offset.x % bg_size[0] + (i-1) * bg_size[0],
        #                          self.camera_offset.y % bg_size[1] + (v-1) * bg_size[1]))

        if keys.individual_frame_down[pygame.K_w]:
            if self.player.dead:
                self.player.save_position = pos
            self.player.position = (pos)

        if keys.individual_frame_down[pygame.K_TAB]:
            self.snap_toggle += 1
            self.snap_toggle = self.snap_toggle % 3
            if self.snap_toggle == 0:
                self.snap = 32
            elif self.snap_toggle == 1:
                self.snap = 16
            elif self.snap_toggle == 2:
                self.snap = 4
                return
            else:
                self.snap = 32
                return

        if keys.individual_frame_down[pygame.K_t]:
            self.place_angle += 90
            if self.placing == 2:
                self.preview_sprite.add(
                    BasicSprite(preview_pos, self.images[1], start_angle=self.place_angle))
            elif self.placing == 3:
                self.preview_sprite.add(
                    BasicSprite(preview_pos, self.images[2], start_angle=self.place_angle))

        if keys.current_frame_down[pygame.K_1]:
            self.placing = 1
            self.place_offset = (-16, 16)
            self.preview_sprite.add(BasicSprite(preview_pos, self.images[0]))
        elif keys.current_frame_down[pygame.K_2]:
            self.place_angle = 0
            self.placing = 2
            self.place_offset = (-16, 16)
            self.preview_sprite.add(BasicSprite(preview_pos, self.images[1], start_angle=self.place_angle))
        elif keys.current_frame_down[pygame.K_3]:
            self.place_angle = 0
            self.placing = 3
            self.place_offset = (-8, -8)
            self.preview_sprite.add(BasicSprite(preview_pos, self.images[2], start_angle=self.place_angle))
        elif keys.current_frame_down[pygame.K_4]:
            self.placing = 4
            self.place_offset = (-16, -16)
            self.preview_sprite.add(BasicSprite(preview_pos, self.images[3]))

        if keys.current_frame_down[pygame.K_BACKSPACE]:
            self.delete(self.snap_pos, tolerance=10)

        if keys.individual_frame_down[pygame.K_DELETE]:
            level["killers"].empty()
            level["tiles"].empty()
            level["tiles"].add(Block((32, 288)))
            self.player.position = self.startpos
            self.save()
            self.reset()

        if keys.individual_frame_down[pygame.K_k]:
            # if not self.save_cd:
            self.save_data()
            self.save_cd = True
        # else:
        #     self.save_cd = False

        if keys.individual_frame_down[pygame.K_l]:
            # if not self.load_cd:
            self.load_data(0)

        # self.load_cd = True

        # else:
        #     self.load_cd = False

    def save_data(self):
        # pickle_out = open(f'level{0}_data', 'wb')
        # pickle.dump(level, pickle_out)
        # pickle_out.close()

        data_string = ""

        for sprite in level["tiles"].sprites():
            data_string += f"{sprite.tile_id},{sprite.rect.topleft[0]},{sprite.rect.topleft[1]};"

        for sprite in level["killers"].sprites():
            data_string += f"{sprite.tile_id},{sprite.rect.topleft[0]},{sprite.rect.topleft[1]},{sprite.angle};"

        data_file = open("data.txt", "w")
        data_file.write(data_string)
        data_file.close()

    def load_data(self, data):
        loaded_objects = load_data(data)
        # loaded_objects = old_loader()
        level["tiles"] = loaded_objects[0]
        level["killers"] = loaded_objects[1]
        self.reset()


class MouseSystem:
    def __init__(self):
        self.og_pos = pygame.Vector2(0, 0)
        self.previous_frame_down = False
        self.current_frame_down = False
        self.individual_frame_down = False
        self.current_pos = self.og_pos

    def update(self):
        ms = pygame.mouse


        self.current_frame_down = True if ms.get_pressed()[0] else False
        self.individual_frame_down = False
        if self.current_frame_down and not self.previous_frame_down:
            self.og_pos = pygame.mouse.get_pos()
            self.individual_frame_down = True
        elif self.current_frame_down:
            pass
        self.previous_frame_down = self.current_frame_down
        self.current_pos = ms.get_pos()


class KeySystem:
    def __init__(self):
        self.previous_frame_down = [None] * 512
        self.current_frame_down = [None] * 512
        self.individual_frame_down = [None] * 512

    def update(self):
        keys = pygame.key.get_pressed()
        for key in range(512):
            self.current_frame_down[key] = True if keys[key] else False
            self.individual_frame_down[key] = False
            if self.current_frame_down[key] and not self.previous_frame_down[key]:
                self.individual_frame_down[key] = True
            elif self.current_frame_down[key]:
                pass
            self.previous_frame_down[key] = self.current_frame_down[key]


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, start_angle=0, size=1):
        super().__init__()
        self.image_data = image
        self.original_image = (self.image_data)
        self.image = (self.image_data)

        self.rect = self.image.get_rect(topleft=pos)
        self.angle = start_angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * size, self.image.get_height() * size))


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, image=loaded_images[0]):
        super().__init__()
        self.image_data = image
        self.image = (self.image_data)
        self.init_pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.tile_id = 0

    def draw(self):
        pygame.draw.rect(screen, "Black", self.rect)


class Killer(pygame.sprite.Sprite):
    def __init__(self, pos, tile_id=1, start_angle=0):
        super().__init__()
        self.image_data = loaded_images[tile_id]
        self.original_image = (self.image_data)
        self.image = (self.image_data)
        self.tile_id = tile_id

        self.init_pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.sprite = pygame.sprite.GroupSingle()
        self.sprite.add(self)
        self.angle = start_angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)


class Save(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image1 = (loaded_images["Save0"])
        self.image2 = (loaded_images["Save1"])
        self.image = self.image1
        self.init_pos = pos
        self.rect = self.image.get_rect(topleft=pos)

    def update_image(self, active):
        if active:
            self.image = self.image2
        else:
            self.image = self.image1


class Water(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 32)).convert_alpha()
        self.image.fill((109, 109, 248, 127.5))
        self.rect = pygame.Rect(pos, (32, 32))
        self.init_pos = pos
        self.rect = pygame.Rect(pos, (32, 32))

    def draw(self):
        pygame.draw.rect(screen, "Black", self.rect)


# stuff
level = {
    "tiles": pygame.sprite.Group(
        Block((32, 288)),
    ),
    "killers": pygame.sprite.Group(

    ),
    "saves": pygame.sprite.Group(
        Save((640, 256)),
        Save((784, 192)),
        Save((1392, 480)),
        Save((1616, 512)),
        Save((1472, -144)),
        Save((3104, -224)),

    ),
    "visuals": pygame.sprite.Group(
        (BasicSprite((10, 950), loaded_images["bag"])),
        (BasicSprite((2094, 625), loaded_images["burto"], size=1))
    ),
    "waters": pygame.sprite.Group(
        # Water((100,100)),
        # Water((100, 132)),
        # Water((100, 164)),
        # Water((100, 196)),

    )

}

pygame.mixer.music.play(-1)

bg_scale = 2.8
backgrouds = []
bg_speeds = [0, 0.1, 0.3, 0.5, 1]
for i in range(5):
    bg = (loaded_images["bg_sprite_sheet"])
    bg = pygame.transform.scale(bg, (bg.get_width() * bg_scale, bg.get_height() * bg_scale))
    bg = bg.subsurface(((i * bg.get_width() / 6, 0), (bg.get_width() / 6, bg.get_height())))
    backgrouds.append(bg)



key_sys = KeySystem()
world = World()
# Game loop
while is_running:

    # makes it so you can quit out of the game by clicking x or pressing escape
    user_events = pygame.event.get()
    for event in user_events:
        if event.type == pygame.QUIT:
            is_running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEWHEEL:
            world.scroll_index += event.y

    # white background
    screen.fill("#000000")

    world.run()

    world.draw()


    # show FPS
    fps_text = font.render(str(round(FPS.get_fps(), 1)), True, "White")
    screen.blit(fps_text, (screen_width - 30, 0))

    # cords
    if game_mode < 2:
        cords_text = font.render(
            f"({round(world.snap_pos[0])}, {round(world.snap_pos[1])}, {world.player.position.x % 3:.1f})", True, "White")
    else:
        cords_text = font.render(
            f"({round(world.player.position.x)}, {round(world.player.position.y, 1)}, {world.player.position.x % 3:.1f})",
            True, "White")
    screen.blit(cords_text, (3, 0))

    # you need this at end of loop, it updates the screen and limits the frame rate
    pygame.display.update()
    FPS.tick(50)
