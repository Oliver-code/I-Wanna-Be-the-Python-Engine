import pygame
class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("../graphics/Block0.png").convert_alpha()
        self.rect = pygame.Rect(pos, (32, 32))



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

