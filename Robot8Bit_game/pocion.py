import pygame
from config import *
from player import Player

pocion = pygame.image.load("images/pocion.png")
pocion = pygame.transform.scale(pocion, (44, 44))

class Pocion(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._layer = POCION_LAYER
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image = pygame.image.load("images/pocion.png")
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
                self.game.player.current_health = 300