# sprites.py
import pygame
from pygame.examples.grid import TILE_SIZE

from config import *

from obstaculo import *
from healthbar import *

player_image_stanBy = pygame.image.load("images/front_player.png")
player_image_stanBy = pygame.transform.scale(player_image_stanBy, (44, 44))

player_image_left_stop = pygame.image.load("images/left_stop.png")
player_image_left_stop = pygame.transform.scale(player_image_left_stop, (44, 44))

player_image_left_run = pygame.image.load("images/left_run.png")
player_image_left_run = pygame.transform.scale(player_image_left_run, (44, 44))

player_image_right_stop = pygame.image.load("images/right_stop.png")
player_image_right_stop = pygame.transform.scale(player_image_right_stop, (44, 44))

player_image_right_run = pygame.image.load("images/right_run.png")
player_image_right_run = pygame.transform.scale(player_image_right_run, (44, 44))


player_image_bottom_run = pygame.image.load("images/front_run.png")
player_image_bottom_run = pygame.transform.scale(player_image_bottom_run, (44, 44))

player_image_bottom_stop = pygame.image.load("images/front_player.png")
player_image_bottom_stop = pygame.transform.scale(player_image_bottom_stop, (44, 44))

player_image_up_run = pygame.image.load("images/up_run.png")
player_image_up_run = pygame.transform.scale(player_image_up_run, (44, 44))

player_image_up_stop = pygame.image.load("images/up_stop.png")
player_image_up_stop = pygame.transform.scale(player_image_up_stop, (44, 44))

# Ice versions
player_image_stanBy_ice = pygame.image.load("images/front_player_ice.png")
player_image_stanBy_ice = pygame.transform.scale(player_image_stanBy_ice, (44, 44))

player_image_right_run_ice = pygame.image.load("images/right_run_ice.png")
player_image_right_run_ice = pygame.transform.scale(player_image_right_run_ice, (44, 44))

player_image_left_run_ice = pygame.image.load("images/left_run_ice.png")
player_image_left_run_ice = pygame.transform.scale(player_image_left_run_ice, (44, 44))

player_image_right_stop_ice = pygame.image.load("images/right_stop_ice.png")
player_image_right_stop_ice = pygame.transform.scale(player_image_right_stop_ice, (44, 44))

player_image_bottom_run_ice = pygame.image.load("images/front_run_ice.png")
player_image_bottom_run_ice = pygame.transform.scale(player_image_bottom_run_ice, (44, 44))

player_image_up_run_ice = pygame.image.load("images/up_run_ice.png")
player_image_up_run_ice = pygame.transform.scale(player_image_up_run_ice, (44, 44))

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
        self.traje_agua = False
        self.explotar = False
        self.diamantes_en_mapa=0
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
            if self.traje_agua == True:
                self.image = player_image_right_run_ice
            else:
                self.image = player_image_right_run
            self.collide_block('x')
        elif self.mover_izquierda:
            self.rect.x -= PLAYER_SPEED
            if self.traje_agua == True:
                self.image = player_image_left_run_ice
            else:
                self.image = player_image_left_run
            self.collide_block('x')
        elif self.mover_arriba:
            self.rect.y -= PLAYER_SPEED
            if self.traje_agua == True:
                self.image=player_image_up_run_ice
            else:
                self.image = player_image_up_run
            self.collide_block('y')
        elif self.mover_abajo:
            self.rect.y += PLAYER_SPEED
            if self.traje_agua == True:
                self.image = player_image_bottom_run_ice
            else:
                self.image = player_image_bottom_run
            self.collide_block('y')
        else:
            if self.traje_agua ==True:
                self.image = player_image_stanBy_ice
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
            elif isinstance(hit, Toxic):
                if self.current_health == 0:
                    self.game.game_over()
                if direction == "x" and self.mover_derecha or self.mover_izquierda:
                    if not self.traje_agua:
                        self.current_health -= 1
                elif direction == "y" and self.mover_abajo or self.mover_arriba:
                    if not self.traje_agua:
                        self.current_health -= 1


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
            if isinstance(hit, Pocion) and self.inventory["Pocion"] > 0:
                self.current_health = 300
                self.inventory["Pocion"] -= 1

    def poner_traje_agua(self):
        if self.traje_agua == True:
            self.traje_agua == False
        if self.traje_agua == False:
            self.inventory["Armadura"] > 0
            self.inventory["Armadura"] -= 1

    def explotar_bomba(self):
        from bomba import Bomba
        if self.inventory["Bomba"] > 0:
            self.inventory["Bomba"] -= 1
            self.explotar = True
            current_x, current_y = self.rect.x, self.rect.y
            explosion_range = 50
            for x in range(current_y - explosion_range, current_x + explosion_range + 1, TILESIZE):
                for y in range(current_y - explosion_range, current_y + explosion_range + 1, TILESIZE):
                    hits = pygame.sprite.spritecollide(self, self.game.all_sprites, False)

                    for hit in hits:
                        if isinstance(hit, Muro) and hit.rect.collidepoint(x, y):
                            self.game.all_sprites.remove(hit)
                            self.game.block.remove(hit)
                            self.game.block.empty()



    def otorgar_vida_maxima(self):
        self.current_health = self.max_health
        self.inventory["Pocion"] -= 1