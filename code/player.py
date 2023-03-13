import json

import pygame
import settings
import __main__
import image_loading


# TODO
# Make animations, 3 frames(50ms) per image
#

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frame = 0

        self.original_image = pygame.image.load(settings.tile_set2[1]).convert_alpha()

        self.image = self.original_image

        self.run_animation = image_loading.Animation(settings.player_sprites["PlayerRunAnim"], [], self, image_type=1,
                                                     animation_speed=3)
        self.idle_animation = image_loading.Animation(settings.player_sprites["PlayerIdleAnim"], [], self, image_type=1,
                                                      animation_speed=6)
        self.fall_animation = image_loading.Animation(settings.player_sprites["PlayerFallAnim"], [], self, image_type=1,
                                                      animation_speed=3)
        self.jump_animation = image_loading.Animation(settings.player_sprites["PlayerJumpAnim"], [], self, image_type=1,
                                                      animation_speed=3)

        self.idle_animation.play()

        self.mask = pygame.mask.from_surface(pygame.image.load(settings.player_sprites["PlayerMask"]).convert_alpha())
        mask_rect = (self.mask.get_bounding_rects())[0]
        self.offset = pygame.math.Vector2(mask_rect[0], mask_rect[1])

        self.speed = 3
        self.jump_vel = 8.5
        self.djump_vel = 7
        self.jumps = 3
        self.max_dash = 1
        self.dashed = 0
        self.gravity = 0.4
        self.jump_cooldown = True
        self.max_fall = 9
        self.multiplier = __main__.delta_time
        self.dash_frame_counter = -1
        self.dash_dir = pygame.math.Vector2(0, 0)
        self.coyote_time_frame_counter = 0
        self.coyote_time_frames = 3

        self.dead = False
        self.jumps_counter = 1
        self.grounded = False
        self.coyote_time = False
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(1, 0)
        self.sprite_facing = 1
        self.state = 0
        self.running = False

        self.position = pygame.math.Vector2(pos)
        self.hitbox = mask_rect
        self.hitbox.topleft = self.position
        self.rect = self.image.get_rect()  # pygame.Rect(pos, (size[0], size[1]))
        self.update_sprite()
        self.save_position = self.hitbox.topleft

        self.input_log = []
        # with open('data.txt', 'r') as f:
        #     self.tas_thing = json.loads(f.read())

    def input(self):
        keys = pygame.key.get_pressed()
        self.input_log.append(
            [keys[pygame.K_RIGHT], keys[pygame.K_LEFT], keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LSHIFT],
             keys[pygame.K_RSHIFT]])
        if keys[pygame.K_RIGHT]:
            self.velocity.x = 1 * self.speed
            self.sprite_facing = 1
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.velocity.x = -1 * self.speed
            self.sprite_facing = -1
            self.direction.x = -1
        else:
            self.velocity.x = 0
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = 1
        elif keys[pygame.K_DOWN]:
            self.direction.y = -1
        else:
            self.direction.y = 0

        if self.velocity.x == 0:
            self.running = False
        else:
            self.running_first_frame = False
            if self.running == False:
                self.running_first_frame = True
            self.running = True

        if __main__.key_sys.individual_frame_down[pygame.K_z] and self.state == 0:
            if self.direction.xy == (0, 0):
                self.dash_dir.xy = (self.sprite_facing, 0)

            else:
                self.dash_dir.xy = self.direction
            self.state = 1

        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.jump_cooldown == False:
            self.jump_cooldown = True
            if self.jumps_counter == 0 and (self.grounded or self.coyote_time):
                self.velocity.y = self.jump_vel
                self.grounded = False
                self.coyote_time = False
                self.jumps_counter += 1

            elif self.jumps_counter < self.jumps:
                self.velocity.y = self.djump_vel
                self.grounded = False
                self.jumps_counter += 1
        elif (not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]) and self.jump_cooldown == True:
            if self.velocity.y > 0:
                self.velocity.y *= 0.45
            self.jump_cooldown = False

    def read_tas(self):
        keys = [0]
        if len(self.tas_thing) > self.frame-1:
            keys = self.tas_thing[self.frame-1]
        if keys[0]:
            self.velocity.x = 1 * self.speed
            self.sprite_facing = 1
            self.direction.x = 1
        elif keys[1]:
            self.velocity.x = -1 * self.speed
            self.sprite_facing = -1
            self.direction.x = -1
        else:
            self.velocity.x = 0
            self.direction.x = 0

        if keys[2]:
            self.direction.y = 1
        elif keys[3]:
            self.direction.y = -1
        else:
            self.direction.y = 0

        if self.velocity.x == 0:
            self.running = False
        else:
            self.running_first_frame = False
            if self.running == False:
                self.running_first_frame = True
            self.running = True

        if __main__.key_sys.individual_frame_down[pygame.K_z] and self.state == 0:
            if self.direction.xy == (0, 0):
                self.dash_dir.xy = (self.sprite_facing, 0)

            else:
                self.dash_dir.xy = self.direction
            self.state = 1

        if keys[4] and self.jump_cooldown == False:
            self.jump_cooldown = True
            if self.jumps_counter == 0 and (self.grounded or self.coyote_time):
                self.velocity.y = self.jump_vel - self.gravity
                self.grounded = False
                self.coyote_time = False
                self.jumps_counter += 1

            elif self.jumps_counter < self.jumps:
                self.velocity.y = self.djump_vel - self.gravity
                self.grounded = False
                self.jumps_counter += 1
        elif not keys[4] and self.jump_cooldown == True:
            if self.velocity.y > 0:
                self.velocity.y *= 0.45
            self.jump_cooldown = False
    def check_grounded(self, tiles):
        pass
        # for tile in tiles:
        #     temp_rect = pygame.Rect((self.position), (self.hitbox.size[0], self.hitbox.size[1] + 1))
        #     if self.rect.colliderect(tile.rect):
        #         self.coyote_time_frame_counter = 0
        #         self.grounded = True
        #         self.coyote_time = True
        #         self.jumps_counter = 0
        #     else:
        #         if self.coyote_time_frame_counter >= self.coyote_time_frames:
        #             self.coyote_time = False
        #             if self.jumps_counter < 1:
        #                 self.jumps_counter = 1
        #         # self.grounded = False

    def block_collision(self, tiles):
        self.horizontal(tiles)
        self.vertical(tiles)

    def horizontal(self, tiles):
        self.position.x += self.velocity.x * self.multiplier
        self.hitbox.topleft = self.position
        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity.x < 0:
                    self.hitbox.left = tile.rect.right
                    self.velocity.x = 0
                    self.position.x = self.hitbox.left
                elif self.velocity.x > 0:
                    self.hitbox.right = tile.rect.left
                    self.velocity.x = 0
                    self.position.x = self.hitbox.left

    def vertical(self, tiles):

        if not self.grounded:  # so it doesn't push me slightly into the ground every frame
            self.apply_gravity()

        self.position.y -= self.velocity.y * self.multiplier
        self.hitbox.topleft = self.position

        self.grounded = False

        for tile in tiles:

            temp_rect = pygame.Rect(self.position, (self.hitbox.size[0], self.hitbox.size[1] + 1))
            if temp_rect.colliderect(tile.rect):
                self.grounded = True

            if self.hitbox.colliderect(tile.rect):
                if self.velocity.y < 0:

                    self.hitbox.bottom = tile.rect.top
                    self.velocity.y = 0
                    self.jumps_counter = 0
                    self.position.y = self.hitbox.top
                elif self.velocity.y > 0:
                    self.hitbox.top = tile.rect.bottom
                    self.velocity.y = 0
                    self.position.y = self.hitbox.top

        self.coyote_time_frame_counter += 1
        # print(self.position, self.grounded)
        if self.grounded:
            self.coyote_time_frame_counter = 0
            self.coyote_time = True
            self.jumps_counter = 0
        else:
            if self.coyote_time_frame_counter >= self.coyote_time_frames:
                self.coyote_time = False
                if self.jumps_counter < 1:
                    self.jumps_counter = 1

    def kill_collision(self, killers):
        for sprite in killers:
            if pygame.sprite.collide_rect(self, sprite):
                if pygame.sprite.collide_mask(self, sprite):
                    return True

    def save_collision(self, saves):
        for save in saves:
            if pygame.Rect.colliderect(save.rect, self.hitbox) and __main__.key_sys.current_frame_down[pygame.K_s]:
                save.update_image(True)
                self.save_position = self.hitbox.topleft
                return
            else:
                save.update_image(False)

    def water_collision(self, waters):
        for water in waters:
            if pygame.Rect.colliderect(water.rect, self.hitbox):
                self.jumps_counter = 1
                self.multiplier = 0.8
                return
            else:
                self.multiplier = 1

    def apply_gravity(self):
        self.velocity.y -= self.gravity
        if self.velocity.y < self.max_fall * -1:
            self.velocity.y = self.max_fall * -1

    def update_sprite(self):

        self.update_animation()

        self.rect.topleft = self.position - self.offset
        # self.image = self.original_image

        if self.sprite_facing == -1:
            self.rect.topleft = (self.rect.topleft[0] + 3, self.rect.topleft[1])
            self.image = pygame.transform.flip(self.image, True, False)

    def manage_dash(self):
        if self.state == 1:

            if self.dash_frame_counter == -1:
                self.dash_frame_counter = self.frame + 10

            self.velocity = self.dash_dir * 10

        if self.frame >= self.dash_frame_counter and not self.dash_frame_counter == -1:
            self.velocity.xy = (0, 0)
            self.state = 0
            self.dash_frame_counter = -1

    def update_animation(self):
        self.image = self.original_image

        if self.running:
            self.run_animation.resume()
            self.idle_animation.stop()
        elif not self.running:
            self.run_animation.stop()
            self.idle_animation.resume()

        if self.velocity.y < -self.gravity and not self.grounded:
            self.fall_animation.resume()
            self.jump_animation.stop()

        elif self.velocity.y > self.gravity and not self.grounded:
            self.jump_animation.resume()
            self.fall_animation.stop()

        elif not self.grounded:
            self.jump_animation.stop()
            self.fall_animation.resume()
        else:
            self.jump_animation.stop()
            self.fall_animation.stop()
            self.idle_animation.resume()

        self.idle_animation.update()
        self.run_animation.update()
        self.fall_animation.update()
        self.jump_animation.update()

    def update(self):

        if not self.dead and __main__.transition_percent <= 0.9:
            self.frame += 1
            self.input()
            self.manage_dash()
            self.check_grounded(__main__.level["tiles"])
            self.block_collision(__main__.level["tiles"])
            self.update_sprite()
            self.save_collision(__main__.level["saves"])
            self.water_collision(__main__.level["waters"])
            if self.kill_collision(__main__.level["killers"]):
                self.dead = True
