# sprites.py
import pygame
from config import *

player_image_stanBy = pygame.image.load("images/front_player.png")
player_image_stanBy = pygame.transform.scale(player_image_stanBy, (54,54))

player_image_left_stop = pygame.image.load("images/left_stop.png")
player_image_left_stop = pygame.transform.scale(player_image_left_stop, (54,54))

player_image_left_run = pygame.image.load("images/left_run.png")
player_image_left_run = pygame.transform.scale(player_image_left_run, (54,54))

player_image_right_stop = pygame.image.load("images/right_stop.png.")
player_image_right_stop = pygame.transform.scale(player_image_right_stop, (54,54))

player_image_right_run = pygame.image.load("images/right_run.png")
player_image_right_run = pygame.transform.scale(player_image_right_run, (54,54))

player_image_bottom_run = pygame.image.load("images/front_run.png")
player_image_bottom_run = pygame.transform.scale(player_image_bottom_run, (54,54))

player_image_bottom_stop = pygame.image.load("images/front_player.png")
player_image_bottom_stop = pygame.transform.scale(player_image_bottom_stop, (54,54))

player_image_up_run = pygame.image.load("images/up_run.png")
player_image_up_run = pygame.transform.scale(player_image_up_run, (54,54))

player_image_up_stop = pygame.image.load("images/up_stop.png")
player_image_up_stop = pygame.transform.scale(player_image_up_stop, (54,54))


class Healthbar(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, max_hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self._layer = HEALTHBAR_LAYER
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self._layer = PLAYER_LAYER
        self.image = player_image_stanBy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.healt_bar = Healthbar(250,200,300,40,100)
        self.game.all_sprites.add(self.healt_bar)
        self.mover_derecha = False
        self.mover_izquierda = False
        self.mover_arriba = False
        self.mover_abajo = False


    def update(self):
        self.mover()

    def mover(self):
        if self.mover_derecha:
            self.rect.x += PLAYER_SPEED
            self.image = player_image_right_run
            self.collide_block('x')
        elif self.mover_izquierda:
            self.rect.x -= PLAYER_SPEED
            self.image = player_image_left_run
            self.collide_block('x')
        elif self.mover_arriba:
            self.rect.y -= PLAYER_SPEED
            self.image = player_image_up_run
            self.collide_block('y')
        elif self.mover_abajo:
            self.rect.y += PLAYER_SPEED
            self.image = player_image_bottom_run
            self.collide_block('y')
        else:
            self.image = player_image_stanBy

    def collide_block(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.block, False)
            if hits:
                if self.mover_derecha:
                    self.rect.right = hits[0].rect.left
                elif self.mover_izquierda:
                    self.rect.left = hits[0].rect.right
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.block, False)
            if hits:
                if self.mover_abajo:
                    self.rect.bottom = hits[0].rect.top
                elif self.mover_arriba:
                    self.rect.top = hits[0].rect.bottom


# Clase Obstaculo
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


# Clase Obstaculo (actualizada)
class Obstaculo(Tile):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "muro.png")

        # Puedes agregar más atributos si es necesario
