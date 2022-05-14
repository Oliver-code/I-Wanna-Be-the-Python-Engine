import math

import pygame
import sys
import settings
import rooms

# --TODO--
# tiled (don't have to use this)
# make sprites, tiles are 20x20
# rename to "I Wanna Steal The Intellectual Property!" (IWSTIP)

# settings
screen_width = settings.width
screen_height = settings.height

# pygame setup
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = pygame.time.Clock()
is_running = True


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


def round_to(rounf_put, val):
    rounf_put /= val
    output = (round(rounf_put)) * val
    return output


def load_data(lines):
    data_file = open("all_saves", "r")
    data_list = []
    line = lines
    if lines < 1:
        line = 1

    for i in range(line):
        data_list = data_file.readline()
        print(data_list)
    data_file.close()

    tiles = pygame.sprite.Group()
    killers = pygame.sprite.Group()

    concat = ""
    index = 0
    temp = []
    for letter in str(data_list):
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


def check_in_bounds(rect):
    if rect.left > screen_width or rect.right < 0 or rect.top > screen_height or rect.bottom < 0:
        return False
    return True


def wrap(rect):
    if rect.left > screen_width or rect.right < 0:
        return math.fabs(rect.left - screen_width), rect.top
    if rect.top > screen_height or rect.bottom < 0:
        return rect.left, math.fabs(rect.left - screen_width)


def distance(pos1, pos2):
    dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    return dist


