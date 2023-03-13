import pygame
import os


def load_images(images):
    image_list = {}
    for image in images:
        if type(images[image]) == str:
            image_list[image] = pygame.image.load(images[image]).convert_alpha()
    return image_list


def load_spritesheet(image, scale=1):
    tile_size = 8
    loaded_image = pygame.image.load(image).convert_alpha()

    images = []
    x = 0
    for column in range(loaded_image.get_width() // tile_size):
        x += 1
        y = 0
        for row in range(loaded_image.get_height() // tile_size):
            y += 1
            images.append(pygame.transform.scale(loaded_image, (
                loaded_image.get_width() * scale, loaded_image.get_height() * scale)).subsurface(
                (((x - 1) * tile_size * scale, (y - 1) * tile_size * scale), (tile_size * scale, tile_size * scale))))
    return images


def load_silly(image, width, height, tiles=None, x_offset=0, y_offset=0):
    loaded_image = pygame.image.load(image).convert_alpha()

    tiles_out = tiles
    if tiles_out is None:
        tiles_out = loaded_image.get_width() // width
    images = []
    x = x_offset
    for column in range(tiles_out):
        x += 1
        y = y_offset + 1
        images.append(loaded_image.subsurface((((x - 1) * width, (y - 1) * height), (width, height))))
    return images


class Animation:
    def __init__(self, images, frames, player, image_type=0, animation_speed="no"):

        # -image type guide-
        # 0 means each image has its path specified in a list
        # 1 means path points to a directory/folder with each path in it. there's only 1 path in that case
        # 3 uses a sprite sheet so it's a dictionary containing path to sprite sheet and parameters for the sprite sheet
        if image_type == 0:
            self.images = images
        self.animation_index = 0
        self.playing = False
        self.single_play = False

        self.sprites = []
        if image_type == 0:
            for path in images:
                self.sprites.append(pygame.image.load(images[path]).convert_alpha())
        elif image_type == 1:

            images_dir = os.listdir(images)

            images_dir.sort()
            for path in images_dir:
                # print(f"{images}/{path}")
                if not path.startswith("."):
                    self.sprites.append(pygame.image.load(f"{images}/{path}").convert_alpha())

        self.player = player
        self.frame_data = frames
        if isinstance(animation_speed, int):
            self.frame_data = []
            for i in range(len(self.sprites)):
                self.frame_data.append((i + 1) * animation_speed)

        self.animation_length = self.frame_data[-1]

    def update(self):
        if self.playing:
            self.animation_index += 1
            self.animation_index = self.animation_index % self.animation_length
            if self.animation_index == 0 and self.single_play:
                self.single_play = False
                self.playing = False

            animation_frame = 0
            for frame in self.frame_data:
                if self.animation_index < frame:
                    break
                animation_frame += 1

            self.player.image = self.sprites[animation_frame]

    def play(self):
        self.playing = True
        self.animation_index = 0

    def stop(self):
        self.playing = False
        self.animation_index = 0

    def pause(self):
        self.playing = False

    def resume(self):
        self.playing = True

    def play_once(self):
        self.playing = True
        self.single_play = True
