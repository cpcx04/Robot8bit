import pygame
from config import *

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