# Classes
class World:
    def __init__(self):
        # self.tiles = [, Block((200, 200), (50, 100)), Block((300, 100), (50, 100))]
        self.tile_sprites = pygame.sprite.Group()
        self.tile_sprites.add(Block((32, 288)))
        self.player = Player((40, 250))
        self.player_sprite = pygame.sprite.GroupSingle()
        self.player_sprite.add(self.player)
        self.killers = pygame.sprite.Group()
        self.mouse = MouseSystem()

        self.preview_sprite = pygame.sprite.GroupSingle()
        self.preview_sprite.add(BasicSprite((0, 0), "../graphics/Block0.png"))
        self.placing = 1
        self.snap = 32
        self.snap_toggle = 1
        self.snap_cd = False
        self.rotate_cd = False
        self.save_cd = False
        self.load_cd = False
        self.reset_cd = False
        self.place_angle = 0
        self.room_togle = 1
        self.images = {
            "Spike": "../graphics/Spike.png",
            "Block": "../graphics/Block0.png",
            "MiniSpike": "../graphics/MiniSpike.png"
        }
        self.place_offset = (-16, -16)

    def delete(self, pos, tolerance=0):
        for sprite in self.tile_sprites:
            if distance(sprite.rect.topleft, pos) <= tolerance:
                self.tile_sprites.remove(sprite)

        for sprite in self.killers:
            if distance(sprite.rect.topleft, pos) <= tolerance:
                self.killers.remove(sprite)

    def draw(self):
        self.tile_sprites.draw(screen)
        self.killers.draw(screen)

        self.player_sprite.draw(screen)
        self.player.draw()
        self.preview_sprite.draw(screen)

    def run(self):
        # does collision
        self.player.update(self.tile_sprites, self.killers)
        if self.player.dead:
            self.reset()
        self.create()
        self.mouse.update()
        # if not check_in_bounds(self.player.rect):
        #     self.room_togle *= -1
        #     print(self.room_togle)
        #     if self.room_togle == -1:
        #         self.load_room(room1)
        #     else:
        #         self.load_room(room2)
        # self.reset()

    def reset(self):
        self.player = Player((40, 250))
        self.player_sprite.add(self.player)

    def create(self):
        keys = pygame.key.get_pressed()
        pos = self.mouse.current_pos
        pos = (round_to(pos[0] + self.place_offset[0], self.snap), round_to(pos[1] + self.place_offset[0], self.snap))
        self.preview_sprite.sprite.rect.topleft = pos

        if self.mouse.individual_frame_down:
            if self.placing == 1:
                self.tile_sprites.add(Block(pos))
            elif self.placing == 2:
                self.killers.add(Killer(pos, start_angle=self.place_angle))
            elif self.placing == 3:
                self.killers.add(Killer(pos, start_angle=self.place_angle, image="../graphics/MiniSpike.png"))

        if keys[pygame.K_w]:
            self.player.hitbox.center = (self.mouse.current_pos)

        if keys[pygame.K_TAB]:
            if not self.snap_cd:
                print(self.snap_toggle)
                self.snap_toggle *= -1
                self.snap = 16
                if self.snap_toggle < 1:
                    self.snap = 4
            self.snap_cd = True
        else:
            self.snap_cd = False

        if keys[pygame.K_r]:
            if not self.reset_cd:
                self.reset()
                self.reset_cd = True
        else:
            self.reset_cd = False

        if keys[pygame.K_t]:
            if not self.rotate_cd:
                self.rotate_cd = True
                self.place_angle += 90
                if self.placing == 2:
                    self.preview_sprite.add(BasicSprite(pos, self.images["Spike"], start_angle=self.place_angle))
                elif self.placing == 3:
                    self.preview_sprite.add(BasicSprite(pos, self.images["MiniSpike"], start_angle=self.place_angle))

        else:
            self.rotate_cd = False

        if keys[pygame.K_1]:
            self.placing = 1
            self.place_offset = (-16, 16)
            self.preview_sprite.add(BasicSprite(pos, "../graphics/Block0.png"))
        elif keys[pygame.K_2]:
            self.place_angle = 0
            self.placing = 2
            self.place_offset = (-16, 16)
            self.preview_sprite.add(BasicSprite(pos, "../graphics/Spike.png", start_angle=self.place_angle))
        elif keys[pygame.K_3]:
            self.place_angle = 0
            self.placing = 3
            self.place_offset = (-8, -8)
            self.preview_sprite.add(BasicSprite(pos, self.images["MiniSpike"], start_angle=self.place_angle))

        if keys[pygame.K_BACKSPACE]:
            self.delete(pos, tolerance=30)

        if keys[pygame.K_DELETE]:
            self.killers.empty()
            self.tile_sprites.empty()
            self.reset()

        if keys[pygame.K_k]:
            if not self.save_cd:
                self.save_data()
                print(len(self.killers), len(self.tile_sprites))
                self.save_cd = True
        else:
            self.save_cd = False

        if keys[pygame.K_l]:
            if not self.load_cd:
                self.load_data("data.txt")
            self.load_cd = True

        else:
            self.load_cd = False

    def save_data(self):

        tile_data = []
        for sprite in self.tile_sprites.sprites():
            tile_data.append(sprite.rect.topleft)

        killer_data = []
        for sprite in self.killers.sprites():
            killer_data.append(((sprite.rect.topleft[0]), (sprite.rect.topleft[1]), sprite.angle))

        data = (str(tile_data) + str(killer_data))
        data_file = open("data.txt", "w")
        data_file.write(data)
        data_file.close()

    def load_data(self, data):
        loaded_objects = load_data(3)
        self.tile_sprites = loaded_objects[0]
        self.killers = loaded_objects[1]
        self.reset()

    def load_room(self, room):
        self.killers.empty()
        for killer in room.killers:
            self.killers.add(killer)
        self.tile_sprites.empty()
        for tile in room.tiles:
            self.tile_sprites.add(tile)


