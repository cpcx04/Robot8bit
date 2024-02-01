import pygame
from config import *
from player import Player

armadura = pygame.image.load("images/armadura.png")
armadura = pygame.transform.scale(armadura, (44, 44))

class Armadura(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._layer = ARMADURA_LAYER
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image = pygame.image.load("images/armadura.png")
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        # Verifica la colisión con el jugador
        hits = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for hit in hits:
            if isinstance(hit, Player):
                self.game.all_sprites.remove(self)
                self.game.block.remove(self)
                hit.inventory["Armadura"] += 1