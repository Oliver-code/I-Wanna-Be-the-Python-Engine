import math
import random

import pygame
import sys
import settings
import player
import image_loading
import pickle
import json

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

volume = settings.music_vol
pygame.mixer.music.load(settings.sounds["Moonsong"])
pygame.mixer.music.set_volume(0.5 * volume)
pygame.mixer.music.play(-1)

pygame.mixer.init()
death_sound = pygame.mixer.Sound(settings.sounds["death1"])
death_sound.set_volume(1)

pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

pygame.display.set_caption("I Wanna Steal The Intellectual Property!")
clock = pygame.time.Clock()
FPS = 50
delta_time = 50 / FPS
is_running = True

font = pygame.font.SysFont('arial', 15)

loaded_images = image_loading.load_images(settings.tile_set2)
# for image in settings.tile_set2:
#     loaded_images[image] = pygame.image.load(settings.tile_set2[image]).convert_alpha()


game_mode = settings.game_mode
scene = 0

# functions
display_save = None

transition_percent = 0


def main_game():
    running = True
    while running:
        user_events = pygame.event.get()
        for event in user_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    running = False
                    pygame.mixer.music.set_volume(0.1 * volume)
                    pygame.mixer.pause()

                    pause_screen(screen.copy())
                # if main_event.key == pygame.K_COMMA:
                #     world.run()

        # white background
        screen.fill("#000000")

        if scene == 0:
            world.run()

        world.draw()

        # particles
        if world.frame % 3 == 0:
            farticles.append(Particle((world.player.rect.center[0], world.player.rect.center[1] - 6), 50,
                                      (random.randint(-1 * 20, 1 * 20) / 20, -1 + random.randint(-1 * 20, 1 * 20) / 20),
                                      acceleration=(0, 0.05)))

        for fart in farticles:
            fart.draw()
            fart.update()

        # show FPS
        fps_text = font.render(str(round(clock.get_fps(), 1)), True, "White")
        screen.blit(fps_text, (screen_width - 30, 0))

        pygame.display.update()
        clock.tick(FPS)


count  = 0


def pause_screen(screen_copy):
    running = True

    def options():
        # font2 = pygame.font.SysFont("arial", 35)
        # text = "hello, i am very well"
        # text_rect = pygame.Rect((screen_width / 2 - font2.size(text)[0] / 2, 100), font2.size(text))
        # screen.blit(font2.render(text, True, "white"), text_rect.topleft)
        pygame.draw.rect(screen, "White", pygame.rect.Rect(100,50,100,100))

    while running:
        user_events = pygame.event.get()
        for pause_event in user_events:
            if pause_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pause_event.type == pygame.MOUSEBUTTONDOWN:
                print(pause_event.pos)
            if pause_event.type == pygame.KEYDOWN:
                if pause_event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if pause_event.key == pygame.K_p:
                    running = False
                    pygame.mixer.music.set_volume(0.5 * volume)

                    main_game()
                # if pause_event.key == pygame.K_COMMA and scene == 0:
                #     main_game()

        screen.blit(screen_copy, (0, 0))

        dark_bg = pygame.Surface((screen_width, screen_height))
        dark_bg.fill("Black")
        dark_bg.set_alpha(200)
        screen.blit(dark_bg, (0, 0))


        options()

        # - center menu -
        # menu_width = int(screen_width * 0.4)
        # menu_height = int(screen_height * 0.8)
        # pygame.draw.rect(screen, "Grey",
        #                  ((screen_width - menu_width) / 2, (screen_height - menu_height) / 2, menu_width, menu_height))

        pygame.display.update()
        clock.tick(FPS)
        # count = 2


def cap(value, minimum, maximum):
    if value > maximum:
        pass
        if True:
            return maximum
    elif value < minimum:
        return minimum
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
    swag_offset = pygame.math.Vector2(round(offset.x), round(offset.y))
    for sprite in sprites:
        sprite.rect.topleft += swag_offset
    sprites.draw(screen)
    for sprite in sprites:
        sprite.rect.topleft -= swag_offset
    # if sprite.rect.right+offset.x > 0 or sprite.rect.left+offset.x < screen_width or sprite.rect.top+offset.y < screen_width or sprite.rect.bottom+offset.y > 0:


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


loaded_diamond = list(reversed(image_loading.load_silly(settings.tile_set2["diamondAnim"], 32, 32)))


def diamond(pos, progress):
    fixed_progress = cap(progress, 0, 1)
    # print(int(fixed_progress * 31))
    screen.blit(loaded_diamond[int(fixed_progress * 31)], pos)