class Room:
    def __init__(self, data):
        print(data)
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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frame = 0

        self.original_image = pygame.image.load("../graphics/PlayerIdle.png").convert_alpha()

        self.image = self.original_image

        self.mask = pygame.mask.from_surface(pygame.image.load("../graphics/PlayerMask.png").convert_alpha())
        mask_rect = (self.mask.get_bounding_rects())[0]
        self.offset = pygame.math.Vector2(mask_rect[0], mask_rect[1])

        self.speed = 3
        self.jump_vel = 8.5
        self.djump_vel = 7
        self.jumps = 2
        self.gravity = 0.4
        self.jump_cooldown = False
        self.max_fall = 9

        self.dead = False
        self.jumps_counter = 1
        self.grounded = False
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = 1

        self.hitbox = mask_rect
        self.hitbox.topleft = pos
        self.rect = self.image.get_rect()  # pygame.Rect(pos, (size[0], size[1]))
        self.update_sprite()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.velocity.x = 1 * self.speed
            self.image = self.original_image
            self.direction = 1
        elif keys[pygame.K_LEFT]:
            self.velocity.x = -1 * self.speed
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.direction = -1
        else:
            self.velocity.x = 0

        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.jump_cooldown == False:
            self.jump_cooldown = True
            if self.jumps_counter == 0 and self.grounded:
                self.velocity.y = self.jump_vel - self.gravity
                self.grounded = False
                self.jumps_counter += 1
            elif self.jumps_counter < self.jumps:
                self.velocity.y = self.djump_vel - self.gravity
                self.grounded = False
                self.jumps_counter += 1
        elif (not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]) and self.jump_cooldown == True:
            if self.velocity.y > 0:
                self.velocity.y *= 0.45
            self.jump_cooldown = False

    def check_grounded(self, tiles):
        for tile in tiles:
            temp_rect = pygame.Rect((self.hitbox.topleft), (self.hitbox.size[0], self.hitbox.size[1] + 1))
            if temp_rect.colliderect(tile.rect):
                self.grounded = True
                self.jumps_counter = 0
                return
            else:
                self.grounded = False
                if self.jumps_counter < 1:
                    self.jumps_counter = 1

    def block_collision(self, tiles):
        self.horizontal(tiles)
        self.vertical(tiles)

    def horizontal(self, tiles):
        self.hitbox.x += self.velocity.x
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity.x < 0:
                    self.hitbox.left = tile.rect.right
                    self.velocity.x = 0
                elif self.velocity.x > 0:
                    self.hitbox.right = tile.rect.left
                    self.velocity.x = 0

    def vertical(self, tiles):

        if not self.grounded:
            self.apply_gravity()

        self.hitbox.y -= self.velocity.y
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity.y < 0:
                    self.hitbox.bottom = tile.rect.top
                    self.velocity.y = 0
                    self.grounded = True
                    self.jumps_counter = 0
                elif self.velocity.y > 0:
                    self.hitbox.top = tile.rect.bottom
                    self.velocity.y = 0

    # def platform_collision(self, tiles):
    #     if not self.grounded:
    #         self.apply_gravity()
    #     self.hitbox.x += self.velocity.x
    #     self.hitbox.y -= self.velocity.y
    #     for tile in tiles:
    #         if self.hitbox.colliderect(tile.rect):
    #             if self.hitbox.bottom < tile.rect.top+10:
    #                 self.hitbox.bottom = tile.rect.top
    #                 self.velocity.y = 0
    #                 self.grounded = True
    #                 self.jumps_counter = 0

    def kill_collision(self, killers):
        for sprite in killers:
            if pygame.sprite.collide_rect(self, sprite):
                if pygame.sprite.collide_mask(self, sprite):
                    return True

    def apply_gravity(self):
        self.velocity.y -= self.gravity
        if self.velocity.y < self.max_fall * -1:
            self.velocity.y = self.max_fall * -1

    def update_sprite(self):
        self.rect.topleft = self.hitbox.topleft - self.offset
        if self.direction == -1:
            self.rect.topleft = (self.rect.topleft[0] + 3, self.rect.topleft[1])

    def update(self, tiles, killers):
        self.frame += 1
        self.input()
        self.check_grounded(tiles)
        self.block_collision(tiles)
        self.update_sprite()
        if self.kill_collision(killers):
            self.dead = True

    def draw(self):
        # pygame.draw.rect(screen, "Black", self.hitbox)
        pass


class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("../graphics/Block0.png").convert_alpha()
        self.rect = pygame.Rect(pos, (32, 32))

    def draw(self):
        pygame.draw.rect(screen, "Black", self.rect)


class Killer(pygame.sprite.Sprite):
    def __init__(self, pos, image="../graphics/Spike.png", start_angle=0):
        super().__init__()
        self.image_data = image
        self.original_image = pygame.image.load(self.image_data).convert_alpha()
        self.image = pygame.image.load(self.image_data).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.sprite = pygame.sprite.GroupSingle()
        self.sprite.add(self)
        self.angle = start_angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    # def draw(self):
    #     self.sprite.draw(screen)


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, start_angle=0):
        super().__init__()
        self.image_data = image
        self.original_image = pygame.image.load(self.image_data).convert_alpha()
        self.image = pygame.image.load(self.image_data).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.angle = start_angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)


# room1 = Room(rooms.room1)
# room2 = Room()

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

    world.draw()
    world.run()

    # you need this at end of loop, it updates the screen and limits the frame rate
    pygame.display.update()
    FPS.tick(50)
