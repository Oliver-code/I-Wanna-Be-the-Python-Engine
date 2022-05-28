import pygame
import settings
import __main__


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frame = 0
        self.frame_index = -1
        self.dash_dir = pygame.math.Vector2(0, 0)

        self.original_image = pygame.image.load(settings.tile_set2["PlayerIdle"]).convert_alpha()

        self.image = self.original_image

        self.mask = pygame.mask.from_surface(pygame.image.load(settings.tile_set2["PlayerMask"]).convert_alpha())
        mask_rect = (self.mask.get_bounding_rects())[0]
        self.offset = pygame.math.Vector2(mask_rect[0], mask_rect[1])

        self.speed = 3
        self.jump_vel = 8.5
        self.djump_vel = 7
        self.jumps = 2
        self.max_dash = 1
        self.dashed = 0
        self.gravity = 0.4
        self.jump_cooldown = True
        self.max_fall = 9
        self.multiplier = 1

        self.dead = False
        self.jumps_counter = 1
        self.grounded = False
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = pygame.math.Vector2(1, 0)
        self.sprite_facing = 1
        self.state = 0

        self.position = pygame.math.Vector2(pos)
        self.hitbox = mask_rect
        self.hitbox.topleft = self.position
        self.rect = self.image.get_rect()  # pygame.Rect(pos, (size[0], size[1]))
        self.update_sprite()
        self.save_position = self.hitbox.topleft

    def input(self):
        keys = pygame.key.get_pressed()
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

        if __main__.key_sys.individual_frame_down[pygame.K_z] and self.state == 0:
            if self.direction.xy == (0,0):
                self.dash_dir.xy = (self.sprite_facing,0)

            else:
                self.dash_dir.xy = self.direction
            self.state = 1

        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.jump_cooldown == False:

            self.jump_cooldown = True
            if self.jumps_counter == 0 and self.grounded:
                self.velocity.y = self.jump_vel
                self.grounded = False
                self.jumps_counter += 1
            elif self.jumps_counter < self.jumps:
                self.velocity.y = self.djump_vel
                self.grounded = False
                self.jumps_counter += 1
        elif (not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]) and self.jump_cooldown == True:
            if self.velocity.y > 0:
                self.velocity.y *= 0.45
            self.jump_cooldown = False



    def check_grounded(self, tiles):
        for tile in tiles:
            temp_rect = pygame.Rect((self.position), (self.hitbox.size[0], self.hitbox.size[1] + 1))
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
        self.position.x += self.velocity.x*self.multiplier
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

        if not self.grounded:
            self.apply_gravity()

        self.position.y -= self.velocity.y*self.multiplier
        self.hitbox.topleft = self.position

        for tile in tiles:
            if self.hitbox.colliderect(tile.rect):
                if self.velocity.y < 0:
                    self.hitbox.bottom = tile.rect.top
                    self.velocity.y = 0
                    self.grounded = True
                    self.jumps_counter = 0
                    self.position.y = self.hitbox.top
                elif self.velocity.y > 0:
                    self.hitbox.top = tile.rect.bottom
                    self.velocity.y = 0
                    self.position.y = self.hitbox.top

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
        self.rect.topleft = self.position - self.offset
        self.image = self.original_image

        if self.sprite_facing == -1:
            self.rect.topleft = (self.rect.topleft[0] + 3, self.rect.topleft[1])
            self.image = pygame.transform.flip(self.original_image, True, False)


    def manage_dash(self):
        if self.state == 1:

            if self.frame_index == -1:
                self.frame_index = self.frame+10

            self.velocity = self.dash_dir*10

        if self.frame >= self.frame_index and not self.frame_index == -1:
            self.velocity.xy = (0,0)
            self.state = 0
            self.frame_index = -1


    def update(self):
        if not self.dead:
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
