import pygame
from config import *
class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image_path):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer = BLOCK_LAYER
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.image.load("images/" + image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Obstaculo(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "muro.png")
class Muro(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "hielo.jpg")

