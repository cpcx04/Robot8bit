# sprites.py
import pygame
from config import *
from player import *

bomba = pygame.image.load("images/bomba.png")
bomba = pygame.transform.scale(bomba, (44, 44))

class Bomba(pygame.sprite.Sprite):

    def __init__(self, game, damage, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._layer = BOMBA_LAYER
        self.game = game
        self.damage = 10
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.explosion_timer = 0
        self.image= bomba
    def update(self, *args):
        self.explosion_timer += 1
        if self.explosion_timer >= TIEMPO_DE_EXPLOSION:
            self.explotar()

    def explotar(self):
        affected_blocks = []  # Almacena las posiciones de los bloques afectados
        hits = pygame.sprite.spritecollide(self, self.game.block, False)

        for hit in hits:
            if isinstance(hit, Player):
                distancia = pygame.math.Vector2(hit.rect.centerx - self.rect.centerx,
                                                hit.rect.centery - self.rect.centery).length()
                if distancia < DISTANCIA_DE_EXPLOSION:
                    print("AUCH ME HA DADO")
                    hit.current_health -= self.damage
            elif isinstance(hit, Obstaculo):
                affected_blocks.append((hit.rect.x, hit.rect.y))

        for block_pos in affected_blocks:
            # Crear un nuevo Tile solo si no hay otro sprite en esa posición
            if not any(sprite.rect.x == block_pos[0] and sprite.rect.y == block_pos[1] for sprite in
                       self.game.all_sprites):
                Tile(self.game, block_pos[0], block_pos[1], "suelo.jpg")

        self.kill()
