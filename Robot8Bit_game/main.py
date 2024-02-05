# main.py
import random

import pygame

from armadura import Armadura
from bomba import Bomba
from diamantes import Diamante
from obstaculo import *
from player import Player
from config import *
from healthbar import *
from pocion import Pocion


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("font/AncientModernTales-a7Po.ttf", 38)
        self.running = True
        self.playing = False
        self.blocks_with_positions = []
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.block = pygame.sprite.LayeredUpdates()
        self.player_layer = pygame.sprite.LayeredUpdates()
        self.block = pygame.sprite.Group()
        self.player = None
        self.intro_music_played = False

    def createTileMap(self):
        with open("mapa.txt", "r") as file:
            lines = file.readlines()

        map_height = len(lines)
        map_width = len(lines[0].strip())
        bomb_positions = []

        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                x = j * TILESIZE
                y = i * TILESIZE

                if char == "P":
                    self.player = Player(self, x, y)
                    self.all_sprites.add(self.player)
                    Tile(self, x, y, "arena.jpg")
                elif char == ".":
                    Tile(self, x, y, "arena.jpg")
                    bomb_positions.append((x, y))
                elif char in ["B", "O", "T"]:
                    block = (char, x, y)  # Guardar el tipo de bloque y su posición
                    self.blocks_with_positions.append(block)
                    if char == "B":
                        obstaculo = Obstaculo(self, x, y)
                        self.block.add(obstaculo)
                    elif char == "O":
                        muro = Muro(self, x, y)
                        self.block.add(muro)
                    elif char == "T":
                        toxico = Toxic(self, x, y)
                        self.block.add(toxico)
                elif char == "E":
                    Tile(self, x, y, "arena.jpg")

        object_counts = {"Bomba": 4, "Diamante": 4, "Armadura": 2, "Pocion": 3}

        for object_type, count in object_counts.items():
            for _ in range(min(count, len(bomb_positions))):
                random_position = random.choice(bomb_positions)
                bomb_positions.remove(random_position)
                x, y = random_position

                if object_type == "Bomba":
                    new_object = Bomba(self, x, y)
                elif object_type == "Diamante":
                    new_object = Diamante(self, x, y)
                    print("Diamante generado")
                elif object_type == "Armadura":
                    new_object = Armadura(self, x, y)
                elif object_type == "Pocion":
                    new_object = Pocion(self, x, y)

                self.block.add(new_object)
                self.all_sprites.add(new_object)

    def new(self):
        self.playing = True
        self.intro_music_played = False
        self.createTileMap()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sonidos/level1.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def update(self):
        if self.player:
            vida = self.player.current_health
            if vida == 0:
                self.game_over()
            else:
                self.player.update()
                self.all_sprites.update(self.player.current_health)

    def update_victory_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pygame.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.block.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.draw_inventory()
        pygame.display.flip()

    def draw_inventory(self):
        bomba_img = pygame.image.load("images/bomba.png")
        bomba_img = pygame.transform.scale(bomba_img, (44, 44))
        armadura_img = pygame.image.load("images/armadura.png")
        armadura_img = pygame.transform.scale(armadura_img, (44, 44))
        diamante_img = pygame.image.load("images/diamante.png")
        diamante_img = pygame.transform.scale(diamante_img, (44, 44))

        self.screen.blit(bomba_img, (400, 10))
        self.screen.blit(armadura_img, (500, 10))
        self.screen.blit(diamante_img, (600, 10))

        bomba_count_text = str(self.player.inventory['Bomba'])
        armadura_count_text = str(self.player.inventory['Armadura'])
        diamante_count_text = str(self.player.inventory['Diamante'])

        count_font = pygame.font.Font(None, 36)

        bomba_count_surface = count_font.render(bomba_count_text, True, (255, 255, 255))
        armadura_count_surface = count_font.render(armadura_count_text, True, (255, 255, 255))
        diamante_count_surface = count_font.render(diamante_count_text, True, (255, 255, 255))

        self.screen.blit(bomba_count_surface, (400 + 50, 25))
        self.screen.blit(armadura_count_surface, (500 + 50, 25))
        self.screen.blit(diamante_count_surface, (600 + 50, 25))

    def show_victory_screen(self, score):
        self.playing = False

        # Fondo redondo para los textos
        text_background = pygame.image.load("images/victory.jpg").convert()
        text_background_rect = text_background.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.screen.blit(text_background, text_background_rect)

        # Mensaje de victoria
        victory_message = self.font.render("¡Has ganado!", True, (255, 255, 255))
        victory_rect = victory_message.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 100))
        self.screen.blit(victory_message, victory_rect)

        # Puntuación
        score_text = self.font.render(f"Puntuación: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, score_rect)

        # Mensaje adicional
        message = self.font.render("Presiona cualquier tecla para volver al menú", True, (255, 255, 255))
        message_rect = message.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        self.screen.blit(message, message_rect)

        pygame.mixer.music.stop()
        pygame.mixer.music.load("sonidos/winner.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
        pygame.display.flip()

        # Espera a que el jugador presione una tecla
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

        self.all_sprites.remove()
        self.all_sprites.empty()
        self.block.remove()
        self.block.empty()
        self.player_layer.remove()
        self.player = None
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
                elif event.key == pygame.K_b:
                    if game.player.inventory["Bomba"] > 0:
                        game.player.explotar_bomba()
                        game.player.explotar = True
                elif event.key == pygame.K_t:
                    if game.player.inventory["Armadura"] > 0:
                        game.player.traje_agua = not game.player.traje_agua
                        game.player.poner_traje_agua()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    game.player.mover_derecha = False
                elif event.key == pygame.K_LEFT:
                    game.player.mover_izquierda = False
                elif event.key == pygame.K_UP:
                    game.player.mover_arriba = False
                elif event.key == pygame.K_DOWN:
                    game.player.mover_abajo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    game.player.poner_traje_agua()

        if not game.playing:
            game.intro_screen()
        else:
            game.update()
            game.draw()
            game.clock.tick(60)

    pygame.quit()