def screen_wipe(progress):
    if progress == 1:
        progress = 500
    cell_size = (32, 32)
    rows = screen_height // cell_size[1]
    columns = screen_width // cell_size[0]
    delay = 0.05  # next row starts when last row is this percent done with its animation
    cell_animation_length = 1 / ((rows - 1) * delay + 1)
    for y in range(rows):
        for x in range(columns):
            cell_row = y  # nothing being done
            # cell_row = rows - y #flips vertically
            cell_row = (-abs(y - rows / 2) + rows / 2) * 2
            diamond((x * 32, y * 32), (progress - cell_animation_length * delay * cell_row) / cell_animation_length)


# Classes
class World:
    def __init__(self):
        self.frame = 0
        # self.tiles = [, Block((200, 200), (50, 100)), Block((300, 100), (50, 100))]
        self.startpos = (40, 250)
        self.player = player.Player(self.startpos)
        self.save_facing = self.player.direction
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player)

        self.camera_position = pygame.math.Vector2(self.player.hitbox.center[0] + screen_width / 2,
                                                   self.player.hitbox.center[1] - screen_height / 2)
        self.lookahead_offset = 0
        self.bg_offset = 0

        self.images = loaded_images
        self.tile_sprites = pygame.sprite.Group()
        self.tile_sprites.add(Block((32, 288)))
        self.bg_visuals = pygame.sprite.Group()
        self.visuals = pygame.sprite.Group()
        self.death_screen = pygame.sprite.GroupSingle()
        # self.bg_visuals.add()
        self.death_screen.add(BasicSprite((100, 200), self.images["death_screen"]))

        self.mouse = MouseSystem()

        self.death_cd = False
        self.reset_anim_timer = 0

        self.scroll_index = 0
        self.preview_sprite = pygame.sprite.GroupSingle()
        self.preview_sprite.add(BasicSprite((0, 0), self.images[0]))
        self.placing = 1
        self.snap = 32
        self.snap_pos = [0,0]
        self.lines = False
        self.snap_toggle = 0
        self.place_angle = 0
        self.room_togle = 1
        self.place_offset = (-self.snap / 2, -self.snap / 2)
        self.create_hold_list = []
        self.undo_list = []
        if game_mode >= 2:
            self.load_data(0)

        # TAS shit
        self.input_log = []

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
        if len(self.undo_list) > 0:
            global level
            level = (self.undo_list[-1])
            self.undo_list.pop()

    def draw(self):
        # BAD FIX LATER
        # for bg_index in range(len(backgrouds)):
        #     self.looping_image(backgrouds[len(backgrouds) - 1 - bg_index], bg_speeds[bg_index])
        #
        # self.bg_visuals.draw(screen)

        draw_offset(self.visuals, self.camera_position)

        draw_offset(self.player_sprite, self.camera_position)
        ## player debug stuff
        # pygame.draw.rect(screen, "Green", pygame.rect.Rect((self.player.hitbox.x +self.camera_position.x,self.player.hitbox.y+self.camera_position.y), (self.player.hitbox.size)))
        # s = pygame.Surface(self.player.rect.size)  # the size of your rect
        # s.set_alpha(50)  # alpha level
        # s.fill((255, 255, 255))  # this fills the entire surface
        # screen.blit(self.player.mask.to_surface(), (self.player.rect.x + self.camera_position.x, self.player.rect.y + self.camera_position.y))

        for group in level:
            draw_offset(level[group], self.camera_position)

        if game_mode < 2:
            self.preview_sprite.draw(screen)
            if self.lines:
                line_distane = self.snap
                for i in range(int(screen_width / line_distane) + 1):
                    # print(self.camera_offset.x % line_distane + i * line_distane)

                    color = "White"
                    width = 1
                    if (
                            self.camera_position.x % line_distane + i * line_distane) - self.camera_position.x % screen_width == 0:
                        width = 3
                    pygame.draw.line(screen, color, (self.camera_position.x % line_distane + i * line_distane, 0),
                                     (self.camera_position.x % line_distane + i * line_distane, screen_height),
                                     width=width)
                for i in range(int(screen_height / line_distane) + 1):
                    color = "White"
                    width = 1
                    if (
                            self.camera_position.y % line_distane + i * line_distane) - self.camera_position.y % screen_height == 0:
                        width = 3
                    pygame.draw.line(screen, color, (0, self.camera_position.y % line_distane + i * line_distane),
                                     (screen_width, self.camera_position.y % line_distane + i * line_distane),
                                     width=width)

        screen_wipe(transition_percent)

        if self.death_cd and transition_percent >= 0.5:
            self.death_screen.draw(screen)

        self.post_draw()

    def post_draw(self):

        # cords
        if game_mode < 2:
            cords_text = font.render(
                f"({round(world.snap_pos[0])}, {round(world.snap_pos[1])}, {world.player.position.x % 3:.1f})", True,
                "White")
        else:
            cords_text = font.render(
                f"({round(world.player.position.x)}, {round(world.player.position.y, 1)}, {world.player.position.x % 3:.1f})",
                True, "White")
        screen.blit(cords_text, (3, 0))

    def run(self):
        global transition_percent
        self.frame += 1

        key_sys.update()

        self.bg_offset -= 10

        # does collision
        # if game_mode >= 2:
        self.follow_player()

        self.player.update()

        if self.player.dead and not self.death_cd:
            self.player.kill()
            death_sound.play()
            self.death_cd = True

        if game_mode == 1:
            self.mouse.update()
            self.create()

        if key_sys.individual_frame_down[pygame.K_r]:
            self.reset()

        # if self.death_cd:
        #     self.reset_anim_timer -= 1
        #
        # if self.reset_anim_timer <= 0:
        #     # self.reset()
        #     death_sound.fadeout(650)

        if key_sys.individual_frame_down[pygame.K_s] and game_mode < 2 and not self.death_cd:
            self.save()

        if world.death_cd:
            transition_percent += 1 / 20
        elif world.reset_anim_timer <= 0:
            transition_percent -= 1 / 20
        transition_percent = cap(transition_percent, 0, 1.5)

    def scroll(self):
        player_pos = self.player.hitbox.center
        screen_size = (settings.width, settings.height)
        self.camera_position = pygame.math.Vector2(-round_down(player_pos[0], screen_size[0]),
                                                   -round_down(player_pos[1], screen_size[1]))

    def follow_player(self):
        player_pos = self.player.hitbox.center
        lookahead = 0  # lookahead = screen_width/8

        self.lookahead_offset += self.player.sprite_facing * 5
        self.lookahead_offset = cap(self.lookahead_offset, -lookahead, lookahead)

        self.camera_position.x -= (player_pos[0] + self.camera_position.x - (
                screen_width / 2 - self.lookahead_offset)) / 4
        self.camera_position.y -= (player_pos[1] + self.camera_position.y - screen_height / 2) / 2

    def looping_image(self, image, speed):
        bg_size = image.get_size()
        for i in range(int(screen_width / bg_size[0]) + 2):
            for v in range(int(screen_height / bg_size[1]) + 2):
                screen.blit(image,
                            (((self.camera_position.x + self.bg_offset) * speed % bg_size[0]) + (i - 1) * bg_size[0],
                             0 + (v - 1) * bg_size[1]))

    def save(self):
        self.player.save_position = self.player.hitbox.topleft
        self.save_facing = self.player.direction
        self.input_log.extend(self.player.input_log)
        self.player.input_log.clear()

    def reset(self):
        global transition_percent
        # self.player.position = self.startpos
        transition_percent = 100
        self.player = player.Player(self.player.save_position)
        self.player.direction = self.save_facing
        self.player_sprite.add(self.player)
        self.follow_player()
        self.death_cd = False
        death_sound.fadeout(650)

    def copy_level_data(self):
        return_list = {}

        for group in level:
            # print(level[group], group)
            return_list.update({group: pygame.sprite.Group()})

            for item in level[group]:
                return_list[group].add(item)

        return return_list

    def create(self):
        keys = key_sys
        mods = pygame.key.get_mods()
        pos = self.mouse.current_pos - self.camera_position
        self.snap_pos = (pos[0] // self.snap * self.snap, pos[1] // self.snap * self.snap)
        # self.scroll_index = self.scroll_index % len(tiles_test)
        # self.preview_sprite.sprite.image = tiles_test[self.scroll_index]

        preview_pos = self.snap_pos + self.camera_position
        self.preview_sprite.sprite.rect.topleft = preview_pos

        if self.mouse.individual_frame_down:
            self.undo_list.append(self.copy_level_data())

        if keys.individual_frame_down[pygame.K_BACKSPACE]:
            self.undo_list.append(self.copy_level_data())

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

        if keys.individual_frame_down[pygame.K_z] and mods == 1024:
            self.undo()

        if keys.individual_frame_down[pygame.K_t]:
            self.save()
            with open('data.txt', 'w') as f:
                f.write(json.dumps(self.input_log))

        # old cam controls
        if game_mode == 1:
            cam_speed = 20
            fast = True
            if keys.current_frame_down[pygame.K_LEFTBRACKET]:
                if not self.cam_cd or fast:
                    self.camera_position.x += cam_speed  # settings.width
                self.cam_cd = True
            elif keys.current_frame_down[pygame.K_BACKSLASH]:
                if not self.cam_cd or fast:
                    self.camera_position.x -= cam_speed  # settings.width
                self.cam_cd = True
            elif keys.current_frame_down[pygame.K_RIGHTBRACKET]:
                if not self.cam_cd or fast:
                    self.camera_position.y -= cam_speed  # settings.height
                self.cam_cd = True
            elif keys.current_frame_down[pygame.K_EQUALS]:
                if not self.cam_cd or fast:
                    self.camera_position.y += cam_speed  # settings.height
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
        self.individual_frame_up = [None] * 512

    def update(self):
        keys = pygame.key.get_pressed()
        for key in range(512):
            self.current_frame_down[key] = True if keys[key] else False
            self.individual_frame_down[key] = False
            self.individual_frame_up[key] = False
            if self.current_frame_down[key] and not self.previous_frame_down[key]:
                self.individual_frame_down[key] = True
            elif self.previous_frame_down[key]:
                self.individual_frame_up[key] = True
            self.previous_frame_down[key] = self.current_frame_down[key]


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, start_angle=0, size=1):
        super().__init__()
        self.name = "image"
        self.image_data = image
        self.original_image = (self.image_data)
        self.image = (self.image_data)

        self.init_pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.angle = start_angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * size, self.image.get_height() * size))


