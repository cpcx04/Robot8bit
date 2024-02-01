# main.py
import random

import pygame
from bomba import  *
from obstaculo import *
from player import *
from config import *
from healthbar import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/AncientModernTales-a7Po.ttf", 38)
        self.running = True
        self.playing = False
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.block = pygame.sprite.LayeredUpdates()
        self.player_layer = pygame.sprite.LayeredUpdates()
        self.player = None
        self.intro_music_played = False

    def createTileMap(self):
        with open("mapa.txt", "r") as file:
            lines = file.readlines()
        map_height = len(lines)
        map_width = len(lines[0].strip())
        random_x = random.randint(0, map_width - 1)
        random_y = random.randint(0, map_height - 1)

        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                x = j * TILESIZE
                y = i * TILESIZE

                if char == "P":
                        self.player = Player(self, x, y)
                        self.all_sprites.add(self.player)
                        Tile(self, x, y, "suelo.jpg")
                if char == ".":

                        Tile(self, x, y, "suelo.jpg")
                elif char == "B":
                    obstacle = Obstaculo(self, x, y)
                    self.block.add(obstacle)
                    self.all_sprites.add(obstacle)
                elif char == "O":
                    muro = Muro(self, x, y)
                    self.block.add(muro)
                    self.all_sprites.add(muro)
                elif char == "E":
                    bomba = Bomba(self, 10, x, y)
                    self.block.add(bomba)
                    self.all_sprites.add(bomba)
                    Tile(self, x, y, "suelo.jpg")
    def new(self):
        self.playing = True
        self.intro_music_played = False
        self.createTileMap()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sonidos/level1.mp3")
        pygame.mixer.music.play(-1)

    def update(self):
        if self.player:
            vida = self.player.current_health
            if vida == 0:
                self.game_over()
            else:
                self.player.update()
                self.all_sprites.update(self.player.current_health)

    def draw(self):
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def game_over(self):
        self.playing = False

        background = pygame.image.load("images/game_over.jpg").convert()
        self.screen.blit(background, (0, 0))
        message = self.font.render("Press any key to go to the main menu", True, (0, 0, 0))
        message_rect = message.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
        self.screen.blit(message, message_rect)

        pygame.display.flip()

        # Wait for a key press
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    key_pressed = True
                elif event.type == pygame.KEYDOWN:
                    self.reset_game()
                    self.intro_screen()
                    key_pressed = True

            self.clock.tick(60)

    def reset_game(self):
        self.intro_music_played = False

        self.all_sprites.empty()
        self.block.empty()
        self.player_layer.empty()
        self.createTileMap()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sonidos/level1.mp3")
        pygame.mixer.music.play(-1)

    def intro_screen(self):
        background = pygame.image.load("images/menu.jpg").convert()
        self.screen.blit(background, (0, 0))

        menu = ["Jugar", "Salir"]
        text_color = (255, 255, 255)
        selected_color = (255, 0, 0)

        menu_height = len(menu) * 50
        menu_y = (WIN_HEIGHT - menu_height) // 2
        option_index = 0
        if not self.intro_music_played:
            pygame.mixer.music.load("sonidos/intro.mp3")
            pygame.mixer.music.play(-1)
            self.intro_music_played = True

        while not self.playing and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        option_index = (option_index - 1) % len(menu)
                    elif event.key == pygame.K_DOWN:
                        option_index = (option_index + 1) % len(menu)
                    elif event.key == pygame.K_RETURN:
                        if menu[option_index] == "Jugar":
                            self.new()
                        elif menu[option_index] == "Salir":
                            pygame.quit()
                            self.playing = False
                            self.running = False

            for i, option in enumerate(menu):
                text = self.font.render(option, True, selected_color if i == option_index else text_color)
                text_rect = text.get_rect(center=(WIN_WIDTH // 2, menu_y + i * 50))
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)


# Código principal
if __name__ == "__main__":
    game = Game()

    while game.running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.player.mover_derecha = True
                elif event.key == pygame.K_LEFT:
                    game.player.mover_izquierda = True
                elif event.key == pygame.K_UP:
                    game.player.mover_arriba = True
                elif event.key == pygame.K_DOWN:
                    game.player.mover_abajo = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    game.playing = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    game.player.mover_derecha = False
                elif event.key == pygame.K_LEFT:
                    game.player.mover_izquierda = False
                elif event.key == pygame.K_UP:
                    game.player.mover_arriba = False
                elif event.key == pygame.K_DOWN:
                    game.player.mover_abajo = False

        if not game.playing:
            game.intro_screen()
        else:
            game.update()
            game.draw()
            game.clock.tick(60)

    pygame.quit()
