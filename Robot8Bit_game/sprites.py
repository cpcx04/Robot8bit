# sprites.py
import pygame
from config import *

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

bomba = pygame.image.load("images/bomba.png")
bomba = pygame.transform.scale(bomba, (44, 44))

class Healthbar(pygame.sprite.Sprite):

    heart_image = pygame.image.load("images/corazon.png")
    heart_image = pygame.transform.scale(heart_image, (20, 20))

    def __init__(self, x, y, width, height, max_health):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.heart_image = pygame.image.load("images/corazon.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (20, 20))


    def update(self, current_health):
        self.current_health = current_health
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.width, self.height), border_radius=10)
        filled_width = int(self.current_health / self.max_health * self.width)
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, filled_width, self.height), border_radius=10)
        pygame.draw.rect(self.heart_image, (255,0,0), (0, 0, filled_width, self.height))


    def draw(self, surface):
        pygame.sprite.Sprite.draw(self, surface)
        surface.blit(self.heart_image, (self.rect.x + self.width + 5, self.rect.y))


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
        hits = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for hit in hits:
            if isinstance(hit, Player):
                distancia = pygame.math.Vector2(hit.rect.centerx - self.rect.centerx,
                                                hit.rect.centery - self.rect.centery).length()
                if distancia < DISTANCIA_DE_EXPLOSION:
                    hit.current_health -= self.damage
            elif isinstance(hit, Obstaculo):
                hit.kill()
                Tile(self.game, hit.rect.x, hit.rect.y, "suelo.jpg")

        # Finalmente, elimina la bomba
        self.kill()

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
        vida = self.current_health
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.block, False)
            if hits:
                if self.mover_derecha:
                    self.rect.right = hits[0].rect.left
                    self.current_health = self.current_health -1
                elif self.mover_izquierda:
                    self.rect.left = hits[0].rect.right
                    self.current_health = self.current_health - 1
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.block, False)
            if hits:
                if self.mover_abajo:
                    self.rect.bottom = hits[0].rect.top
                    self.current_health = self.current_health - 1
                elif self.mover_arriba:
                    self.rect.top = hits[0].rect.bottom
                    self.current_health = self.current_health - 1


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

