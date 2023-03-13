import math
import pygame
import sys
import settings
import player

# --list--
# tiled (don't have to use this)
# make sprites, tiles are 20x20
# rename to "I Wanna Steal The Intellectual Property!" (IWSTIP)

# settings
screen_width = settings.width
screen_height = settings.height

# pygame setup
pygame.init()

pygame.mixer.music.load("../sounds/Moonsong.ogg")
pygame.mixer.music.set_volume(0)

pygame.mixer.init()
death_sound = pygame.mixer.Sound("../sounds/vine-boom.mp3")
death_sound.set_volume(0.1)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("I Wanna Steal The Intellectual Property!")
clock = pygame.time.Clock()
FPS = pygame.time.Clock()
is_running = True

# Set the game mode here!
# 0 is debug,
# 1 is create
# 2 is play
# 3 is build
game_mode = settings.game_mode


# stuff
# size = 20
# width = 20
# height = 20

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
        data_file = open(settings.game_path + r"\..\all_saves.txt", "r")

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
                    print(temp[-1])
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
    data_file = open(r"C:\Users\687338\PycharmProjects\IWBTripoff\code\IWSTIP\all_saves.txt", "r")
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


# Classes
class World:
    def __init__(self):
        # self.tiles = [, Block((200, 200), (50, 100)), Block((300, 100), (50, 100))]
        self.startpos = (40, 220)
        self.camera_offset = pygame.math.Vector2(0, 0)

        self.images = settings.tile_set2
        self.tile_sprites = pygame.sprite.Group()
        self.tile_sprites.add(Block((32, 288)))
        self.bg_visuals = pygame.sprite.Group()
        self.visuals = pygame.sprite.Group()
        self.death_screen = pygame.sprite.GroupSingle()
        self.bg_visuals.add(BasicSprite((835, 110), self.images["troll"], size=0.55))
        self.visuals.add(BasicSprite((10, 950), self.images["bag"]))
        self.visuals.add(BasicSprite((2094, 625), self.images["burto"], size=1))
        print("HIIII")
        print(self.images["death_screen"])
        self.death_screen.add(BasicSprite((100, 200), self.images["death_screen"]))


        self.player = player.Player(self.startpos)
        self.save_position = self.player.hitbox.topleft
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player)
        self.killers = pygame.sprite.Group()
        self.mouse = MouseSystem()
        self.keys = pygame.key.get_pressed()
        self.death_cd = False

        self.preview_sprite = pygame.sprite.GroupSingle()
        self.preview_sprite.add(BasicSprite((0, 0), self.images[0]))
        self.placing = 1
        self.snap = 16
        self.snap_toggle = 1
        self.snap_cd = False
        self.rotate_cd = False
        self.save_cd = False
        self.load_cd = False
        self.reset_cd = False
        self.cam_cd = False
        self.place_angle = 0
        self.room_togle = 1
        self.place_offset = (-16, -16)
        if game_mode >= 2:
            self.load_data(0)

    def delete(self, pos, tolerance=0):
        for sprite in self.tile_sprites:
            if distance(sprite.rect.topleft, pos) <= tolerance:
                self.tile_sprites.remove(sprite)

        for sprite in self.killers:
            if distance(sprite.rect.topleft, pos) <= tolerance:
                self.killers.remove(sprite)

    def draw_offset(self, sprites, offset):
        for sprite in sprites:
            sprite.rect.center += offset
        sprites.draw(screen)
        for sprite in sprites:
            sprite.rect.center -= offset

    def draw(self):
        self.bg_visuals.draw(screen)

        self.draw_offset(self.visuals, self.camera_offset)

        self.draw_offset(self.tile_sprites, self.camera_offset)
        self.draw_offset(self.killers, self.camera_offset)
        self.draw_offset(self.player_sprite, self.camera_offset)
        if game_mode < 2:
            self.preview_sprite.draw(screen)
        if self.player.dead:
            self.death_screen.draw(screen)

    def run(self):
        self.keys = pygame.key.get_pressed()

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
        if self.keys[pygame.K_r]:
            if not self.reset_cd:
                self.reset()
                self.reset_cd = True
        else:
            self.reset_cd = False
        if self.keys[pygame.K_s]:
            self.save()

    def scroll(self):
        player_pos = self.player.hitbox.center
        screen_size = (settings.width, settings.height)
        self.camera_offset = pygame.math.Vector2(-round_down(player_pos[0], screen_size[0]),
                                                 -round_down(player_pos[1], screen_size[1]))

    def save(self):
        self.save_position = self.player.hitbox.topleft

    def reset(self):
        # self.player.hitbox.topleft = self.startpos
        self.player = player.Player(self.save_position)
        self.player_sprite.add(self.player)
        self.scroll()
        self.death_cd = False

    def create(self):
        keys = self.keys
        pos = self.mouse.current_pos
        preview_pos = (
            round_to(pos[0] + self.place_offset[0], self.snap), round_to(pos[1] + self.place_offset[0], self.snap))
        pos -= self.camera_offset
        snap_pos = preview_pos - self.camera_offset
        self.preview_sprite.sprite.rect.topleft = preview_pos

        if self.mouse.individual_frame_down:
            print(pos)
            if self.placing == 1:
                self.tile_sprites.add(Block(snap_pos))
            elif self.placing == 2:
                self.killers.add(Killer(snap_pos, start_angle=self.place_angle))
            elif self.placing == 3:
                self.killers.add(Killer(snap_pos, start_angle=self.place_angle, tile_id=2))

        if keys[pygame.K_s]:
            self.save()

        # old cam controls
        if game_mode == 1:
            cam_speed = 10
            fast = False
            if keys[pygame.K_LEFTBRACKET]:
                if not self.cam_cd or fast:
                    self.camera_offset.x += settings.width
                self.cam_cd = True
            elif keys[pygame.K_BACKSLASH]:
                if not self.cam_cd or fast:
                    self.camera_offset.x -= settings.width
                self.cam_cd = True
            elif keys[pygame.K_RIGHTBRACKET]:
                if not self.cam_cd or fast:
                    self.camera_offset.y -= settings.height
                self.cam_cd = True
            elif keys[pygame.K_EQUALS]:
                if not self.cam_cd or fast:
                    self.camera_offset.y += settings.height
                self.cam_cd = True
            else:
                self.cam_cd = False

        if keys[pygame.K_w]:
            self.player.hitbox.center = (pos)

        if keys[pygame.K_TAB]:
            if not self.snap_cd:
                self.snap_toggle *= -1
                self.snap = 16
                if self.snap_toggle < 1:
                    self.snap = 4
            self.snap_cd = True
        else:
            self.snap_cd = False

        if keys[pygame.K_t]:
            if not self.rotate_cd:
                self.rotate_cd = True
                self.place_angle += 90
                if self.placing == 2:
                    self.preview_sprite.add(
                        BasicSprite(preview_pos, self.images[1], start_angle=self.place_angle))
                elif self.placing == 3:
                    self.preview_sprite.add(
                        BasicSprite(preview_pos, self.images[2], start_angle=self.place_angle))

        else:
            self.rotate_cd = False

        if keys[pygame.K_1]:
            self.placing = 1
            self.place_offset = (-16, 16)
            self.preview_sprite.add(BasicSprite(preview_pos, self.images[0]))
        elif keys[pygame.K_2]:
            self.place_angle = 0
            self.placing = 2
            self.place_offset = (-16, 16)
            self.preview_sprite.add(BasicSprite(preview_pos, self.images[1], start_angle=self.place_angle))
        elif keys[pygame.K_3]:
            self.place_angle = 0
            self.placing = 3
            self.place_offset = (-8, -8)
            self.preview_sprite.add(BasicSprite(preview_pos, self.images[2], start_angle=self.place_angle))

        if keys[pygame.K_BACKSPACE]:
            self.delete(snap_pos, tolerance=10)

        if keys[pygame.K_DELETE]:
            self.killers.empty()
            self.tile_sprites.empty()
            self.tile_sprites.add(Block((32, 288)))
            self.player.hitbox.topleft = self.startpos
            self.save()
            self.reset()

        if keys[pygame.K_k]:
            if not self.save_cd:
                self.save_data()
                self.save_cd = True
        else:
            self.save_cd = False

        if keys[pygame.K_l]:
            if not self.load_cd:
                self.load_data(0)
            self.load_cd = True

        else:
            self.load_cd = False

    def save_data(self):
        data_string = ""

        for sprite in self.tile_sprites.sprites():
            data_string += f"{sprite.tile_id},{sprite.rect.topleft[0]},{sprite.rect.topleft[1]};"

        for sprite in self.killers.sprites():
            data_string += f"{sprite.tile_id},{sprite.rect.topleft[0]},{sprite.rect.topleft[1]},{sprite.angle};"

        data_file = open("data.txt", "w")
        data_file.write(data_string)
        data_file.close()

    def load_data(self, data):
        loaded_objects = load_data(data)
        # loaded_objects = old_loader()
        self.tile_sprites = loaded_objects[0]
        self.killers = loaded_objects[1]
        self.reset()