class Test(BasicSprite):
    def __init__(self, pos):
        super().__init__(pos, image=loaded_images[0])
        self.swah = pos


class Block(BasicSprite):
    def __init__(self, pos, image=loaded_images[0]):
        super().__init__(pos, image)
        self.name = "tile"
        self.tile_id = 0

    # def draw(self):
    #     pygame.draw.rect(screen, "Black", self.rect)


class Killer(pygame.sprite.Sprite):
    def __init__(self, pos, tile_id=1, start_angle=0):
        super().__init__()
        self.name = "spike"

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
        self.name = "save"
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
        self.name = "wter"
        self.image = pygame.Surface((32, 32)).convert_alpha()
        self.image.fill((109, 109, 248, 127.5))
        self.rect = pygame.Rect(pos, (32, 32))
        self.init_pos = pos
        self.rect = pygame.Rect(pos, (32, 32))

    def draw(self):
        pygame.draw.rect(screen, "Black", self.rect)


class Particle:
    def __init__(self, pos, lifespan, velocity, acceleration=(0, 0)):
        self.pos = pygame.math.Vector2(pos)
        self.lifespan = lifespan  # dont change this one
        self.lifespan_countdown = self.lifespan
        self.vel = pygame.math.Vector2(velocity)
        self.acc = pygame.math.Vector2(acceleration)
        self.size = 4
        self.dead = False
        self.color = "red"

    def update(self):
        self.lifespan_countdown -= 1
        self.color = pygame.Color.lerp(pygame.Color(251, 255, 193), pygame.Color(255, 0, 0), cap(self.lifespan_countdown/self.lifespan, 0, 1))


        self.pos += self.vel
        self.vel += self.acc
        self.size = 7 * self.lifespan_countdown/self.lifespan

        if self.lifespan_countdown == 0:
            self.dead = True

    def draw(self):
        if not self.dead:
            pygame.draw.circle(screen, self.color, self.pos + world.camera_position, self.size)

    @staticmethod
    def draw_offset_circle(pos, radius, offset, color):
        pygame.draw.circle(screen, color, pos + offset, radius)


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
        (BasicSprite((2094, 625), loaded_images["burto"], size=1)),
        BasicSprite((710, 95), loaded_images["troll"], size=0.45)
    ),
    "waters": pygame.sprite.Group(
        # Water((100,100)),
        # Water((100, 132)),
        # Water((100, 164)),
        # Water((100, 196)),

    )

}

bg_scale = 2.8
backgrouds = []
bg_speeds = [0, 0.1, 0.3, 0.5, 1]
for i in range(5):
    bg = (loaded_images["bg_sprite_sheet"])
    bg = pygame.transform.scale(bg, (bg.get_width() * bg_scale, bg.get_height() * bg_scale))
    bg = bg.subsurface(((i * bg.get_width() / 6, 0), (bg.get_width() / 6, bg.get_height())))
    backgrouds.append(bg)

key_sys = KeySystem()
farticles = []

inputs = {

}
frame_advance = 0
# user_events = None
world = World()
# Game loop
main_game()
# while is_running:
#     global user_events
#     # makes it so you can quit out of the game by clicking x or pressing escape
#     for event in user_events:
#         if event.type == pygame.QUIT:
#             is_running = False
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 is_running = False
#                 pygame.quit()
#                 sys.exit()
#             # if event.key == pygame.K_COMMA and scene == 0:
#             #     main_game()
#
#     if scene == 0:
#         main_game()
#     elif scene == 1:
#         pause_screen()
#
#     # screen_wipe((math.sin(world.frame / 20))/2 + 0.5)
#
#     # blit_alpha(screen, loaded_images[1], (100,100), 100)
#
