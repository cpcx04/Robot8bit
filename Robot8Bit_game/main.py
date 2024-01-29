# main.py
import pygame
from pygame.locals import *
from sprites import *
from config import *


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
        self.player = None
        self.intro_music_played = False

    def createTileMap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE

                if column == ".":
                    Tile(self, x, y, "suelo.jpg")
                elif column == "P":
                    Obstaculo(self, x, y)
                elif column == "B":
                    Obstaculo(self, x, y)

    def new(self):
        self.playing = True
        self.intro_music_played = False  # Reiniciamos para la música de intro
        self.player = Player(self, 0, 0)
        self.all_sprites.add(self.player)
        self.createTileMap()
        pygame.mixer.music.stop()
        # Cargamos y reproducimos la nueva música (level1.mp3)
        pygame.mixer.music.load("sonidos/level1.mp3")
        pygame.mixer.music.play(-1)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def game_over(self):
        pass

    def intro_screen(self):
        print("Pantalla de introducción")
        # Carga la imagen de fondo de la pantalla de inicio
        background = pygame.image.load("images/menu.jpg").convert()
        self.screen.blit(background, (0, 0))

        # Configuración del texto del menú
        menu = ["Jugar", "Salir"]
        text_color = (255, 255, 255)
        selected_color = (255, 0, 0)

        # Dibujaoms el menú en el centro de la pantalla
        menu_height = len(menu) * 50
        menu_y = (WIN_HEIGHT - menu_height) // 2
        option_index = 0
        if not self.intro_music_played:
            pygame.mixer.music.load("sonidos/intro.mp3")
            pygame.mixer.music.play(-1)
            self.intro_music_played = True

        while not self.playing:
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
                            self.new()  # Cambia a la pantalla de juego
                        elif menu[option_index] == "Salir":
                            pygame.quit()
                            self.playing = False
                            self.running = False

            # Dibuja el menú con la opción seleccionada resaltada
            for i, option in enumerate(menu):
                text = self.font.render(option, True, selected_color if i == option_index else text_color)
                text_rect = text.get_rect(center=(WIN_WIDTH // 2, menu_y + i * 50))
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(10)  # Controla la velocidad del bucle


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
