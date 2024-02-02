# sprites.py
import pygame
from config import *
from player import Player

bomba = pygame.image.load("images/bomba.png")
bomba = pygame.transform.scale(bomba, (44, 44))

class Bomba(pygame.sprite.Sprite):
    def __init__(self, game, damage, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._layer = BOMBA_LAYER
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image = pygame.image.load("images/bomba.png")
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, *args):
        hits = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for hit in hits:
            if isinstance(hit, Player):
                self.game.all_sprites.remove(self)
                self.game.block.remove(self)
                hit.inventory["Bomba"] += 1