class Room:
    def __init__(self, data):
        self.tiles = [data.killers]
        self.killers = [data.tiles]


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


class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image_data = settings.tile_set2[0]
        self.image = pygame.image.load(self.image_data).convert_alpha()
        self.init_pos = pos
        self.rect = pygame.Rect(pos, (32, 32))
        self.tile_id = 0

    def draw(self):
        pygame.draw.rect(screen, "Black", self.rect)


class Killer(pygame.sprite.Sprite):
    def __init__(self, pos, tile_id=1, start_angle=0):
        super().__init__()
        self.image_data = settings.tile_set2[tile_id]
        self.original_image = pygame.image.load(self.image_data).convert_alpha()
        self.image = pygame.image.load(self.image_data).convert_alpha()
        self.tile_id = tile_id

        self.init_pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.sprite = pygame.sprite.GroupSingle()
        self.sprite.add(self)
        self.angle = start_angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    # def draw(self):
    #     self.sprite.draw(screen)


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, start_angle=0, size=1):
        super().__init__()
        self.image_data = image
        print(self.image_data)
        self.original_image = pygame.image.load(self.image_data).convert_alpha()
        self.image = pygame.image.load(self.image_data).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.angle = start_angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*size, self.image.get_height()*size))




# room1 = Room(rooms.room1)
# room2 = Room()
pygame.mixer.music.play(-1)
bg = pygame.image.load("../graphics/bkMoon.pbm")
bg_size = 3.3
bg = pygame.transform.scale(bg, (bg.get_width()*bg_size, bg.get_height()*bg_size))




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

    # white background
    screen.fill("#FFFFFF")
    screen.blit(bg, (0, 0))

    world.run()
    world.draw()

    # you need this at end of loop, it updates the screen and limits the frame rate
    pygame.display.update()
    FPS.tick(50)
