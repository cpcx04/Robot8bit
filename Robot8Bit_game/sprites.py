import pygame
from config import *
player1_image_left = pygame.image.load("images/3397.png")
player1_image_left = pygame.transform.scale(player1_image_left,(80,80))

player1_image_right = pygame.image.load("images/3397_derecha.png")
player1_image_right = pygame.transform.scale(player1_image_right,(80,80))

class Robot:
    def __init__(self):
        self.image1 = player1_image_left
        self.image2 = player1_image_right
        self.position = [0, 0]
        self.speed = 5
        self.mover_izquierda = False
        self.mover_derecha = False
        self.mover_arriba= False
        self.mover_abajo = False




    def mover(self):
        if self.mover_derecha:
            self.position[0] += self.speed

        if self.mover_izquierda:
            self.position[0] -= self.speed

        if self.mover_arriba:
            self.position[1] -= self.speed

        if self.mover_abajo:
           self.position[1] += self.speed

#pygame.sprite.Sprite#
class Obstaculo():
    def __init__(self):
        #self._layer = BLOCK_LAYER
        self.position = [100, 100]
        self.size = [20, 20]
        #pygame.sprite.Sprite.__init__(self,self)