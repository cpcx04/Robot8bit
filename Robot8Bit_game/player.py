# sprites.py
import pygame
from config import *
from obstaculo import *
from healthbar import *

player_image_stanBy = pygame.image.load("images/front_player.png")
player_image_stanBy = pygame.transform.scale(player_image_stanBy, (44,44))

player_image_left_stop = pygame.image.load("images/left_stop.png")
player_image_left_stop = pygame.transform.scale(player_image_left_stop, (44,44))

player_image_left_run = pygame.image.load("images/left_run.png")
player_image_left_run = pygame.transform.scale(player_image_left_run, (44,44))

player_image_right_stop = pygame.image.load("images/right_stop.png.")
player_image_right_stop = pygame.transform.scale(player_image_right_stop, (44,44))

player_image_right_run = pygame.image.load("images/right_run.png")
player_image_right_run = pygame.transform.scale(player_image_right_run, (44,44))

player_image_bottom_run = pygame.image.load("images/front_run.png")
player_image_bottom_run = pygame.transform.scale(player_image_bottom_run, (44,44))

player_image_bottom_stop = pygame.image.load("images/front_player.png")
player_image_bottom_stop = pygame.transform.scale(player_image_bottom_stop, (44,44))

player_image_up_run = pygame.image.load("images/up_run.png")
player_image_up_run = pygame.transform.scale(player_image_up_run, (44,44))

player_image_up_stop = pygame.image.load("images/up_stop.png")
player_image_up_stop = pygame.transform.scale(player_image_up_stop, (44,44))
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.current_health = 300
        self._layer = PLAYER_LAYER
        self.image = player_image_stanBy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.healt_bar = Healthbar(10,10,300,20,300)
        self.game.all_sprites.add(self.healt_bar)
        self.mover_derecha = False
        self.mover_izquierda = False
        self.mover_arriba = False
        self.mover_abajo = False


    def update(self, *args):
        self.mover()
        self.healt_bar.update(self.current_health)

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
                    self.current_health -= 30
                    self.mover_derecha = False
                    self.image = player_image_left_stop
                elif self.mover_izquierda:
                    self.rect.left = hits[0].rect.right
                    self.current_health -= 30
                    self.mover_izquierda = False
                    self.image = player_image_right_stop
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.block, False)
            if hits:
                if self.mover_abajo:
                    self.rect.bottom = hits[0].rect.top
                    self.current_health -= 30
                    self.mover_abajo = False
                    self.image = player_image_up_stop
                elif self.mover_arriba:
                    self.rect.top = hits[0].rect.bottom
                    self.current_health -= 30
                    self.mover_arriba = False
                    self.image = player_image_bottom_stop


