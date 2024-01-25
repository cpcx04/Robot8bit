# sprites.py
import pygame
from config import *

player_image_left = pygame.image.load("images/3397.png")
player_image_left = pygame.transform.scale(player_image_left, (80, 80))

player_image_right = pygame.image.load("images/3397_derecha.png")
player_image_right = pygame.transform.scale(player_image_right, (80, 80))

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self._layer = PLAYER_LAYER
        self.image = player_image_left  # Inicia con la imagen de izquierda
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mover_derecha = False
        self.mover_izquierda = False
        self.mover_arriba = False
        self.mover_abajo = False

    def update(self):
        if self.mover_derecha:
            self.rect.x += PLAYER_SPEED
            self.image = player_image_right  # Cambia la imagen a la derecha
        elif self.mover_izquierda:
            self.rect.x -= PLAYER_SPEED
            self.image = player_image_left  # Cambia la imagen a la izquierda

        if self.mover_arriba:
            self.rect.y -= PLAYER_SPEED
        elif self.mover_abajo:
            self.rect.y += PLAYER_SPEED

    def mover(self):
        if self.mover_derecha:
            self.position[0] += self.speed
        if self.mover_izquierda:
            self.position[0] -= self.speed
        if self.mover_arriba:
            self.position[1] -= self.speed
        if self.mover_abajo:
            self.position[1] += self.speed

# Clase Obstaculo
class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image_path):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._layer=BLOCK_LAYER
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.image.load("images/" + image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# Clase Obstaculo (actualizada)
class Obstaculo(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "muro.png")

        # Puedes agregar más atributos si es necesario
