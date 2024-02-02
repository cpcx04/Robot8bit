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
        self.collide_bomba()
        self.collide_diamante()
        self.inventory = {
            "Bomba": 0,
            "Diamante": 0,
            "Pocion": 0,
            "Armadura": 0
        }

    def update(self, *args):
        self.mover()
        self.healt_bar.update(self.current_health)
        inventory_text = f"Bombas: {self.inventory['Bomba']} Diamante: {self.inventory['Diamante']} Pocion: {self.inventory['Pocion']} Armadura: {self.inventory['Armadura']}"
        inventory_surface = self.game.font.render(inventory_text, True, (255, 255, 255))
        inventory_rect = inventory_surface.get_rect(topleft=(10, 40))
        self.game.screen.blit(inventory_surface, inventory_rect)
        self.collide_bomba()
        self.collide_diamante()
        self.collide_armadura()
        self.collide_pocion()

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
        hits = pygame.sprite.spritecollide(self, self.game.block, False)

        for hit in hits:
            if isinstance(hit, (Obstaculo, Muro)):
                if direction == "x":
                    if self.mover_derecha:
                        self.rect.right = hit.rect.left
                        self.current_health -= 30
                        self.mover_derecha = False
                        self.image = player_image_left_stop
                    elif self.mover_izquierda:
                        self.rect.left = hit.rect.right
                        self.current_health -= 30
                        self.mover_izquierda = False
                        self.image = player_image_right_stop
                elif direction == "y":
                    if self.mover_abajo:
                        self.rect.bottom = hit.rect.top
                        self.current_health -= 30
                        self.mover_abajo = False
                        self.image = player_image_up_stop
                    elif self.mover_arriba:
                        self.rect.top = hit.rect.bottom
                        self.current_health -= 30
                        self.mover_arriba = False
                        self.image = player_image_bottom_stop

    def collide_bomba(self):
        from bomba import Bomba
        hits = pygame.sprite.spritecollide(self, self.game.block, False)
        for hit in hits:
            if isinstance(hit, Bomba):
                self.game.all_sprites.remove(hit)
                self.game.block.remove(hit)
                self.inventory["Bomba"] += 1

    def collide_diamante(self):
        from diamantes import Diamante
        hits = pygame.sprite.spritecollide(self, self.game.block, False)
        for hit in hits:
            if isinstance(hit, Diamante):
                self.game.all_sprites.remove(hit)
                self.game.block.remove(hit)
                self.inventory["Diamante"] += 1

    def collide_armadura(self):
        from armadura import Armadura
        hits = pygame.sprite.spritecollide(self, self.game.block, False)
        for hit in hits:
            if isinstance(hit, Armadura):
                self.game.all_sprites.remove(hit)
                self.game.block.remove(hit)
                self.inventory["Armadura"] += 1

    def collide_pocion(self):
        from pocion import Pocion
        hits = pygame.sprite.spritecollide(self, self.game.block, False)
        for hit in hits:
            if isinstance(hit, Pocion):
                self.game.all_sprites.remove(hit)
                self.game.block.remove(hit)
                self.inventory["Pocion"] += 1